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

## 2026-10-05 fix-forward: geometry-preparation wording

Sections now distinguishes geometry preparation from other model evaluation and explains waiting or
cancelling through the status bar. It explicitly says Inspector need not be closed. This changes
feedback only; clipping evaluation and lock behavior remain intact.

Local owner base: `06d073f73720a391f5d806911a3d91a27b1ebd4e`, with uncommitted delta
`runs/20261005-inspector-selection-feedback/clipping.patch`, SHA256
`d2e47fe3c5d121617564f4186337d54b0a4cbad7908887d7b93f4e22e6f0a44b` (container-relative).
The companion Inspector change and combined native verification are recorded in that run's report.
No commit, push, promotion or release replacement was made.

## 2026-10-06 fix-forward: deletion, restart state and cutting-plane guide

The local owner now removes remembered IDs together with deleted Section definitions, supports
removing missing-definition rows, and excludes session-only IDs from persisted settings, even
after document teardown. Delete copies its argument because synchronous document signals can
change the selected ID. Source-backed definitions retain the existing undo/edit lifecycle.

The panel replaces Backing/Transient/Unavailable terminology with Storage/Session only/Missing
definition, and explains explicit saving into source. The default helper is a translucent plane
spanning model bounds. Move/rotate handles are separately enabled, initially off; invisible
handles do not capture clicks. Alpha blending preserves GLView's opaque framebuffer alpha for
Qt composition. Ordinary source/offset/angle and explicit handle interactions remain supported.

The full local clipping delta against `06d073f73720a391f5d806911a3d91a27b1ebd4e` is
`runs/20261006-sections-usability/clipping.patch`, SHA256
`f4745eba5bd6c48100aa2ad68753cf0f663e20be818cf835ea040436223ab392` (container-relative).
It supersedes the preceding small clipping-wording patch and includes it. The run report records
combined verification, final results and retained failed attempts. Changes remain uncommitted and
unpromoted; no release replacement. The separate rotation-stutter report remains unresolved.

## 2026-10-06: standalone Sections development build

User requested a Sections-only build for further development before the next integrated build.
Rebuilt the owner checkout at 06d073f73720a391f5d806911a3d91a27b1ebd4e plus the existing five-file
local delta, using its own runs/20261004-live-clipping-sections/build and shared vcpkg installation.
No other feature delta was imported. Reproducible source patch, submodules, configuration, build/deploy
commands, executable hashes and native checks are in D:/openscad/runs/20261006-sections-standalone.
Runnable output: D:/openscad/artifacts/scadmaxx-sections/20261006T070059977Z/staging/scadmaxx.exe.
This separate development collection preserves the integrated release and current app/launcher settings.
No source commit or push was made; the branch remains local and unpromoted at this modified state.

## 2026-10-06: cross-section terminology discussion

Changed only the checkbox label to Enable cross section clipping, as explicitly requested.
The user prefers cross section for the UI; a wider terminology rename remains under discussion.
No persisted Section type, API identifier or other UI label has been renamed in this change.
Standing workspace instruction: do not build or run tests until explicitly requested by the user.
No build or tests were run for this text edit; existing executables retain their previous label.

## 2026-10-06: accepted cross-section terminology

Applied the agreed UI vocabulary in the Sections owner: Cross sections for the dock/tool and records,
cutting plane for the guide and its position controls, clipping for hiding geometry. New preset names
use XY/XZ/YZ cross section; saving reads Save cross section in source. Updated user-facing preparation,
capability and error text and the feature documentation, including optional move/rotate handles.
Existing user labels, source type Section, stable IDs and settings keys retain their identities.
These are presentation edits only. No build or tests were run, as instructed.
Future integration must use this owner delta; other worktrees and existing executables were not updated.

## 2026-10-06 fix-forward: origin and cut-away direction UI

Status: implemented locally, **unbuilt, untested and uncommitted**. This replaces the historical angle,
offset-slider and optional handle UI described above. Existing runtime evidence does not validate this revision.
Owner checkout: `D:/openscad/wt-openscad-live-clipping-sections`, branch `feature/live-clipping-sections`,
HEAD `03e99c7d5d0660e04bd763f3eb2c2cf823fe9bed`. The existing incomplete nine-file clipping delta was
finished in place. Unrelated branding icons and the dirty Clipper2 version header were preserved.

The dock has one New cross section button, world Origin X/Y/Z and Cut away with Above (+Z), Below (-Z),
Toward +Y/-Y/+X/-X and Custom X/Y/Z. New sections default to Above (+Z), using stored normal -Z at model center.
Custom uses scientific-number text inputs so tiny or huge representable finite components are accepted.
The controller scales before normalization, rejects nonfinite/zero input without changing pose, and reports why.
Entered text and magnitude survive successive component edits and rejected zero. Custom state is scoped to
the active document and selection; external direction changes (including Flip/undo) refresh the displayed vector.
Pick point, Pick + align and Flip remain explicit one-shot commands. Plane dragging, rotation rings, angle controls,
offset controls, Model range, reset presets and show-handles controls and their obsolete consumers are removed.
The shared selection router's unrelated drag support remains intact.

Storage retains the existing base origin/normal/up, quaternion adjustment, translation, offset and rigid parent frame.
No storage schema, migration, alias or compatibility path was added. Clipping retains the positive stored-normal
half-space, so UI cut-away direction maps to its negative normalized normal. `sectionFrame` resolves:
`worldOrigin = parent * (baseOrigin + translation + offset * (rotation * baseNormal))`.
`poseChanges` compensates translation for the rotated offset; direction edits keep the actual resolved origin
stationary, and origin edits preserve orientation. Parent normal/up conversion uses transpose because section parents
are required to be rigid. The previous helper up vector is transported into the new plane, with a deterministic
fallback for parallel degeneracy, preserving a stable internal roll without exposing roll controls.

The shaded helper rectangle has a blue origin dot matching its border. Dot size and border width scale with DPR;
the overlay registry's `ScopedGLState` restores point/smoothing/blend and other GL state. The help icon beside Save
cross section to source explains session/source saving, no filled cap, the dot and removed-side/custom direction.
Healthy-state explanatory text now lives in help; status remains available for actionable feedback.

Updated (not executed) native coverage covers six presets, default creation, sequential custom text edits, zero rejection,
scientific magnitude, document ownership, source undo, internal nonzero offset with a rotated/translated rigid parent,
origin/orientation invariants, sign/magnitude/extreme normalization, picking, no handle dragging and removed controls.
Math coverage checks parallel/antiparallel normals, deterministic up fallback and normalized quaternion mapping.
Static `git diff --check` passed; reference searches found no remaining clipping gesture/angle/offset-control callers.
No build, test, staging, commit, push, merge, promotion, readiness-pin, plan-lane or README change was performed.

Reproducible nine-file delta against the recorded HEAD:
`D:/openscad/runs/20261006-cross-section-direction-ui/source.patch`, SHA256
`02ab956b36798201a6d78b80b92236ce10faa352fd21aac330215206d33fa6d0`.
Accepted dependencies remain persistence `4652ee8a816b0d7dc7411f4b7b3112a49175b545` and shortcuts
`3014fb55405759bfa1871e79f50cbee4c2a2c638` (unchanged manifest).
Actual submodule HEADs match tracked pins: MCAD `1ea402208c3127ffb443931e9bb1681c191dacca`,
Clipper2 `c7f820f6a03fa91f189b866d27bf40dfe47abaa6`, OpenCSG `9bf122715213dca05e70993dd8672fe3aa36c518`,
manifold `0edd9d54876f3135e431575214dd6d8a72866fee`, mimalloc `30b2d9d89099bee08e9f67a1ffb3e12e7ba45227`,
sanitizers-cmake `bcb1fc68616e9645ca5acea2992412606373ab04`. Clipper2's existing dirty
`CPP/Clipper2Lib/include/clipper2/clipper.version.h` remains outside the feature snapshot.

Remaining verification is explicit-authorized compilation and native/DPI checks; Qt input/focus behavior and the
GL marker's appearance have only static review. Earlier binaries retain their previous controls.
Follow-up choices: fix forward (bounded corrections), replan (revise strategy), restart (revisit assumptions),
or supersede (replace the objective). These are optional, not a requirement to start further work.
