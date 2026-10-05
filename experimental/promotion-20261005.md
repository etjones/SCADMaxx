# Private promotion, 2026-10-05

The user explicitly requested committing everything, pushing to the Dropbox bare repositories,
and making a new integrated build. The source push used explicit branch refspecs, no force,
and was verified against `E:/Dropbox/bare_repos/openscad.git`. No GitHub push was made.
Inventory and full promotion hashes: `runs/20261005-scadmaxx-updated/` in the workspace container.

New owner commits separate viewport freshness/performance from the Model structure UI:

| Feature | Promoted head |
| --- | --- |
| Selection / Inspector | ced629047eaa725a319f0c5a6a3602330b033c6d |
| HTTP server | 9aa372e8fcb012d8bcfe6344483d83f3bcd4f2d0 |
| Clipping | 06d073f73720a391f5d806911a3d91a27b1ebd4e |
| Model hierarchy | 966b68b98fc21308d1fd1d40dbcb8eebeda7cc2f |
| Anchors | 56ceab74239507093067f11d078d73c12ae431c4 |
| Contextual insertion | b298c802905289b4fb94178d9127c6a8283342b7 |
| UI polish | 2217d2c7d54743c93cefb9418b208825168ddc1c |
| Navigation | 6b42cbf3f95bfe1ad2ff4b845a6dc20f4ed336fe |
| PR 6642 variant | 1dad283e17be06380f2ff6b23daca68719d1f70c |

Selected owner pins advance to these committed changes for this requested build. The three
foundation-follow-up pins, all delta bases, entry order and enabled membership are unchanged.
At preparation, registry `validatedHead` retained the prior full-feature acceptance while
`promotedHead` identified the new input. The fresh combined run now validates the nine
promoted heads above; `validatedHead` has advanced to match. Foundation pins are unchanged.

The performance fixes passed focused and native checks in `runs/20261005-viewport-performance`.
The Model structure followups passed the recorded unit/native checks in
`runs/20261005-model-structure-init` and `runs/20261005-component-parameters-inspector`.
The previous composition plus these changes is retained at
`0a53d34ce3ccb45fe0950f52b51f4d142cdc7149`; it is verification evidence, not a fresh baseline.

For replay, follow [viewport freshness](repairs/viewport-redraw-freshness.md) when composing
later sealed-input foundations. Preserve their hypothetical-pixel guards. The Inspector
`addPanel` prerequisite appears in both selection and hierarchy owner deltas; keep one copy.
Preserve the integrated foreign-presentation ownership guard and its native regression.
Component parameters now belong to Inspector; the global Customizer is independent.

Fresh integration: `wt-scadmaxx-20261005`, branch `scadmaxx-20261005`, final source
`dcd732fefa0aef5b12d4e5d0a2097223caf32726`, on upstream
`c0ac8289f1c9db6f70891da5df3b4085b7eaf8b6`. All 22 entry checkpoints passed. Full native
validation passed 188 checks; the seven DPI suites passed 116 checks at each of 150%
and 200%. The anchor test needed a separate [projection snapshot repair](repairs/anchor-pick-frame-test.md)
because opening Inspector changes the viewport after picking. Its original tolerance
and all production behavior remain unchanged. The final source archive includes that repair.
See [run report](../../runs/20261005-scadmaxx-all-features/report.md) for exact runtimes,
test-only patch identity, delivery verification and retained superseded candidate.

Previously committed experiments and verification branches were also retained privately,
including edit-evaluation performance. They remain outside the selected stack. Generated
Clipper2 line-ending noise and Python caches are intentionally uncommitted. The independent
legacy `openscad-6991` clone has no new changes and is not a selected private source.
