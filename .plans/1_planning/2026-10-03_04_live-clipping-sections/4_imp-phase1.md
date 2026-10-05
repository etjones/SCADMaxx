# Phase 1: prepared inspection mesh and GPU half-spaces

Covers CL06-CL09/CL12. Requires implemented 03/14; no private persistence or geometry service dependency.

1. Implement ClippingState validation and ClippedMeshRenderer with the exact eight-plane discard/recentring/tolerance
   contract. Share the predicate with 03 SurfacePick and edge shaders; register shader resources in normal install.
2. Implement ClipMeshJob as 03's priority-0 mesh provider and ClippedMeshRenderer as its registered effect, following
   the [shared presentation contract](../2026-10-03_00_source-first-cad-overview/inspection-presentation-contract.md).
   Preserve supplied per-piece masks/IDs/transforms through every pass. Use retained tree/cache ownership,
   cancellation and result guards. The root provider's preview uses
   the existing instantiated preview tree; final geometry reuses its current mesh. Never retain a borrowed mutable
   MainWindow Tree beyond its lifetime or bypass the existing compile/cache lock.
3. Add [clipping-math] for normals, recentering, plane intersection predicate, invalid values and epsilon bounds.
   Add TestClipping native class/runner and `OPENSCAD_CLIPPING_TESTS_ONLY` with fixed-programmatic planes.
4. Native fixtures: solid cube, hollow difference box, oblique hollow cylinder and two intersecting solids. Cut away
   the nearest wall and assert that retained rear/interior surfaces and their picks are visible. Compare preview mesh
   geometry with the same frozen-tree GeometryEvaluator result; do not compare it with a rerun using $preview=false.
   Also register a fake two-piece priority-100 provider without 07 linked: mask one piece, clip the other, verify
   correct draw ID and rear-surface hit, then disable clipping and retain the active mask/display request. A pending
   or failed higher provider must never fall through to the merged root and lose ownership.
5. Instrument source evaluation, boolean jobs, mesh uploads and frame timing: 100 plane updates after preparation
   cause zero new jobs/evaluations/uploads. Report first preparation time and p50/p95 frame time separately on a
   recorded 100k-triangle, 1280x720, one/eight-plane fixture. Target p95 <=33 ms on the supported desktop; investigate
   missed target with logs before accepting interactive behavior. This is a target, not a measured planning claim.

Exit: hollow/intersection rear surfaces are correct, numerical samples pass, cancellation never installs stale output,
and dragging is uniform updates only. Unsupported inputs report status; do not use wrong OpenCSG fragment clipping
as a fallback. If this route cannot meet supported behavior, stop with concrete evidence before adding UI phases.
