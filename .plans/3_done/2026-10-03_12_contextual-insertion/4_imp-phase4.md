# Phase 4: Palette, controls and draft presentation

Requirements: IN01-06, IN13-17. Read 3_overall-plan.md and both source/preview contracts first.

1. Register insertion actions and controller lifetime in MainWindow. Build searchable palette from registry metadata,
   disabled availability reasons and type-generated parameter controls. Keep config persistence in existing settings.
2. Implement pick-first/Shift-A, explicit eligible source target/shared scope, and destination/operation/mode display.
   Use a session focus group spanning viewport/palette/panel. Missing provenance does not create a guessed target.
3. Implement numeric offsets/spin and G/R/F through the shared frame model. Use captured plane/camera rays for drag,
   preserve navigation outside the drag, and keep focused editor/Vim inputs untouched.
4. Add ghost overlays with GL guards, 150 ms debounce, visible pending/error state and latest-candidate-only delivery.
   Acquire 03 draft display lease; show actual candidate mesh only through that coordinator. Suspend live hide/clip
   presentation with a clear Full insertion preview state, preserving settings for restoration.
5. Disable Commit until exact candidate success. First Enter in a focused numeric control accepts its field; viewport
   Enter activates Commit only when Ready. Escape always discards this insertion session.

Checks: insertion-ui widget tests and TestContextualInsertion native selector OPENSCAD_INSERTION_TESTS_ONLY.
Exercise palette filtering/unavailable items, invalid numbers/enum constraints, repeated shared scopes, named anchor
choice, plane move/spin/flip numeric equivalence, parallel camera ray feedback and no near-zero-radius spin jumps.
Native GL: ghost never hit/exported, real cut visible, all affected instances shown, candidate pixels cannot become
live source selection, navigation works, camera not reset, base restores after cancel and worker error.
Native focus: panel/viewport transitions retain draft; unrelated editor/tab cancels; ordinary typing and Vim commands
do not trigger insertion shortcuts. Replacing another tool cancels exactly once; no annotation/measurement capture leak.
Run at normal DPI, 150% and 200% on the real Windows GL context, not just offscreen Qt.

Exit: the entire requested interaction works to a ready candidate with unchanged editor bytes/undo/disk. Do not
implement Commit until this state can be cancelled reliably under rapid changes and window teardown.

Use the overview verification-contract.md with the actual isolated build path: build OpenSCADExe and
OpenSCADUnitTests, run ctest -N, then the named CTest labels. Native cases use the registered GUI harness selector.
No zero-test result counts as passing; retain commands, discovery and logs in the feature run directory.
