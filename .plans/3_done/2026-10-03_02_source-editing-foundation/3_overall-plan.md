# Source editing foundation: implementation design

Target implementer: GPT-6.1 Sol. Read [requirements](2_requirements.md) and the shared
[handoff standard](../../1_planning/2026-10-03_00_source-first-cad-overview/implementation-handoff.md).
Source evidence is from `4c325716b94e444637a80df3966197ce110b2b75`; recheck symbols at branch preflight.

## Branch and existing code

Use proposed `feature/source-editing-foundation`, with selected annotation/HTTP prerequisites and their closure.
Record the prerequisite-only base under the [composition rules](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

- `src/gui/Editor.h`: existing `sourceRevision`, `sourceFingerprint`, annotation store and document signals.
- `src/gui/ScintillaEditor.cc`: UTF-8 mode; textChanged increments revision; SCN_MODIFIED handles annotation tokens;
  `appendAnnotationUndo()` adds container actions. `setPlainText()` clears annotation history and cannot apply patches.
- `src/gui/TabManager.cc`: `open`, `refreshDocument`, `saveDocument`, `saveSource`, `saveAs`, `saveACopy`.
- `src/gui/MainWindow.cc`: `fileChangedOnDisk`, `checkEditorModified`, `editorContentChanged`.
- `src/gui/SavedViews.cc`: fingerprint/lock and callback-based source save; keep its partial-save reporting.
- `src/gui/annotations/AnnotationBridge.cc`: source snapshots use editor revision and annotation session ID.

## New files and exact transaction contract

Add `src/gui/source/SourceEditTransaction.h/.cc` and `SourceEditTransaction_test.cc` in namespace `SourceEditing`.
Names below are proposed new API, not existing symbols:

```cpp
struct ByteEdit { qsizetype begin, end; QByteArray expected, replacement; }; // [begin,end), original UTF-8
struct EditRequest {
  QString documentId;
  quint64 sourceRevision;
  QString sourceFingerprint;
  QVector<ByteEdit> edits;
};
enum class EditError {
  None, WrongDocument, StaleSource, ReadOnly, InvalidRange, InvalidUtf8, Overlap, ExpectedTextMismatch
};
struct EditResult { EditError error; bool changed; quint64 sourceRevision; QString detail; };
EditResult apply(EditorInterface& editor, const EditRequest& request);
```

Use the existing annotation session ID behind a new `EditorInterface::documentId() const` accessor. Do not invent
another registry/ID. The caller retains a QPointer to the intended editor; a null pointer is rejected before `apply`.
`apply` must run on the editor's GUI thread. Add a narrow virtual editor operation for applying already-validated
byte edits; implement it in ScintillaEditor. Keep validation separate from QScintilla calls for focused tests.

Algorithm: snapshot current UTF-8 once; validate ID/revision/fingerprint and read-only status; reject negative/out-of-
range positions, continuation-byte boundaries, invalid replacement UTF-8, duplicate starts and overlapping ranges.
Compare each expected byte slice before mutation. Adjacent ranges are allowed. Remove true no-ops; if none remain,
return success/changed=false. Apply remaining edits in descending start order so original offsets stay valid.

Add `EditorInterface::prepareExternalEdit()` emitting a synchronous `externalEditStarting()` signal. Invoke it after
successful validation/no-op removal but before opening an undo group or applying any non-Vim programmatic mutation.
Use it in ScintillaEditor's existing programmatic insert/replace/replaceAll/number/block-edit and annotation-history
entrypoints as well. No-op/rejected transactions emit nothing. Feature 05 consumes this hook to finish an active Vim
insertion group before another undo action starts; 02 imports no Vim code. Feature 05 therefore depends on 02.

Use Scintilla target-start/target-end/replacement APIs inside beginUndoAction/endUndoAction. Never call setText,
setPlainText, reset the undo buffer or reprint an AST. Range validation happens before opening the undo action.
Use an RAII batch guard to unwind correctly; normal recoverable errors occur before mutation. A programming failure
during mutation must not be converted into a successful partial edit.

During this explicit batch, defer the existing textChanged revision/fingerprint publication and final editor signals
until all patches are applied; outside the batch retain the existing behavior. Do not block SCN_MODIFIED or annotation
container undo processing. On commit compute the final fingerprint, advance the existing revision and emit one final
contentsChanged/modificationChanged notification. Undo/redo must advance revisions, not rewind them to old values.
Do not require a particular count of intermediate revision increments from QScintilla undo internals.

## Source file conflict contract

Add `src/gui/source/DiskSourceState.h/.cc` and tests. A snapshot contains canonical destination identity, existence,
raw-byte SHA-256 and read status. Editor state records the last successful source read/save snapshot; untitled editors
have no source baseline. Keep raw disk hashes separate from editor UTF-8 fingerprints because disk encoding/EOL
normalization is an existing load/save concern. Reuse Qt hashing; no new library.

Capture the snapshot with the bytes read by TabManager open/reload, and after successful source commit. Use QFile
Unicode paths and content hashes for change detection; remove the obsolete timestamp/size-only decision path for
source conflict detection. Unreadable, removed or replaced files are distinct outcomes, not "unchanged".

Before `saveDocument` starts source/companion changes, compare destination with its expected snapshot. For Save As or
Copy, use the exact destination state that the user approved for replacement. Conflict choices are Cancel (default),
Save As, or explicit overwrite of the observed version; do not repeatedly prompt when the version still matches.
If the version changes again, reject that authorization and report the new conflict.

Keep QSaveFile. Check the expected disk state before writing and again immediately before commit, then update the
baseline only after success. This detects observed conflicts; it cannot provide cross-process compare-and-swap
against an editor that writes in the final check/rename interval. Do not claim that a Qt lock excludes every editor.
Save a Copy leaves editor baseline/path/dirty state unchanged. Preserve existing saved-view/annotation ordering and
report partial metadata failures honestly; do not roll back a successfully saved source by guessing old contents.

## Phases and verification

1. [Validated text transactions](4_imp-phase1.md): API, pure validation and real editor undo/revision tests.
2. [Content-aware file conflicts](4_imp-phase2.md): snapshots, load/save wiring and deterministic conflict tests.
3. [Native integration and handoff](4_imp-phase3.md): document/annotation/HTTP integration, build and recorded delta.

GUI unit files are discovered by the existing GUI_TEST_SOURCES glob after reconfigure. Add production sources to
the GUI CMake source/header lists. Native harness additions go in `src/guitests` and its explicit CMake/runner lists.
No storage-schema or expression-rewrite question remains for this foundation; do not expand into those consumers.
