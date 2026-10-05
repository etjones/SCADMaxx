# Strict CGAL preparation correction

This replaces only the initial design's direct use of generic CGAL-to-PolySet conversion. Requirements remain valid.
Extend the existing shared converter in `src/geometry/cgal/CGALUtils.h/.cc` with Render and StrictAnalysis behavior;
the GeometryAnalysis adapter selects StrictAnalysis. Reuse its facet/cycle traversal and triangulation.

StrictAnalysis must avoid color/global application state, retain original double output coordinates, and detect
distinct exact Nef points that collapse to one float triangulation/reindex key. Reject collapsed/repeated vertices,
dropped faces, failed or count-changing triangulation and unconnected topology before producing a mesh.
Do not weld, quantize, hull or switch kernels to obtain a successful measurement.

Expose classified strict conversion failures so the adapter reports InvalidTopology for topology rejection and
BackendFailure for precision/backend conversion failure, with useful detail and no measurement payload.
Ordinary Render behavior remains available to its existing consumers; this is an analysis capability, not a
legacy fallback. All changes belong to the geometry-services source delta and its explicit test registration.

For valid empty solids, area and volume are zero. An unavailable/nonphysical negative backend tolerance sentinel
becomes absent optional diagnostic data; nonempty numeric tolerance validation remains strict.

Net section area is computed from sanitized contour winding using translated shoelace sums, avoiding the existing
Polygon2d::area global-render-backend dependency. Hole classification, units, slice boundary and public API stay fixed.
