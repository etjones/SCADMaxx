import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/Test-RenderPerformance.py"
spec = importlib.util.spec_from_file_location("render_performance", SCRIPT)
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)
POLICY = dict(repetitions=5, relative_limit=.15, absolute_limit_seconds=.1, max_relative_mad=.15)


def samples(times):
    return [dict(seconds=t, status="ok") for t in times]


class RegressionPolicyTests(unittest.TestCase):
    def test_known_slowdown_is_detected(self):
        self.assertEqual(suite.classify(samples([1]*5), samples([1.3]*5), POLICY)["status"], "regression")

    def test_absolute_limit_avoids_tiny_sample_false_alarm(self):
        self.assertEqual(suite.classify(samples([.02]*5), samples([.04]*5), POLICY)["status"], "pass")

    def test_failure_is_never_fast_success(self):
        candidate = samples([.001]*5)
        candidate[0]["status"] = "execution_failed"
        self.assertEqual(suite.classify(samples([1]*5), candidate, POLICY)["status"], "execution_or_output_failure")

    def test_missing_samples_do_not_pass(self):
        self.assertEqual(suite.classify(samples([1]*5), samples([1]*4), POLICY)["status"], "incomplete")

    def test_unstable_timings_need_review(self):
        self.assertEqual(suite.classify(samples([1]*5), samples([.6,.9,1.3,1.8,2.1]), POLICY)["status"], "noisy_inconclusive")

    def test_configuration_changes_do_not_pass(self):
        self.assertEqual(suite.classify(samples([1]*5), samples([.1]*5), POLICY, False)["status"], "incompatible_configuration")

    def test_interrupted_report_preserves_missing_cases(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            suite.save(root / "metadata.json", {"cases": [{"id": "cube", "stages": ["csg"]},
                       {"id": "panel", "stages": ["csg"]}], "stages": ["csg"]})
            suite.save(root / "interruption.json", {"error": "timeout"})
            self.assertEqual(suite.report(root, [], POLICY, True), "interrupted")
            summary = suite.read(root / "summary.json")
            self.assertEqual(len(summary["cases"]), 2)
            self.assertTrue(all(x["status"] == "incomplete" for x in summary["cases"]))

    def test_output_mismatch_fails_even_with_improved_timings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            suite.save(root / "metadata.json", {"cases": [{"id": "cube", "stages": ["csg"]}], "stages": ["csg"]})
            a, b = root / "a.csg", root / "b.csg"
            a.write_text("cube([1,1,1]);")
            b.write_text("cube([2,2,2]);")
            rows = [dict(case="cube", stage="csg", build=label, repetition=n, warmup=False,
                         status="ok", seconds=t, dependencies=[{"path": "same", "sha256": "same"}],
                         output=path.name, output_sha256=suite.file_hash(path))
                    for label, path, t in [("baseline", a, 1), ("candidate", b, .1)] for n in range(5)]
            self.assertEqual(suite.report(root, rows, POLICY, True), "needs_review")
            self.assertEqual(suite.read(root / "summary.json")["cases"][0]["status"], "execution_or_output_failure")

    def test_real_failed_process_retains_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = suite.execute([sys.executable, "-c", "import sys; print('ERROR: failed'); sys.exit(2)"],
                                   root, None, 10, root / "failure")
            self.assertEqual(result["exit_code"], 2)
            self.assertTrue(result["diagnostics"])
            self.assertTrue((root / "failure.stdout.txt").exists())

    def test_empty_csg_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.csg"
            path.write_text("group() {}")
            with self.assertRaisesRegex(ValueError, "No geometry"):
                suite.valid_output(path, "csg")


if __name__ == "__main__":
    unittest.main()
