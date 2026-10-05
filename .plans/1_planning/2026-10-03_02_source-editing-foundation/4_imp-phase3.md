# Phase 3: native integration and feature handoff

Requirements: all SE requirements, especially coherent undo/save/document identity with existing features.

1. Add a focused `TestSourceTransactions` native Qt test class under `src/guitests`, following TestTabManager's window
   fixture. Register its header/source under ENABLE_GUI_TESTS and call it from `guitests.cc` in the ordinary native
   suite. Give dialogs predictable object names; drive explicit button choices and fail a timed-out dialog test.
2. Test typing -> annotation action -> source transaction -> undo/redo in order. Test two open documents, a tab change,
   a closed captured editor and source snapshots before/after edits. Existing read-only HTTP observations must report
   the final source revision/fingerprint and reject stale guards; do not add an HTTP mutation route.
3. Test a dirty source changed externally, Cancel and Save As, saved-view persistence, annotation persistence and a
   simulated metadata failure after source success. Keep real files in a fresh temporary directory.
4. Build the GUI validation configuration with ENABLE_GUI_TESTS using the shared Windows profile/dependencies.
   Run the tagged unit checks and `scadmaxx.exe --run-all-gui-tests` with isolated test settings/output. Confirm the
   new native class actually ran. Record desktop checks separately from offscreen evidence.
5. Inspect the feature-only base-to-head diff and the intended selected composition for common editor/save conflicts.
   Record reviewed prerequisite SHAs, source changes, tests and limits in `5_post-implementation-notes.md`.

Exit: all new checks and affected existing annotation/save/HTTP checks pass on the recorded source; the delta excludes
prerequisite code and unrelated work. A commit or push is performed only when authorized under the workspace rules.
If a future Vim branch is absent, record its integration test as a later composition check, not a test already passed.
