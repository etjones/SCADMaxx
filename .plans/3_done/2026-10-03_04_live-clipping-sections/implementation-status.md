# Implementation status — locally complete

Started 2026-10-04 after completed, locally verified 03 → 05 → 06 → 14.
This is the final entry in the authorized queue. All four phase specifications were read.
Source: `D:/openscad/wt-openscad-live-clipping-sections`, branch `feature/live-clipping-sections`,
base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`.
Run: `D:/openscad/runs/20261004-live-clipping-sections`.

Direct prerequisites 03/14 are replayed from 14's verified complete working input:
`56275040c8fde09076ce5ae8510927d5845cf5f882ba27cab5142a59f4ec6c9a`.
Owner evidence: `62717755b051cc4bc8c996e3e532036587d745c723ea9077496da645f8b22cd3`.
This includes 02 and pinned parser prerequisites; 05/06/07/08/09/10/12/15 are excluded.
No private Section store, contour kernel, caps or OpenCSG fragment-discard shortcut is authorized by this plan.
Baseline passed: fresh build, 48 focused CTest cases and all 75 inherited native rows.
Phase 1 passed: 52 focused CTest cases; TestClipping 7 native rows (5 behavior + 2 setup),
including nine frozen-preview/final rear-surface fixtures, supplied-piece ownership and masks,
cancellation/unsupported/empty status, and 24 scaled/translated/mirrored one/eight-plane GPU samples.
The 102,396-triangle 1280×720 fixture recorded preparation 225.897 ms,
one-plane p50/p95 2.906/4.290 ms and eight-plane 2.854/4.047 ms on RTX 3070 Ti, NVIDIA 616.92.
Uniform updates caused zero additional jobs/evaluations/uploads. The first numerical screenshot
check used almost-transparent integer fixture colors; the corrected floating-point fixture passes.
Failed compile/native evidence is retained. Phase 2/3 editing and manipulation now follow this gate.
Shared dependency profile remains unchanged.
Phase 2 native gate passed all 10 rows (8 behavior + 2 setup), including source offset
undo/redo with `height/2` preserved, deletion and missing reference, transient naming/promotion,
Save/reopen with stable Section ID and personal toggles, presets/eight-plane refusal,
computed/missing/invalid Sections and routed picks/100-event transient gestures.
Reopened editors must load personal state; Save As carries the same live document's state.
The corrected distinction is retained with the failed first reopening test.
Final manipulation adds source-backed normal/ring gesture proof and broader native lifecycle cases.
Phase 3 gate passed all 12 native rows (10 behavior + 2 setup).
The source handle delivered 110 actual mouse-move events, kept one latest draft field,
and caused zero additional source evaluations/mesh jobs/uploads. Release produced one undo action.
Native ring rotation snapped to 30 degrees with Shift and retained its pivot; source expressions
remained intact. Parallel views, camera/tab changes, Escape/replacement and owner closure cancel safely.
Cavity, rotated and mirrored pick alignment passed. Failed fixture attempts remain retained.
Phase 4 now verifies both final backends, extracted runtime, DPI and full prerequisite regressions.
Source stays uncommitted, with no staging, pushes, promotion or stack edits.

Phase 4 and the authorized queue are complete. - 52 focused CTest cases pass; full discovery has 112 unique cases and the final JUnit
  report has 193 rows, zero failures/errors. Four parser echo checks and OEP8/attribute coexistence pass.
- Extracted native suite: 89 results (71 behavior, 18 setup/cleanup) across nine classes.
  Existing annotation/navigation/selection checks run with the Sections dock visible.
- Extracted DPR 1.5 and 2: 14 results each (12 behavior, 2 setup/cleanup), zero skips.
  Both deliver 110 actual source-drag move events with no extra evaluations/jobs/uploads.
- Each native clipping run checks 72 backend numerical samples across frozen preview,
  actual Manifold and actual convertible CGAL geometry: scales 1e-4/1/1e4, oblique/mirrored,
  centers up to 1e5 scale units, one/eight planes, coincident removal and a wall at 1e-4*D.
  Twenty-four independent supplied-piece pixel/depth/normal samples also pass.
- Native orthogonal-plane intersection, global restoration, origin/offset edits, Pick point
  orientation preservation, cavity alignment, normal/ring gestures, Shift snapping, undo/redo,
  deletion/missing references, transient promotion and Save/reopen pass.
- Seven Unicode exports pass through each extracted launcher under a clean runtime PATH.
  Installed shaders match source; the original Clipper2 header is restored after all builds.
  Shared dependency status is unchanged; source patches replay independently.

Final extracted performance: 102,396 triangles at 1280×720 physical pixels,
preparation 235.104 ms; one-plane p50/p95
5.478/7.093 ms, eight-plane
5.427/6.666 ms. The 220 plane updates create no additional
source evaluations, mesh jobs or uploads. Hardware: NVIDIA RTX 3070 Ti, OpenGL 4.6,
driver 616.92; shared Windows Release toolset 14.51.36231, SDK 10.0.26100.0,
Qt 6.11.1/QScintilla 2.14.1. These timings describe this machine.

Final feature patch: `cf1245b8dbd1f02aa16173265610b55645192c57fe5e49650b69d34286c4898e`.
Complete working input: `cb314b33ef95c8baf19cd2fb392b6761a9f12f42797c59f8662ce7a477596dee`.
Verification evidence: `a6984899c4e260cfae6bf906187249d45284c304bb46153c9f038adf66addf76`.
Extracted package `portable-verification-v2.zip`: `f2f18bc90a3ac1fb6be3f1dd81e9fbbfaa0435b61f1b132e6e970f6621fe4598`.
Source evidence identifies 36 feature files. Base/HEAD alone does not identify this build.

Final handoff: [completion notes](5_post-implementation-notes.md).

2026-10-06 UI fix-forward: the existing Cross sections owner now exposes world Origin and Cut away presets/custom
vector, with a single creation button and no offset/angle/drag-handle UI. Internal quaternion/translation/offset and
parent storage remain intact. This new delta is unbuilt, untested and uncommitted against migrated HEAD
`03e99c7d5d0660e04bd763f3eb2c2cf823fe9bed`; historical phase results above apply only to their frozen earlier input.
See the dated completion-note entry for exact patch hash, retained dependencies, static checks and verification limits.
