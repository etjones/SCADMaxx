import tempfile
import unittest
from pathlib import Path
import os
import sys
from unittest.mock import patch
import io
import zipfile
import numpy as np
import trimesh
from geometry import compare_meshes
from benchmark import dependency_identity, execute
from corpus import acquire


class GeometryTests(unittest.TestCase):
    def compare(self, a, b, **kwargs):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "a.off", Path(directory) / "b.off"
            a.export(first)
            b.export(second)
            return compare_meshes(first, second, samples=128, **kwargs)

    def test_triangle_order_does_not_matter(self):
        a = trimesh.creation.box()
        b = trimesh.Trimesh(vertices=a.vertices, faces=a.faces[::-1], process=False)
        self.assertEqual(self.compare(a, b)["status"], "exact_surface")

    def test_rounding_is_tolerated_and_measured(self):
        a = trimesh.creation.box()
        b = a.copy()
        b.apply_translation([1e-7, 0, 0])
        result = self.compare(a, b)
        self.assertEqual(result["status"], "within_tolerance_sampled")
        self.assertGreater(result["surface_max_delta"], 0)

    def test_different_triangulation_is_tolerated(self):
        a = trimesh.creation.box()
        b = a.subdivide()
        self.assertEqual(self.compare(a, b)["status"], "within_tolerance_sampled")

    def test_translation_is_not_aligned_away(self):
        a = trimesh.creation.box()
        b = a.copy()
        b.apply_translation([.1, 0, 0])
        self.assertEqual(self.compare(a, b)["status"], "different")

    def test_tiny_missing_component_is_detected(self):
        a = trimesh.creation.box()
        small = trimesh.creation.box(extents=[.001] * 3)
        small.apply_translation([2, 0, 0])
        b = trimesh.util.concatenate([a, small])
        result = self.compare(a, b)
        self.assertEqual(result["status"], "different")
        self.assertTrue(result["topology_changed"])

    def test_hole_is_detected(self):
        a = trimesh.creation.box()
        b = trimesh.Trimesh(vertices=a.vertices, faces=a.faces[:-1], process=False)
        self.assertEqual(self.compare(a, b)["status"], "different")

    def test_equal_invalid_is_not_passed(self):
        a = trimesh.creation.box()
        b = trimesh.Trimesh(vertices=a.vertices, faces=a.faces[:-1], process=False)
        self.assertEqual(self.compare(b, b)["status"], "inconclusive_invalid_mesh")

    def test_scale_changes_fail(self):
        a = trimesh.creation.box()
        b = a.copy()
        b.apply_scale(1.01)
        self.assertEqual(self.compare(a, b)["status"], "different")

    def test_same_volume_and_bounds_can_still_differ(self):
        left = trimesh.creation.box(extents=[1, 4, 1])
        left.apply_translation([-2, 0, 0])
        right = left.copy()
        right.apply_translation([4, 0, 0])
        small = trimesh.creation.box(extents=[.2, .2, .2])
        small.apply_translation([0, .7, 0])
        shifted = small.copy()
        shifted.apply_translation([0, -1.4, 0])
        result = self.compare(trimesh.util.concatenate([left, right, small]),
                              trimesh.util.concatenate([left, right, shifted]))
        self.assertLess(result["bounds_max_delta"], 1e-10)
        self.assertLess(result["volume_absolute_delta"], 1e-10)
        self.assertEqual(result["status"], "different")


class ExecutionTests(unittest.TestCase):
    def test_timeout_retains_logs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = execute([sys.executable, "-c", "import time; print('started', flush=True); time.sleep(30)"], root,
                             os.environ.copy(), .5, root / "process")
            self.assertTrue(result["timed_out"])
            self.assertIn("started", (root / "process.stdout.txt").read_text())

    def test_warning_not_hidden_by_zero_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = execute([sys.executable, "-c", "print('WARNING: missing library')"], root,
                             os.environ.copy(), 5, root / "process")
            self.assertEqual(result["exit_code"], 0)
            self.assertTrue(result["diagnostics"])

    def test_external_dependency_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "corpus"
            corpus.mkdir()
            source = root / "unfrozen library.scad"
            source.write_text("cube(1);")
            deps = root / "model.d"
            deps.write_text("model.stl: \\\n\t" + source.as_posix().replace(" ", "\\ ") + "\n")
            records, external = dependency_identity(deps, corpus, root / "runtime")
            self.assertEqual(len(records), 1)
            self.assertEqual(len(external), 1)


class AcquisitionTests(unittest.TestCase):
    def test_archive_path_traversal_is_rejected(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.comment = b"a" * 40
            archive.writestr("repo/../../outside.scad", "cube(1);")
        with tempfile.TemporaryDirectory() as directory, patch("corpus.fetch", return_value=buffer.getvalue()):
            repo = {"full_name": "test/repo", "default_branch": "main"}
            with self.assertRaisesRegex(ValueError, "Unsafe archive path"):
                acquire(Path(directory), repo)

    def test_pinned_archive_mismatch_is_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as directory, patch("corpus.fetch", return_value=b"changed"):
            repo = {"full_name": "test/repo"}
            locked = {"archive_url": "https://example.invalid/pinned", "archive_sha256": "0" * 64}
            with self.assertRaisesRegex(ValueError, "Pinned archive hash differs"):
                acquire(Path(directory), repo, locked=locked)


if __name__ == "__main__":
    unittest.main()
