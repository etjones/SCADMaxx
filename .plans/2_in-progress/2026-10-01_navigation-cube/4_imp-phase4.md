# Phase 4 — Saved cameras and document persistence

Status: complete. Depends on [phases 1–3](3_overall-plan.md#ordered-phases-and-coverage).
Primary requirements: R12–R16, R24 in [requirements](2_requirements.md).

## Outcome

Complete the popup's per-document camera library, including full camera recall, inline editing, document dirty state,
save/reload/copy semantics and recoverable failure handling. No mutation writes a companion before document saving.

## Work

- [x] Implement the versioned store described in the overall plan: `model.scad.views.json`, stable record IDs, names
  and complete camera snapshots. Define bounded file/entry/name limits and finite/range validation before parsing into
  live state. Reject invalid or unsupported data without replacing it. Exclude viewport size and execution flags.
- [x] Bind each library to its document and the popup to the viewport's displayed-document owner, using phase 1's
  ownership boundary. Show the owner when it differs from the active editor. Disable mutations with an explanation
  when ownership is unavailable; keep ownership for successful empty results and retained geometry after failure.
- [x] Implement Add with a unique default View N name and immediate inline editing, Rename, and direct Remove of the
  selected entry. Stable IDs permit duplicate user names. Cancel/blank edits retain the previous/generated name.
  Complete nonempty focus-loss edits; popup dismissal must not discard Add. No new deletion confirmation or undo
  history is required; use the established save/discard lifecycle for unsaved library changes.
- [x] Single-click only selects. Double-click/Enter recalls through the shared camera controller and leaves the popup
  open; Enter during editing only commits the name. Add snapshots the displayed pose during a transition. Recall
  restores projection, rotation, translation, distance and FOV without auto-fitting or restoring overlays.
- [x] Extend dirty indicators, Save All filtering, maybeSave/close checks and document teardown to include metadata.
  Source-text undo remains independent. Selection, recall and loading unchanged views never dirty the library.
- [x] Introduce explicit save intent in TabManager: ordinary save, Save As and Save a Copy. Metadata-only ordinary
  save writes only the companion; As/Copy still write the destination source. Untitled first-save assigns the companion
  location. Copy keeps original path and dirty state; successful As changes identity consistently with source saving.
- [x] Persist an explicit empty library after Remove-last. Do not create a companion merely by opening an untouched
  document. Source refresh/reload preserves in-memory views and their unsaved state.
- [x] Write companions through atomic replacement with cooperative writer locking and an expected on-disk fingerprint.
  Detect external modifications, competing windows and existing destination companions before overwrite. Present
  recoverable conflicts instead of silently merging, replacing unreadable data or changing the source-save decision.
- [x] Track source and companion save success separately. Retain dirty metadata on companion failure, report partial
  success accurately, and allow retry without unnecessary source rewriting. Preserve recovery copies before an
  explicitly chosen conflict overwrite; never treat two file replacements as one crash-atomic transaction.
- [x] Extend the existing backup/recovery path with a matching view-library snapshot and document identity. Restore
  recoverable in-memory metadata without overwriting a newer companion; cancel callbacks when the owner closes.

## Validation

- Store tests cover both projections, roll, translation, distance/FOV, Unicode/duplicate names, IDs, empty libraries,
  malformed/unsupported/oversized data and invalid numeric values. Round trips must preserve camera fields exactly
  within the representation's documented numerical tolerance.
- Native document tests cover untitled first save, source-only and metadata-only changes, Save All, As, Copy, reload,
  close/discard/cancel/reopen, different active/rendered editors, empty/failed results and multiple windows.
- Assert SCAD timestamps/content and compilation counts remain unchanged for metadata-only ordinary Save. Verify Copy
  leaves original dirty state intact and Remove-last remains empty after reopening.
- Inject write/rename/lock failures, source-success/companion-failure, companion collisions and concurrent changes.
  Verify data survives retry and recovery; compare files before/after each rejected operation.
- Exercise Add during animation, cancel/focus-loss naming, Enter while editing, recalling after aspect-ratio changes
  and document close during a transition. Confirm saved-view edits never modify source text or its undo stack.

## Exit and evidence

Record the schema and limits, lifecycle matrix, failure/recovery results and native list screenshots. All three list
buttons must now perform real operations. Complete the document lifecycle before treating saved views as usable;
successful Add/recall alone is insufficient. Use isolated documents and backup/settings directories for every test.

## Phase result

Implemented version-1 JSON, UUID records, complete poses, 4 MiB/1000-entry/256-character bounds, atomic replacement,
writer locks and SHA-256 expected-content checks. Conflicts retain both versions and use Save As to a fresh filename;
there is deliberately no destructive overwrite action. Source and companion failures are reported separately.
Native transaction and document tests pass (runs/navigation-cube/phase4/complete), including metadata-only timestamp,
Copy/As/All, reload, Unicode duplicate names, empty files, backup reopening, lock/conflict and partial-write retry.
Broader close/cancel, malformed-input and ownership coverage continues in phase 6.

