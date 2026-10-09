# Shared geometry core requirements

This is the bounded first delivery of [the exploration](1_exploration.md), shared by drawings and analysis tools.
It does not define the richer analysis/reconstruction scope of feature 13.

- GS01: Provide stateless, GUI-independent operations for world-space bounds, closed-solid area/volume and an
  arbitrary-plane section of evaluated 3D geometry. Accept immutable geometry and an explicit object-to-world transform.
- GS02: Support evaluated ManifoldGeometry and valid indexed PolySet solids, plus existing CGAL-to-PolySet conversion
  when compiled in. Reject unresolved GeometryList aggregates rather than silently concatenating or unioning targets.
- GS03: Bounds may inspect finite open meshes. Solid measurements and sections require valid closed geometry. Never
  silently repair, weld, hull or resample an invalid input to make an analysis succeed. Unknown validity is not failure
  until checked; `PolySet::isManifold() == false` means unknown in the existing source.
- GS04: A section receives world origin, normal and drawing-up direction and returns contours in a right-handed
  orthonormal 2D frame plus the inverse frame transform. Retain holes and disconnected contours, with net section area.
- GS05: Explicitly handle empty geometry, no intersection, nonfinite values, invalid/degenerate transforms, zero
  normals, parallel up directions, invalid topology, unsupported geometry and unavailable backends. No NaN success.
- GS06: Use caller geometry units consistently: lengths, squared units and cubed units. Report method and backend
  tolerance. These results measure evaluated/tessellated geometry, not exact analytic source intent.
- GS07: Adopt the existing Manifold boundary convention: in section coordinates, bottom faces are included and top
  faces excluded. Do not offset the requested plane to fabricate a contour. This numerical convention is separate
  from feature 04's display rule for removing coincident faces.
- GS08: Preserve input geometry, transforms and caller identity. No active document lookup, persistence, source edits,
  Qt dock, HTTP server or stale-result policy inside the service. Consumers retain request/result identity themselves.
- GS09: Support caller cancellation checkpoints and input limits without promising interruption inside a synchronous
  backend call. Return typed diagnostics; do not return a partially successful solid measurement after cancellation.
- GS10: Register production code and numerical tests explicitly in CMake. Compile with the existing Windows dependency
  set; no new geometry library or automatic installation. Preserve ordinary projection/export behavior.

## Required fixtures

| Fixture | Expected result |
| --- | --- |
| Box [0,20] x [0,10] x [0,6] | Bounds as specified; volume 1200; surface area 760. |
| Same box, section z=3, normal +Z, up +Y | One outer contour; area 200; frame X/Y matches world X/Y. |
| Same box at z=0 / z=6 | Bottom area 200 / top empty under the documented convention. |
| Through-hole [5,15] x [3,7] x [-1,7] subtracted | Volume 960; middle section one outer/one hole; area 160. |
| Two disjoint boxes as one evaluated solid | Volume 2400; section two outer contours; area 400. |
| Box scaled by (2,3,4) | Dimensions (40,30,24); volume 28800; area 5760. |
| Rigidly rotate both box and section frame | Same section area and local contour geometry within tolerance. |
| Open, nonfinite, degenerate, 2D or unresolved aggregate | Typed failure where unsupported; no repaired result. |

Use absolute 1e-7 and relative 1e-8 tolerances for these simple fixtures; include scale variants to expose assumptions.
Record actual backend tolerance. Do not claim these fixture thresholds are a universal accuracy guarantee.

## Non-goals

Hidden-line drawing, dimensions/layout, GPU clipping/caps, thickness/clearance/interference algorithms, adaptive
reconstruction, topology naming, asynchronous job infrastructure and unit conversion belong to concrete consumers
or subsequent explicitly scoped extensions. Do not add speculative public operations now.
