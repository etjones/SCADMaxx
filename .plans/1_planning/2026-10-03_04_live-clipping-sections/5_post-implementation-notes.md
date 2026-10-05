# Local live-clipping completion, 2026-10-04

All four phases and CL01–CL12 are locally implemented and verified. The authorized queue
**03 → 05 → 06 → 14 → 04 is complete**, each in its isolated feature worktree.
Source: `D:/openscad/wt-openscad-live-clipping-sections`, branch `feature/live-clipping-sections`,
base/HEAD `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`, uncommitted by instruction.
Run: `D:/openscad/runs/20261004-live-clipping-sections`.

Direct verified prerequisites 03/14 are replayed once from 14 complete input
`56275040c8fde09076ce5ae8510927d5845cf5f882ba27cab5142a59f4ec6c9a`, including 02 and pinned
OEP8/Customizer parser repairs. There is no 05/06/07/08/09/10/12/15 dependency in this branch.

The Sections dock consumes canonical 14 Section records, preserving their ID and source expressions.
Transient presets remain transient until explicit promotion. Personal state contains only enable/helper IDs,
selection and the global toggle. One shared draft previews each gesture; absolute built-in field changes coalesce,
while registered custom consumers retain their ordered stream. Release commits one editor undo action.
Source commits invalidate evaluation and require ordinary Preview/Render. Stale gestures/picks cancel safely.

Prepared meshes use the frozen preview tree or current final geometry. One common strict positive-half-space
predicate drives color/edge/depth/ID/normal passes. Uniform changes leave geometry and vertex buffers intact.
Provider-owned IDs/transforms/colors/roles/masks survive clipping, and helpers remain outside pick buffers.
CGAL conversion and polygon tessellation use private recentered copies before native float indexing, preserving
the evaluated geometry and the original epsilon. This corrects the distant small CGAL failure found by phase 4.
Worker-local cancellation retains the frozen scene; obsolete deliveries cannot replace a newer presentation.

- 52 focused CTest cases pass; full discovery has 112 unique cases and the final JUnit
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

Public contract: `D:/openscad/wt-openscad-live-clipping-sections/doc/live-sections.md`.
Matching executable: `D:/openscad/runs/20261004-live-clipping-sections/portable-extracted-v2/scadmaxx.exe`.
Native evidence: `D:\openscad\runs\20261004-live-clipping-sections\native-20261004T053015115Z`; screenshots were visually reviewed.

Limits: eight positive half-spaces; caps, computed contours/measurements/export and slabs are unavailable.
Computed/helper adjustment fields require direct source editing. Unsupported 2D/Thrown Together/nonconvertible
inputs report feedback. The verified scales/translations have finite precision; broader ranges need evidence.
Other platforms, clean-machine portability and a complete selected-stack composition remain unverified.
Failed fixture/compile/native attempts and the earlier package remain retained.
No staging, commits, pushes, promotion, enabled-stack changes, plan lane moves or README edits were performed.
Later selected navigation `bfd009ef0047452c09e3629d0af25efd6af34700` remains a future composition obligation.
Rework choices: fix forward (bounded correction), replan (revised approach), restart (fresh implementation),
or supersede (replacement feature). No rework is needed to complete this queue.
