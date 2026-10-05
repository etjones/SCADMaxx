# Phase 1: validated editor transactions

Requirements: SE-01 through SE-05 and SE-09. Input: recorded prerequisite branch, existing editor/annotation tests.

1. Add the types and validator in `SourceEditTransaction.h/.cc` from the overall plan. Use original UTF-8 byte offsets,
   validate the entire request before mutation and return the named failure category. Build table-driven validator
   tests for stale revision/hash, wrong ID, out-of-range/multibyte offsets, overlapping/duplicate positions, adjacent
   edits, wrong expected text, invalid replacement UTF-8 and a no-op set.
2. Add `documentId()` and a narrow virtual byte-edit operation to EditorInterface; implement it in ScintillaEditor.
   Preserve annotation session identity. Add transaction batching around the existing textChanged publication, not
   around all Qt/Scintilla signals. Keep annotation SCN_MODIFIED processing intact.
   Add prepareExternalEdit()/externalEditStarting() and invoke after validation, before the new undo group. Route
   existing external edit/annotation-history entrypoints through it. A test observer closes an existing group:
   verify the following transaction is a separate undo step; rejected/no-op requests do not invoke the observer.
3. Apply descending replacements through Scintilla target APIs and one undo group. Restore read-only/caret behavior
   deliberately; rejecting a read-only target must not temporarily make it editable. Transform caret/selection
   endpoints through edits: before a range unchanged, after it shift by byte delta, inside it move to replacement end.
   Retain selection direction; only scroll if the resulting caret would otherwise be inaccessible.
4. Register production sources and reconfigure. Add actual editor tests using the existing GUI unit-test setup pattern
   (`src/gui/Icons_test.cc` / neighboring widget tests), with isolated settings and an offscreen QApplication.
5. Use test tag `source-editing`; verify discovery, then run the filtered cases through the shared handoff commands.

Required fixtures: two replacements around comments; insert+delete; empty change; LF and CRLF; `é` and a non-BMP
character before a target; typed edit invalidating a request; a read-only editor; a changed active tab; one undo/redo
restoring the complete patch set. Observe final contentsChanged text, revision monotonicity and fingerprint agreement.

Exit: library and tests build; all fixtures pass; no document save occurs. Capture the test count and logs. Stop if
applying a transaction requires clearing undo history, bypassing document identity or exposing partially patched
text to normal consumers; repair the transaction design rather than hiding the failure in a test adapter.
