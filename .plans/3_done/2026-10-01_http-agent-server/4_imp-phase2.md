# Phase 2 — Live targets, source snapshots and diagnostics

Status: implemented; source commit `195a3be74`. Dependency enrichment continues in phases 3–4.

## Implementation

1. Introduce a GUI-owned registry for windows, open editors and viewports. Use UUID lifetimes independent of paths;
   register/remove via native lifecycle, retaining explicit active-editor and displayed-root relationships.
2. Track editor text revision, dirty state, automatic-reload state, pending evaluation and displayed result separately.
   Reuse annotation result ownership where available; make shared ownership authoritative for both APIs. Avoid two
   counters that can disagree about the same viewport. Source/metadata dirty flags remain separate.
3. Add source-snapshot operations for an explicit document and origin. Disk reads use the actual native path and
   bounded file reads; editor text is copied on the GUI thread. Capture expected revision, bytes/text representation,
   normalized-content hash and origin before off-thread hashing/encoding. A caller-supplied expected hash mismatch
   yields stale, never an implicit retry using newer content. Untitled disk origin is explicitly unavailable.
4. Resolve allowed dependency handles from known document context rather than arbitrary path URLs. Preserve native
   relative/library path semantics. Detect change-during-read where possible and expose uncertainty. Do not claim
   a filesystem transaction or use this facility as unrestricted file browsing.
5. Instrument normal compilation start, parsing, instantiation, rendering publication, failure and empty-success
   paths. Reconcile annotation lifecycle hooks. Assign attempts at start and results only at successful publication;
   preserve actual renderer ownership after failure. Closing a document invalidates pending work and target handles.
6. Add typed diagnostic observation around `Message`/output handlers. Preserve normal console/error-log delivery;
   scoped operation context attributes messages to parse/evaluation or explicitly global. Audit worker callbacks and
   reentrancy so interleaved windows cannot inherit the wrong context. Do not scrape the visible console.
7. Publish immutable state snapshots and bounded diagnostic/dependency records to the worker. GET reads are cached;
   explicit source snapshot requests perform bounded I/O. State generation changes on state, heartbeat on liveness.
   No repeated file hashing, frame grabs or compilation on ordinary status polls.

## Validation

- Two windows, two copies of one path, an untitled document, and editor B active while A owns the viewport yield
  distinct, stable targets. Closing/reopening A invalidates old requests without retargeting B.
- Disk/editor differences, CRLF/LF normalization, non-ASCII paths/text, BOM handling and file replacement are reported
  correctly. Verify original byte hashes and normalized text hashes are not conflated.
- Assert source bytes, undo availability, dirty flags, active tab, camera and result identity do not change after reads.
- Observe success, empty success, parse failure and F6 failure/success; ensure a failed attempt can retain the prior
  display with its original result ID. Never-evaluated documents report no model tree.
- Trigger native echo/assert/warnings in both windows and parse contexts; verify attribution and unchanged GUI output.
  Messages before service observation remain unavailable, not reconstructed as current output.
- Normal external include/use/root changes produce new results only through existing reload behavior. Disabled reload
  and unsaved conflicts remain explicit; bounded polling must not change preferences or cause paint/evaluation.

## Exit evidence and handoff

Retain lifecycle timelines and before/after state fixtures, including a stale viewport after failure. Native tests prove
diagnostic attribution and target invalidation; unit tests cover hashing and generation transitions. Phase 3 receives
immutable source snapshots and an exclusive native-compilation gate. Phase 4 receives result publication hooks.
