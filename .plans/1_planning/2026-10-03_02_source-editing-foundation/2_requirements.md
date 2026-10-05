# Source editing foundation: requirements

Status: specified for implementation planning, 2026-10-03. Scope is one live document per transaction.
The [exploration](1_exploration.md) records the user decisions; [overall plan](3_overall-plan.md) defines the mechanism.

## Observable requirements

- SE-01: typing and programmatic source edits share the existing editor buffer, document identity and revision.
  No hidden editable model or second source buffer is authoritative.
- SE-02: a transaction identifies its document, expected source revision/fingerprint and exact original ranges.
  Reject a closed/wrong document, stale revision, changed range, invalid boundary, overlapping edits or read-only
  target before changing any text. Failure leaves text, selection, dirty state and undo history unchanged.
- SE-03: apply validated insert/replace/delete operations as one logical undo action. Undo/redo restores complete
  transaction text; existing annotation undo and normal typed edits remain coherent.
  Notify synchronous edit participants before opening the new undo group, so an existing modal insertion group can
  finish first. Rejected/no-op requests must not change input state through that notification.
- SE-04: preserve all untouched editor bytes, comments, blank lines, expression spelling and line endings. Generated
  replacement text is the caller's responsibility; this foundation does not reformat or invert expressions.
- SE-05: a successful nonempty change marks the document dirty and updates existing revision/fingerprint observation.
  Notify consumers after the whole patch set is present. Committing a transaction does not write a file or force a
  geometry evaluation. A no-op transaction creates no undo step or dirty/revision change.
- SE-06: explicit Save detects content changes/deletion/replacement since the last successful read/save, including
  equal-length edits with unchanged timestamps. Keep the unsaved buffer and permit Cancel, Save As or an explicit
  overwrite decision. Recheck a changed disk version before overwriting it.
- SE-07: Save As and Save a Copy protect an existing destination. Save a Copy does not change current path, baseline,
  dirty state or source identity. A failed write leaves the original file intact and the buffer unsaved.
- SE-08: preserve current saved-view and annotation save coordination. Do not claim an atomic multi-file commit;
  report which content saved if a subsequent companion write fails. A known source conflict must be detected before
  saving companions. This feature does not replace their formats.
- SE-09: support Unicode text/paths and normal multi-document use. A transaction never follows a change of active tab
  to a different editor. An included file may be edited only as an explicitly identified open document.
- SE-10: external file detection/reload must not discard a dirty buffer. Preserve existing explicit reload/close
  choices. Backups remain backups, not an implicit source Save.

## Acceptance examples

1. Change two literals around comments in a buffer containing `é` and a non-BMP character: only the requested UTF-8
   spans change; one undo restores both. Repeat with LF and CRLF already present in the buffer.
2. Insert a typed character after preparing a transaction: application rejects it as stale without partial edits.
3. Submit overlapping spans or a byte offset inside a multibyte character: application rejects the entire transaction.
4. Alternate a typed edit, an annotation command and a programmatic edit: undo/redo follows the actual sequence.
5. Modify the on-disk file with equal byte length and restore its timestamp: Save still detects the changed content.
6. Cancel that conflict, then Save As: both versions survive and the intended editor adopts only its successful save.
7. Select another tab after preparing an edit: the transaction targets its captured document or rejects a closed one.

## Boundaries

No cross-document atomic edit, disk-only included-file editing, AST reprinting, external-editor broker, CRDT,
new HTTP mutation endpoint or persistence schema is included. 06/10/12 decide source meaning and transformation.
14 reuses the document transaction/conflict machinery for typed, annotated declarations in main or included `.scad` files.
