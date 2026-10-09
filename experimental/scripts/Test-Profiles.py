"""Plan or run explicit SCADMaxx test profiles. Planning never executes tests."""
import argparse
import ctypes
import getopt
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

CONTROL = Path(__file__).resolve().parents[2]
CATALOG = CONTROL / "experimental/testing/catalog.json"
SHARED = CONTROL / "tools/evaluation-benchmark/realworld"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class WindowsBudget:
    """A kill-on-close job bounds the entire suite process tree, including grandchildren."""
    def __init__(self, memory_mb, threads, quiet):
        self.handle = None
        if os.name != "nt":
            raise RuntimeError("This Windows profile runner requires Windows resource controls")
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel = kernel
        kernel.CreateJobObjectW.restype = wintypes.HANDLE
        kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]

        class Basic(ctypes.Structure):
            _fields_ = [("ProcessTime", ctypes.c_longlong), ("JobTime", ctypes.c_longlong),
                        ("Flags", wintypes.DWORD), ("MinWorking", ctypes.c_size_t),
                        ("MaxWorking", ctypes.c_size_t), ("Processes", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("Priority", wintypes.DWORD),
                        ("Scheduling", wintypes.DWORD)]

        class IO(ctypes.Structure):
            _fields_ = [(name, ctypes.c_ulonglong) for name in
                        ("ReadOps", "WriteOps", "OtherOps", "ReadBytes", "WriteBytes", "OtherBytes")]

        class Extended(ctypes.Structure):
            _fields_ = [("Basic", Basic), ("IO", IO), ("ProcessMemory", ctypes.c_size_t),
                        ("JobMemory", ctypes.c_size_t), ("PeakProcess", ctypes.c_size_t),
                        ("PeakJob", ctypes.c_size_t)]

        limits = Extended()
        # Kill on close, aggregate job commit limit, inherited processor affinity and priority.
        limits.Basic.Flags = 0x2000 | 0x200 | 0x10 | 0x20
        limits.Basic.Affinity = (1 << min(threads, os.cpu_count() or 1, 32)) - 1
        limits.Basic.Priority = 0x20 if quiet else 0x4000
        limits.JobMemory = memory_mb * 1024 * 1024
        self.handle = kernel.CreateJobObjectW(None, None)
        if not self.handle or not kernel.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            self.close()
            raise ctypes.WinError(ctypes.get_last_error())

    def attach(self, process):
        if not self.kernel.AssignProcessToJobObject(self.handle, wintypes.HANDLE(int(process._handle))):
            process.kill()
            process.wait()
            raise ctypes.WinError(ctypes.get_last_error())

    def resume(self, pid):
        # Popen closes the primary thread handle. Locate that still-suspended thread after job assignment,
        # so no descendant can escape the job by starting before resource controls are attached.
        class ThreadEntry(ctypes.Structure):
            _fields_ = [("size", wintypes.DWORD), ("usage", wintypes.DWORD), ("thread", wintypes.DWORD),
                        ("process", wintypes.DWORD), ("base", wintypes.LONG), ("delta", wintypes.LONG),
                        ("flags", wintypes.DWORD)]

        kernel = self.kernel
        kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        kernel.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(ThreadEntry)]
        kernel.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(ThreadEntry)]
        kernel.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenThread.restype = wintypes.HANDLE
        kernel.ResumeThread.argtypes = [wintypes.HANDLE]
        kernel.ResumeThread.restype = wintypes.DWORD
        snapshot = kernel.CreateToolhelp32Snapshot(4, 0)
        if snapshot == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            entry = ThreadEntry()
            entry.size = ctypes.sizeof(entry)
            available = kernel.Thread32First(snapshot, ctypes.byref(entry))
            while available:
                if entry.process == pid:
                    thread = kernel.OpenThread(2, False, entry.thread)
                    if not thread:
                        raise ctypes.WinError(ctypes.get_last_error())
                    try:
                        if kernel.ResumeThread(thread) == 0xFFFFFFFF:
                            raise ctypes.WinError(ctypes.get_last_error())
                        return
                    finally:
                        kernel.CloseHandle(thread)
                available = kernel.Thread32Next(snapshot, ctypes.byref(entry))
            raise RuntimeError("Suspended process primary thread not found")
        finally:
            kernel.CloseHandle(snapshot)

    def close(self):
        if self.handle:
            try:
                self.terminate_and_wait()
            finally:
                self.kernel.CloseHandle(self.handle)
                self.handle = None

    def terminate_and_wait(self):
        # TerminateJobObject requests tree termination; waiting only on Popen's parent does not
        # establish that descendants have released inherited stdout/stderr file handles.
        kernel = self.kernel
        kernel.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                                     wintypes.DWORD, ctypes.c_void_p]
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.WaitForSingleObject.restype = wintypes.DWORD
        capacity = 64
        while True:
            buffer = ctypes.create_string_buffer(8 + ctypes.sizeof(ctypes.c_size_t) * capacity)
            if kernel.QueryInformationJobObject(self.handle, 3, buffer, len(buffer), None):
                break
            if ctypes.get_last_error() != 234:  # ERROR_MORE_DATA
                raise ctypes.WinError(ctypes.get_last_error())
            capacity *= 2
        count = wintypes.DWORD.from_buffer(buffer, 4).value
        pids = (ctypes.c_size_t * count).from_buffer(buffer, 8)
        handles = []
        try:
            for pid in pids:
                handle = kernel.OpenProcess(0x100000, False, pid)  # SYNCHRONIZE
                if handle:
                    handles.append(handle)
                elif ctypes.get_last_error() != 87:  # Process already gone
                    raise ctypes.WinError(ctypes.get_last_error())
            if not kernel.TerminateJobObject(self.handle, 124):
                raise ctypes.WinError(ctypes.get_last_error())
            deadline = time.monotonic() + 10
            for handle in handles:
                result = kernel.WaitForSingleObject(handle, max(0, int((deadline - time.monotonic()) * 1000)))
                if result == 258:
                    raise RuntimeError("Timed-out suite descendants did not finish terminating")
                if result != 0:
                    raise ctypes.WinError(ctypes.get_last_error())
        finally:
            for handle in handles:
                kernel.CloseHandle(handle)


def execute(command, cwd, env, timeout, folder, args, quiet=False):
    folder.mkdir(parents=True, exist_ok=True)
    save(folder / "command.json", {"argv": list(map(str, command)), "cwd": str(cwd),
                                   "environment": env, "timeout_seconds": timeout,
                                   "threads": args.threads, "memory_mb": args.memory_mb})
    budget = WindowsBudget(args.memory_mb, args.threads, quiet)
    started = time.monotonic()
    try:
        with (folder / "stdout.txt").open("wb") as out, (folder / "stderr.txt").open("wb") as err:
            process = subprocess.Popen(list(map(str, command)), cwd=cwd, env={**os.environ, **env},
                                       stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW | 4)
            budget.attach(process)
            budget.resume(process.pid)
            try:
                code = process.wait(timeout=timeout)
                status = "PASS" if code == 0 else "FAIL"
            except subprocess.TimeoutExpired:
                budget.terminate_and_wait()
                process.wait()
                code, status = 124, "INCONCLUSIVE"
    except FileNotFoundError as error:
        return {"status": "NOT_RUN", "exit_code": None, "seconds": time.monotonic() - started,
                "reason": f"Missing executable or working directory: {error}"}
    finally:
        budget.close()
    return {"status": status, "exit_code": code, "seconds": time.monotonic() - started}


def environment(args, desktop=False):
    env = {"OMP_NUM_THREADS": str(args.threads), "TBB_NUM_THREADS": str(args.threads),
           "OPENBLAS_NUM_THREADS": str(args.threads), "MKL_NUM_THREADS": str(args.threads),
           "QT_QPA_PLATFORM": "windows" if desktop else "offscreen"}
    if args.runtime:
        env.update(QT_PLUGIN_PATH=str(args.runtime), QT_QPA_PLATFORM_PLUGIN_PATH=str(args.runtime / "platforms"))
        env["PATH"] = str(args.runtime) + os.pathsep + os.environ.get("PATH", "")
        if args.profile == "distribution":
            system = Path(os.environ.get("SystemRoot", "C:/Windows"))
            env["PATH"] = os.pathsep.join(map(str, (args.runtime, system / "System32", system)))
    # Clear selectors inherited from another investigation, including the removed temporary performance adapter.
    for key in os.environ:
        if key.startswith("OPENSCAD_") and ("TEST" in key or "BENCHMARK" in key):
            env[key] = ""
    return env


def ctest_inventory(build, config, args):
    proc = subprocess.run([args.ctest, "--test-dir", str(build), "-C", config, "--show-only=json-v1"],
                          capture_output=True, text=True, timeout=60,
                          creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    if proc.returncode:
        raise RuntimeError(f"CTest discovery failed: {proc.stderr}")
    return read_json_output(proc.stdout)["tests"]


def read_json_output(output):
    # CMake's EnforceConfig may print a status line before the JSON document.
    document, _ = json.JSONDecoder().raw_decode(output[output.index("{"):])
    return document


def approved(test, catalog):
    command = test.get("command", [])
    if not command:
        return False
    binary = Path(command[0]).name.lower()
    if binary in ("scadmaxx.com", "scadmaxx.exe", "openscad.com", "openscad.exe"):
        return "-o" in command and "--run-all-gui-tests" not in command
    if binary in ("cmake.exe", "cmake"):
        return command[1:3] == ["-E", "cat"]
    scripts = [Path(value).name for value in command if str(value).endswith(".py")]
    return bool(scripts) and all(name in catalog["ctest"]["approved_scripts"] for name in scripts)


def ctest_chunks(selected, config):
    """Keep dependencies/fixtures in the same invocation; do not rely on old output artifacts."""
    tests = {name: row["test"] for name, row in selected.items() if row["config"] == config}
    parent = {name: name for name in tests}

    def root(name):
        while parent[name] != name:
            name = parent[name]
        return name

    def join(a, b):
        parent[root(b)] = root(a)

    fixtures = {}
    for name, test in tests.items():
        props = {p["name"]: p["value"] for p in test.get("properties", [])}
        for dependency in props.get("DEPENDS", []):
            if dependency not in tests:
                raise ValueError(f"Unselected or cross-configuration dependency: {name} -> {dependency}")
            join(name, dependency)
        for key in ("FIXTURES_SETUP", "FIXTURES_REQUIRED", "FIXTURES_CLEANUP"):
            for fixture in props.get(key, []):
                if fixture in fixtures:
                    join(name, fixtures[fixture])
                fixtures[fixture] = name
    groups = {}
    for name in tests:
        groups.setdefault(root(name), []).append(name)
    chunks, current = [], []
    for group in sorted(groups.values(), key=lambda values: min(values)):
        if len("|".join(map(re.escape, current + group))) > 6000 and current:
            chunks.append(sorted(current))
            current = []
        if len("|".join(map(re.escape, group))) > 6000:
            raise ValueError("Dependent CTest group exceeds command budget; add a dedicated adapter")
        current.extend(group)
    if current:
        chunks.append(sorted(current))
    return chunks


def missing_golden(test):
    command = test.get("command", [])
    scripts = [i for i, value in enumerate(command) if Path(value).name == "test_cmdline_tool.py"]
    if not scripts:
        return None
    index = scripts[0]
    try:
        options, arguments = getopt.getopt(command[index + 1:], "gs:k:e:c:t:f:m:x:X", [
            "generate", "convexec=", "suffix=", "kernel=", "expected-dir=", "test=", "file=",
            "comparator=", "stdin", "stdout", "exclude-line=", "exclude-debug"])
    except getopt.GetoptError:
        return None  # Let the driver report unsupported syntax.
    options = dict(options)
    directory = options.get("-e", options.get("--expected-dir", options.get("-t", options.get("--test"))))
    filename = options.get("-f", options.get("--file"))
    if not directory or not filename:
        return None
    suffix = options.get("-s", options.get("--suffix", "txt")).lstrip(".")
    expected = Path(command[index]).parent / "regression" / directory / f"{filename}-expected.{suffix}"
    return None if expected.is_file() else str(expected)


def healthy_selection(inventories, catalog, critical=False):
    bugs = {t["name"] for t in inventories[catalog["ctest"]["bug_config"]]}
    selected, excluded = {}, []
    for config in catalog["ctest"]["healthy_configs"]:
        for test in inventories[config]:
            name = test["name"]
            if name in selected:
                continue
            if name in bugs:
                excluded.append({"name": name, "reason": "KNOWN_BASELINE_FAILURE_CATEGORY"})
                continue
            if critical and name not in catalog["ctest"]["critical_names"]:
                continue
            if not approved(test, catalog):
                # Catch tests are run directly by their own suites; unknown commands stay visible.
                binary = Path(test.get("command", [""])[0]).name if test.get("command") else ""
                if binary not in ("OpenSCADUnitTests.exe", "VimEngineTests.exe"):
                    excluded.append({"name": name, "reason": "UNCLASSIFIED_COMMAND"})
                continue
            props = {p["name"]: p["value"] for p in test.get("properties", [])}
            if any(value.startswith("QT_QPA_PLATFORM=") and value != "QT_QPA_PLATFORM=offscreen"
                   for value in props.get("ENVIRONMENT", [])):
                excluded.append({"name": name, "reason": "DESKTOP_ENVIRONMENT"})
                continue
            golden = missing_golden(test)
            if golden:
                excluded.append({"name": name, "reason": "MISSING_GOLDEN: " + golden})
                continue
            selected[name] = {"config": config, "test": test}
    missing = set(catalog["ctest"]["critical_names"]) - set(selected) if critical else set()
    return selected, excluded, sorted(missing)


def require(args, *names):
    absent = ["--" + name.replace("_", "-") for name in names if not getattr(args, name)]
    if absent:
        raise ValueError("Required: " + ", ".join(absent))


def jobs(suite, entry, args, root, catalog, discover=False):
    """Return commands and explicit coverage gaps; never run tests while constructing a plan."""
    adapter = entry["adapter"]
    folder = root / suite
    env = environment(args, entry["execution"] == "desktop")
    result, gaps = [], []

    def add(name, command, cwd=CONTROL, extra=None):
        result.append({"id": name, "command": list(map(str, command)), "cwd": str(cwd),
                       "env": {**env, **(extra or {})}, "timeout": entry["timeout"],
                       "execution": entry["execution"]})

    if adapter == "catch":
        require(args, "build")
        binary = args.build / entry["binary"]
        filters = ["~[providers-external]~[insertion-providers]~[anchor-bosl2]"] if suite == "unit" else []
        add(suite, [binary, *filters, "--reporter", "junit", "--out", folder / "results.xml"])
    elif adapter == "provider-external":
        require(args, "build")
        if not args.provider_libraries:
            gaps.append({"id": suite, "status": "NOT_RUN", "reason": "Requires --provider-libraries with pinned BOSL2/BOLTS file inventories"})
        else:
            libraries = read(args.provider_libraries)
            extra = {}
            for name, key in (("bosl2", "SCADMAXX_PROVIDER_BOSL2_ROOT"), ("bolts", "SCADMAXX_PROVIDER_BOLTS_ROOT")):
                record = libraries[name]
                directory = Path(record["root"]).resolve(strict=True)
                actual = {p.relative_to(directory).as_posix(): digest(p) for p in directory.rglob("*") if p.is_file()}
                if not actual or actual != record["files"]:
                    raise ValueError(f"Pinned provider library inventory mismatch: {name}")
                extra[key] = str(directory)
            add(suite, [args.build / "OpenSCADUnitTests.exe", "[providers-external],[insertion-providers],[anchor-bosl2]",
                        "--reporter", "junit", "--out", folder / "results.xml"], extra=extra)
    elif adapter == "unit-visual":
        require(args, "build", "runtime")
        add(suite, [args.build / "OpenSCADUnitTests.exe", "[icons-visual],[dialogs-visual],[customizer-visual],[typography-visual]",
                    "--reporter", "junit", "--out", folder / "results.xml"],
            extra={"OPENSCAD_TYPOGRAPHY_OUTPUT": str(folder / "captures")})
    elif adapter == "smoke":
        require(args, "runtime")
        executable = args.runtime / "scadmaxx.com"
        fixture = folder / "smoke.scad"
        add(suite + "-version", [executable, "--version"])
        add(suite + "-exe-version", [args.runtime / "scadmaxx.exe", "--version"])
        for backend in ("Manifold", "CGAL"):
            add(suite + "-" + backend, [executable, "--backend=" + backend, "-o", folder / (backend + ".stl"), fixture])
        add(suite + "-png", [executable, "--preview", "--autocenter", "--viewall", "-o", folder / "preview.png", fixture])
        add(suite + "-pdf", [executable, "-o", folder / "smoke.pdf", folder / "flat.scad"])
    elif adapter == "ctest":
        require(args, "build")
        if not discover:
            gaps.append({"id": suite, "status": "NOT_RUN", "reason": "CTest selection requires --discover or --run"})
        else:
            configs = catalog["ctest"]["healthy_configs"] + [catalog["ctest"]["bug_config"]]
            inventories = {config: ctest_inventory(args.build, config, args) for config in configs}
            selected, excluded, missing = healthy_selection(inventories, catalog, entry["selection"] == "critical")
            if entry["selection"] == "healthy" and args.source:
                source_definition = (args.source / "tests/CMakeLists.txt").read_text(encoding="utf-8")
                for owner, names in catalog["source_declared_ctest"].items():
                    for name in names:
                        declaration = name if owner != "pr-7091" else name.split("_", 1)[0]
                        if declaration in source_definition and name not in selected:
                            gaps.append({"id": name, "status": "NOT_RUN", "reason": f"{owner}: source declares coverage absent from compiled registration; reconfigure/build required"})
            for name in missing:
                gaps.append({"id": name, "status": "NOT_RUN", "reason": "Required critical test is absent or excluded"})
            if not selected:
                gaps.append({"id": suite, "status": "NOT_RUN", "reason": "No approved CTest tests selected"})
            for row in excluded:
                if row["reason"] != "KNOWN_BASELINE_FAILURE_CATEGORY":
                    gaps.append({"id": row["name"], "status": "NOT_RUN", "reason": row["reason"]})
            # Bound regex argument length on Windows. One process at a time, exact names only.
            for config in catalog["ctest"]["healthy_configs"]:
                for index, chunk in enumerate(ctest_chunks(selected, config)):
                    add(f"{suite}-{config}-{index}", [args.ctest, "--test-dir", args.build, "-C", config,
                        "-j", "1", "--timeout", "180", "--output-on-failure", "--no-tests=error",
                        "--fixture-exclude-any", ".*", "--output-junit", folder / f"{config}-{index}.xml",
                        "-R", "^(" + "|".join(map(re.escape, chunk)) + ")$"])
            result.append({"id": suite + "-inventory", "inventory": inventories, "selection": selected, "excluded": excluded})
    elif adapter == "language":
        require(args, "runtime", "source")
        fixture = args.source / "tests/data/scad/experimental/object/geometry-bounds-tests.scad"
        if not fixture.is_file():
            gaps.append({"id": suite, "status": "NOT_RUN", "reason": "Full language guide requires geometry-bounds source fixture: " + str(fixture)})
        else:
            add(suite, [sys.executable, CONTROL / "experimental/scripts/Test-LanguageExamples.py",
                        "--runtime", args.runtime, "--source", args.source, "--output", folder / "examples"])
    elif adapter == "standalone":
        build = getattr(args, entry["argument"])
        if not build:
            gaps.append({"id": suite, "status": "NOT_RUN", "reason": "Provide --" + entry["argument"].replace("_", "-") + " for its separately built test project"})
        else:
            add(suite, [args.ctest, "--test-dir", build, "-C", "Release", "-j", "1", "--timeout", "120",
                        "--no-tests=error", "--output-on-failure", "--output-junit", folder / "results.xml",
                        "-R", "^(" + "|".join(map(re.escape, entry["tests"])) + ")$"])
    elif adapter == "harness":
        add("realworld-harness", [sys.executable, "-m", "unittest", "-v", "test_benchmark"], SHARED)
        add("performance-harness", [sys.executable, "-m", "unittest", "discover", "-s", "tests"], CONTROL / "experimental/performance")
        add("profile-harness", [sys.executable, "-m", "unittest", "discover", "-s", "experimental/testing", "-p", "test_profiles.py"])
    elif adapter == "build-tools":
        add(suite, [args.pwsh, "-NoProfile", "-File", CONTROL / "experimental/scripts/Test-BuildTools.ps1"])
    elif adapter == "gui":
        require(args, "runtime", "build")
        cache = args.build / "CMakeCache.txt"
        if not cache.exists() or "ENABLE_GUI_TESTS:BOOL=ON" not in cache.read_text(encoding="utf-8"):
            gaps.append({"id": suite, "status": "NOT_RUN", "reason": "Requires a separately identified ENABLE_GUI_TESTS=ON build"})
        else:
            selectors = args.gui_suite or ["all"]
            if "all" in selectors and len(selectors) != 1:
                raise ValueError("Select all GUI suites or individual suites, not both")
            for selection in selectors:
                if selection in catalog["source_required_gui_selectors"]:
                    source_runner = args.source / "src/guitests/guitests.cc" if args.source else None
                    if not source_runner or not source_runner.exists() or catalog["gui_selectors"][selection] not in source_runner.read_text(encoding="utf-8"):
                        gaps.append({"id": "gui-" + selection, "status": "NOT_RUN", "reason": "Matching source does not declare this selector; never substitute the full GUI suite"})
                        continue
                extra = {"OPENSCAD_GUI_TEST_OUTPUT": str(folder / selection),
                         "OPENSCAD_NAVIGATION_TEST_OUTPUT": str(folder / selection),
                         "OPENSCAD_ANNOTATION_TEST_LOG": str(folder / selection / "annotation.log")}
                if args.gui_function:
                    source_runner = args.source / "src/guitests/guitests.cc" if args.source else None
                    if not source_runner or not source_runner.exists() or '"OPENSCAD_GUI_TEST_FUNCTIONS"' not in source_runner.read_text(encoding="utf-8"):
                        gaps.append({"id": "gui-" + selection, "status": "NOT_RUN", "reason": "Matching source does not declare function filtering"})
                        continue
                    extra["OPENSCAD_GUI_TEST_FUNCTIONS"] = ",".join(args.gui_function)
                if selection in ("all", "annotations"):
                    script = args.source / "tests/annotations/LiveHttpWorkflow.py" if args.source else None
                    if script and script.exists():
                        extra.update(OPENSCAD_AGENT_TEST_WORKFLOW=str(script), OPENSCAD_ANNOTATION_TEST_PYTHON=sys.executable)
                    else:
                        gaps.append({"id": "http-live", "status": "NOT_RUN", "reason": "Provide matching --source for tests/annotations/LiveHttpWorkflow.py"})
                # IsSet selectors must be absent, not empty. Remove them from inherited environment below.
                if selection != "all":
                    extra[catalog["gui_selectors"][selection]] = "1"
                add(suite + "-" + selection, [args.runtime / "scadmaxx.com", "--run-all-gui-tests"], extra=extra)
    elif adapter == "performance":
        require(args, "baseline", "candidate")
        add(suite, [sys.executable, CONTROL / "experimental/scripts/Test-RenderPerformance.py", "--baseline", args.baseline,
                    "--candidate", args.candidate, "--output", folder / "measurement", "--backend", args.backend,
                    "--suite", "extended" if args.profile == "perf-extended" else "quick"])
    elif adapter in ("corpus", "corpus-report"):
        require(args, "corpus", "baseline_executable", "candidate_executable")
        for index, corpus in enumerate(args.corpus):
            samples = root / "corpus" / str(index) / "samples"
            if adapter == "corpus":
                command = [sys.executable, SHARED / "benchmark.py", "--corpus", corpus, "--output", samples,
                           "--build", "baseline=" + str(args.baseline_executable), "--build", "candidate=" + str(args.candidate_executable),
                           "--stages", "stl", "--backend", args.backend, "--repetitions", str(args.repetitions), "--timeout", str(args.model_timeout)]
                for argument in args.build_argument:
                    command.append("--build-argument=" + argument)
                add(suite + "-" + str(index), command)
            else:
                add(suite + "-" + str(index), [sys.executable, SHARED / "report.py", samples, "--output", folder / str(index) / "report"])
    else:
        raise ValueError(f"Unknown adapter: {adapter}")
    return result, gaps


def identity(args):
    value = {"runner_sha256": digest(__file__), "catalog_sha256": digest(CATALOG), "runtime_files": {},
             "feature_inventory_sha256": digest(CONTROL / read(CATALOG)["feature_inventory"])}
    for name in ("baseline", "candidate"):
        path = getattr(args, name)
        if path:
            value[name] = {"path": str(path), "sha256": digest(path)}
    if args.corpus:
        value["corpus_manifest_sha256"] = {str(corpus): digest(corpus / "manifest.json") for corpus in args.corpus}
    if args.provider_libraries:
        value["provider_libraries"] = {"descriptor_sha256": digest(args.provider_libraries), "libraries": {}}
        for name, record in read(args.provider_libraries).items():
            directory = Path(record["root"])
            value["provider_libraries"]["libraries"][name] = {p.relative_to(directory).as_posix(): digest(p)
                for p in directory.rglob("*") if p.is_file()}
    if args.runtime:
        for pattern in ("*.exe", "*.com", "*.dll", "platforms/*.dll"):
            for path in sorted(args.runtime.glob(pattern)):
                value["runtime_files"][str(path)] = digest(path)
    for executable in (args.baseline_executable, args.candidate_executable):
        if executable:
            for path in [executable, executable.with_suffix(".exe"), *executable.parent.glob("*.dll")]:
                if path.is_file():
                    value["runtime_files"][str(path)] = digest(path)
    if args.build:
        for name in ("CMakeCache.txt", "experimental-state.json", "OpenSCADUnitTests.exe", "VimEngineTests.exe", "scadmaxx.exe", "scadmaxx.com"):
            path = args.build / name
            if path.exists():
                value.setdefault("build_files", {})[str(path)] = digest(path)
        state = args.build / "experimental-state.json"
        value["build_state"] = read(state) if state.exists() else None
    if args.source:
        proc = subprocess.run(["git", "-C", str(args.source), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        value["observed_source_head"] = proc.stdout.strip()
        proc = subprocess.run(["git", "-C", str(args.source), "status", "--porcelain"], capture_output=True, text=True, check=True)
        value["observed_source_status"] = proc.stdout
        value["test_input_files"] = {}
        for path in sorted((args.source / "tests").rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and not any(part.startswith("build") for part in path.relative_to(args.source / "tests").parts):
                value["test_input_files"][str(path)] = digest(path)
    return value


def main(argv=None):
    catalog = read(CATALOG)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=list(catalog["profiles"]))
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--run", action="store_true", help="Execute tests; omitted means print a plan")
    parser.add_argument("--discover", action="store_true", help="Read CTest metadata without executing tests")
    parser.add_argument("--allow-desktop", action="store_true", help="Explicit authorization to open and manipulate windows")
    parser.add_argument("--quiet-machine", action="store_true", help="Confirm no competing builds/benchmarks; use consistent CPU budget")
    for name in ("output", "build", "runtime", "source", "annotation-build", "customizer-build", "baseline", "candidate", "baseline-executable", "candidate-executable", "provider-libraries"):
        parser.add_argument("--" + name, type=lambda value: Path(value).resolve())
    parser.add_argument("--corpus", type=lambda value: Path(value).resolve(), action="append")
    parser.add_argument("--build-argument", action="append", default=[], help="Corpus: label=argument; repeat for effective feature switches")
    parser.add_argument("--ctest", default=shutil.which("ctest") or "ctest")
    parser.add_argument("--pwsh", default=shutil.which("pwsh") or "pwsh")
    parser.add_argument("--gui-suite", action="append", choices=["all", *catalog["gui_selectors"]])
    parser.add_argument("--gui-function", action="append", default=[], help="Run named Qt test functions in one selected GUI suite; repeat to retain order")
    parser.add_argument("--expected-version", help="Required version substring for runtime smoke checks")
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument("--memory-mb", type=int, default=4096)
    parser.add_argument("--backend", choices=["CGAL", "Manifold"])
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--model-timeout", type=float, default=60)
    args = parser.parse_args(argv)
    if args.gui_function and (args.profile != "desktop" or not args.gui_suite or len(args.gui_suite) != 1 or args.gui_suite[0] == "all"):
        parser.error("--gui-function requires the desktop profile and exactly one named --gui-suite")
    if args.list:
        print(json.dumps(catalog, indent=2))
        return 0
    if not args.profile:
        parser.error("--profile is required")
    args.backend = args.backend or ("Manifold" if args.profile.startswith("perf-") else "CGAL")
    if args.threads < 1 or args.threads > 32 or args.memory_mb < 256 or args.repetitions < 1 or args.model_timeout <= 0:
        parser.error("Invalid resource or sampling budget")
    suites = catalog["profiles"][args.profile]
    if args.run:
        require(args, "output")
        if args.output.exists():
            parser.error("Use a new output directory; existing evidence is preserved")
        if any(catalog["suites"][s]["execution"] == "desktop" for s in suites) and not args.allow_desktop:
            parser.error("Desktop profile requires --allow-desktop; it opens windows and sends input")
        if any(catalog["suites"][s]["execution"] == "quiet" for s in suites) and not args.quiet_machine:
            parser.error("Timing profile requires --quiet-machine")
    root = args.output or Path("PROFILE_OUTPUT")
    commands, gaps = [], []
    for suite in suites:
        selected, absent = jobs(suite, catalog["suites"][suite], args, root, catalog, args.discover or args.run)
        commands.extend(selected)
        gaps.extend(absent)
    plan = {"profile": args.profile, "commands": commands, "coverage_gaps": gaps,
            "resources": {"threads": args.threads, "memory_mb": args.memory_mb, "parallel_suites": 1},
            "separate_coverage": catalog["separate_coverage"],
            "selected_feature_coverage": read(CONTROL / catalog["feature_inventory"])}
    feature_index = plan["selected_feature_coverage"]
    feature_index["matches_current_selection"] = feature_index["selection_sha256"] == digest(CONTROL / "experimental/PR_STACK.md") and feature_index["dependencies_sha256"] == digest(CONTROL / "experimental/DEPENDENCIES.json")
    print(json.dumps(plan if not args.run else {"profile": args.profile, "suites": suites,
          "command_count": sum("command" in c for c in commands), "coverage_gaps": gaps,
          "resources": plan["resources"], "output": str(root)}, indent=2), flush=True)
    if not args.run:
        return 0
    before = identity(args)
    feature_index["matches_observed_source"] = before.get("observed_source_head") == feature_index["integration_head"] if args.source else None
    feature_index["matches_build_revision"] = before["build_state"].get("builtSha") == feature_index["integration_head"] if args.build and before["build_state"] else None
    if args.build and args.source and before["build_state"]:
        if before["build_state"].get("builtSha") != before["observed_source_head"] or before["observed_source_status"]:
            raise ValueError("Source differs from recorded build: preserve evidence and use matching source/build inputs")
    args.output.mkdir(parents=True, exist_ok=False)
    save(root / "plan.json", plan)
    save(root / "identity.json", before)
    rows = list(gaps)
    # A lock covers all profiles, so background jobs cannot overlap a timing or desktop profile.
    lock = CONTROL.parent / "runs/.test-profile.lock"
    lock_fd = None
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(lock_fd, json.dumps({"pid": os.getpid(), "output": str(root), "profile": args.profile}).encode())
        for suite in suites:
            folder = root / suite
            folder.mkdir(parents=True, exist_ok=True)
            if catalog["suites"][suite]["adapter"] == "smoke":
                (folder / "smoke.scad").write_text("difference(){cube([12,12,6],center=true);cylinder(h=10,r=3,center=true,$fn=32);}", encoding="ascii")
                (folder / "flat.scad").write_text("difference(){square([20,20],center=true);circle(r=5,$fn=32);}", encoding="ascii")
            for command in (c for c in commands if "command" in c and (c["id"] == suite or c["id"].startswith(suite + "-") and
                             not (suite == "corpus" and c["id"].startswith("corpus-report-")) or
                             suite == "harness" and c["id"].endswith("-harness"))):
                if command["id"].startswith("gui-"):
                    selection = command["id"][4:]
                    (folder / selection).mkdir(exist_ok=True)
                env = command["env"]
                # qEnvironmentVariableIsSet requires absence for unused selectors.
                inherited = {k: os.environ.pop(k) for k in list(os.environ) if k in catalog["gui_selectors"].values()}
                env = {k: v for k, v in env.items() if k not in catalog["gui_selectors"].values() or v}
                try:
                    result = execute(command["command"], command["cwd"], env, command["timeout"],
                                     folder / command["id"], args, command["execution"] == "quiet")
                finally:
                    os.environ.update(inherited)
                result["id"] = command["id"]
                if suite == "cli-smoke" and result["status"] == "PASS":
                    argv = command["command"]
                    log = "\n".join((folder / command["id"] / name).read_text(encoding="utf-8", errors="replace")
                                    for name in ("stdout.txt", "stderr.txt"))
                    if "ERROR:" in log:
                        result.update(status="FAIL", reason="Export reported an error")
                    if "--version" in argv and args.expected_version and args.expected_version not in log:
                        result.update(status="FAIL", reason="Unexpected runtime version")
                    if "-o" in argv:
                        path = Path(argv[argv.index("-o") + 1])
                        if not path.exists() or path.stat().st_size < 100:
                            result.update(status="FAIL", reason="Missing or empty exported artifact")
                if suite == "corpus" and result["status"] == "PASS":
                    result.update(status="OBSERVATION", reason="Corpus failures are classified per model; completion is not acceptance")
                rows.append(result)
                save(root / "results.json", rows)
                print(f"{result['status']} {result['id']}", flush=True)
                if result["status"] in ("FAIL", "INCONCLUSIVE"):
                    break
        after = identity(args)
        if after != before:
            rows.append({"id": "identity", "status": "INCONCLUSIVE", "reason": "Inputs changed during execution"})
    except (Exception, KeyboardInterrupt) as error:
        rows.append({"id": "runner", "status": "INCONCLUSIVE", "reason": str(error) or "Interrupted"})
    finally:
        if lock_fd is not None:
            os.close(lock_fd)
            lock.unlink()
        completed = {r["id"] for r in rows}
        rows.extend({"id": c["id"], "status": "NOT_RUN", "reason": "Earlier execution stopped"}
                    for c in commands if "command" in c and c["id"] not in completed)
        save(root / "results.json", rows)
        status = "PASS" if rows and all(r["status"] == "PASS" for r in rows) else "NEEDS_REVIEW"
        if args.profile == "realworld" and all(r["status"] in ("PASS", "OBSERVATION") for r in rows):
            status = "VERIFICATION_RECORDED"
        save(root / "summary.json", {"profile": args.profile, "status": status, "results": rows,
                                     "scope": "Selected profile only; separate coverage is listed in plan.json"})
        (root / "report.md").write_text("# SCADMaxx test profile\n\n" + f"Profile: {args.profile}\n\nOutcome: {status}\n\n"
            + "| Check | Outcome |\n| --- | --- |\n" + "".join(f"| {row['id']} | {row['status']} |\n" for row in rows)
            + "\nSee plan.json for exclusions and separate coverage; identity.json identifies the actual inputs.\n", encoding="utf-8")
        print(f"{status}: {root / 'summary.json'}")
    return 0 if status in ("PASS", "VERIFICATION_RECORDED") else 2


if __name__ == "__main__":
    raise SystemExit(main())
