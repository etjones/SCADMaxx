# Background evaluation integration-readiness handoff

Latest checkpoint, 2026-10-08: native integration blockers are repaired and committed locally. The full combined
GUI sequence passes **200 checks across 15 classes**, with no failures or skips. Repairs are forward-merged
through background evaluation, persistence, hierarchy, anchors, insertion and clipping; the stack pins are updated.
See [the current repair report](../../../../runs/20261008-native-integration-repairs/report.md) for exact owner,
build and runtime identities. No push/promotion occurred. The feature remains in progress for the separate
Customizer responsiveness, strict-action admission and lifecycle/configuration acceptance work below.

## Forward-integration checkpoint, 2026-10-07

The user manually tested the standalone runtime and approved continuing local integration/commits.
The feature is now committed at `f4b6d0c3d51c672df4dc1525eb912f7565692167`, after its real Customizer
prerequisite merge and extracted Inspector/Customizer owner contracts. Normal forward merges now reach
persistence, hierarchy, cross sections, anchors and insertion. Worker publication preserves design objects,
syntax/provenance and semantic records; captured actions reject invalid parameter values again.

The authoritative current checkpoint is [the forward-integration report](../../../../runs/20261007-background-forward-integration/report.md),
with owner heads, preservation records and combined validation progress. The separate verification checkout
is `D:/openscad/wt-openscad-background-consumer-check`. Stack order now places the evaluator before persistence,
its direct consumer. Readiness remains false; no push or promotion occurred. The user subsequently authorized
native desktop testing; its integration failures are recorded below. Cold Customizer publication, asynchronous
strict-action admission and extended lifecycle/configuration acceptance remain open.

The source-only and initial validation descriptions below are preserved historical checkpoints; their
statements about uncommitted source and missing consumer composition are superseded by the report above.

Current verification composition `8b8b5261640f934096be1d27c194df8d96a76856` builds and passes 81,064 unit
assertions, runtime smoke, five critical CLI cases, annotations/Customizer helpers and 603,802 external-provider
assertions. Inspector's unresolved-library lookup repair and Customizer's CRLF metadata repair are committed
in their owners and merged forward. The completed CLI sweep records 3,026 passes, 11 failures and 75 disabled
cases across 3,112 selected names. The failures are six crashes reproduced in the previous delivery, one
baseline-identical line-number comparison and four checks needing Ghostscript. Separate missing-golden,
Vim and full-language coverage gaps remain explicit. Exact evidence and unchanged input identities are in
the run report; none of this background evidence is native GUI acceptance.

Authorized native checks on the same composition passed nine complete suites, including background cancellation,
both render backends, provenance, design objects, semantic hierarchy, anchors and selection. Across completed
standalone native logs there are 156 passing and 10 failing rows; navigation separately crashes with access
violation. Clipping has a confirmed synthetic-provider priority collision; insertion retains spin and
failed-evaluation bookkeeping failures after pinned libraries resolve five environment failures. Annotation
checks expose synchronous-completion assumptions and a busy guard that omits background attempts. Native
save dialogs also fail. The full shared-window sequence stalls in modal MainWindow cleanup after a source-save
failure and was stopped with a retained stack. See the report's native section and `desktop-*` evidence.
No source changes, rebuild, push or promotion were made during this test pass. Native acceptance remains blocked.

## Native repair pass, 2026-10-08

The user authorized fixing the native failures. See the current
[native repair report](../../../../runs/20261008-native-integration-repairs/report.md).
Repairs use isolated owner-based branches because another chat is advancing the same owners. The verification
checkout `wt-openscad-native-consumer-repair` includes those current Inspector-demand inputs through normal
merges. Do not merge this verification composition back into feature owners.

The rebuilt composition passes 81,163 ordinary assertions and critical CLI/export checks. Native busy state,
failed-source bookkeeping, explicit Preview/Render camera cancellation, annotation capture, bounded fixture
cleanup, repeatable Save As, navigation window lifetime, insertion gestures and clipping readiness are repaired.
The complete shared-window sequence passes 200/200 checks in `desktop-full-8`; all owner repairs are adopted.
The final verification merge has the identical tree to the tested build; the report distinguishes their SHAs.
The separate Vim executable is absent and other selected features outside this focused composition remain
explicit coverage gaps. Earlier runtimes and failed evidence are preserved. No push, promotion or feature-wide
readiness change is claimed.

## Earlier standalone readiness checkpoint

Status: in progress, Windows build and focused checks pass; **not integration-ready**, 2026-10-07.
Selected as PR stack row 24; `SOURCES.json` deliberately retains `ready: false`.

The user requested all remaining readiness work and addition to the stack, including local validation in this pass.
No local commits or promotion have been performed. The workspace requires an explicit push request for promotion.
Preserve unrelated control edits, all occupied source checkouts and the existing pending prerequisite merge.

## Source and evidence

Checkout: `D:/openscad/wt-openscad-background-model-evaluation`, branch `feature/background-model-evaluation`.
HEAD: Inspector `b93c9c219198630a2fde3822f2b90c29d88d9180`; resolved staged normal merge:
Customizer `13697aa98f18e1d1b26187d2cf5a253e8b6dce07`. `MERGE_HEAD` remains present. Feature changes are
unstaged/untracked. No unmerged index entries remain; staged and working whitespace checks pass.

Current evidence: `D:/openscad/runs/20261007-background-integration-readiness/report.md` and
`source-identity.json`, binding prerequisite, feature and complete patches, new files and submodule pins.
The original source-only checkpoint under `runs/20261007-background-evaluation` is preserved independently.

Final production test runtime: `runs/20261007-background-integration-readiness/staging-9/openscad.exe`, SHA-256
`7518d374dba6526374c5d194a11041a21173261a0b65a55da0c69c1794971529`.
Shared branch-title/icon patches were used for builds then reversed in source to separate branding from feature
history. Replay them before rebuilding. Benchmark wiring is removed from product source and retained separately.

## Passing validation

- Windows Release/Qt 6.11.1 build, Manifold and CGAL enabled, GUI tests enabled, Python disabled.
- Background evaluation: 9 native rows, including priority/coalescing, cancel/recovery, both Render backends,
  queued cancellation, stale queued Preview rejection and failed Preview retaining the previous display.
- Selection: 24 rows, including conflicting buffers, dependencies, owner closure and stale picking.
- Inspection/draft: 10 rows; focused Customizer dependency order: 3 rows; module cache: 4 rows.
  These 50 rows include setup/cleanup. Exact runtime identities are in the run report.
- Unit suite: 94 cases / 75,889 assertions pass with staged Qt TLS plugins available.
- Real `module_plus.scad`: three successful Previews per run, matching CSG hash
  `7b048a2a944c5e565c345ca1c1b307dcbd865232d961df1d682ef69d0b8590ff`.
  Earlier upstream/hierarchy reference outputs match, but their different compositions prevent a controlled
  speed comparison. The measured Preview times are roughly 3.4–4.2 seconds.
- Language cancellation acknowledgement is under 1 ms in these samples; ordinary recovery passes the native test.
  Native-library stopping remains cooperative at supported boundaries.

Fixed build/runtime failures include missing declarations/includes, invalid lambda member captures, a null input
owner after conflicting-buffer capture, terminal metadata overwriting full evaluation status, and test fixtures
closing their own window. Earlier failed logs are retained.

## Remaining work

1. **Owner history and interfaces.** Generic Customizer, captured-input and HTTP changes currently reside in this
   feature working tree. Extract reusable interfaces into their owners and merge them forward, preserving real
   ancestry. Do not cherry-pick, copy prerequisite deltas, or use the integrated release as a feature base.
2. **Measured Customizer publication pause.** Schema-2 heartbeat includes completion intervals. In `real-model-3`,
   p95 is 77.6 ms but maximum is 491.7 ms. Initial publication takes 446.8 ms: Customizer construction 370.8 ms,
   metadata 73.5 ms. Warm Customizer updates are below 1 ms. Suppressing layout/painting (`real-model-4`) did not
   materially improve it; that experiment was reverted. Split cold widget construction across bounded GUI turns
   with generation/cancellation/ownership checks; do not pump events inside atomic scene installation.
3. **Strict-action async admission.** Publication validates disk bytes in the worker, but
   `EvaluationBinding::validate`, `validateModel`, `inputsCurrent` and strict consumers still hash synchronously
   on the GUI. Add asynchronous captured-input admission in the owner and adapt picking, source transactions,
   exports and draft actions. Recheck identities before delivery; retain exact byte guards.
4. **Actual downstream composition.** Persistence/provenance/hierarchy, clipping and anchors/insertion are absent
   from the minimal checkout. Their removed MainWindow parse/instantiate hooks need pipeline adaptation: provenance
   parse scope, syntax ownership, session collector, scene semantic/design-object/provenance metadata and preview
   provenance assembly. Build and test the actual forward composition before integration readiness.
5. **Lifecycle acceptance.** Native-gate contention, parser/include/CSG/backend cancellation, inactive results,
   two windows, busy shutdown, diagnostic floods and repeated-cancellation retention need evidence. Measure F6
   cancellation separately; the benchmark currently cancels Preview. Peak working set is about 1.8–1.9 GiB in
   the benchmark process; this is not a proven leak or a repeated-run retention result.
6. **Configuration coverage.** Python/GIL and library-thread diagnostics/settings remain unvalidated. Review
   OpenCSG-disabled and `USE_POLYSET_FOR_CGAL` variants. GUI VBO assembly/upload remains an explicit measured limit.
7. After acceptance, bind local committed/validated SHAs separately from promotion. Only an explicitly authorized,
   verified push to the declared Dropbox source branch can make it ready for future integrated builds.

Corrected heartbeat fails the maximum-gap target. Schema 1's earlier `target_met: true` omitted publication and
must not be used as acceptance evidence. Passing focused tests do not establish downstream compatibility.

## Replay

Read the current run report and identity before continuing. On recorded HEAD, `prerequisite-merge.patch` restores
the resolved index, `feature-working.patch` restores tracked feature edits, and `untracked-source/` supplies new
files. Alternatively use `tracked-worktree.patch` plus the new files. Patch snapshots preserve evidence; retain
and finish real merge ancestry separately. The occupied checkout already contains the recorded source state.

Fix forward makes targeted corrections; replan changes strategy; restart revisits assumptions; supersede records
a replacement objective. No rollback, promotion or scope reduction is implied.
