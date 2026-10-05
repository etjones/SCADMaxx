# Phase 5: Atomic Commit, Undo and stale-state handling

Requirements: IN08-10, IN14, IN16, IN18. Read 3_overall-plan.md and both source/preview contracts first.

1. Implement the six-step Commit algorithm in preview-contract.md. Bind proof to candidate bytes, source/configuration,
   library/catalog/profile identities, explicit target editor and shared scope. No event-loop yield before 02 apply.
2. Adapt the complete patch list to one SourceEditing::EditRequest. Generated references are source only; do not
   combine a separate 14 promotion with a second edit group. 02 supplies its synchronous pre-edit boundary.
3. End draft display only after successful apply, request ordinary root reevaluation, and distinguish source commit
   success from a later evaluation failure. Do not install worker output as the live scene.
4. Wire source/HTTP edits, dependency revision/close/path changes, catalog reload, tab/window teardown and ordinary
   compile actions to cancellation. Cache invalidation is not permission to reuse a stale hit.
5. Add real-editor Undo/Redo and included-document tests; normal Save remains separate.

Checks: insertion-commit and native insertion selector. Commit plus one Undo restores exact pre-insertion bytes
including includes/helpers/wrappers/references, preserving preceding undo history; Redo recreates the candidate.
Capture/prove no disk changes until Save. Cancel, bad preview, failed currentness check and read-only target add no
undo entry. Post-commit evaluation failure keeps source plus one Undo, without retry or hidden rollback.
Edit another included buffer, switch tabs, change a same-version library file, change library search order, reload a
catalog or deliver an HTTP source patch while preview is pending/Ready: no stale mutation in any document.
Explicit included target commits exactly that open document while root evaluation uses its candidate content.
Verify normal 02/14 lifecycle handling removes/restores generated declarations without stale UI drafts.
Composition with 05: an active Vim insert group closes before the insertion transaction; one Undo cannot consume
both the preexisting Vim typing and the full new insertion.

Exit: source/preview proof, one-Undo semantics and lifecycle are demonstrated in native editor tests. Any partial
mutation, wrong-document effect or candidate/live-result identity confusion is a stop condition.

Use the overview verification-contract.md with the actual isolated build path: build OpenSCADExe and
OpenSCADUnitTests, run ctest -N, then the named CTest labels. Native cases use the registered GUI harness selector.
No zero-test result counts as passing; retain commands, discovery and logs in the feature run directory.
