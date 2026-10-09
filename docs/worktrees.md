# Checkout inventory

## Current retention policy, 2026-10-08

Keep the shared `openscad-master` checkout, one current integration checkout, and feature checkouts
needed for active editing, builds or investigations. Retain committed history as branches; historical
evidence does not require a permanent checked-out directory. Reuse suitable checkouts before creating new ones.

Retire temporary repair and verification checkouts at handoff after their owner changes are incorporated
and their evidence is secured. Before removal, inspect current usage, tracked/untracked/ignored files and
submodules; preserve unique files and any detached HEAD. Keep required build dependencies and packaged
releases. Do not remove an occupied checkout or discard changes. Recreate retired checkouts only when needed.

The user approved retirement of 21 reviewed checkouts on 2026-10-08, reducing the shared source repository
from 44 worktrees to 23. Branches remain intact. The exact paths, heads, recovery reference, verified local-file
archives and removal results are in the [retirement record](../../runs/20261008-worktree-retirement/report.md).

Retired groups:

- Integrations `wt-scadmaxx-20260930`, `wt-scadmaxx-20261001`, `wt-scadmaxx-20261002`,
  `wt-scadmaxx-20261004`, and `wt-scadmaxx-20261005`.
- `wt-openscad-readme-baseline` and `wt-openscad-readme-captures`.
- The anchors, insertion and semantic `*-composition-check` worktrees, plus
  `wt-openscad-navigation-annotations-check` and `wt-openscad-oep8-customizer-check`.
- `wt-openscad-background-native-repair`, `wt-openscad-clipping-native-repair`, and
  `wt-openscad-insertion-native-repair`; all three repair heads are merged into their owner branches.
- `wt-openscad-fix-windows-unicode`, `wt-openscad-issue-5425-path-after-2024-10-28`,
  `wt-openscad-pr-6776-dynamic-dark-mode-switching`, both PR 6871 worktrees, and
  `wt-openscad-pr-6999-customizer-header-text-contrast`.

Retained: `openscad-master`, `wt-scadmaxx-20261006`, the 18 maintained feature/PR owner checkouts,
`wt-openscad-edit-evaluation-performance`, `wt-openscad-background-consumer-check`, and
`wt-openscad-native-consumer-repair`. The two current verification checkouts remain useful until their
pending work is incorporated and validated in the full integration. The separate `openscad-6991` clone
and its shared vcpkg packages are outside this retirement and remain in place.

Use `git worktree list` for live paths and inspect current Git status before use. The sections below are
historical observations; their old "preserve" wording does not override this approved retirement.

## Historical observations

New on 2026-10-07: `D:/openscad/wt-openscad-geometry-bounds`, branch `feature/geometry-bounds`,
created from the shared `openscad-master` clone at accepted OEP8 #6081 head
`07b22af25704af0db39959773751fb5c6e4debbe`. Submodules are initialized. The feature now has a local
uncommitted implementation; no build, validation or promotion is claimed. See its
[exploration](../.plans/3_done/2026-10-07_geometry-bounds/1_exploration.md).

Current ancestry and source revisions are in [maintained feature ancestry](feature-ancestry.md) and
[DEPENDENCIES.json](../experimental/DEPENDENCIES.json). Historical inventory entries below retain earlier evidence.

The current integrated source is `wt-scadmaxx-20261006`, branch `scadmaxx-20261006`, at
`569220a50377c705a4c3af5cc21fd106b2e91662`. It includes all 19 frozen entries from
`runs/20261006-scadmaxx-all-features`, on upstream `c0ac8289f1c9db6f70891da5df3b4085b7eaf8b6`.
Its build uses `scadmaxx.exe`/`scadmaxx.com`; see that run's report for current acceptance
and delivery evidence. The older integration branches remain as historical checkpoints; their checkouts
were retired on 2026-10-08.
Recheck live status before using any checkout.

The historical records below describe their observation dates, not current Git status.
On 2026-10-05 the user requested committing and privately pushing all source work.
Owner and previously unpromoted experiment branches were retained in the Dropbox bare
repository; [promotion record](../experimental/promotion-20261005.md) and the preflight
inventory in `runs/20261005-scadmaxx-updated` identify the actual heads. Experiments outside
the selected stack remain excluded. Generated Clipper2 metadata and Python caches are not
source changes and were not committed.

For new integration worktrees, use `wt-scadmaxx-YYYYMMDD` with branch `scadmaxx-YYYYMMDD`;
see the [creation-date naming rule](git-layout.md#integration-branch-and-worktree-names).
The two integration worktrees were renamed on 2026-10-02; see [migration details](layout-migration.md).

Observed locally on 2026-09-30. Recheck Git status and worktree ownership before every use; this is not live state.
Remotes renamed on 2026-10-02: `openscad-master` uses local `origin = E:/Dropbox/bare_repos/openscad.git`,
`upstream = https://github.com/openscad/openscad.git` (push disabled), and explicit
`publish = https://github.com/roel-v/openscad.git`. All source branches push locally by default.
The control checkout `D:/openscad/scadmaxx` has its own origin at `E:/Dropbox/bare_repos/scadmaxx.git`.
`D:/openscad` itself is no longer a Git repository.

All nine source checkouts below were updated to include upstream master
`612e684c2cbbcdcb9a7a8307973f33fd910f9c17` on 2026-09-30. Existing local edits were restored, submodule revisions
were synchronized, and nothing was pushed. See the [update report](../../runs/20260930-worktree-update/report.md)
for resulting commits, conflict resolutions, recovery refs, and verification limits.

| Directory | Observed role / branch | Existing changes |
| --- | --- | --- |
| `wt-openscad-readme-baseline` | `codex/readme-baseline`, source `8bef263eb` (upstream `03da906b4` plus four Windows build repairs) | Isolated baseline screenshot harness for matched UI comparisons; preserves regular UI. |
| `wt-openscad-readme-captures` | `codex/readme-captures`, based on integrated source `bcf48145d9ebc7ffdcde0414ddde38ceb62f0b6a` | Reusable native Qt documentation capture harness; keep separate from feature integrations and releases. Runner: `experimental/scripts/Capture-Readme.ps1`. |
| `wt-openscad-http-agent-server` | `codex/http-agent-server`, head `498c4774d26e7235fbc4cbb9b34f56afb39ca645` | Seven phases committed; private origin verified; annotations/navigation prerequisite boundary `85829fa71870c4aa6945d3cd4abbc932faeab392`; [handoff](../.plans/3_done/2026-10-01_http-agent-server/5_post-implementation-notes.md). Preserve validation build and excluded generated files. |
| `openscad-master` | Main checkout, `master`, updated HEAD `612e684c2cbbcdcb9a7a8307973f33fd910f9c17` | Clean; matched upstream master at final verification |
| `wt-openscad-fix-windows-unicode` | `fix/windows-unicode-filenames`, base `31b1430530c295c4b24662b2d5a4b989bbbabc7d` | Focused Unicode CLI filename repair based on the existing experimental composition; shared vcpkg; evidence in `runs/20261001-unicode-filename-fix/` |
| `wt-openscad-ui-visual-polish` | `codex/ui-visual-polish`, HEAD `8f5b3ae47`, base `464e25dad0c01af5488375c15aa6734190531eb5` | All four UI features accepted as done on 2026-10-02; committed head verified at private origin. Uncommitted measurement/help/icon follow-ups are preserved; see handoff. UI-only delta after `be352f279`, depending on selected #6776. [Final audit/handoff](../.plans/3_done/2026-10-01_ui-preferences-dialog-polish/5_post-implementation-notes.md); future work deferred to a larger fixup pass |
| `wt-openscad-navigation-cube` | `feature/navigation-cube`, head `c54886b822ed39ff91369c335472788f106e2c50` | Six phases committed; private origin verified; runnable local dev build. [Evidence](../.plans/3_done/2026-10-01_navigation-cube/5_post-implementation-notes.md). Preserve checkout and build. |
| `wt-scadmaxx-20260930` | `scadmaxx-20260930`, HEAD `31b1430530c295c4b24662b2d5a4b989bbbabc7d` | Four baseline repair commits, then #6878 and #6776; shared-dependency rebuild/package passed; current evidence and limits in `runs/20261001-shared-rebuild/` |
| `wt-scadmaxx-20261001` | `scadmaxx-20261001`, HEAD `0a1df09ea9d1e278606434ce254671001c468278` at migration | Baseline repairs and #6878/#6776 integrated; local feature integrations remain pending. Preserve frozen run `20261001-scadmaxx-all-features`; see migration notes before resuming builds. |
| `wt-openscad-annotations` | `feature/annotations`, created from upstream master `612e684c2cbbcdcb9a7a8307973f33fd910f9c17` on 2026-09-30 | Six phase commits through `d670fad09`; private origin verified; ready for integration. Existing Clipper2 generated-header dirtiness is excluded; no submodule revision changed |
| `wt-openscad-pr-6642-dynamic-parameter-changes` | `codex/pr6642`, head `8ea442737` retained privately | OEP8-compatible annotation syntax ready; existing group-visibility GUI edits remain excluded |
| `wt-openscad-oep8-customizer-check` | `codex/oep8-customizer-check`, head `ae5e50d7a` retained privately | Tested OEP8a #6081 plus fixed-key Customizer syntax and Windows repairs; evidence in `runs/20261002-oep8-customizer`; not a selected aggregate source |
| `wt-openscad-pr-6776-dynamic-dark-mode-switching` | `codex/pr-6776-dynamic-dark-mode-switching` | Modified GroupWidget.cc/.h |
| `wt-openscad-pr-6871-msvc-build-and-compilation-fixes` | `codex/pr6871-msvc` | Modified core/utility files and dirty Clipper2 submodule; several build directories |
| `wt-openscad-pr-6871-msvc-build-baseline` | Detached updated baseline at `7887eb609dc03b8b4dca69cc86a264d30ac7673d` | Dirty Clipper2 submodule retained; original baseline has a recovery ref |
| `wt-openscad-pr-6999-customizer-header-text-contrast` | `codex/fix-customizer-header-contrast` | Modified GroupWidget.cc/.h |
| `wt-openscad-issue-5425-path-after-2024-10-28` | `codex/issue-5425-canonical-path` | Untracked reproduction script and SCAD fixtures |
| `openscad-6991` | Separate checkout with upstream as `origin`, user fork as `fork` | Modified GroupWidget.cc/.h; existing local plan |

The existing Customizer investigation is at
`openscad-6991/.plans/2_in-progress/2026-09-02_customizer-theme-behavior/1_exploration.md`.
Read it when advancing the Customizer work. Preserve its local-only planning scope and distinguish its historical
repository references from current state. Do not merge its changes with the similar worktree without comparison.

The HTTP agent-server checkout now contains the validated, privately retained
[v1-only follow-up](../.plans/3_done/2026-10-02_agent-api-v1-only/5_post-implementation-notes.md).
Its committed head is `991bb09aee1c5d3f432b4e4352ff96254821b4b5`; the table above records the previous baseline.
The [direct-HTTP follow-up](../.plans/3_done/2026-10-02_agent-direct-http/5_post-implementation-notes.md)
is validated and retained privately at `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`; selected-source readiness is true.
Preserve its edits and validation outputs.

The `OpenSCAD-*` directories and `PythonSCAD` contain installed/extracted applications, not registered worktrees of
`openscad-master`. Dependency and application directories are not available scratch space.

For new worktrees, follow the [standard clone and worktree workflow](workspace.md#standard-clone-and-worktree-workflow).
Use `openscad-master` as the shared repository and create the separate checkout alongside it under `D:/openscad`.
Inspect existing worktrees first and reuse only an available, suitable checkout. Record the actual path here.
Preserve existing independent clones and worktrees; do not rename or migrate them merely to match this convention.

- Navigation/annotations verification: `wt-openscad-navigation-annotations-check`, branch
  `codex/navigation-annotations-check`, merge `d16b00019` (navigation `c54886b82`, annotations `d670fad09`).
  Native annotation tests pass. Separate verification checkout, not a selected distribution. Preserve it.

## New-feature implementation worktrees, 2026-10-03

The user requested features 01, 02 and 15. Each has a separate branch and checkout; implementation is local,
without promotion or an enabled-stack change. Preserve these occupied worktrees and their verification outputs.

| Directory | Branch / recorded base | Ownership |
| --- | --- | --- |
| `wt-scadmaxx-agent-skill-workflows` | Control repo `feature/agent-skill-workflows`, base `a05b64c17a2e0b95fbeb44fe6a5cdbc7c3979a8c` | Feature 01 skill and frozen companion build/delivery. Existing skill/script edits were copied from the primary controls and recorded under `runs/20261003-agent-skill-workflows/input`; primary files are preserved. |
| `wt-openscad-source-editing-foundation` | Source repo `feature/source-editing-foundation`, base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1` | Feature 02, on the retained HTTP/annotation/navigation prerequisite composition. |
| `wt-openscad-geometry-services` | Source repo `feature/geometry-services`, upstream base `31f27b7522af858ebabed764e67ecc10d9e27add` | Feature 15 strict geometry measurements and sections. Separate repair inputs and checks are recorded under `runs/20261003-geometry-services`. |

Feature source remains uncommitted until a commit is explicitly requested. Verification records include source
patches/hashes so a base SHA alone is never presented as the identity of an edited build. Final application
composition and real-release companion acceptance require their own requested build.

Feature 03 is locally complete in `wt-openscad-selection-model-inspector`, branch `feature/selection-model-inspector`,
based on the retained HTTP/annotation/navigation composition `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`.
Its phase records and separate repair inputs are under `runs/20261003-selection-model-inspector`.
Preserve this occupied worktree; 02/15 source changes are excluded. The later navigation selected head remains
a separately recorded composition obligation. Its final feature patch is frozen in the run's `final-feature.patch`
(`fc9f0e8da7fa019447700bee498b09a689f00152d8ae965a106341a0569290bb`), with source/API and native/DPI verification
in the plan's completion notes. No commits/promotion. The remaining queue for this chat is 05, 06, 14, 04.

Feature 05 is locally complete in `wt-openscad-vim-editor-mode`, branch `feature/vim-editor-mode`,
HEAD/base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Its working prerequisite input adds the
verified feature 02 patch and selected shortcuts PR #6878, recorded separately from the base SHA.
Pinned Geany vimode source, port evidence and build outputs are under `runs/20261004-vim-editor-mode`.
Preserve this occupied checkout. No feature commits or stack promotion are authorized. The final feature patch
is `runs/20261004-vim-editor-mode/final-v2-feature.patch`, SHA256
`05946cc5b49ba36b979fe556298299213298e360a82408c936a05c7f5955c724`; the matching source, runtime and
passing native/restart evidence are recorded in the plan's completion notes. Remaining queue: 06, 14, 04.

Feature 06 is locally complete in `wt-openscad-source-geometry-provenance`, branch `feature/source-geometry-provenance`,
base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. The verified 02/03 patches and pinned OEP8/Customizer parser
inputs are its prerequisites. Run evidence is under `runs/20261004-source-geometry-provenance`.
Preserve this occupied checkout. No feature commits or stack promotion are authorized.
Its final feature patch is `runs/20261004-source-geometry-provenance/final-v2-feature.patch`, SHA256
`dfc078d2b428df12e5225fa514bd0c6c9d09f45c458a5cbd8f7545032c90ca6c`; matching source/runtime and passing
native/DPI evidence are recorded in its completion notes. Remaining queue: 14, then 04.

Feature 14 is locally complete in `wt-openscad-design-object-persistence`, branch `feature/design-object-persistence`,
base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. It uses verified 02/03 and pinned OEP8/Customizer inputs,
without a dependency on 06 or downstream clipping/semantic/drawing features. Run evidence is under
`runs/20261004-design-object-persistence`. Preserve this occupied checkout. No commits or promotion are authorized.
Final feature patch: `1eff9db907b673fd4971b5f8338a433931f242edddb3ca8add5fae1d0696d598`;
complete input `56275040c8fde09076ce5ae8510927d5845cf5f882ba27cab5142a59f4ec6c9a`.
Matching source, native/DPI, undo/conflict and extracted-runtime checks are recorded in its completion notes.
Remaining queue: 04.

Feature 04 is locally complete in `wt-openscad-live-clipping-sections`, branch `feature/live-clipping-sections`,
base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`, with the verified 03/14 working closure above.
Run: `runs/20261004-live-clipping-sections`. Preserve this occupied checkout. It has no 06/07/15 dependency;
no feature commits or promotion are authorized. This is the final queue entry for the current chat.

Queue 03 → 05 → 06 → 14 → 04 is locally complete. Feature 04's final patch is `cf1245b8dbd1f02aa16173265610b55645192c57fe5e49650b69d34286c4898e`;
verification `a6984899c4e260cfae6bf906187249d45284c304bb46153c9f038adf66addf76`, with extracted native/DPI/runtime evidence in its completion notes.
No source commits, promotion, stack changes or integrated release were performed.

Feature 11 is locally complete in `wt-openscad-component-provider-adapters`, branch
`feature/component-provider-adapters`, frozen upstream base `9899c745e47dbf0f48b3ca23562eea31e66f9b82`.
Run evidence: `runs/20261004-component-providers`. Its source changes and Windows repairs remain uncommitted;
the repair inputs are retained separately in the run. This checkout belongs to the 11 → 07 → 08 → 12 implementation
queue. Preserve it and its build outputs. No promotion or selected-stack change is authorized.

Its feature-only patch is `79a0cc3aad41a4d2da9884324e4b2cb0818a495c32656c709d98fd070550d0f5`, with exact source,
21 focused tests and extracted package evidence in the completion notes under `.plans/3_done`.

Feature 07 is locally complete in `wt-openscad-semantic-model-hierarchy`, branch `feature/semantic-model-hierarchy`.
The intentionally retained prerequisite base is `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`, plus the verified 03/02,
OEP8/Customizer closure and separate 06/14 owner deltas. Source composition is recorded in
`runs/20261004-semantic-hierarchy`; prerequisite patch SHA-256
`386e30092a30f76a469e04e94cebe91ab012dfe25e4977ff3d1ba8aaba46185f`.
Its feature-only patch is `555f4cc75b97856c0073a2f63cc2e8416d62e18991c0b03a1a30131be8c38383`, complete input
`7da00d78d6886e7d984067bdcaf01f5363bd674d42d5ac6cf8b05c0c37aff904`, with minimal/extracted/DPI and real 04/05
composition acceptance in `.plans/3_done/2026-10-03_07_semantic-model-hierarchy/5_post-implementation-notes.md`.
This occupied checkout is preserved. The 11 → 07 → 08 → 12 queue is locally complete; source remains uncommitted.

`wt-openscad-semantic-composition-check`, branch `codex/semantic-composition-check`, is an isolated verification
checkout for 07 with the retained 04/05 features and selected #6878 shortcut prerequisite. Its base is
`6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`; source inputs and overlap resolutions belong to
`runs/20261004-semantic-hierarchy/composition-check`. It is not a selected build or release. Preserve owner worktrees.

`wt-openscad-anchors-attachments`, branch `feature/anchors-attachments`, is locally complete for feature 08.
Its retained base is `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`; the exact 07 closure and separately tested
generic owner refinements are retained in `runs/20261004-anchors-attachments`. Feature patch:
`474b690a175d2ea4eb6d6e6c096968494e1c76d3f96809055130c5ce92736676`; complete input:
`61a07718bbca47e5ec09270b4b0ca9db49dd03a75e5898dc3fe1d0311e5a926e`. Native, DPI, extracted-runtime and real
library acceptance are recorded in its `.plans/3_done` completion notes. Preserve this occupied checkout.

`wt-openscad-anchors-composition-check`, branch `codex/anchors-composition-check`, verifies 08 with the actual
04/05 features and selected #6878. Its source and acceptance evidence belong to
`runs/20261004-anchors-attachments/composition-check`. It is separate from the minimal feature handoff and selected
distribution. Preserve it and the earlier owner worktrees.

`wt-openscad-contextual-insertion`, branch `feature/contextual-insertion`, is locally complete for feature 12.
Retained base: `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`, plus frozen 08 complete input, 11 feature delta and
#6878. Run records: `runs/20261004-contextual-insertion`. Generic 03 sealed-input/draft-display and 07 ownership
refinements are tested and frozen separately. All six phases pass, including isolated preview and guarded Commit.
The final source is bound to feature patch `78a2eea6c88d81be251946efd412a81243df3c0d05fe92d04a917089ab930191` and
complete input `41cf37d49217ac09de4140664880f6d39cbd32a7987b31e6843e816c7a8cc1c1`. Evidence includes 295 unit cases,
155 extracted native rows, 31 insertion rows at each of 150%/200%, and 16 real catalog checks through both launchers.
See [the completion notes](../.plans/3_done/2026-10-03_12_contextual-insertion/5_post-implementation-notes.md).
Preserve the local uncommitted source and runtime; no promotion, selected-stack change or integrated release occurred.

`wt-openscad-insertion-composition-check`, branch `codex/insertion-composition-check`, is the separate actual 04/05
verification checkout for feature 12, at base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Its final uncommitted source
is independently replayed and recorded in `runs/20261004-contextual-insertion/composition-check`. All 66 affected unit
cases and 15 native classes / 184 rows pass, including actual clipping/visibility restoration and Vim typing Undo
boundaries. Preserve this occupied checkout and all original owner worktrees.

## Edit-evaluation performance exploration, 2026-10-04

`wt-openscad-edit-evaluation-performance`, branch `feature/edit-evaluation-performance`, is dedicated to faster
source/parameter reevaluation. Fresh upstream base: `9899c745e47dbf0f48b3ca23562eea31e66f9b82`; all six submodules
are initialized at their recorded revisions. The standalone benchmark fixtures are under
`tests/data/scad/benchmarks/edit-evaluation/`; phases 1/2/3 add interpreter changes and language regressions
described below. Preserve this occupied worktree.

The plan is `.plans/2_in-progress/2026-10-04_edit-evaluation-performance/1_exploration.md`; runner and case catalog
are under `tools/evaluation-benchmark`, with evidence in `runs/20261004-edit-evaluation-performance` (container
relative). Full support and an explicitly selected mode excluding exactly Hull/Minkowski are separate research
tracks. Phase 2 replaces the built-in sin/cos shortcut with lazy entry contexts for every function call;
no restricted backend exists. Its source snapshots, matching comparison runtimes, semantic/mesh checks and
timings are in `runs/20261004-evaluation-general-contexts`. Earlier phase-1 builds and isolated Windows repairs
remain in `runs/20261004-evaluation-math-fastpath`. The initial corpus run used the older integrated SCADMaxx binary,
recorded separately. Source remains uncommitted; there is no promotion or selected-stack change.

Phase 3 transfers the already-bound ordinary parameter map into a fresh function body while preserving special
variable merging and heap accounting. It retains phase 2 and adds a native test plus two SCAD regressions.
Evidence and frozen source/runtimes are in `runs/20261004-evaluation-parameter-transfer`. Panel language time
improves 6.79% against phase 2; repeated-update medians improve 3.69-8.66%, with substantial sample variation.
Brackets show no useful gain. All 128 echo comparisons and 306 mesh comparisons match the previous runtime;
known baseline failures remain documented. Preserve this local uncommitted experiment and its earlier inputs.

The #4654 upstream-speedup composition is now benchmarked in the same performance working tree. Four applicable
PRs are ported; three are already represented by current upstream code. Original phase-3 source/impact and the
combined patch are frozen in `runs/20261004-evaluation-upstream-speedups`. Combined patch SHA256:
`06716fa6f704c208da8fe3361d4dd934b863cc71584dceccf5243ac240511daf`; executable SHA256:
`2809e523cdf6460a962c34fbb1a2121d9ff23ee264ed5269880220318333f443`. All 123 native cases and 129 language
comparisons pass their recorded expectations; 8,000 corpus executions and 3,210 output checks are retained in
`runs/20261004-realworld-upstream-speedups`. Typical-model gains remain near zero; evaluator-heavy examples show
larger gains, while incremental upstream attribution is limited by timing variation. Read that run's `results.md`.
The source stays uncommitted on the same base. Preserve the worktree; no promotion or selected-stack change.

## Background evaluation source implementation, 2026-10-07

Current forward-integration checkpoint: feature `f4b6d0c3d51c672df4dc1525eb912f7565692167` is committed,
with extracted owner contracts and normal downstream merges. `wt-openscad-background-consumer-check`, branch
`codex/background-consumer-check`, is the isolated insertion/hierarchy/anchor/cross-section verification
composition. Source/build evidence belongs to `runs/20261007-background-forward-integration`; it is not a
release input and must never be merged back into owners. Preserve existing owner branding/provenance edits.
The following source-only description is historical; use the current run report and manifests for exact heads.

`wt-openscad-background-model-evaluation`, branch `feature/background-model-evaluation`, is occupied by the initial
background evaluator implementation. HEAD is Inspector `b93c9c219198630a2fde3822f2b90c29d88d9180`, with a resolved,
staged normal merge of Customizer `13697aa98f18e1d1b26187d2cf5a253e8b6dce07` still pending. Feature changes are
unstaged/untracked; preserve the merge index and new files. All six submodules are initialized at recorded revisions.

Initial source-only evidence is in `runs/20261007-background-evaluation`. Subsequent Windows build, focused native
tests, all 94 unit cases and real-model benchmark evidence are in `runs/20261007-background-integration-readiness`.
The corrected heartbeat measurement exposes an initial Customizer construction pause above the target; strict-action
admission and downstream owner composition remain unfinished. No commit, push or promotion was made. Stack row 24 is
selected but its source remains `ready: false`. The feature remains in progress; remaining work and limits are in
[the handoff](../.plans/2_in-progress/2026-10-07_background-model-evaluation/5_post-implementation-notes.md).

## Native integration repair worktrees, 2026-10-08

The background-evaluation source-only entry above is historical. Its implementation and native repairs are
committed locally and merged forward through persistence, hierarchy, anchors, insertion and clipping.
Current owner heads and validation are recorded in
[`runs/20261008-native-integration-repairs`](../../runs/20261008-native-integration-repairs/report.md).
Preserve these isolated repair checkouts and runtimes:

| Checkout | Branch | Role |
| --- | --- | --- |
| `wt-openscad-background-native-repair` | `repair/background-native` | Background controller and native consumer/test repairs |
| `wt-openscad-clipping-native-repair` | `repair/clipping-native` | Clipping test-provider registration repair |
| `wt-openscad-insertion-native-repair` | `repair/insertion-native` | Insertion completion and viewport gesture tests |
| `wt-openscad-native-consumer-repair` | `repair/native-consumer-check` | Frozen combined verification; never merge back into owners |

The separate checkouts avoided concurrent use of `wt-openscad-background-consumer-check`. Normal owner
merges preserve pre-existing build branding and submodule changes. No push or promotion is authorized by this run.
