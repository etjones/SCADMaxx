"""Selection and authorization checks; no OpenSCAD processes or desktop windows."""
import importlib.util
import contextlib
import io
import json
import ctypes
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/Test-Profiles.py"
spec = importlib.util.spec_from_file_location("test_profiles_runner", SCRIPT)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
CATALOG = runner.read(runner.CATALOG)


def cli(name, script="test_cmdline_tool.py", properties=None):
    return {"name": name, "command": ["python.exe", script], "properties": properties or []}


class SelectionTests(unittest.TestCase):
    def test_union_keeps_default_only_and_deduplicates(self):
        inputs = {"Good": [cli("common")], "Default": [cli("common"), cli("default-only")], "Bugs": []}
        selected, excluded, missing = runner.healthy_selection(inputs, CATALOG)
        self.assertEqual(set(selected), {"common", "default-only"})
        self.assertEqual(selected["common"]["config"], "Good")
        self.assertEqual(excluded, [])
        self.assertEqual(missing, [])

    def test_known_bugs_never_enter_acceptance_union(self):
        inputs = {"Good": [cli("broken")], "Default": [], "Bugs": [cli("broken")]}
        selected, excluded, _ = runner.healthy_selection(inputs, CATALOG)
        self.assertEqual(selected, {})
        self.assertEqual(excluded[0]["reason"], "KNOWN_BASELINE_FAILURE_CATEGORY")

    def test_unknown_commands_cannot_enter_background(self):
        inputs = {"Good": [cli("unknown", "show_windows.py")], "Default": [], "Bugs": []}
        selected, excluded, _ = runner.healthy_selection(inputs, CATALOG)
        self.assertFalse(selected)
        self.assertEqual(excluded[0]["reason"], "UNCLASSIFIED_COMMAND")

    def test_windows_override_is_rejected(self):
        test = cli("windowed", properties=[{"name": "ENVIRONMENT", "value": ["QT_QPA_PLATFORM=windows"]}])
        selected, excluded, _ = runner.healthy_selection({"Good": [test], "Default": [], "Bugs": []}, CATALOG)
        self.assertFalse(selected)
        self.assertEqual(excluded[0]["reason"], "DESKTOP_ENVIRONMENT")

    def test_missing_critical_tests_are_reported(self):
        _, _, missing = runner.healthy_selection({"Good": [], "Default": [], "Bugs": []}, CATALOG, True)
        self.assertEqual(set(missing), set(CATALOG["ctest"]["critical_names"]))

    def test_missing_golden_remains_an_explicit_coverage_gap(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "test_cmdline_tool.py"
            test = cli("example", str(script))
            test["command"] += ["-s", "csg", "-t", "dump", "-e", "shared", "-f", "example", "app.exe", "example.scad"]
            inventories = {"Good": [test], "Default": [], "Bugs": []}
            selected, excluded, _ = runner.healthy_selection(inventories, CATALOG)
            self.assertFalse(selected)
            self.assertTrue(excluded[0]["reason"].startswith("MISSING_GOLDEN:"))
            golden = Path(directory) / "regression/shared/example-expected.csg"
            golden.parent.mkdir(parents=True)
            golden.write_text("cube(1);", encoding="utf-8")
            selected, excluded, _ = runner.healthy_selection(inventories, CATALOG)
            self.assertEqual(set(selected), {"example"})
            self.assertEqual(excluded, [])

    def test_dependencies_stay_in_same_ctest_invocation(self):
        selected = {"run": {"config": "Default", "test": cli("run")},
                    "check": {"config": "Default", "test": cli("check", properties=[{"name": "DEPENDS", "value": ["run"]}])}}
        self.assertEqual(runner.ctest_chunks(selected, "Default"), [["check", "run"]])

    def test_unselected_dependency_is_rejected(self):
        selected = {"check": {"config": "Default", "test": cli("check", properties=[{"name": "DEPENDS", "value": ["missing"]}])}}
        with self.assertRaises(ValueError):
            runner.ctest_chunks(selected, "Default")

    def test_background_profiles_exclude_desktop_and_corpus(self):
        for profile in ("everyday", "deep-background", "distribution", "tools"):
            for suite in CATALOG["profiles"][profile]:
                self.assertEqual(CATALOG["suites"][suite]["execution"], "background")
                self.assertNotIn(suite, ("corpus", "gui", "performance"))

    def test_desktop_execution_requires_explicit_authorization(self):
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(SystemExit) as error:
            runner.main(["--profile", "desktop", "--run", "--output", str(Path(directory) / "new")])
        self.assertEqual(error.exception.code, 2)

    def test_visual_profile_cannot_enter_background(self):
        self.assertEqual(CATALOG["suites"]["unit-visual"]["execution"], "desktop")


class GuiFunctionSelectionTests(unittest.TestCase):
    def test_filter_requires_one_named_desktop_suite(self):
        for options in ([], ["--gui-suite", "all"], ["--gui-suite", "navigation", "--gui-suite", "insertion"]):
            with self.subTest(options=options), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                runner.main(["--profile", "desktop", "--gui-function", "cubeTargetsAndGestures", *options])
            self.assertEqual(error.exception.code, 2)

    def test_explicit_filter_survives_inherited_selector_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CMakeCache.txt").write_text("ENABLE_GUI_TESTS:BOOL=ON\n", encoding="utf-8")
            source = root / "src/guitests/guitests.cc"
            source.parent.mkdir(parents=True)
            source.write_text('qEnvironmentVariable("OPENSCAD_GUI_TEST_FUNCTIONS")', encoding="utf-8")
            output = io.StringIO()
            with patch.dict(os.environ, OPENSCAD_GUI_TEST_FUNCTIONS="unrelated"), contextlib.redirect_stdout(output):
                runner.main(["--profile", "desktop", "--gui-suite", "navigation", "--gui-function", "documentMetadataLifetimeProbe",
                             "--gui-function", "cubeTargetsAndGestures", "--source", directory, "--build", directory, "--runtime", directory])
            plan = json.loads(output.getvalue())
            self.assertEqual(len(plan["commands"]), 1)
            self.assertEqual(plan["commands"][0]["env"]["OPENSCAD_GUI_TEST_FUNCTIONS"],
                             "documentMetadataLifetimeProbe,cubeTargetsAndGestures")


class FeatureInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script = SCRIPT.parent / "Audit-FeatureTests.py"
        specification = importlib.util.spec_from_file_location("feature_audit", script)
        cls.audit = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(cls.audit)

    def test_only_enabled_table_rows_are_selected(self):
        text = "## Enabled stack (ordered)\n| 1 | sample | feature | source | latest | merge | none declared | reason |\n## Disabled\n| 2 | excluded | feature | source | latest | merge | none declared | reason |\n"
        self.assertEqual([e["id"] for e in self.audit.selection(text)], ["sample"])

    def test_customizer_standalone_is_not_mistaken_for_main_unit(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "group_visibility_test.cc"
            target.touch()
            row = self.audit.classify("tests/customizer-group-visibility/group_visibility_test.cc", "", target, "", "", "", set(), set(), "")
        self.assertEqual(row["suite"], "customizer")

    def test_missing_owner_case_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "Example_test.cc"
            target.touch()
            row = self.audit.classify("src/core/Example_test.cc", 'TEST_CASE("new case", "[x]") {}', target, "", "", "", set(), set(), "")
        self.assertEqual(row["missing_case_names"], ["new case"])
        self.assertEqual(row["status"], "REVIEW_SOURCE_WIRING")


@unittest.skipUnless(os.name == "nt", "Windows job-object execution")
class ResourceControlTests(unittest.TestCase):
    def test_missing_binary_is_not_run_and_next_command_can_execute(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            args = SimpleNamespace(threads=1, memory_mb=512)
            absent = runner.execute([folder / "missing.exe"], folder, {}, 10, folder / "absent", args)
            self.assertEqual(absent["status"], "NOT_RUN")
            self.assertIn("Missing executable", absent["reason"])
            next_result = runner.execute([sys.executable, "-c", "print('next suite')"], folder, {}, 10,
                                         folder / "next", args)
            self.assertEqual(next_result["status"], "PASS")

    def test_python_process_runs_with_bounded_affinity(self):
        code = "import ctypes; k=ctypes.WinDLL('kernel32'); p=ctypes.c_size_t(); s=ctypes.c_size_t(); k.GetProcessAffinityMask(ctypes.c_void_p(-1),ctypes.byref(p),ctypes.byref(s)); print(p.value)"
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            result = runner.execute([sys.executable, "-c", code], folder, {}, 10, folder,
                                    SimpleNamespace(threads=1, memory_mb=512))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual((folder / "stdout.txt").read_text().strip(), "1")

    def test_timeout_kills_descendant_process(self):
        code = "import subprocess,sys,time; child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); print(child.pid,flush=True); time.sleep(60)"
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            result = runner.execute([sys.executable, "-c", code], folder, {}, 1, folder,
                                    SimpleNamespace(threads=1, memory_mb=512))
            self.assertEqual(result["status"], "INCONCLUSIVE")
            pid = int((folder / "stdout.txt").read_text().strip())
            kernel = ctypes.WinDLL("kernel32")
            kernel.OpenProcess.restype = ctypes.c_void_p
            handle = kernel.OpenProcess(0x1000, False, pid)
            if handle:
                try:
                    status = ctypes.c_ulong()
                    kernel.GetExitCodeProcess(ctypes.c_void_p(handle), ctypes.byref(status))
                    self.assertNotEqual(status.value, 259)
                finally:
                    kernel.CloseHandle(ctypes.c_void_p(handle))


if __name__ == "__main__":
    unittest.main()
