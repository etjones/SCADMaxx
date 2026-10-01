# Phase 7 — Later saved-view integration

Status: separately scheduled follow-on, not part of the first core delivery. Covers N01–N03 plus integrated
R05, R14–R16 and R20. Depends on phases 1–6 and a reviewed committed navigation implementation.

## Entry conditions

Read navigation's current requirements/overall plan and identify committed saved-view and camera-operation APIs.
Lock its exact revision/delta with the core and annotation revisions. Do not read/write a guessed companion format
directly, copy unfinished navigation changes, or implement a second store. If the prerequisite is unavailable,
leave this phase pending and the already verified core deliverable usable.

## Implementation

1. Bind SavedViewsAdapter to the native library for the viewport's displayed document, independently of the active
   editor. Publish its capability only when the integration is live. Library/session revisions are opaque and scoped
   to the owning runtime document; paths and view names never replace record IDs.
2. Implement list/add/rename/remove/recall through native operations. Add captures the displayed full camera; rename
   and remove do not move it. Recall restores pose, distance, FOV and projection without fit, overlay or pixel-size
   restoration. Preserve the navigation feature's naming/validation and ordered records.
3. Require expected library revision for metadata mutation, and expected result/view for camera operations. Duplicate
   request receipts prevent duplicate additions/removals. Concurrent native edits return stale; do not silently refresh
   preconditions and repeat the operation. Route changes through the same native history policy as the UI.
4. Preserve companion dirty state and normal Save/Save As/copy/all/close/reload behavior. No HTTP save endpoint is added.
   Neither reading nor recalling views writes metadata. Untitled views remain in memory until normal saving.
5. Integrate the shared camera operation and capture boundary. Navigation's plan freezes capture at the displayed
   transition camera and cancels remaining callbacks; use that boundary rather than another animation controller.
   Report the post-operation view revision. Preserve annotation locks and native final camera notifications.
6. Adopt the native clean-capture policy for agent captures: exclude navigation controls, palette, statistics, axes,
   scale markers and crosshairs; retain model surface/edge rendering. Reuse guarded render/readback, restore temporary
   state on every exit and leave original annotation PNGs untouched.
7. Extend contract/CLI/skill with capability-gated saved-view commands and persistence semantics. Keep legacy captures
   compatible with the composed application's intended clean-capture behavior and identity/outcome contract.

## Validation

- UI-created views are immediately readable via API; API-created/renamed/removed entries appear in the native UI.
  Replay identical add/remove requests and prove a single metadata mutation.
- Recall round-trips complete cameras in both projections and at a changed viewport aspect ratio without auto-fit.
  Add during a transition records the displayed camera, not a queued destination.
- Native saving/reopening, untitled first save, Save As/copy, external source reload, final-entry deletion and external
  companion conflicts follow navigation's existing persistence tests. API does not silently save or clear dirty state.
- Test stale view/library IDs, duplicate paths, wrong displayed owner, close/reopen and concurrent user edits.
- In a combined native application, exercise marked/unmarked drafts, animation/capture interruption and Stop/restart.
  Inspect actual helper-free images with all guides enabled in the live viewport; live settings recover afterward.
- Run both clients and relevant navigation/annotation regression suites with the locked committed inputs. Record
  exact feature deltas and any integration repairs separately from core functionality.

## Completion

Update adapter capability evidence and post-implementation notes. Keep the earlier core completion and this later
integration distinct. Combined build selection/publication remain governed by the workspace workflow; phase completion
does not authorize an experimental composition, GitHub push or unrelated feature edits.
