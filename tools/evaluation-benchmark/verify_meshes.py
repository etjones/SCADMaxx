"""Validate evaluation fixtures; no mesh repair, resampling or topology alteration."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import trimesh


def inspect_mesh(path, cache):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest in cache:
        return cache[digest]
    # Preserve indexed OFF topology. STL necessarily needs positional vertex merging.
    mesh = trimesh.load_mesh(path, process=(path.suffix.lower() == ".stl"))
    triangles = np.round(mesh.triangles, 5)
    for tri in triangles:
        tri[:] = tri[np.lexsort((tri[:, 2], tri[:, 1], tri[:, 0]))]
    flat = triangles.reshape((-1, 9))
    flat = flat[np.lexsort(tuple(flat[:, i] for i in reversed(range(9))))]
    result = {
        "triangles": len(mesh.faces),
        "vertices": len(mesh.vertices),
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent),
        "positive_volume": bool(mesh.is_volume and mesh.volume > 0),
        "finite": bool(np.isfinite(mesh.vertices).all()),
        "components": len(mesh.split(only_watertight=False)),
        "volume": float(mesh.volume),
        "bounds": mesh.bounds.tolist(),
        "canonical_triangle_hash_1e5": hashlib.sha256(flat.tobytes()).hexdigest(),
    }
    cache[digest] = result
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}")
    cache, records, failures, comparisons = {}, [], [], []
    for run in args.runs:
        metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8-sig"))
        results = json.loads((run / "results.json").read_text(encoding="utf-8-sig"))
        if isinstance(results, dict):
            results = [results]
        fresh = {}
        for record in results:
            if record["stage"] not in ("stl", "off"):
                continue
            outputs = record["outputs"]
            expected = 1 if record["workload"] == "panel" else [4, 16, 36][metadata["quality"]]
            frames = []
            for output in outputs:
                path = Path(output["path"])
                geometry = inspect_mesh(path, cache)
                passed = (geometry["watertight"] and geometry["winding_consistent"]
                          and geometry["positive_volume"] and geometry["finite"]
                          and geometry["components"] == expected)
                records.append({"file": str(path), "passed": passed, **geometry})
                if not passed:
                    failures.append(f"Invalid geometry/components: {path}")
                frames.append(geometry)
            if metadata.get("animationSequence"):
                for a, b in [(0, 5), (1, 2), (3, 4)]:
                    equal = frames[a]["canonical_triangle_hash_1e5"] == frames[b]["canonical_triangle_hash_1e5"]
                    comparisons.append({"case": record["id"], "frames": [a, b], "expected_equal": True, "passed": equal})
                    if not equal:
                        failures.append(f"Repeat/restore mismatch: {record['id']} frames {a},{b}")
                if record["scenario"] != "baseline":
                    for a, b in [(0, 1), (1, 3)]:
                        changed = abs(frames[a]["volume"] - frames[b]["volume"]) > 1e-5
                        comparisons.append({"case": record["id"], "frames": [a, b], "expected_changed": True, "passed": changed})
                        if not changed:
                            failures.append(f"Edit had no volume change: {record['id']} frames {a},{b}")
            else:
                fresh[(record["workload"], record["scenario"], record["repetition"])] = frames[0]
        for (workload, scenario, repetition), geometry in fresh.items():
            base = fresh.get((workload, "baseline", repetition))
            if scenario != "baseline" and base:
                changed = abs(base["volume"] - geometry["volume"]) > 1e-5
                comparisons.append({"case": f"{workload}/{scenario}/{repetition}", "expected_changed": True, "passed": changed})
                if not changed:
                    failures.append(f"Edit had no volume change: {run}/{workload}/{scenario}")
    report = {"passed": not failures, "numpy": np.__version__, "trimesh": trimesh.__version__,
              "mesh_count": len(records), "unique_mesh_count": len(cache), "failures": failures,
              "meshes": records, "comparisons": comparisons,
              "limits": "Canonical triangle hash ignores triangle/vertex order and rounds coordinates to 1e-5 model units; it is not a general equivalence proof for different triangulations."}
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("passed", "mesh_count", "unique_mesh_count", "failures")}))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
