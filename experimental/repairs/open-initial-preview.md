# Initial Preview after File > Open

2026-10-09: source fix pending validation and commit in
`D:/openscad/wt-openscad-background-model-evaluation`, branch
`feature/background-model-evaluation`, based on `d76e0f75f85b404f14742496888adfb2a937f174`.
The delivered integration `62b78cb87` still contains the reported behavior.

## Cause and change

- Startup Preview was gated by `designActionAutoReload`, whose default is false. Initial display
  must be independent of the disabled periodic reload loop.
- File > Open emitted `editorContentReloaded`, whose handler requests only parameter metadata.
  New tabs emit that notification before entering `editorList`, so controller admission rejects it.
- Add `TabManager::editorFileOpened` after loading and registration for both reused blank tabs and
  newly created tabs. The controller handles this explicit open event with a Preview request.
- The controller's startup callback requests Preview for the active nonempty document, independently
  of auto-reload. Metadata-only jobs can be upgraded; already pending Preview/Render jobs are preserved.
- Content edits, dependency changes and tab switching do not acquire this new open trigger. Existing
  explicit Preview/Render, metadata, Customizer and auto-reload pathways remain distinct.

The F5 Design > Preview action still submits a Preview in inspected source; no separate failure of
that action has been reproduced. View > Preview selects a preview renderer and cannot substitute
for calculating one. Regression coverage now exercises the actual Render/Preview actions as well.

## Handoff

Changed owner files: `src/gui/TabManager.{h,cc}`, `src/gui/evaluation/EvaluationController.cc`,
`src/guitests/TestBackgroundEvaluation.{h,cc}`. Pre-existing dirty Clipper2 content is preserved.
No build, tests, commit, merge, push or package was performed for this fix. Existing accepted pins
and binary validation remain tied to their original commits; they do not validate this working diff.

Added native cases `openPreviewsWithoutAutoReload` and `startupPreviewsWithoutAutoReload` cover
blank-tab reuse, opening a second tab, startup, no edit-triggered preview, and F6 followed by F5.
Run these only with the required build/test and desktop authorization. Also retain the existing
cancelled/stale/failed Preview tests when validating changed startup behavior.

When requested, commit on the owner and merge forward through maintained dependencies and the
integration; do not copy this fix into each branch or cherry-pick it. Rebuild incrementally only
after authorization, preserving the last delivered package until the new build is verified.

## Requested integration/build, 2026-10-09

Committed locally in the owner and merged normally into `f4f87a8eea11172037c459dd5ae9848b566fd044`, with prerequisite closure updated. See [run evidence](../../../runs/scadmaxx-all-features-2026-10-09_19-45/report.md). Incremental build, everyday (516 unit case rows), tool checks and extracted package checks passed. New native initial-open cases were not compiled/run in the release configuration; desktop validation remains pending. Quick performance comparison was interrupted twice by an unrelated artcraft-hub linker and remains incomplete. No push/promotion or full-validation tag. Hierarchy/integration test conflicts are resolved by retaining both independent sets of includes and slots.
