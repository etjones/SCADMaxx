"""Paired integration benchmarks. Reuses the existing real-world process/geometry harness."""
import argparse
import csv
import json
import os
from pathlib import Path
import platform
import re
import shutil
import statistics
import subprocess
import sys
import time

CONTROL = Path(__file__).resolve().parents[2]
SHARED = CONTROL / "tools/evaluation-benchmark/realworld"
sys.path.insert(0, str(SHARED))
from benchmark import execute, file_hash, runtime_identity, dependency_identity, SCOPES, STAGES
from geometry import compare_outputs, load_mesh, metrics
from PIL import Image
import numpy as np

PASS_OUTPUT = {"exact_surface", "within_tolerance_sampled", "identical_text", "identical_image"}
BUILD_TOOLS = {"cl.exe", "link.exe", "ninja.exe", "cmake.exe"}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def active_builds():
    if os.name != "nt":
        return []  # Non-Windows contention must be assessed by the operator.
    # Toolhelp avoids tasklist's expensive session/name resolution between every sample.
    import ctypes
    from ctypes import wintypes
    class Entry(ctypes.Structure):
        _fields_ = [("size", wintypes.DWORD), ("usage", wintypes.DWORD), ("pid", wintypes.DWORD),
                    ("heap", ctypes.c_size_t), ("module", wintypes.DWORD), ("threads", wintypes.DWORD),
                    ("parent", wintypes.DWORD), ("priority", wintypes.LONG), ("flags", wintypes.DWORD),
                    ("name", wintypes.WCHAR * 260)]
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.Process32FirstW.argtypes = kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(Entry)]
    handle = kernel.CreateToolhelp32Snapshot(2, 0)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        entry = Entry()
        entry.size = ctypes.sizeof(entry)
        found, result = kernel.Process32FirstW(handle, ctypes.byref(entry)), []
        while found:
            if entry.name.lower() in BUILD_TOOLS:
                result.append([entry.name, entry.pid])
            found = kernel.Process32NextW(handle, ctypes.byref(entry))
        if ctypes.get_last_error() != 18:  # ERROR_NO_MORE_FILES
            raise ctypes.WinError(ctypes.get_last_error())
        return result
    finally:
        kernel.CloseHandle(handle)


def wait_idle(limit):
    start = time.monotonic()
    while busy := active_builds():
        if time.monotonic() - start >= limit:
            raise RuntimeError(f"Compiling processes still active: {busy}; no clean timing claim")
        print(f"Waiting for other compilation: {busy[:4]}", flush=True)
        time.sleep(10)


def describe_build(path):
    descriptor = read(path)
    required = {"label", "executable", "source_revision", "source_dirty", "configuration", "evidence"}
    if not required <= descriptor.keys():
        raise ValueError(f"Build descriptor needs {sorted(required)}")
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", descriptor["label"]):
        raise ValueError("Invalid build label")
    executable = Path(descriptor["executable"]).resolve(strict=True)
    if not re.fullmatch(r"[0-9a-f]{40}", descriptor["source_revision"]):
        raise ValueError("Record the full source revision used to build this executable")
    if descriptor["source_dirty"] and not descriptor.get("source_snapshot_sha256"):
        raise ValueError("Dirty builds require their actual built source snapshot hash")
    if not descriptor["evidence"] or not descriptor["configuration"]:
        raise ValueError("Build configuration and evidence are required")
    evidence = {str(Path(p).resolve(strict=True)): file_hash(p) for p in descriptor["evidence"]}
    return {"descriptor": descriptor, "descriptor_sha256": file_hash(path), "evidence": evidence,
            "runtime": runtime_identity(executable)}


def environment(executable, folder, library_paths):
    env = os.environ.copy()
    for name in list(env):
        if name.startswith(("SCADMAXX_PROBE", "SCADMAXX_PROFILE", "QT_")):
            env.pop(name)
    runtime = executable.parent
    env.update(OPENSCADPATH=os.pathsep.join(map(str, library_paths)),
               OPENSCAD_TEST_SETTINGS_DIR=str(folder / "settings"),
               QT_QPA_PLATFORM="offscreen", QT_PLUGIN_PATH=str(runtime),
               QT_QPA_PLATFORM_PLUGIN_PATH=str(runtime / "platforms"))
    if os.name == "nt":
        env["PATH"] = str(runtime) + os.pathsep + str(Path(os.environ["SystemRoot"]) / "System32")
    return env


def valid_output(path, stage):
    if not path.is_file() or not path.stat().st_size:
        raise ValueError("Missing or empty output")
    if stage == "csg":
        if not re.search(r"\b(cube|sphere|cylinder|polyhedron|polygon|square|circle|text|import|surface)\s*\(",
                         path.read_text(errors="replace")):
            raise ValueError("No geometry in CSG output")
        return {"sha256": file_hash(path)}
    if stage == "preview":
        with Image.open(path) as image:
            image.load()
            if image.size != (512, 512) or np.unique(np.asarray(image).reshape(-1, len(image.getbands())), axis=0).shape[0] < 2:
                raise ValueError("Invalid size or blank preview")
        return {"sha256": file_hash(path), "size": [512, 512]}
    result = metrics(load_mesh(path))
    if not result["watertight"] or not result["winding_consistent"] or result["volume"] <= 0:
        raise ValueError("Final solid is not closed, consistently wound, positive-volume geometry")
    return result


def classify(baseline, candidate, policy, compatible=True):
    """Never turn failed, missing, noisy or incompatible samples into a speedup/pass."""
    if not compatible:
        return {"status": "incompatible_configuration"}
    if len(baseline) != len(candidate) or len(baseline) < policy["repetitions"]:
        return {"status": "incomplete"}
    if any(x["status"] != "ok" for x in baseline + candidate):
        return {"status": "execution_or_output_failure"}
    a, b = [x["seconds"] for x in baseline], [x["seconds"] for x in candidate]
    ma, mb = statistics.median(a), statistics.median(b)
    if ma <= 0 or mb <= 0:
        return {"status": "invalid_timing"}
    mad_a = statistics.median(abs(x - ma) for x in a) / ma
    mad_b = statistics.median(abs(x - mb) for x in b) / mb
    delta = mb - ma
    result = {"baseline_seconds": ma, "candidate_seconds": mb, "delta_seconds": delta,
              "delta_percent": 100 * delta / ma, "baseline_range": [min(a), max(a)],
              "candidate_range": [min(b), max(b)], "relative_mad": [mad_a, mad_b]}
    if max(mad_a, mad_b) > policy["max_relative_mad"]:
        result["status"] = "noisy_inconclusive"
    elif delta > max(policy["absolute_limit_seconds"], ma * policy["relative_limit"]):
        result["status"] = "regression" if sum(y > x for x, y in zip(a, b)) >= len(a) * .8 else "noisy_inconclusive"
    else:
        result["status"] = "pass"
    return result


def sample(executable, case, stage, repetition, label, root, fixtures, args, extra_arguments, warmup):
    folder = root / "samples" / case["id"] / stage / ("warmup" if warmup else str(repetition)) / label
    folder.mkdir(parents=True)
    source = Path(case.get("local_path", fixtures / case["file"]))
    result = folder / ("model" + STAGES[stage])
    command = [str(executable), "--backend=" + args.backend, *extra_arguments,
               "-D", "$preview=" + ("false" if stage == "off" else "true"),
               "-o", str(result), "-d", str(folder / "dependencies.txt")]
    if stage == "preview":
        command += ["--preview", "--imgsize=512,512", "--autocenter", "--viewall"]
    command.append(str(source))
    wait_idle(args.wait_idle)
    row = execute(command, source.parent, environment(executable, folder, args.library_path if case.get("local_path") else []),
                  args.timeout, folder / "process")
    busy_after = active_builds()
    dependencies, external = dependency_identity(folder / "dependencies.txt", fixtures, executable.parent)
    row.update(case=case["id"], stage=stage, repetition=repetition, build=label, warmup=warmup,
               output=str(result.relative_to(root)), dependencies=dependencies,
               build_processes_after=busy_after, status="ok")
    if row["timed_out"] or row["exit_code"] or row["diagnostics"]:
        row["status"] = "execution_failed"
    elif busy_after:
        row["status"] = "contended"
    elif not dependencies or (external and not case.get("local_path")):
        row["status"] = "unfrozen_dependency"
    else:
        try:
            row["output_metrics"] = valid_output(result, stage)
            row["output_sha256"] = file_hash(result)
        except Exception as error:
            row.update(status="invalid_output", error=str(error))
    return row


def report(root, rows, policy, compatible):
    metadata = read(root / "metadata.json")
    groups = sorted({(c["id"], stage) for c in metadata["cases"] for stage in metadata["stages"] if stage in c["stages"]})
    results = []
    comparisons = {}
    for case, stage in groups:
        group = [r for r in rows if r["case"] == case and r["stage"] == stage]
        good = [r for r in group if r["status"] == "ok"]
        # Frozen dependencies and stable output must hold across warmups and both builds.
        identities = {json.dumps(r["dependencies"], sort_keys=True) for r in good}
        first = good[0] if good else None
        for row in good:
            key = (first["output_sha256"], row["output_sha256"], stage)
            if key not in comparisons:
                try:
                    comparisons[key] = compare_outputs(root / first["output"], root / row["output"], stage)
                except Exception as error:
                    comparisons[key] = {"status": "comparison_error", "error": str(error)}
            row["comparison"] = comparisons[key]
            if comparisons[key]["status"] not in PASS_OUTPUT:
                row["status"] = "output_changed"
        baseline = [r for r in group if not r["warmup"] and r["build"] == "baseline"]
        candidate = [r for r in group if not r["warmup"] and r["build"] == "candidate"]
        result = classify(baseline, candidate, policy, compatible)
        if len(identities) > 1:
            result["status"] = "dependency_mismatch"
        elif any(r["status"] != "ok" for r in group if r["warmup"]):
            result["status"] = "warmup_failed"
        results.append(dict(case=case, stage=stage, **result))
    status = "pass" if results and all(r["status"] == "pass" for r in results) else "needs_review"
    if (root / "interruption.json").exists():
        status = "interrupted"
    save(root / "results.json", rows)
    save(root / "summary.json", {"status": status, "policy": policy, "cases": results,
                                "coverage": "Fresh-process CLI CSG, PNG preview and OFF final geometry; no native GUI timings"})
    lines = ["# SCADMaxx performance regression comparison", "", f"Outcome: **{status}**.", "",
             "Fresh processes; OS caches uncontrolled. PNG preview is not native GUI first-frame latency.",
             "No GUI re-preview, viewport FPS, responsiveness or cancellation measurements in this run.",
             "Limits are initial conservative screening limits; no baseline is automatically promoted.", "",
             "| Case | Stage | Baseline s | Candidate s | Change | Outcome |",
             "|---|---|---:|---:|---:|---|"]
    for r in results:
        values = [f"{r[k]:.3f}" if k in r else "—" for k in ("baseline_seconds", "candidate_seconds")]
        change = f"{r['delta_percent']:+.1f}%" if "delta_percent" in r else "—"
        lines.append(f"| {r['case']} | {r['stage']} | {values[0]} | {values[1]} | {change} | {r['status']} |")
    (root / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (root / "summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["case", "stage", "baseline_seconds", "candidate_seconds", "delta_percent", "status"], extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True, help="Explicit build descriptor JSON")
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=CONTROL / "experimental/performance/cases.json")
    parser.add_argument("--suite", choices=["quick", "extended"], default="quick")
    parser.add_argument("--backend", choices=["Manifold", "CGAL"], default="Manifold")
    parser.add_argument("--stages", nargs="+", choices=["csg", "preview", "off"], default=["csg", "preview", "off"])
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--wait-idle", type=float, default=600)
    parser.add_argument("--local-model", type=Path, help="Optional read-only private regression model")
    parser.add_argument("--library-path", type=Path, action="append", default=[])
    args = parser.parse_args()
    if args.repetitions < 5 or args.timeout <= 0 or args.wait_idle < 0:
        parser.error("Use at least five measured repetitions and positive timeout")
    manifest = read(args.manifest)
    policy = dict(manifest["policy"], repetitions=args.repetitions, timeout_seconds=args.timeout)
    cases = [c for c in manifest["cases"] if args.suite == "extended" or c["group"] == "quick"]
    if args.ids:
        cases = [c for c in cases if c["id"] in args.ids]
        if set(args.ids) != {c["id"] for c in cases}:
            parser.error("Unknown or excluded case IDs")
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=False)
    fixtures = root / "fixtures"
    shutil.copytree(args.manifest.parent / "fixtures", fixtures)
    shutil.copy2(args.manifest, root / "cases.json")
    tooling = root / "tooling"
    tooling.mkdir()
    shutil.copy2(__file__, tooling / Path(__file__).name)
    for name in ("benchmark.py", "geometry.py", "corpus.py", "uv.lock", "pyproject.toml"):
        shutil.copy2(SHARED / name, tooling / name)
    builds = {"baseline": describe_build(args.baseline), "candidate": describe_build(args.candidate)}
    if args.local_model:
        cases.append({"id": "local-model", "file": "", "local_path": str(args.local_model.resolve(strict=True)),
                      "stages": ["csg", "preview"]})
    fixture_hashes = {p.relative_to(fixtures).as_posix(): file_hash(p) for p in sorted(fixtures.glob("*.scad"))}
    meta = {"schema": 1, "builds": builds, "manifest_sha256": file_hash(args.manifest), "fixture_hashes": fixture_hashes,
            "cases": cases, "policy": policy, "backend": args.backend, "stages": args.stages, "scopes": SCOPES,
            "machine": {"platform": platform.platform(), "processor": platform.processor(), "cpus": os.cpu_count()},
            "library_paths": list(map(str, args.library_path)), "runner_sha256": file_hash(__file__),
            "shared_code_sha256": {name: file_hash(SHARED / name) for name in ("benchmark.py", "geometry.py", "corpus.py")}}
    if os.name == "nt":
        info = subprocess.run(["powershell", "-NoProfile", "-Command",
            "@{cpu=@(Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors);gpu=@(Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion)} | ConvertTo-Json -Depth 4"],
            capture_output=True, text=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
        meta["hardware"] = json.loads(info.stdout) if info.returncode == 0 else {"unavailable": info.stderr}
    save(root / "metadata.json", meta)
    compatible = builds["baseline"]["descriptor"]["configuration"] == builds["candidate"]["descriptor"]["configuration"]
    rows = []
    try:
        for case in cases:
            for stage in args.stages:
                if stage not in case["stages"]:
                    continue
                for repetition in range(-1, args.repetitions):
                    order = ["baseline", "candidate"] if repetition % 2 else ["candidate", "baseline"]
                    for label in order:
                        executable = Path(builds[label]["runtime"]["executable"])
                        row = sample(executable, case, stage, repetition, label, root, fixtures, args, manifest["arguments"], repetition < 0)
                        rows.append(row)
                        with (root / "samples.jsonl").open("a", encoding="utf-8") as stream:
                            stream.write(json.dumps(row) + "\n")
                        print(f"{case['id']} {stage} {label} {'warmup' if repetition < 0 else repetition+1}: {row['seconds']:.3f}s {row['status']}", flush=True)
                        if row["status"] != "ok":
                            raise RuntimeError(f"Failed sample retained: {row['status']}")
        for label, build in builds.items():
            for relative, expected in build["runtime"]["files"].items():
                if file_hash(Path(build["runtime"]["executable"]).parent / relative) != expected:
                    raise RuntimeError(f"Runtime changed during measurement: {label}/{relative}")
    except Exception as error:
        save(root / "interruption.json", {"error": str(error), "completed_samples": len(rows)})
        report(root, rows, policy, compatible)
        raise
    status = report(root, rows, policy, compatible)
    print(f"{status}: {root / 'report.md'}", flush=True)
    return 0 if status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
