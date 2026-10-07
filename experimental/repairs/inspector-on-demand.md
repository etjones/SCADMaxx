# Inspector data on demand — source implementation, 2026-10-07

Implementation checkpoint below records the original working changes. The user subsequently authorized
local commits, forward merges, building and performance comparison. The owners are now committed and
merged forward; the combined application and unit-test targets compile. Focused native validation passes
for on-demand behavior. The same-binary comparison measures approximately 15% lower Preview time with
Inspector preparation off. Broader background validation completed with the same 11
previously recorded CLI failures (six echo crashes, one line-number expectation and four
missing-Ghostscript image comparisons); later CLI batches were skipped by fail-fast.
The two existing clipping and two insertion native failures remain in this checkpoint.
Do not treat it as a fully passing integration or release promotion.
See [the current run report](../../../runs/inspector-on-demand-2026-10-07_22-57/report.md) and its `heads.json`
for current revisions, exact timing conditions, known integration failures and validation limits.
No push or packaging has occurred; upstream-equivalent performance is not established.

## Behavior

- Preferences → 3D View has **Always prepare Inspector data**, default off.
  The persisted key is `advanced/alwaysPrepareInspector`.
- Plain previews omit the provenance syntax table, invocation collector, publication and preview
  source mappings. Captured source inputs, safe evaluation, ordinary surface picking, annotations
  and cross-section clipping retain their existing contracts.
- **Select geometry** reuses a current prepared result, or requests one Preview and displays
  “Preparing Inspector…”. Picking starts only after successful preparation of the same document
  revision. Failure ends the request and leaves an explicit retry; it does not reevaluate in a loop.
- Inspector requests collection while selecting/inspecting. Clear selection, hiding Inspector,
  changing documents, cancellation without a selection, or destruction releases that request.
  Reopening can reuse already prepared current data; the next ordinary evaluation is lean.
- Requests are scoped to consumer lifetime and editor identity. The preference enables collection
  for all documents on subsequent evaluations; changing it does not immediately trigger a build or preview.
- Explicit Part/Assembly/Component declarations require source mappings independently of Inspector.
  A parsed-AST predicate scans module/call attributes, nested scopes and used libraries. Comments,
  strings and Section assignments do not trigger collection. Initially lean structured models
  reparse their captured closure with tracing before geometry evaluation.
- **Add model structure** requests source information before opening its naming dialog. Its guarded
  edit, read-only, revision, dirty-buffer and Undo checks remain in force.
- **Contextual insertion** requests the same data before picking. Preparation is cancellable through
  the insertion controls; a replacement evaluation requires a fresh pick, never reuse of an old hit.
- Background requests snapshot the collection flag on the GUI thread. Workers never consult settings
  or widgets. Successful, failed and cancelled latest attempts notify pending consumers; superseded
  attempts cannot complete a newer request.

`EvaluatedScene::inspectionPrepared` is separate from current/stale geometry. In the base Inspector
owner there is no optional provenance collector, so its successful scene is already prepared. In
provenance/semantic compositions the flag reflects the actual published provenance result.

`EvaluationSession::capturedInputs` keeps shared captured input ownership available when tracing is
off. Semantic scenes use that ownership without manufacturing a syntax table. This matters for
ordinary document-level anchors and other consumers of captured input identity.

## Owner changes and handoff

All paths below are relative to `D:/openscad`. Snapshot patches and file hashes are under
`runs/inspector-on-demand-2026-10-07`; patches are evidence, **not a replay/cherry-pick workflow**.

| Owner worktree | Unchanged HEAD at implementation | Responsibility |
| --- | --- | --- |
| `wt-openscad-selection-model-inspector` | `436e1691d32cac5b8fe0b84524c948c7d03589b8` | Preference, per-consumer/editor demand, readiness, Inspector UI flow, completion signal, shared input ownership |
| `wt-openscad-source-geometry-provenance` | `ef57c1b6be9ea0ae83f93d0f43900df7fb964a4f` | Optional synchronous collection, cache-mode transitions, model-requirement registry |
| `wt-openscad-background-model-evaluation` | `f4b6d0c3d51c672df4dc1525eb912f7565692167` | Immutable request flag, completion notification, worker session input ownership |
| `wt-openscad-semantic-model-hierarchy` | `29c6b9765f8b4d2ba61ef03a84b225450bd8c13c` | Structured-model predicate, optional worker provenance, one-time closure upgrade, Add model structure preparation |
| `wt-openscad-contextual-insertion` | `b3552dc2b653b920c9d88b454890235a7dd04d87` | On-demand insertion preparation and cancellation |

Consumers reference APIs introduced by these **uncommitted** owner changes. They are not independently
buildable until the owners are committed and normally merged forward. Do not copy common modified
files into consumers or report existing binaries as containing this change.

When commits/merges are authorized, follow `docs/feature-ancestry.md` and the actual dependency pins:

1. Commit Inspector, preserving unrelated work; merge it into provenance and background evaluation.
2. Keep provenance's earlier parsed-library-cache and immutable syntax-record optimizations. Its full
   patch includes those pre-existing changes and branding, not just this task's optionality change.
3. Commit the background adapter and merge through persistence. Merge provenance and persistence
   forward into hierarchy, preserving the background evaluator as the evaluation entry point.
4. Commit hierarchy's consumer changes; merge through anchors into insertion. Commit insertion's
   own adapter, then merge the changed owners/consumers into the integration normally.
5. Preserve actual provenance-dependent readiness when resolving scene-construction overlaps. Do
   not let a base-owner `inspectionPrepared = true` override `bool(scene->provenance)` in compositions.
6. When resolving MainWindow overlaps, retain the background evaluator. The optional syntax/collector
   logic belongs in the worker pipeline where background evaluation replaced synchronous methods.
   Carry `capturedInputs` into both surviving evaluation session constructors.

Cache correctness: enabling collection cannot seed lean library ASTs into a new tracing table;
their syntax ordinals would have no corresponding records. The synchronous cache drops/reparses
the complete closure for that transition. Structured models retain their requirement in the cache
only while the captured root/dependencies/configuration still validate. Worker reparsing clears
the lean library cache and restarts parsing against the already captured inputs.

All five worktrees retain these submodule commits (generated Clipper2 modifications were preserved):

| Submodule | Commit |
| --- | --- |
| MCAD | `1ea402208c3127ffb443931e9bb1681c191dacca` |
| Clipper2 | `c7f820f6a03fa91f189b866d27bf40dfe47abaa6` |
| OpenCSG | `9bf122715213dca05e70993dd8672fe3aa36c518` |
| manifold | `0edd9d54876f3135e431575214dd6d8a72866fee` |
| mimalloc | `30b2d9d89099bee08e9f67a1ffb3e12e7ba45227` |
| sanitizers-cmake | `bcb1fc68616e9645ca5acea2992412606373ab04` |

## Original source-only validation status

Only source review and Git whitespace checks were performed. No compiler, test runner, application,
GUI automation or benchmark was launched. README and selected/validated/promoted pins are unchanged.

Authored regression cases, all **unrun**:

- `TestSelection::inspectionDemandLifetime`: preference, multiple documents, changing a consumer's
  document and consumer destruction.
- `TestProvenance::inspectionOnDemand`: lean output, library-cache upgrade, usable source mapping,
  immutable older results, reopening without reevaluation, return to lean and always-on preference.
- `TestProvenance::inspectionPreparationFailure`: malformed source ends preparation; explicit retry works.
- Semantic unit case: plain geometry/comments/strings/Section assignments versus declarations and used libraries.
- `TestSemanticHierarchy::onDemandInspectionAndStructure`: worker-backed lean/prepared transitions and
  preparing/wrapping a plain model without the always-on preference.
- `TestContextualInsertion::preparesInspectionOnDemand`: cancelling before submission, preparing before
  picking, consumer release and return to lean previews.
- Existing provenance/insertion tests explicitly opt into prepared fixtures; the existing captured
  structure-edit guard test requests data for its fixture instead of relying on the former default.

After authorized forward merges/builds, run the affected owner and consumer tests per
`workflows/testing.md`, including anchors and cross sections with collection off. Desktop suites
require desktop authorization. Include background Stop/failure/supersession and document switching.
Then compare off versus always-on in **one frozen Release binary**, same source/model/settings,
using the shared test-profile lock. Verify identical geometry and retained source-edit guards.
Do not infer the savings from earlier before/after optimization benchmarks.

## Forward-integration findings

The synchronous provenance owner and background evaluator have different parser entry points.
When merging provenance into hierarchy, keep the worker pipeline; do not restore the deleted
`compileEnded`, `instantiateRoot`, `parseDocument` or `parseTopLevelDocument` methods, or add unused
`ParsedLibraryCache` members to the background MainWindow. The synchronous cache optimization is
still maintained in its owner; it is not a worker cache implementation.

Combine the captured-input and provenance/design/semantic declarations when those adjacent header
members conflict. A composed scene is inspection-ready only when its provenance result exists;
remove the base owner's unconditional readiness assignment. In anchors, preserve the Inspector
layout size constraint alongside the updated on-demand help text. In insertion, retain only one
`provenanceCollector` member when merging the new captured-input member.

The hierarchy consumer's provenance regressions must wait for worker publication before checking
the new scene. Keep their CSG, dirty-buffer, unchanged-timestamp content-change, library-shadowing
and retained-snapshot assertions. AST pointer reuse is a synchronous-cache contract; the worker
currently creates a new captured parse closure. Inspector interaction tests must wait until
on-demand preparation has entered picking before simulating a viewport click.

The continued build uses the existing background-consumer-check composition and shared dependencies.
Exact source/binary identities, build logs, excluded checks and performance results belong to the
linked run report. Desktop permission from the ongoing native investigation remains in force.
The shared test-profile lock also protects another chat's build/test runs: preserve a live lock
and wait for a quiet machine before timing; lock contention is not a product failure.

The native comparison uses two logical CPUs and equal 8 GiB job limits for both modes.
The initial 4 GiB capped run reached a critical-error dialog near the cap and is excluded;
the successful larger-budget rerun does not validate low-memory recovery. For this model,
the medians are 10.70 to 9.07 seconds for open/first Preview and 10.49 to 8.90 seconds for
unchanged Preview, across five measured processes per mode plus warm-ups. All 36 preview
outputs match. Do not compare those constrained background-consumer timings directly with
earlier unrestricted synchronous-owner timings.
