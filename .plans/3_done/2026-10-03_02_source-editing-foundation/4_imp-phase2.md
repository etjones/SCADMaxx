# Phase 2: source file conflict protection

Requirements: SE-06 through SE-10. Input: phase 1 and existing TabManager/SavedViews save behavior.

1. Add DiskSourceState and deterministic QFile/QTemporaryDir tests. Compare existence, identity/readability and
   raw-byte hashes; test equal-length files whose timestamp is restored, deletion, recreation and Unicode paths.
2. Record the baseline during successful source reads/reloads. Replace source conflict decisions based only on
   `autoReloadId` timestamp/size with the shared snapshot check. Keep UI reload prompting and dirty-buffer protection;
   do not automatically reload a dirty document or claim an unreadable file has no changes.
3. Add preflight in `TabManager::saveDocument` before any source/metadata writes. Connect Cancel, Save As and explicit
   overwrite to the concrete destination snapshot. Recheck immediately before QSaveFile commit. Use the same helper
   in ordinary Save, Save As and Save a Copy; preserve each operation's path/adoption semantics.
4. Keep SavedViews' callback ordering and annotation save behavior. Test that a source preflight failure invokes
   neither source nor companion writes. Test source success followed by a simulated companion failure: source stays
   saved, the failed companion stays dirty, and the message identifies the partial result.
5. Run `source-editing` and new `source-save-conflicts` tagged tests. Re-run only affected existing save/annotation
   checks; do not use a complete application packaging run to validate this phase.

Expected results: cancellation preserves all bytes; successful Save updates the baseline; Copy leaves current editor
state unchanged; a disk change after overwrite approval invalidates that approval; failed QSaveFile commit leaves
the original intact. Use an injected test I/O failure at the helper boundary rather than changing permissions on
user files. Do not add production environment-variable backdoors solely for tests.

Exit: the save/reload paths use one content-aware conflict decision, all fixtures pass, and source/companion partial
success remains accurately reported. No persistence format changes, new HTTP write endpoints or cross-file patching.
