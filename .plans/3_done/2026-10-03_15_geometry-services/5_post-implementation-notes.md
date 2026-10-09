# Geometry services local implementation handoff

Feature 15's bounded implementation is complete in `D:/openscad/wt-openscad-geometry-services`, branch
`feature/geometry-services`. Base and unchanged HEAD: `31f27b7522af858ebabed764e67ecc10d9e27add`.
Feature and required Windows repair inputs remain uncommitted. The base SHA alone does not identify the tested source.
No staging, push, promotion, enabled-stack change or integrated release was performed.

## Delivered behavior and ownership

The public `src/geometry/analysis/GeometryAnalysis.h` API provides world bounds, closed-solid area/volume and
arbitrary-plane sections of immutable evaluated geometry. It uses caller units and transforms, typed diagnostics,
limits/cancellation, right-handed frames and deterministic contours with hole classification and net area.
Bounds use actual referenced transformed vertices. Solid/section conversion rejects invalid topology and precision
loss without welding, merging, hull, resampling or repair. Callers own document identity, scheduling and stale results.

Owned changes are the analysis header/implementation/tests, `doc/geometry-analysis.md`, two shared CGAL converter
files and two explicit registrations in `CMakeLists.txt`. There is no new UI, HTTP mutation or geometry dependency.
The existing CGAL converter has Render and StrictAnalysis modes; ordinary rendering keeps its existing behavior.

Public header SHA-256: `d1957210619986d7552d3b338d68a852625846765ca9374e135c9d94f182726e`.
Developer API document SHA-256: `dc7a538475a6c32fd7b4c90175e94a1decb15caebb04ea2acd99897ebd072659`.
Consumers 09/13 should use this contract rather than copying the implementation.

## Reproducible source and dependencies

Run root: `D:/openscad/runs/20261003-geometry-services`. `handoff-manifest.json` records the full base/HEAD,
submodule revisions, ten separately retained repair patches in application order and seven final source-file hashes.
`feature-only.patch` is relative to the repaired inputs, excluding those repair changes; SHA-256:
`a50ffd8a348284dc50e96ab60cae158f84d01e2c0c0196f80d56337412207d7d`.
Completion review independently verified every source/repair/feature-patch hash. Reverse apply-check with strict
whitespace validation passes; a read-only apply-check against `wt-scadmaxx-20261002` also passes, without modifying it.
The ordinary whole-working-tree whitespace check reports retained repair-input CRLF resource lines, not feature lines.

Manifold 3.5.3 is at `0edd9d54876f3135e431575214dd6d8a72866fee`; all submodules are clean at recorded revisions.
The configure-generated Clipper header was preserved as run evidence and restored to its original content.
Source-local `.serena/` metadata is excluded. Shared dependencies remain at
`D:/openscad/openscad-6991/build/vcpkg_installed`; no install or upgrade occurred. Its package-status hash is unchanged.
The exact MSVC/SDK/Ninja/CMake/Qt/CGAL profile and tool hashes are in `build-fingerprint.json`.

## Verification and correction evidence

- Phase 1: five discovered strict-input/bounds cases passed; historical source and logs remain in the run.
- Final numerical suite: all 12 discovered `geometry-analysis` cases passed. Evidence:
  `logs/20261003T192325074Z-BuildUnit.log`, `20261003T192415779Z-Discovery.log` and
  `20261003T192418765Z-Test.log` in the run's logs directory.
- Final supported Release GUI application and console launcher build passed:
  `logs/20261003T192442280Z-BuildApp.log`.
- Manifold-disabled native library/unit build and all five discovered tests passed:
  `logs/20261003T192256829Z-BuildNoManifold.log`, `20261003T192450226Z-DiscoveryNoManifold.log` and
  `20261003T192453381Z-TestNoManifold.log`. PolySet bounds work; unavailable operations have absent result payloads.
- All eight existing CGAL/Manifold projection/cut and DXF/SVG projection/cut cases passed:
  `logs/20261003T192515119Z-Projection.log`. Existing fixtures require `-C Default`; new Catch tests use Release.

Fixtures cover the 20x10x6 box (volume 1200, area 760, middle-section area 200), bottom/top half-open boundaries,
through-hole (volume 960, net section area 160), disjoint solids, nonuniform scaling, reflection, oblique/rigid frames,
scale variants, empty inputs, cancellation/limits and strict rejection. Bounds ignore unused vertices. CGAL conversion
runs without resource initialization and rejects exact vertices collapsing at triangulator float precision.
Exact commands and exits are retained by `Verify-Geometry.ps1`; `report.md` has the detailed evidence links.

The initial phase 2 run had 10 passing cases and two failures. Its evidence is preserved. The limited technical
replan in `rework/01` corrects the invalid assumption that rendering conversion is strict and stateless: the same
converter now skips render globals, preserves double output coordinates and rejects collapsed/dropped/failed faces.
Signed shoelace sums replace `Polygon2d::area()`'s global render-setting-dependent tessellation for net contour area.
Empty Manifold's negative tolerance sentinel becomes absent optional tolerance, with successful zero measurements.
The corrected suite and existing rendering regressions pass; requirements and consumer ownership are retained.

## Practical limits and later composition

Measurements describe evaluated tessellation. Manifold validity is not exact analytic certification. Polygonal-face
triangulation uses float precision and rejects detected collapse; triangular inputs keep the double fast path.
Clipper sanitization uses a 2^-27 grid and can remove subgrid detail. Cancellation cannot interrupt a synchronous
backend call. Process allocation failures propagate. The fixture tolerances are not a universal accuracy guarantee.

No integrated selected-stack build, extracted ZIP, desktop UI session or clean-machine validation is claimed.
A later requested composition must freeze a reviewed base/head, replay the isolated delta and run integration/delivery
checks. Completion does not enable or promote this feature. Available follow-ups are fix forward for bounded fixes,
replan the approach, restart assumptions, or supersede the objective.


## Lifecycle closure — 2026-10-07

Moved to done at the user's request. Existing verification evidence and historical limits are preserved.
