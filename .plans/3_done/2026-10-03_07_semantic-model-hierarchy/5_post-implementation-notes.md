# Semantic hierarchy: implementation handoff

Locally complete, 2026-10-04. All six phases and real 04/05 composition acceptance pass. No commits, push, promotion, selected-stack
changes or integrated release were requested. Source remains uncommitted; HEAD alone does not identify this build.

## Exact source and dependencies

- Source `D:/openscad/wt-openscad-semantic-model-hierarchy`, branch `feature/semantic-model-hierarchy`.
- Retained base/head `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`, matching the tested owner inputs.
- [Run evidence](../../../../runs/20261004-semantic-hierarchy/final-source-evidence.json) records actual file hashes,
  independently replayed patch layers, six submodule revisions and prerequisite/repair boundaries.
- Feature-only `final-feature.patch`, SHA-256 `555f4cc75b97856c0073a2f63cc2e8416d62e18991c0b03a1a30131be8c38383`,
  273281 bytes. Complete working input `final-complete-input.patch`, SHA-256
  `7da00d78d6886e7d984067bdcaf01f5363bd674d42d5ac6cf8b05c0c37aff904`, 931496 bytes.
- Direct inputs 03/06/14, with the existing 02/OEP8/Customizer closure. The separately frozen generic follow-ups
  cover 06 invocation linking/navigation, 03 captured jobs and worker recursion baselines, 02 context rechecks and
  the 14 unsupported-domain test fixture. Their exact hashes, replay material and tests are in `inputs/manifest.json`.
  Original owner worktrees are preserved. No 04/05/08/09/10/11/12/13/15 implementation is needed by this build.
- Six submodules remain at the indexed revisions: MCAD `1ea402208c3127ffb443931e9bb1681c191dacca`,
  Clipper2 `c7f820f6a03fa91f189b866d27bf40dfe47abaa6`, OpenCSG `9bf122715213dca05e70993dd8672fe3aa36c518`,
  manifold `0edd9d54876f3135e431575214dd6d8a72866fee`, mimalloc `30b2d9d89099bee08e9f67a1ffb3e12e7ba45227`,
  sanitizers `bcb1fc68616e9645ca5acea2992412606373ab04`. The generated Clipper version header is excluded from the feature.

## Implemented behavior and evidence

| Requirements | Implementation and executed acceptance |
| --- | --- |
| SH01–SH02 | Native definition/call annotations and strict kind/host checks; declaration-only templates, explicit Component calls. Grammar retains zero unresolved conflicts. Core grammar/declaration/evaluation tests. |
| SH03–SH05 | Finished Part roots, explicit assembly partition, rejection of cross-component operations, native scene ownership. Core partition/placement tests and desktop bracket/notch/transformed Part picks. |
| SH06 | Actual native parameter binding and winning argument origin, lexical defaults, explicit parent expressions. Core parameter/default-target tests and native distinct instance/default edits. |
| SH07–SH09 | Global/Model Customizer tabs, Selected/Definition defaults/All views, native typed controls, literal-only transactions, scope multiplicity and exact open-owner guards. Seven core source-edit cases, boolean/Unicode string/five-value vector/full-precision native checks, annotation/source undo, closed/read-only/library/tab-change checks. |
| SH10–SH14 | Escaped explicit paths, definition identity, duplicate rejection, result-bound references and owned asynchronous targets. Core identity/reference/default tests, stale delivery and window-close tests. |
| SH15–SH16 | Model tree and exact semantic selection, mask-only eyes/solo, transform/parameter inspection, fit/navigation, transient Section creation, source/definition actions. Desktop picks, Other geometry, 100 mask changes without jobs/evaluation, native tool arbitration, source and Section actions. |
| SH17 | Owned local/placed/default native target export with atomic destination commit and stale/cancellation guards. Core native format/export tests and hidden-target desktop STL export. Real clipping composition is recorded separately below. |
| SH18–SH19 | Ordinary Model/Global behavior, mixed Other geometry, library/default ownership, nested/repeated declarations. Core fixtures, native Other picks and explicit library owner edits. |
| SH20 | Minimal 03/06/14 build and independently replayed feature delta; generic extension hooks have no downstream headers. Separate optional 04/05 checkout preserves this boundary. |

Source/API documentation is `doc/semantic-model-hierarchy.md`. The native grammar and semantic collector own one
pre-publication finalization driver. `Semantic::currentScope`, ordered RAII placement registration and
`PlacementContext::insertTransform` expose generic ownership/placement without consumer types. Root truncation
which would discard a required placement correction is explicitly unsupported. Native geometry, semantic maps and
provenance consume the same finalized tree.

## Executed checks

- Windows Release CLI/GUI/unit build passes with experimental features and Manifold Minkowski enabled.
- 106 focused CTest cases pass, with discovery verified; four object/import/text-metrics parser regressions pass.
- Full unit discovery has 172 unique cases. The passing full-process JUnit report has 253 parameterized rows,
  zero failures/errors. Earlier failing fixture reports remain retained and are not counted as passes.
- Semantic desktop 14/14 passes. Independent Selection 18/18, Provenance 9/9 and Design 9/9 runs pass.
- Fresh extracted runtime full desktop run: all ten suite reports pass, 98 reported rows, zero failures/skips,
  including the real HTTP workflow. The first extraction attempt lacked that workflow's environment and its one
  setup skip is preserved separately. Semantic extracted runs at 150% and 200% scale each pass 14/14.
- Both extracted `.exe` and `.com` pass all seven Unicode filename/include/use cases with clean PATH. Each renders
  an annotated Part/Component fixture through Manifold to bounds [42,10,3]. Installed shader hashes match source.
- Portable verification archive SHA-256 `2965a5e5a6b72f92935541cdc85bdfcc79923cdf99484bf7c13cc996f6101541`.
  This is development verification staging, not a promoted distribution.

The installed toolchain remains MSVC 14.51.36231, SDK 10.0.26100.0, Qt 6.11.1/QScintilla 2.14.1 and the shared vcpkg
tree. GL evidence reports OpenGL 4.6.0 NVIDIA 616.92, GeForce RTX 3070 Ti, QOpenGLWidget with 24-bit depth and 8-bit
stencil. Native transformed semantic checks exercise Manifold and CGAL. No dependency installations were performed.

## Optional composition and remaining delivery obligations

`wt-openscad-semantic-composition-check`, branch `codex/semantic-composition-check`, is a separate verification
checkout on the same base. Its [locked inputs and overlap resolutions](../../../../runs/20261004-semantic-hierarchy/composition-check/inputs.json)
combine the exact 07 complete input, selected #6878 adaptation, 04 feature delta and 05 feature delta. Additive source
registrations and destructor order are retained explicitly. Verification-only native checks live solely there.
The combined Release build and 130 focused cases pass. The full combined native run passes all twelve suites,
128 reported rows with zero failures/skips: semantic 17, clipping 14 and Vim 13, alongside the established desktop
regressions. Three verification-only semantic cases exercise the clipped bracket pair/hollow Part, exact retained
rear-surface paths, mask/clip toggles without new jobs, hidden/clipped export retaining original [45,10,3] bounds,
Vim insertion plus a scoped edit as separate undo/redo steps, and concurrent native root-mesh/semantic-target jobs
cancelled after a source change and window close. Their independently replayed delta has SHA-256
`2ee698c398ab55ddc8de51d4a142de53b7a5d48e7693eb53a023c9d478f73e4f`; it is excluded from the feature-only input.

The first combined full run exposed three older 04 fixture failures: reserved priority 100 and a wait which exited
at an intermediate asynchronous state. A separate 04 test-only follow-up uses unique priority 200 and waits for actual
Ready, SHA-256 `afe589caa9885a1af2fbe88adce2a26bd04004e15d2e8c9bf83a78723584ca76`. Both its independent application
and all 14 clipping desktop checks pass. No 04 product code or original owner checkout changed. The failed run remains
retained. Future compositions need this follow-up; it adds no 07 types or dependency to 04.

[Final verification manifest](../../../../runs/20261004-semantic-hierarchy/verification-evidence.json), SHA-256
`16425437e06b6f8fb1429c3d71dcf27ee93ceabee797340a48c22c41ceec7a31`, binds source, exact composition inputs,
build/test commands, native reports, extracted package and unchanged shared dependency status. No Git index entries
were staged. Generated Clipper build bytes are retained and the original version-header working file restored.

Other platforms, Qt5/headless compilation and clean-machine portability remain unverified. Semantic inspection
requires convertible 3D geometry; unsupported/empty/stale states are visible. Source edits do not bake computed
expressions or silently affect loop-shared calls. General attachment/drawing/insertion controllers remain with their
own features. A later requested integrated build must select exact input revisions and run its release acceptance.
Promotion and readiness registry changes remain a separate user decision.

## 2026-10-06 fix-forward: viewport information placement

Model structure now places the FPS/triangle information to its right with a ten-pixel logical
gap and matching top alignment. Hiding it restores the information's original upper-left
position. Placement follows overlay show/hide and relayout, with no new UI control and no
per-frame work. Existing collapse, interaction and transparency behavior is retained.

Local owner base is `966b68b98fc21308d1fd1d40dbcb8eebeda7cc2f`; the uncommitted delta, exact
hashes, submodules and combined native verification are recorded under container-relative
`runs/20261006-viewport-info-layout`. No commit, push, promotion or delivered-build replacement.

## 2026-10-06: fix forward — optional structure, quiet empty viewport

Removed the viewport initialization prompt. Plain models and absent results hide the overlay;
Inspector > Component parameters retains Add model structure, and Inspector stays hidden by default.
The FPS/triangle label returns left when the overlay hides. Creating structure restores the tree.
Owner HEAD remains 966b68b98fc21308d1fd1d40dbcb8eebeda7cc2f; changes are local and uncommitted.
Cumulative owner/verification patches, exact submodules, executable hashes and native tests are in
D:/openscad/runs/20261006-optional-model-structure. This supersedes the prior viewport-info-layout
owner patch while retaining its behavior; other pending feature-owner fixes remain separate.
No release rebuild, source promotion or readiness update occurred.
