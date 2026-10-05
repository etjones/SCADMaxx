# Current implementation state

Locally complete, all phases accepted, 2026-10-04. The 11 → 07 → 08 → 12 queue is complete.
See [final source, native/package/DPI and composition evidence](5_post-implementation-notes.md).
The earlier implementation checkpoints below are retained as history.

Source `D:/openscad/wt-openscad-anchors-attachments`, branch `feature/anchors-attachments`, retained base
`6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Run `D:/openscad/runs/20261004-anchors-attachments`.
The exact accepted 07 complete closure is replayed from SHA-256
`7da00d78d6886e7d984067bdcaf01f5363bd674d42d5ac6cf8b05c0c37aff904`, including 03/06/14, 02 and
OEP8/Customizer. All six submodules match their indexed revisions. No 04/05/09/10/11/12/13/15 implementation is included.

Preflight found two narrowly missing generic capabilities: evaluation-owned consumer data must be available to
placement passes and published in ordinary as well as semantic results; invalid consumer decoding must notify its
owner without delivering an invalid Record. The separate 07/14 follow-ups have fake-consumer unit tests and are
building on the shared Windows profile. Their verified deltas will be frozen before concrete 08 implementation.
Original owner checkouts and completed 07 handoffs remain unchanged. No commits, staging, promotion or release.
# Prerequisite acceptance and phase 1, 2026-10-04

The generic 07 result-publication/default-context, 14 consumer-rejection and native duplicate-value-proof inputs
passed their combined gates: 110 focused checks, 176 unit cases / 257 JUnit rows, native Semantic 14/14, native
Design 9/9 and four parser/import checks. The first duplicate-value regression failed and was fixed in the ordinary
object evaluator; both attempts are retained. Independent prerequisite replay produces no 08 feature changes.

Frozen complete prerequisite SHA-256: 166763303cd3988a96ab92ed6b58f12f3d637ee0cb2f5791a5fbc1ccf8bfdf6e.
Generic follow-ups remain separate from 08 and original owner worktrees remain unchanged.

Phase 1 passed 84 focused checks and four parser/import checks. Phase 2 passed all 26 reference/frame/graph/solver
checks. Phase 3 passed 117 affected checks and native TestAnchors 5/5, including GPU picking at solved positions,
hidden targets, parameter reevaluation and stale last-good publication after relation failure. Both launchers in the
extracted verification runtime passed solved CSG/STL comparisons and rejected a missing relation without usable export.

Phase 3 independently replayed feature SHA-256: b8f5b4f19444976d79789f1510bb0dc6c6a4dbcbd8da42fe77bac1a3325b5a94.
Complete working input: 5ee5472eb5d55d47f7ce2aa14470b61da7ea899b1bc5a8e1560a3747c75c39fa.
Evidence: `phase3-source-evidence.json`, `phase3-cli-v3/results.json`,
`native-Anchor-scale-1-20261004T122609425Z/TestAnchors.txt` in the run. Earlier failures are retained: a composite
wrapper assertion incorrectly claimed unique face provenance; native fixture exposure needed the established
hide/show initialization; GPU hit X/Y comparison now accounts for the sampled physical pixel. All source-invocation
links, final transform matrices, actual tip Z and normal remain asserted. First clean-PATH launch lacked deployed
DLLs; a fresh staged/extracted runtime resolved that packaging prerequisite. CSG comparisons decode matrices rather
than assuming exact printed floating-point zeroes.

Phase 4 passed two native typed bridge cases and 26 installed-launcher cases. Supported primitives, edge/corner,
cylinder end/radial, sphere, named oblique anchors, explicit reorientation and override callbacks publish ordinary
Anchor data. C++ affine frames and the implemented helper agree; actual BOSL2 attach transforms pass, including spin
and negative gap. Wrong version, missing library, unsupported descriptors and singular/ill-conditioned placement
report expected diagnostics. External BOSL2 source hashes and revision remain unchanged, and BOSL2 is not bundled.
The first CLI negative expectation used the wrong wording (open/find); its failed output is retained.
Phase 4 feature SHA-256: 5326fc6d55dd9e2a0c56169f2697f99986c444d03a0602b466bf172760d7ff35.

A separate generic 14 consumer-draft/source-field follow-up passed 26 focused checks and native Design 10/10.
It owns transient creation, validated immutable previews and promotion undo/redo, plus explicit field whitelists and
finite typed replacement literals. Frozen SHA-256: 1ca334f384c1fa79356e915fdf49fd2b92c907f76ac60f6ff3f0b2bad3b592a8.
Its first native assertion used different serializer whitespace; the corrected test also verifies native parsing,
retained previews and exact source undo/redo. This prerequisite delta is excluded from the independently replayed
08 feature patch. Original 14 source remains unchanged.

GUI authoring and final composition/package acceptance remain outstanding. Feature 12 follows
08 acceptance. No commits, promotion, stack changes or integrated release have been performed.

# Final local acceptance, 2026-10-04

All six phases are complete. Final feature patch 474b690a175d2ea4eb6d6e6c096968494e1c76d3f96809055130c5ce92736676;
complete input 61a07718bbca47e5ec09270b4b0ca9db49dd03a75e5898dc3fe1d0311e5a926e. See the completion notes and
runs/20261004-anchors-attachments/acceptance-evidence.json for source, owner follow-ups, native/package/DPI and
real clipping/Vim acceptance. The full loaded composition's one timing failure passes unchanged with the build idle.
No source index, commits, promotion, stack/readiness registry or integrated release changed.
The subsequent feature 12 acceptance completes the 11 → 07 → 08 → 12 queue.
