# Remaining evaluation performance: investigation, 2026-10-07

Status: production fixes were committed locally and merged forward through hierarchy on 2026-10-07.
The hierarchy build and targeted native regressions pass; new timings and broad-suite limitations are in
`runs/hierarchy-freshness-2026-10-07_16-57/report.md`. No push or integrated release was made.
The earlier investigation and pending-implementation handoff below are historical checkpoints.
Investigation evidence is in `D:/openscad/runs/20261007-remaining-performance`. The user's model and
libraries were read without modification. That investigation made no integration, package, commit or push.

## Reproduction and comparison

Model: `E:/Dropbox/3D Printing/Designs/20260913 Desk organizer/models/module_plus.scad`.
The library-only fixture imports the same libraries but generates just a cube.

- Feature owner: `feature/semantic-model-hierarchy`, `49b30bae3cac3d148a1fefc0604c13e089b4c8d6`.
  This contains the preceding Inspector lookup and hierarchy snapshot optimizations.
- Local baseline: `wt-openscad-readme-baseline`, `f65fe98dd007f1ed7482bd5420392917c040c80d`.
  This is an existing upstream-based baseline with Windows/capture support, not precisely the
  integrated upstream revision. Its current source was rebuilt with the phase timers.
- Both local builds use MSVC 14.51, Release `/O2`, and the shared vcpkg installation.
- Downloaded comparison: `OpenSCAD-2026.09.27-x86-64/openscad.exe` (different compiler/build inputs).

`Measure-Owner.ps1` measures separate-process CSG export with `$preview=true`, two repeats per case.
`Measure-Gui.ps1` opens the real model, requests Preview, and exits after compilation completes.
GUI settings are isolated with `OPENSCAD_TEST_SETTINGS_DIR`; the diagnostic launch suppresses
Windows icon registration. GUI compilation completion is not a precisely measured first painted
frame, and complete process wall time includes startup and shutdown. No FPS claim is made.

All successful CLI modes produce the same CSG SHA-256:
`6062B14BDE6C20FFBD19498E7063AF7EB135E0D6AC7B602495195AB6CD72D923`.
Successful GUI runs normalize to 42 CSG elements. Source patches, original file backups, logs,
executable hashes and diagnostic runtimes are retained in the run. No compilation ran concurrently
with benchmark samples. Small two-repeat differences are indicative, not precise speedup estimates.

## Measured costs

| Measurement | Observed time |
|---|---:|
| Downloaded normal build, CSG model evaluation/process | 3.239–3.240 s |
| Rebuilt local baseline, same task | 3.782–3.862 s |
| Instrumented feature owner, same task | 5.906–6.104 s |
| Owner without parser provenance/invocation capture, diagnostic only | 5.030–5.036 s |
| Owner without semantic/design collection, diagnostic only | 5.449–5.494 s |
| Owner without both groups, diagnostic only | 4.629–4.853 s |

Do not add these differences: the bypasses overlap and change allocation/lifetime work. They are
diagnostic controls for this ordinary model, not supported feature-disable modes. The approximately
0.6-second downloaded/local-baseline difference is a build-comparison effect; compiler, dependencies
and upstream revision were not independently isolated.

The detailed owner timers show roughly 0.44–0.48 s creating about 49,000 parser source records,
0.13–0.15 s finalizing the semantic scene, and only 0.04–0.06 s recording evaluated module invocations.
Initial input reads and validation total about 0.11 s (nested hashing about 0.009 s).
Provenance lookup therefore matters, but recording geometry-producing invocations is not a
multi-second bottleneck. Basic vertex/edge measurement still uses the renderer's existing geometry.

### Repeated GUI freshness validation

`EvaluationBinding::inputsCurrent()` ran **45 times** during one open/preview/exit cycle and took
**1.710 s**. Total source fingerprints were **2,025**, compared with 45 when that validation was
bypassed in the same diagnostic executable. The bypass took total process time from 10.143 to
8.476 s; GUI compile/UI completion fell from 5.770 to 5.122 s. Thus about **0.65 s** of the measured
validation cost delays compile completion; the remainder includes shutdown callbacks. Do not claim
that all 1.71 s is first-view latency.

UI consumers call `validate()`, `validateModel()` and `scene()`, which re-enter full content checks.
Those checks reread/hash included files and repeatedly rebuild each editor's input identity/text
inside the per-file loop. Consumers include the semantic panel/target service, design records,
saved-view status and viewport tool routing. They need inexpensive display eligibility checks;
every display refresh should not be treated as a guarded source-edit commit.

The existing cheap `current()` path already tracks source revision/fingerprint plus invalidation.
A follow-up belongs in the Inspector/evaluation-binding owner: provide clearly separated cheap
display checks and strict operation validation. Retain exact-content validation before source
edits/export commits and at appropriate result installation boundaries. Coalesce duplicate checks
within a refresh and capture open-editor inputs once per validation pass. Do not ship the diagnostic
always-true bypass, weaken multi-document ownership checks, or rely solely on watcher delivery at
mutation boundaries. Then propagate by normal forward merges and test stale-file/editor cases.

### GUI publication and cleanup

With the dependency-order diagnostic correction below, provenance publication costs 0.17–0.18 s,
and CSG preview preparation 0.062–0.064 s. The comparable local baseline GUI compile completes in
3.750–3.818 s; the feature owner in 5.771–5.913 s. This is a feature-owner comparison, not a newly
profiled complete integration binary.

Destroying captured library ASTs costs approximately 0.63 s in the GUI probe. It occurs during
shutdown here, not before the first preview. CLI post-export cleanup was about 0.7–0.9 s from the
phase boundaries. Normal OpenSCAD retains its singleton library cache until process termination,
so CLI wall-time comparisons include a different cleanup policy. Do not present all CLI cleanup
as interactive preview overhead. Repeated-preview cache reuse is a separate follow-up requiring
captured-buffer/source consistency, not permission to reuse arbitrary stale ASTs.

## Separate Customizer dependency-order bug

The first deployed feature-owner GUI probe failed before evaluation:

```
Ignoring unknown function 'module_plus_layout_names'
Assertion 'is_list(list)' failed: "Input is not a list"
```

`MainWindow::parseDocument()` calls `ParameterWidget::setParameters()`, whose `CustomizerContext`
constructs a `FileContext` and evaluates top-level assignments. `use` libraries have not yet been
loaded into the fresh captured cache; `handleDependencies()` normally runs later in `compile()`.
The CLI does not construct this Customizer context, and therefore did not expose the failure.
The integrated source contains the same ordering/context construction; its GUI was not rerun here.

For profiling only, dependencies were loaded immediately before `setParameters()`. The model then
evaluated successfully, and the later dependency pass cost only about 0.006 s. Customizer context
construction itself was less than 0.001 s on this model; the whole widget update took 0.263–0.309 s.
This is an ordering bug, not evidence of seconds spent reevaluating top-level variables.

A production correction must reconcile dynamic Customizer (`codex/pr6642`) with captured evaluation
(`feature/selection-model-inspector`): ensure dependency availability before context evaluation,
preserve included dirty-buffer capture and parameter application order, and test a fresh launch
whose top-level assignment calls a function from `use`. Do not introduce geometry reevaluation just
to initialize Customizer. The temporary early dependency load was removed after measurement.

## Workspace state after the investigation

All temporary source instrumentation, bypasses and the dependency-order diagnostic correction were
removed. The hierarchy source retains only its pre-existing shared icon/title edits and generated
Clipper2 state; the baseline source returns to its original state apart from its existing generated
Clipper2 change. Its original baseline executable was restored byte-for-byte. The feature application
was rebuilt after source restoration. Diagnostic executables under this run are for reproduction only,
not releases or launcher candidates. Existing integrated source, build and packaged delivery are unchanged.

## Implementation handoff (2026-10-07)

The subsequent request to fix the two identified issues has been implemented in source.
The user's standing restriction on builds/tests remains in force. Only source review and
`git diff --check` were performed; no performance improvement is claimed as measured yet.
No commits, forward merges, pushes, pin updates or packaging were performed.

| Owner/worktree | Unchanged HEAD beneath the pending edits | Pending change |
|---|---|---|
| `wt-openscad-selection-model-inspector` | `335a5762cc2fa18124b1ced717e60771c6164c5b` | Explicit display-only binding API, one live-editor capture/hash per strict validation pass, cheap invalidation callbacks, avoid rechecking already-stale results on editor close |
| `wt-openscad-pr-6642-dynamic-parameter-changes` | `306c92d39c4cbb7fe82981e179161aa85d44774e` | Load `use` dependencies before Customizer context construction; own the parsed AST before potentially throwing initialization |
| `wt-openscad-design-object-persistence` | `265856584f4c0ed961e847281eb9b40f89c3456f` | Display-only record listing and saved-view status; reject unavailable validated scenes before applying source views |
| `wt-openscad-semantic-model-hierarchy` | `49b30bae3cac3d148a1fefc0604c13e089b4c8d6` | Cheap panel/tree/selection display queries, explicit display target resolution, preserve strict operations and asynchronous installation guards |

`EvaluationBinding::displayCurrent`, `modelDisplayCurrent` and `displayScene` do no filesystem
reads or hashing. They preserve owner, revision, result/configuration identity and active-editor
checks. The model-only variant intentionally ignores viewport generation and permits draft pixels,
matching `validateModel`; the viewport variant rejects draft pixels. Watcher delivery can lag
by an event-loop turn, which is acceptable only for display. `validate`, `validateModel` and
`scene` still validate exact live contents on every call. No cross-action success cache was added.

Hierarchy's `TargetService::resolveForDisplay` is for UI presentation. Existing `resolve` remains
strict for actions and external consumers. Parameter edits, source navigation, picking, exports,
draft commits and worker-result publication retain strict guards. In particular, the mesh-provider
completion callback explicitly validates after `Controller::current()` became display-only.
Dependency loading remains inside the caller's native captured-evaluation scope, so it must keep
using captured dirty buffers. It does not evaluate geometry to initialize Customizer.

### Required forward integration

The persistence/hierarchy consumer edits reference the new Inspector API. **Do not build those
dirty consumers as-is: their checked-in prerequisites do not contain that API yet.** Once commits
are authorized, commit the owner fixes and consumer adaptations in their respective worktrees,
then follow `docs/feature-ancestry.md` with normal forward merges:

1. Inspector and Customizer into both provenance and persistence.
2. Persistence into Cross sections; provenance and persistence into hierarchy.
3. Hierarchy into anchors, then anchors into contextual insertion.
4. Only then re-integrate the resulting selected heads into the existing integrated branch.

Preserve captured parsing/parameter revision hooks when merging the Customizer `parseDocument`
change. Do not copy foundational files into consumers or cherry-pick patches. Accepted dependency,
validation and promotion pins still describe the earlier committed heads; these working changes
must not be represented as already selected or validated.

Persistence and hierarchy already had unrelated common icon/title edits and generated Clipper2
changes; those were preserved. Submodule revisions match in all four worktrees:

- MCAD `1ea402208c3127ffb443931e9bb1681c191dacca`
- Clipper2 `c7f820f6a03fa91f189b866d27bf40dfe47abaa6`
- OpenCSG `9bf122715213dca05e70993dd8672fe3aa36c518`
- manifold `0edd9d54876f3135e431575214dd6d8a72866fee`
- mimalloc `30b2d9d89099bee08e9f67a1ffb3e12e7ba45227`
- sanitizers-cmake `bcb1fc68616e9645ca5acea2992412606373ab04`

### Validation to run when requested

Added/extended native GUI cases (not executed):

- Inspector `TestSelection::cachedDisplayFreshness`: repeated display queries before watcher
  delivery retain the scene; strict viewport/model checks reject changed disk contents immediately.
- Inspector `staleAndWrongDocument` and `TestInspectionDraft::baseCandidateBasePreservesModelAndRejectsCapture`:
  verify display ownership and draft-pixel rules.
- Inspector `dirtyDependencies`: now calls a `use` function from a top-level assignment with an
  assertion. Run again in the combined consumer to cover Customizer plus dirty captured libraries.
- Customizer `TestMainWindow::customizerLoadsUseBeforeEvaluatingAssignments`: fresh unique library
  paths, nested `use`, and an asserted top-level assignment, before geometry evaluation.
- Hierarchy `TestSemanticHierarchy::displayRefreshKeepsStrictEditGuards`: repeated panel/Inspector
  refreshes before watcher delivery, followed by a rejected parameter edit against changed bytes.

Also rerun the existing persistence saved-view/dirty-include cases and semantic stale-job/export
cases. After those pass, repeat the isolated-settings GUI benchmark on `module_plus.scad`, verifying
successful preview/42 CSG elements rather than exit status alone. Compare compile/UI completion
separately from total process duration. Existing runtime probes are diagnostic-only and must not
be restored into production source; never use the always-true freshness bypass as a fix.

## Committed owner/consumer build checkpoint, 2026-10-07

Under explicit commit/merge/build authorization, the four fixes were committed in their owners:
Inspector `b93c9c219`, Customizer `13697aa98`, persistence `df5cc797b`, and hierarchy `803a1512d`.
Inspector and Customizer were normally merged into provenance (`d4c2ee5f4`) and persistence
(`a004cbad1`), then both into hierarchy (`72730cb9b`). No cherry-picks or copied foundation fixes.

Customizer's parse ownership conflicted with the consumers' existing failed-parse cleanup. Retain
the explicit failed-parse delete/null logic, then construct `parsedSource` before dependency loading.
Keep captured parameter revision/fingerprint and override hooks. Remove the manual delete from
override rejection because `parsedSource` now owns that AST. This reconciliation is the same in
both consumer merges and should be retained during later integrations.

The first build exposed a test-only compile error: `Controller::refreshParameters` is private.
Use `controller->parameterPanel()->refresh()` in the regression. Repair commit `62e869fd7` is
the final tested hierarchy source. Its standard title/icon patches remain separately uncommitted.
Shared vcpkg, the existing Release build directory and its compatible configuration were reused.

Isolated native suites pass: Selection 24 rows, SemanticHierarchy 18, InspectionDraft 10 and
Provenance 9. The broad run also passed the new Customizer test and all 10 design-object rows,
but reported save-dialog and selection-feedback failures before it was interrupted; it is not a
passing full-suite record. Detailed logs, benchmark sources/identity and remaining timing gap are
in [the new run report](../../../runs/hierarchy-freshness-2026-10-07_16-57/report.md).

Native timing uses one shared GUI-test helper, without validation bypasses. Test-only adapters
were removed from source after producing separately identified benchmark binaries; production
binaries were preserved/restored. These measurements distinguish open-plus-Preview, repeated
Preview, CLI process duration and framebuffer capture. They do not establish first-present latency.

Local accepted heads/dependency pins now describe this five-branch closure. Historical promoted
and validated heads remain separately recorded. Cross sections, anchors, insertion and the full
integration have not received these commits; merge them forward before claiming those builds
contain the fixes. No push, release packaging or launcher update was performed.

## Measured remaining captured-cache overhead, 2026-10-07

An observational native GUI profile of fixed hierarchy `62e869fd7` against local upstream `f65fe98dd`
is retained in [the cache profiling report](../../../runs/captured-cache-profile-2026-10-07_18-40/report.md).
No features or freshness guards were disabled. With profiling off, five measured processes per build
gave median open-plus-Preview 9.59 s versus 4.63 s, and unchanged Preview 7.79 s versus 2.14 s.
The repeated metric averages two Previews within each process before taking the process median.

Every fixed-build Preview constructs a new captured `SourceFileCache`, reparsing 13 library entries
and recording 63,239 syntax sites. Upstream reparses zero libraries on unchanged Preview. Captured
library parsing takes 2.524 s per repeat; syntax recording (0.571 s) is mostly nested inside that
time and must not be added again. Opening also loads those libraries into the global cache through
Customizer dependency preparation (3.129 s), before Preview reparses them into its captured cache.
Do not remove that preparation: it fixes legitimate top-level `use` function assignments.

`EvaluationBinding::install` takes another 1.722 s in the paired profile. Together, library parsing
and installation account for about 81% of the 5.274 s profiled repeat gap. A focused follow-up confirms
the expensive installation block is pruning expired renderer bindings: `renderers.erase` releases
the old retained evaluation. It takes about 1.6–2.5 s in that later, more variable series. The cache
destructor body itself is only about 0.23 ms; do not confuse it with destruction of the complete
evaluation graph. Individual subobject destruction/allocator costs have not been isolated.

Strict freshness is around 0.10 s for three checks, and unchanged Customizer refresh is around
0.002 s. The next optimization should preserve captured versions/dirty-buffer correctness while
reusing immutable parsed library/provenance data and reducing old evaluation retention/destruction.
Replacing captured parsing with unvalidated global-cache access is not a correct fix. Cache keys
must cover exact inputs, dependency/include resolution, parser context and provenance ownership.

All 84 accepted Previews across the paired and focused series produced identical CSG; all 47 frozen
dependencies remained unchanged. Seven overlapping compilation attempts were excluded, plus an
initial counter-only smoke run. These checks cover this workload, not the full acceptance suite.
The report retains instrumentation sources, before/after snapshots, scripts, exact runtime/configuration
identities and restoration checks. Production source and normal build executables were restored;
diagnostic binaries remain isolated in the run. No optimization, merge, commit, push or promotion
was performed by this profiling task. Reuse this evidence before implementing the next change.

## Implemented captured-library/syntax reuse, 2026-10-07

The provenance owner now has a locally implemented and tested optimization on `d4c2ee5f4`:
one bounded parsed-library snapshot, exact captured-input and lookup validation, shared immutable
per-file syntax records, and a common captured parse path for opening and Preview. Root parsing
remains fresh; dirty buffers, changed dependency contents (even unchanged size/mtime), newly
shadowing libraries and parser-context changes invalidate correctly. Root text changes currently
invalidate the snapshot; arbitrary root-edit reuse is outside this implementation.

On `module_plus.scad`, five measured processes per build reduce the same owner's initial native
open-plus-Preview median from 8.966 to 6.364 seconds and unchanged Preview from 6.593 to 3.039
seconds. Upstream remains faster at 4.612 / 2.117 seconds. This removes 79.4% of the repeat-time
gap, not the entire gap. All 54 Previews match; 45 focused native rows and 122 unit cases / 76,272
assertions pass. See [implementation, exact evidence and local handoff](../../../runs/captured-cache-reuse-2026-10-07_19-27/report.md).

The change remains uncommitted/unpromoted in `wt-openscad-source-geometry-provenance`; no downstream
or integrated build includes it yet. Commit on request, normally merge into hierarchy and its
declared consumers, and verify the final integration. Selected input/dependency pins remain unchanged.
Temporary benchmark hooks are removed from production source; the measured binary remains isolated.

An incremental-build trap was diagnosed with CDB: copying/restoring source with preserved timestamps
can leave newer objects built against an obsolete class layout. Content restoration is insufficient.
Advance affected source/header timestamps or force dependent objects to rebuild; retain the exact
source/binary identity. Rejected stale-object test runs are separate from passing consistent-build
evidence. Previously restored profiling files in hierarchy/upstream were content-verified and touched
so their next build replaces diagnostic objects.

## Remaining overhead after reuse: measured 2026-10-07

A new observational profile of the optimized provenance owner (current head `e3363f822` plus its
uncommitted cache changes) versus upstream `f65fe98dd` records unchanged Preview medians of
2.996 versus 2.111 seconds with timers off. The profiled gap is 0.962 seconds: approximately
211 ms extra root parsing/capture preparation, 341 ms extra model/provenance instantiation,
254 ms retained-result installation, 54 ms Preview preparation and 102 ms other/residual work.
See [the detailed profile and exact next targets](../../../runs/captured-cache-reprofile-2026-10-07_20-25/report.md).

The key remaining copy is now proven: each unchanged root parse writes 5,052 sites but detaches
34 shared file tables containing 62,818 records, costing 126 ms. Library AST reuse itself works
(zero library parses per repeat). Invocation publication/Preview also copies immutable data.
About 1.473 million captured-library lookups incur an estimated 108 ms extra versus upstream
(sampled 1/1,024 calls; do not treat the extrapolation as full-call precision).

Old renderer-binding disposal still costs 214 ms, but total context garbage collection is only
12 ms versus 10 ms upstream. Do not blame GC for that disposal delay. Per-member destruction
is not fully attributed; avoiding syntax/invocation copies should also reduce allocations to free,
but that expected benefit requires measurement. Keep captured-input freshness and edit guards.

All 72 accepted Previews match, model/47 dependency/runtime hashes are unchanged, and all temporary
instrumentation and production executables are restored. Three compilation-overlap attempts and
an earlier interrupted warmup-only series are excluded. This diagnostic task made no new optimization,
commit, merge, promotion, integrated release or selected-input change.

## Unchanged syntax-record reuse implemented, 2026-10-07

The provenance owner's local follow-up replaces per-file copy-on-write detachment with per-table
pending/changed records. Completed identical records return to the immutable shared base; genuinely
changed/published versions stay isolated. No previous-generation ownership chain is introduced.
New parser regressions prove actual pointer sharing across nested-include reparses and preservation
of separately published incomplete/complete records.

The clean paired comparison against the previous optimized owner reduces open-plus-Preview from
6.348 to 5.868 seconds (7.6%) and unchanged Preview from 3.046 to 2.750 seconds (9.7%). Syntax recording
falls from 178 to 44 ms; old-scene disposal falls from 218 to 122 ms. All 63,239 completed records
are shared, with zero remaining overrides for the measured model. This is not an upstream or full
integrated comparison. See [implementation, validation and exact handoff](../../../runs/syntax-record-reuse-2026-10-07_20-58/report.md).

The accepted `quiet-measurements` series holds the shared test-profile lock and excludes overlapping
compilation. An earlier provisional series overlapped another chat's CTest work and is entirely
excluded; compiler-only monitoring was insufficient. The final 72 accepted Previews match exactly.
The production build passes 127 unit cases / 76,348 assertions and 45 focused native rows, plus
real-model CLI geometry equivalence. Instrumentation is removed from production source and binary.

Concurrent normal owner merges advanced the source to `ef57c1b6b`; their unresolved-use/CRLF fixes
are preserved and covered by final production validation. Frozen comparison binaries use the earlier
`e3363f822` base plus their separately recorded working changes. The syntax/cache optimization remains
uncommitted; this task made no commit, merge, push, promotion or integrated release.
