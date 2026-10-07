# Semantic targets with world-space cross sections

The 2026-10-06 integration failed one hierarchy unit test at `b72ab64a2`:
`Semantic nonrigid frames remain affine and Section consumers reject them`.
Evidence: `runs/20261006-scadmaxx-all-features/20261006T214715360Z-test-unit.xml`.

Its source fixture used Section `target` and `frame` members. The selected persistence
owner deliberately removed geometry attachments at the user's request. Those members
are now rejected, so the fixture invalidated the semantic scene before testing anything.
Do not restore the removed API or weaken unknown-member validation.

Integration repair `182c007d3` changes only `SemanticTargets_test.cc`: prepare and resolve
the nonrigid semantic target, assert its [2,3,4] scale, then resolve a separate Section
and assert its world-space origin [1,2,3] and identity orientation. This covers both
remaining behaviors without bringing back attachment compatibility. Check current
owner revisions before reapplying; the obsolete fixture may already be updated.

The first focused repair passed Configure, Build and Test at `182c007d3`, including
684735 assertions with zero failures/errors/skips. Verification:
`runs/20261006-scadmaxx-all-features/logs/20261006T215057354Z-test.json`.

On 2026-10-07 the same fixture correction was made in its hierarchy owner as `e92646c22`,
then propagated by normal forward merges. The owner full suite passes 276 cases; evidence is
`runs/20261007-owner-evaluation-performance/hierarchy-full-unit.xml`. Future integrations inherit
the owner correction and should not need a separate repair. No production behavior changed.
