# Shared geometry core implementation design

Target GPT-6.1 Sol; use [requirements](2_requirements.md) and the
[handoff standard](../2026-10-03_00_source-first-cad-overview/implementation-handoff.md).
Proposed source branch/stack ID: `feature/geometry-services` / `geometry-services`. No new-feature prerequisite.
Record the locked upstream/required-repair base; do not branch from the inspected full application composition.

## Existing code and owned files

Inspected: `Geometry`, `PolySet`, `Polygon2d`, `PolySetUtils::tessellate_faces/getGeometryAsPolySet`,
`ManifoldGeometry::{getManifold,transform,slice}`, `ManifoldUtils::createManifoldFromPolySet`,
`ClipperUtils::sanitize`, `GeometryEvaluator::projectionCut` and Manifold's `Slice/SurfaceArea/Volume/GetTolerance`.
General Manifold conversion tries Merge and CGAL repair. Do not call that path for strict analysis.

New production files: `src/geometry/analysis/GeometryAnalysis.h` and `.cc`. New tests:
`src/geometry/analysis/GeometryAnalysis_test.cc`. Register the production source in the geometry source list and
explicitly append the test to TEST_SOURCES after its glob; the current glob omits geometry. Keep Manifold includes
and implementation guarded by ENABLE_MANIFOLD. The public header has no Qt, GUI or vendor-specific types.

## Public contract to implement

All types below are new, in namespace `GeometryAnalysis`, using existing Vector/Transform/BoundingBox aliases.
Include their actual defining header plus standard memory, optional, vector, string, functional and size headers.

```cpp
enum class Error {
  None, InvalidInput, UnsupportedGeometry, InvalidTopology,
  BackendUnavailable, LimitExceeded, Cancelled, BackendFailure
};
struct Diagnostic {
  Error error = Error::None;
  std::string detail;
  std::string method;
  std::optional<double> backendTolerance;
};
struct Limits {
  size_t maxVertices = 0;  // zero means caller imposes no limit
  size_t maxTriangles = 0;
  std::function<bool()> cancelled;
};
struct Input {
  std::shared_ptr<const Geometry> geometry;
  Transform3d objectToWorld = Transform3d::Identity();
  Limits limits;
};
struct Plane { Vector3d origin, normal, up; };
struct BoundsResult { Diagnostic diagnostic; std::optional<BoundingBox> bounds; };
struct SolidResult {
  Diagnostic diagnostic;
  std::optional<double> surfaceArea, volume;
};
struct Contour { std::vector<Vector2d> points; bool hole = false; };
struct SectionResult {
  Diagnostic diagnostic;
  std::optional<Transform3d> sectionToWorld;
  std::vector<Contour> contours;
  std::optional<double> area;
};
BoundsResult bounds(const Input&);
SolidResult measureSolid(const Input&);
SectionResult section(const Input&, const Plane&);
```

Error None with absent bounds denotes valid empty geometry. Valid empty solid has area/volume zero; a successful
section with no intersection has a valid frame, no contours and area zero. Failures have no measurement/contour
payload. Method strings are `mesh-bounds`, `manifold-solid`, `manifold-section`; diagnostics may add backend errors.
Contour points omit a duplicated closing vertex; hole flags and order are independent of source face indices.
Consumers own unit labels, correlation IDs, scheduling and stale-result rejection.

## Input and strict solid conversion

Validate a non-null 3D geometry, finite transform matrix and affine final row. Reject singular transforms. Check
cancellation before conversion, within vertex/triangle loops, between backend stages and before publishing results.
Use exact determinant zero for singularity, reject nonfinite transformed coordinates, and propagate backend numeric
failure; do not introduce an arbitrary model-size cutoff. Respect nonzero caller vertex/triangle limits before costly
conversion when counts are available, and again after triangulation. Check count multiplication for overflow.

Reject GeometryList before `getGeometryAsPolySet`: that helper can concatenate children without the physical union
semantics a caller may expect. Callers must supply a resolved individual target or already evaluated solid union.
Reject 2D geometry. Allow empty supported 3D geometry without manufacturing a bounding box.

- Existing valid ManifoldGeometry: copy it, apply objectToWorld to the copy, check backend status and finite outputs.
- PolySet: validate finite vertices, face indices, face sizes and limits. Tessellate a copy if not triangular. Populate
  MeshGL64 with numProp=3, XYZ vertex properties and triangle indices using the existing conversion's index ordering.
  Construct Manifold exactly once, check Status, and return InvalidTopology on rejection. Do not call MeshGL::Merge,
  quantizeVertices, a convex hull or CGAL repair. Colors/source provenance need not be reconstructed for measurements.
- Supported CGAL geometry: use the existing CGAL-to-PolySet conversion, then the same strict path. Unsupported or
  failed conversion has an explicit diagnostic; do not switch kernels silently to obtain a different answer.

`PolySet::isManifold()` false does not reject input by itself. Strict conversion may reject a geometrically closed
but disconnected-index triangle soup; explain this limitation in diagnostics/documentation instead of silently welding.
Known backend status/ordinary operation exceptions become BackendFailure with context; do not swallow process-level
failures. No fallthrough returning zero measurements after a failed conversion.

## Bounds and solid measurements

For bounds, iterate actual transformed vertices of supported geometry (including an open finite PolySet) and extend
BoundingBox. Do not transform the old bounding box's eight corners: that can overestimate a rotated object's bounds.
Only use finite referenced geometry vertices; unused PolySet vertices do not enlarge model bounds. Check indices
before dereferencing. For Manifold use its vertex iteration or copied transformed representation.

For solid measurements, obtain the strict transformed Manifold and call SurfaceArea and Volume. Ensure results are
finite and nonnegative; reject invalid orientation/negative-volume input instead of hiding it with abs(). Empty
geometry is the explicit zero case. Manifold transform handling must preserve valid orientation under reflection;
test this. Values are in world geometry units squared/cubed. Return GetTolerance as backend tolerance, not an error bound.

## Arbitrary-plane section algorithm

1. Require finite origin, normal and up. Normal and up lengths must exceed 1e-12 before normalization. Normalize both
   directions; reject an up component perpendicular to normal shorter than 1e-8 (dimensionless near-parallel test).
2. Let N be normalized normal; Y = normalize(up - N * dot(up,N)); X = Y cross N. Thus X cross Y = N. Construct
   worldToSection with rows X,Y,N and translations -dot(axis,origin). Its inverse is sectionToWorld.
3. Strictly convert/copy input with the composed transform worldToSection * objectToWorld. Never mutate caller input.
4. Use ManifoldGeometry::slice at z=0 and sanitize its Polygon2d with ClipperUtils::sanitize, as projectionCut already
   does. This step classifies contour holes; the raw polygonsToPolygon2d helper initializes every outline positive.
5. Return sanitized outlines with hole = !positive, their 2D coordinates, Polygon2d area and sectionToWorld. Verify
   finite coordinates/area and valid backend status. Empty intersection is success. Retain disconnected contours.
6. Stabilize output representation for deterministic tests/consumers: choose a lexicographically smallest first
   vertex per loop, retain its winding, then sort loops by hole flag and coordinate sequence. Do not round geometry
   merely for ordering or assign persistent topology IDs. Comparison tests allow numeric tolerance.

Manifold includes the minimum-Z boundary and excludes maximum-Z. Reversing N can change which coincident boundary
is included. Record this behavior, including planar-touch fixtures. Never apply the display clipping epsilon here.
Clipper sanitization has its own quantization; method documentation must mention both tessellation and sanitization.

## Build and phases

1. [Phase 1](4_imp-phase1.md): public contract, strict preparation, bounds and frame tests.
2. [Phase 2](4_imp-phase2.md): measurements and section operations with numerical regression fixtures.
3. [Phase 3](4_imp-phase3.md): backend/build coverage, existing projection regressions and handoff evidence.

Delivery requires the supported Windows ENABLE_MANIFOLD build. A build without it must compile the public API and
return BackendUnavailable for solid/section operations; PolySet bounds still work. Do not install another backend.
If strict conversion cannot support normal evaluated solids from the locked base, return to design with the failing
fixture; do not quietly introduce repair or duplicate an alternate kernel in features 09/13.
