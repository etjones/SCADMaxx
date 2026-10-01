# Phase 1 — Native foundation and camera integration

Status: completed, source commit `3a60e69bb`. See [evidence and limits](5_post-implementation-notes.md).
Primary requirements: R01, R04, R09, R14, R27 in [requirements](2_requirements.md).

## Outcome

Establish a reproducible baseline, prove the native overlay and document integration approach, and provide a tested
camera adapter/operation boundary for subsequent phases. No new geometry/dependency subsystem is introduced.

## Work

- [x] Recheck dedicated branch/HEAD, worktree status, submodules, checkout instructions and local process ownership.
  Preserve any new user changes; record source state instead of assuming the planning-time clean base still applies.
- [x] Read the current workspace Windows profile and repair catalog. Prepare a dedicated application build using
  the existing shared vcpkg installation, with manifest mode/install disabled. Record generator, MSVC/SDK, CMake,
  dependency status hash and feature flags. Verify Catch2 and Qt Test availability without installing packages.
- [x] Build the baseline and run a narrow existing camera/document/native smoke selection. Diagnose required baseline
  repairs separately; do not import another feature/PR or edit shared dependency installations.
- [x] Map all camera writes and consumers: standard menu views, projection, reset/fit/center, mouse, numeric fields,
  input drivers and evaluation. Identify the post-evaluation synchronization point and the existing Animate behavior.
- [x] Implement a camera value snapshot and matrix/quaternion adapter with explicit coordinate conventions. Generate
  standard directions without copying FreeCAD's basis. Preserve public `$vpr/$vpt/$vpd/$vpf` semantics.
- [x] Introduce the viewport-owned operation boundary: current snapshot, apply target, observe external change,
  cancel/retarget, permission check and final-operation notification. Keep display notifications separate from
  evaluation-triggering completion. Guard feedback when programmatic changes update fields/actions.
- [x] Prove fixed transparent Qt child composition on the real QGLView: resize, hover repaint, moving model beneath,
  light/dark and scaled DPI. Exercise a minimal resizable popup with outside dismissal. Retain useful harness code;
  keep throwaway screenshots/probe records outside source. Do not expand UI before composition is understood.
- [x] Probe document metadata ownership and save intents using the existing TabManager lifecycle. Establish how
  metadata dirty state joins Save All/close indicators without becoming source dirty or causing reload discard prompts.
  Verify displayed-document ownership across active-tab mismatch and failed/empty evaluation before storing cameras.
- [x] Register targeted tests in the actual CMake test lists. Keep GUI-only adapters out of headless targets and
  preserve existing Qt version guards. Record the native test invocation and isolated preference/backup locations.

## Likely source boundaries

`Camera.*`, `QGLView.*`, `MainWindow.*`, `ViewportControl.*`, `Animate.*`, `TabManager.*`, `Editor.h`, CMake and existing
test infrastructure. Add narrowly scoped camera/controller helpers; do not do a general renderer/document refactor.

## Validation

- Camera basis tests use an asymmetric XYZ fixture and independent expected face directions, plus native round trips
  near poles, wrapped Euler angles and nonzero roll. Preserve pan/distance/FOV/projection for orientation-only changes.
- A menu action, manual orbit, numeric edit and script-driven camera update each refresh observers correctly. Count
  notifications/evaluations to detect recursion; establish the baseline for later interpolated updates.
- Native composition screenshots demonstrate transparent invalidation and popup behavior. Distinguish real compositor
  interaction from offscreen tests; offscreen rendering alone is insufficient for popup/repaint acceptance.
- The lifecycle probe keeps metadata through source reload without altering text dirty/undo state. Save As/copy
  intent is distinguishable from a metadata-only Save before phase 4 builds the production store.

## Exit and evidence

Record commands, logs, camera convention table, integration map and native probe images under a fresh phase-1 attempt
in the overall plan's evidence root. The application must link and the selected checks pass. If child composition or
metadata integration fails, resolve the approach here and update the overall plan before phase 2; do not hide that risk
behind mocks. Mark checks only when executed. Phase 2 consumes the adapter/controller and verified widget owner.
