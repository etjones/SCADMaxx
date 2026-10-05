# Phase 4: numerical limits, performance and package verification

Covers all CL requirements as integrated behavior. Follow
[the verification contract](../2026-10-03_00_source-first-cad-overview/verification-contract.md).

1. Run scaled/translated/oblique/mirrored coplanar fixtures: boundary face discarded, adjacent wall at 1e-4*D retained,
   one/eight half-spaces, global off restores full display. Repeat in preview-derived, Manifold and convertible CGAL
   meshes. Record tolerance and actual driver; failing thin-wall cases cannot be excused by increasing epsilon.
2. Verify camera changes/resize/DPI and selection of exposed interior surfaces after clipping. Offscreen screenshots
   alone do not prove input correctness; record pixel/depth/normal and native gestures as separate evidence.
3. Repeat the phase-1 performance/evaluation counters on the final code. Reuse passing evidence if no renderer change
   occurred; broaden tests only for changes or failures. Report initial preparation cost separately from drag latency.
4. Check installed/extracted shaders, dock resources, themes/actions, Save/reopen and unsupported-mode feedback.
   Caps stay explicitly unavailable; computed contours/export are not claimed. Full application integration still
   follows its separately requested workflow and manually selected stack.
5. Record exact source/prerequisite boundaries, actual checks, renderer/precision/performance limits and shared
   Section use in completion notes. No private store, per-drag boolean evaluation or stale-result callback remains.
