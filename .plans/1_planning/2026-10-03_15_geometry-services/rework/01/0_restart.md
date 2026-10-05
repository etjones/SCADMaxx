# Limited replan: strict CGAL conversion

Recorded 2026-10-03 during authorized feature 15 implementation. Response: replan the CGAL preparation route;
retain the accepted requirements, public API and passing Manifold/PolySet/frame work. No rollback is needed.

Trigger: the required CGAL box fixture failed because `CGALUtils::createPolySetFromNefPolyhedron3` reads
`ColorMap::instance()`/`RenderSettings` and reaches an uninitialized application resource path. Source inspection
also found float reindexing of distinct exact vertices, culled collapsed faces and ignored triangulation errors.
The initial design assumed this existing conversion could be used directly by a strict, stateless analysis service.
Actual phase 2 evidence was 12 discovered cases, 10 passing and two failures; exact logs remain in the feature run.

The second failure concerned valid empty Manifold geometry: its negative tolerance sentinel is not an accuracy
value. Empty solid measurements must still return zero area/volume; optional backendTolerance remains absent.

Scope: feature 15's CGAL preparation path and shared converter analysis capability. No consumer ownership change,
new geometry kernel, implicit repair, GUI initialization, new dependency or reduced CGAL coverage is authorized.
Ordinary rendering conversion keeps its existing behavior. The source branch remains uncommitted.

Lessons: statelessness needs an actual no-application-state fixture; generic rendering conversion can change
geometry. Test strict precision loss and failed topology/triangulation, with absent payloads on failure.
Retain passing phase 1 and no-Manifold compile/test evidence. The corrected design and checks follow in this cycle.

## Implementation checkpoint

The shared converter now has explicit Render and StrictAnalysis modes. StrictAnalysis skips render globals,
preserves double output vertices and raises classified errors for float-key collapse, invalid topology and
changed/failed triangulation. The original Render path is retained. Empty backend tolerance is absent.
All 12 discovered geometry-analysis cases pass on the corrected source, including the CGAL box without application
resource initialization and the translated precision-loss regression. Final application, optional backend and
existing projection/export acceptance are still pending at this checkpoint; their final outcome belongs in
`5_post-implementation-notes.md`.

## Final outcome

The corrected source passed the final supported Release application/console build, all 12 numerical cases,
five Manifold-disabled cases and eight existing projection/export cases. The cycle is verified without changing
requirements, consumer ownership or ordinary rendering behavior. Exact source/repair hashes and actual command/log
links are recorded in the feature run's `handoff-manifest.json` and `report.md`, summarized in the central post-notes.
The source is still uncommitted and unpromoted; no integrated release acceptance is implied.
