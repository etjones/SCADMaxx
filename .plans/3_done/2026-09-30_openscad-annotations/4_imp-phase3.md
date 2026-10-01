# Phase 3: editor lifecycle and undo

- [x] Attach store to document creation/open; route dirty indicators and save/close decisions.
- [x] Implement save/copy/as/backup integration, including annotation-only and partial failure behavior.
- [x] Add native container undo commands; keep source dirtiness separate from annotation dirtiness.
- [x] Clear command history on source reload without clearing records or annotation dirty state.
- [x] Native documentLifecycle test passes: undo interleaving, read-only mode, save timestamp, reload retention/history reset, Save As, saved empty store.
- [x] Exercise timed automatic reload, native copy dialog and matching annotation backups in final integration tests.

Exit: saved/unsaved annotations survive all normal document paths and source reload does not overwrite evidence.
