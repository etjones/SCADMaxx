"""Geometry comparisons in model units, without alignment, scaling or mesh repair."""
import hashlib
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image


def canonical_triangles(mesh):
    triangles = np.array(mesh.triangles, dtype=np.float64)
    order = np.lexsort((triangles[:, :, 2], triangles[:, :, 1], triangles[:, :, 0]), axis=1)
    triangles = np.take_along_axis(triangles, order[:, :, None], axis=1)
    flat = triangles.reshape(-1, 9)
    return flat[np.lexsort(tuple(flat[:, i] for i in range(8, -1, -1)))].copy()


def load_mesh(path):
    mesh = trimesh.load_mesh(path, process=False)
    if not isinstance(mesh, trimesh.Trimesh) or not len(mesh.faces) or not np.isfinite(mesh.vertices).all():
        raise ValueError("Missing, empty, non-mesh, or non-finite geometry")
    if Path(path).suffix.lower() == ".stl":
        # STL has no vertex indices. Merge EXACT positions only, not a rounding-based repair.
        vertices, inverse = np.unique(mesh.vertices, axis=0, return_inverse=True)
        mesh = trimesh.Trimesh(vertices=vertices, faces=inverse[mesh.faces], process=False)
    return mesh


def metrics(mesh):
    return {"vertices": len(mesh.vertices), "triangles": len(mesh.faces),
            "bounds": mesh.bounds.tolist(), "area": float(mesh.area), "volume": float(mesh.volume),
            "watertight": bool(mesh.is_watertight), "winding_consistent": bool(mesh.is_winding_consistent),
            "components": int(trimesh.graph.connected_component_labels(mesh.face_adjacency, node_count=len(mesh.faces)).max() + 1),
            "euler": int(mesh.euler_number)}


def sample_points(mesh, samples):
    points, _ = trimesh.sample.sample_surface(mesh, samples, seed=20261004)
    # Explicit coverage of every vertex and face center prevents small disconnected parts being missed
    # for ordinary meshes. Large meshes are capped and marked as sampled, never proven identical.
    rng = np.random.default_rng(20261004)
    vertices = mesh.vertices
    centers = mesh.triangles_center
    if len(vertices) > samples:
        vertices = vertices[rng.choice(len(vertices), samples, replace=False)]
    if len(centers) > samples:
        centers = centers[rng.choice(len(centers), samples, replace=False)]
    return np.vstack((points, vertices, centers))


def surface_distances(source, target, samples):
    points = sample_points(source, samples)
    distances = []
    for start in range(0, len(points), 256):
        _, distance, _ = trimesh.proximity.closest_point(target, points[start:start + 256])
        distances.extend(distance.tolist())
    distance = np.asarray(distances)
    return {"samples": len(distance), "max": float(distance.max()),
            "p95": float(np.quantile(distance, .95)), "rms": float(np.sqrt(np.mean(distance ** 2)))}


def compare_meshes(first, second, absolute=1e-5, relative=1e-6, samples=4096):
    a, b = load_mesh(first), load_mesh(second)
    ma, mb = metrics(a), metrics(b)
    scale = max(float(np.linalg.norm(a.extents)), float(np.linalg.norm(b.extents)), 1e-12)
    tolerance = absolute + relative * scale
    bounds_delta = float(np.max(np.abs(a.bounds - b.bounds)))
    volume_delta = abs(ma["volume"] - mb["volume"])
    # Volume tolerance tied to a shell of thickness tolerance, not a permissive fixed percentage.
    volume_tolerance = max(ma["area"], mb["area"]) * tolerance + tolerance ** 3
    topology_changed = any(ma[k] != mb[k] for k in ("watertight", "winding_consistent", "components", "euler"))
    result = {"baseline": ma, "candidate": mb, "absolute_tolerance": absolute, "relative_tolerance": relative,
              "effective_tolerance": tolerance, "bounds_max_delta": bounds_delta,
              "volume_absolute_delta": volume_delta,
              "volume_relative_delta": volume_delta / max(abs(ma["volume"]), abs(mb["volume"]), 1e-30),
              "volume_tolerance": volume_tolerance, "topology_changed": topology_changed}
    ca, cb = canonical_triangles(a), canonical_triangles(b)
    same_connectivity_geometry = ca.shape == cb.shape and np.array_equal(ca, cb)
    if same_connectivity_geometry:
        result.update(status="exact_surface", surface_max_delta=0.0, method="All triangles identical, ignoring order; topology checked separately")
    else:
        ab, ba = surface_distances(a, b, samples), surface_distances(b, a, samples)
        maximum = max(ab["max"], ba["max"])
        result.update(surface_max_delta=maximum, baseline_to_candidate=ab, candidate_to_baseline=ba,
                      method="Deterministic bidirectional point-to-triangle surface sampling; not a Hausdorff upper bound or equivalence proof")
        result["status"] = "within_tolerance_sampled" if maximum <= tolerance else "different"
    if topology_changed or bounds_delta > tolerance or (ma["watertight"] and mb["watertight"] and volume_delta > volume_tolerance):
        result["status"] = "different"
    elif not (ma["watertight"] and mb["watertight"] and ma["winding_consistent"] and mb["winding_consistent"] and ma["volume"] > 0 and mb["volume"] > 0):
        result["status"] = "inconclusive_invalid_mesh"
    return result


def compare_images(first, second):
    a, b = np.asarray(Image.open(first).convert("RGBA")), np.asarray(Image.open(second).convert("RGBA"))
    if a.shape != b.shape:
        return {"status": "different", "reason": "image dimensions changed"}
    delta = np.abs(a.astype(float) - b.astype(float))
    return {"status": "identical_image" if not np.any(delta) else "image_changed_review",
            "mean_channel_delta_255": float(delta.mean()), "max_channel_delta_255": float(delta.max()),
            "changed_pixel_fraction": float(np.mean(np.any(delta > 0, axis=2))),
            "limits": "Preview is appearance evidence, not 3D geometry equivalence; auto-framing can hide scale changes."}


def compare_outputs(first, second, stage, **kwargs):
    if stage in ("stl", "off"):
        return compare_meshes(first, second, **kwargs)
    if stage == "preview":
        return compare_images(first, second)
    a, b = Path(first).read_bytes(), Path(second).read_bytes()
    return {"status": "identical_text" if a == b else "text_changed_review",
            "baseline_sha256": hashlib.sha256(a).hexdigest(), "candidate_sha256": hashlib.sha256(b).hexdigest(),
            "limits": "AST/CSG identity is diagnostic evidence; mesh and preview checks remain required."}
