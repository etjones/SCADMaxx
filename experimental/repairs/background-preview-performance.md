# Background Preview performance: measured handoff, 2026-10-08

## Further attribution after the lookup/snapshot fixes

The [exact-probe and ablation report](../../../runs/evaluator-detail-2026-10-08_10-02/report.md)
continues the updated diagnostic composition below against the same pinned upstream. No
owner changes, new production fix, merge, commit, push or promotion were made in this pass.
Temporary probes and both diagnostic variants were restored; runtime/source identities and
raw evidence are retained in that run. Existing uncommitted owner fixes below remain intact.

Five measured processes per condition put timer-off first Preview at 4.540 s versus upstream
4.527 s, and unchanged repeat at 2.344 s versus 2.086 s (+12.3%). The paired repeat excess
is 274 ms, range 241–363 ms. The previous run measured +17%; profiling/code-layout/machine
variation is not a newly implemented speedup. These are one model's Preview completion times,
with Inspector preparation and agent access off, not full-stack/F6/viewport performance.

Concrete remaining costs and priorities:

- Capturing/revalidating inputs and the two worker source checks total about 128 ms. Across
  all phases, 138 disk reads cost 68 ms, 239 identity resolutions 41 ms and 141 SHA-256 calls
  27 ms. Those totals overlap the phases; never sum them twice. Optimize checked bulk reads
  and repeated identity work while retaining exact-byte/editor-generation guarantees.
- Persistence `DesignCollector::collect()` performs the outer syntax-validation walk 303
  times per Preview (~28–31 ms), including before the use-library early return. Recreated
  FileContexts repeatedly revisit the same immutable scope. An evaluation-local cache keyed
  by scope and validation mode is a concrete target; retain invalid-local diagnostics.
- Semantic discovery/finalization still costs ~14 ms for this unmarked model. Publication
  costs ~45 ms, primarily metadata/signals; renderer installation is only ~0.3 ms.
- Removing all 29 expression cancellation-check sites in an isolated binary gave no useful
  repeat gain. Do not weaken cancellation. An optional binding-map allocation experiment
  produced only ~8 ms paired median total benefit with a range spanning zero; it is a small,
  unproven overall optimization, not the explanation for the remaining slowdown.

Language instantiation's paired excess is ~100 ms (95–140 ms); the identified language
components explain part, not every millisecond. Preview CSG generation remains fast (~8 ms).
Agent tree serialization/retention does not run with access off. Sparse collector samples
were misleading because calls have very different costs; future work should reuse the exact
collector probes and paired timer-on/off method. All 204 accepted Previews match the same
geometry hash; one parameter-experiment process contended with another compiler and was excluded.

Implement future fixes in their owners and forward-merge normally; never copy the diagnostic
composition into a maintained feature branch. The report records the next targets and limits.

## Lookup and demand-driven snapshot follow-up

The next authorized fix/build/test pass is complete in an isolated diagnostic composition.
New source changes remain **uncommitted** in Inspector (base `7a1149b788ab57e90e800c1c7fc0f18313fe7190`)
and background evaluation (base `737865b6931676b5095eec15bab053bb0a366c72`). Existing commits below
remain intact. No maintained forward merge, push, promotion, readiness update or release occurred.
See the [complete result and reproduction record](../../../runs/lookup-agent-snapshot-2026-10-08_09-31/report.md).

Inspector caches resolved library spellings to stable cache-entry addresses, eliminating the
second hash lookup. Misses are not cached; clear/reseed, alias resolution and map growth have
regression coverage. The background owner returns a weak deferred inspection factory instead
of serializing every model. Agent publication materializes/retains trees only when access is
enabled, using the exact surviving evaluation's roots, ASTs and captured library cache. Late
enable requires no reevaluation. Stop/restart resets tree metadata; expired evaluations remain
unavailable rather than recovering pointers from old renderers. Histories remain bounded and
factories do not retain old evaluation worlds. This is independent of optional Inspector tracing.

The application and focused tests pass: evaluation-input unit cases, two background cache cases,
and six annotation/HTTP cases, including enable after source edits and stop/restart. One old
test expectation was updated: enable adds tree metadata but must preserve result identity;
subsequent source snapshot operations must preserve the whole result. Exact-source consistency
checks remain unchanged. Detailed source patches, hashes, failed-attempt evidence and passing
logs are retained in the linked run.

Five measured processes per condition plus warm-up, same model and pinned upstream:

| Preview | Upstream | Fixed candidate | Remaining regression |
| --- | ---: | ---: | ---: |
| First | 4.536 s | 4.631 s | 2.1% |
| Repeated | 2.091 s | 2.446 s | 17.0% |

All 72 Previews match the same CSG hash with no detected contention. The prior pair was
6.1% / 26.8%. Sampled lookup excess is now approximately 8 ms rather than 129 ms. Agent
preparation is 0.043 ms and retention/page generation has zero calls with access off. Publication
is approximately 44 ms rather than 101 ms. Remaining instantiation excess is approximately
143 ms; source capture and the two worker byte checks remain measurable. Times are specific
to this model, and nested/sampled timers are not exact additive accounting.

After a future commit request, retain these two owner changes separately. Forward-merge Inspector
into background evaluation and provenance, then those prerequisites through persistence,
hierarchy, Cross sections, anchors and insertion together with the earlier committed cache/display
repairs. Do not copy the diagnostic composition back into an owner. Keep the published source
pins and historical validation separate until the resulting composition is validated/promoted.

## Current local commit checkpoint

The user subsequently requested grouped commits. The performance repairs are now retained
locally in their owning branches:

| Owner | Commit |
| --- | --- |
| Persistence display synchronization | `83986a17dcc83f404c13569477f4956e1c4e950a` |
| Hierarchy background parsed-library reuse | `021d0316e94ca31428aeab61aad604a918522d53` |
| Anchor display resolution and strict action boundaries | `aaf3430e3d908ab5ce171d5b07e5eddcdc8855ae` |

All 12 committed source/test files matched the validated source snapshot in
`runs/background-cache-profile-2026-10-08_05-42/source-identity-final.json` before staging.
The event-driven native Preview helper is retained separately in the control repository.
Earlier uncommitted/not-built statements below describe historical checkpoints.

No new build/test run, forward merge, push or promotion accompanied these commits. The
dependency manifests and accepted inputs remain unchanged. The next authorized integration
must merge persistence forward into hierarchy and Cross sections, then hierarchy into anchors,
then anchors into contextual insertion; preserve normal ancestry and revalidate the resulting
composition. The diagnostic archive is evidence, not an owner branch to merge back.
Unrelated title/icon patches, generated Clipper2 changes, control edits and staged plan moves
were left untouched. Detailed source identities, timings and test evidence follow below.

## Earlier profiling checkpoints

See the [complete stage profile](../../../runs/background-upstream-profile-2026-10-08_00-29/report.md)
for reproducible commands/scripts, binary/source identities, raw samples and restoration evidence.
This is a diagnosis, not a product fix or promotion. No commits or pushes were made in this pass.

Frozen candidate `26db20805` is the preceding Inspector-on-demand consumer build, with Inspector
preparation off. Baseline `f65fe98dd` adds Windows build/capture support to common upstream ancestor
`03da906b4`. Newer native-repair owner commits and the full release stack are not part of this pair.
Shared MSVC Release/dependencies, native Qt, identical two-CPU/8-GiB limits and unchanged real model.

Median initial open/Preview: candidate **5.250 s**, upstream **4.419 s**. Unchanged Preview:
candidate **4.978 s**, upstream **2.060 s**. Five measured processes per condition plus warm-up;
two additional focused series attribute individual costs. All 114 accepted Previews match.

## Main causes and ownership

- Background worker recreates `SourceFileCache` on every request. All **13 used libraries** are
  reparsed on every Preview, costing about **1.9 s**; upstream reparses none on unchanged Preview.
  The synchronous provenance owner's reuse optimization exists but is not applied by
  `gui/evaluation/EvaluationPipeline.cc`. Implement worker-safe reuse through the owning
  background/provenance/hierarchy dependency graph, with normal forward merges only.
- Publication notifications invoke **16 strict `EvaluationBinding::validate` calls**, costing
  about **475 ms** within the roughly 582-ms publication phase. They reread/hash dependencies.
  Renderer-replaced callbacks cost 317 ms; binding-installed callbacks 194 ms. Those totals
  include strict validation and must not be added to it. Audit persistence/section/semantic
  display consumers; retain strict validation at action boundaries, use cheap display-current
  state for UI refresh. `DesignDocument::synchronize` is one measured consumer, not the only one.
- Binding installation itself is only 8.6 ms; old renderer-map pruning is negligible here.
  Detached agent model-tree preparation/retention costs about 90 ms even with Inspector off;
  HTTP snapshot publication returns immediately while agent access is disabled.
- Sampled captured-library lookup overhead is approximately 133 ms beyond upstream; this
  accounts for some of the smaller language-evaluation gap. Semantic discovery/finalization
  and Customizer parameter evaluation are small. Do not start by optimizing geometry rendering.

Reuse must preserve dirty buffers, exact captured bytes, lookup/include shadowing, configuration,
provenance mode, cancellation and independently retained old results. Do not restore synchronous
MainWindow methods, bypass validation globally, trust only mtime, or use mutable global ASTs.
Reprofile after the two main fixes; these timings do not promise additive speedups.

## Correct the benchmark before reusing old numbers

The former helper spun continuously in `processEvents()` while waiting for the worker. Under
the CPU cap this substantially inflated worker timings (roughly 9–10 s versus 5 s with an
event-driven wait). The control helper at `experimental/performance/native/GuiPreviewBenchmark.h`
now waits with `QEventLoop`, a completion signal and a timeout. Use that helper for new runs.
The old Inspector-off/on absolute timings are historical observer-affected results; this pass
does not establish a corrected off/on percentage. Earlier synchronous-only comparisons do
not necessarily suffer the same worker-wait bias.

Native desktop authorization and the shared test-profile lock still apply. Preserve the
original executable, source bytes, matching dependencies and timestamps when adding temporary
probes. This run restored all 13 source files and both original production executables;
diagnostic binaries remain isolated in the run. Only the benchmark helper change is retained.

## Source fixes awaiting build and measurement (2026-10-08)

The subsequent "Fix that" pass implemented the two main repairs as **uncommitted owner
changes**. No build, tests, merge, commit, push or promotion was performed. Existing timings
above describe the old binaries; they do not measure these fixes. Accepted dependency pins
and readiness were left unchanged. Preserve unrelated title/icon patches and Clipper2 dirt.

| Owner worktree (under `D:/openscad`) | Unchanged HEAD | Working changes |
| --- | --- | --- |
| `wt-openscad-design-object-persistence` | `cd3d9b9ad89b275e7a0170ab7fa6a47d7ce151d0` | `DesignDocument::synchronize` uses document-scoped `displayScene` for publication; source transactions and pending consumer promotion checks remain strict. New TestDesignObjects case. |
| `wt-openscad-semantic-model-hierarchy` | `fba67821c5b02d4591e159391aa9b5c925cd0fc1` | Background EvaluationPipeline library reuse adapter and two TestBackgroundEvaluation cases. |
| `wt-openscad-anchors-attachments` | `664009a403fcc6e7e9e03d81529693595b42f14c` | Anchor lists, Inspector contribution and overlay preparation use display snapshots/resolution. Edit planning for button eligibility is separate from strict action preparation. Extended included-owner regression case. |

The hierarchy adapter owns the combined pipeline: base background evaluation has no provenance
dependency, while hierarchy already inherits `seedCapturedLibraries`, `reuseForParse`, and lookup
recording from provenance. Do not copy this pipeline backwards into the background owner or add
semantic dependencies there. The existing synchronous provenance cache remains unchanged.

The worker retains one last successful parse closure, keyed by document, root contents, ordered
library path, definitions, working directory and feature settings. It verifies exact consumed
bytes (including dirty editors) and reruns recorded include/use searches to detect shadowing.
Lean/traced transitions reparse; semantic model declarations still force tracing. Root parsing
and Customizer application remain per request. Independent library wrappers and syntax lookup
maps are detached before GUI publication; immutable library scopes/per-file syntax records may
be shared. No evaluated session, renderer or mutable Customizer root is retained by the cache.
Cancellation/failure does not publish a partial entry; Python, parser side effects and diagnostic
runs are excluded. `Result::reusedLibraries` exposes hits for the focused regression cases.

Anchor display resolution has its own private lightweight resolver. The public/published
resolver, picking, source navigation, edit preparation and source transactions still validate
exact dependency bytes. A pending filesystem watcher can briefly leave old display information
visible, but cannot authorize a stale edit. Merely rebuilding a list must not hash the model's
complete source closure.

### Resume after commit/build/test authorization

Commit only the described owner files and tests, in separate owner commits. Forward-merge
persistence into hierarchy and Cross sections, then hierarchy into anchors, then anchors into
contextual insertion. Integrate those owner heads using the documented incremental workflow;
do not copy patches into the old profiling checkout or merge it backwards. No compiled binary
contains this pass yet.

Source tests added/extended, **not run**:

- `TestBackgroundEvaluation::parsedLibraryReuseTracksBytesAndInspection`: repeat hit, same-size
  disk edit, dirty library buffers, cancellation, Inspector on/off, failed parse recovery,
  retained old-result independence and semantic tracing while Inspector is off.
- `TestBackgroundEvaluation::parsedLibraryReuseTracksSearchesAndConfiguration`: new local
  shadowing file, definitions, feature snapshot and root changes.
- `TestDesignObjects::publicationUsesDisplaySnapshotButEditsCheckDisk`: UI synchronization before
  a pending watcher event, with immediate rejection of an edit against changed disk bytes.
- `TestAnchors::includedOwnerAndRetainedResolverGuards`: list/Inspector refresh uses the displayed
  snapshot while strict resolver/action checks reject changed included bytes.

Use the profiles in `workflows/testing.md` once authorized; these existing GUI suites require
desktop authorization. Reprofile initial and unchanged Preview with the corrected event-driven
helper, Inspector off/on, identical resource limits and CSG equivalence checks. Confirm warm
library parse counts and publication validation counts, not just wall-clock improvement.
The smaller instantiation/lookup and detached-agent-tree costs were not changed by this pass.

Direct prerequisite pins at this checkpoint:

- Persistence: source editing `0bcafded2a98d98802a8e869e44a658770ebc3b4`, Inspector
  `7a1149b788ab57e90e800c1c7fc0f18313fe7190`, Customizer
  `d77244154cc2c84a26a8a5fdb1ec20ce4a335b7f`, background
  `737865b6931676b5095eec15bab053bb0a366c72`.
- Hierarchy: provenance `e29b95914c2fc4ca1715f4d5e465203fdb23a8a6` and persistence HEAD above.
- Anchors: hierarchy HEAD above.

All three heads pin MCAD `1ea402208c3127ffb443931e9bb1681c191dacca`, Clipper2
`c7f820f6a03fa91f189b866d27bf40dfe47abaa6`, OpenCSG
`9bf122715213dca05e70993dd8672fe3aa36c518`, manifold
`0edd9d54876f3135e431575214dd6d8a72866fee`, mimalloc
`30b2d9d89099bee08e9f67a1ffb3e12e7ba45227`, sanitizers-cmake
`bcb1fc68616e9645ca5acea2992412606373ab04`. Existing generated Clipper2 modifications
in persistence/hierarchy are unrelated; no submodule source or revision was changed here.

## Repairs built and reprofiled (2026-10-08)

The later authorized measurement pass supersedes the preceding **not built / tests not run**
checkpoint for the diagnostic composition only. Owner changes remain uncommitted, unmerged and
unpromoted; accepted dependency pins and installed releases have not changed.

Full evidence and reproduction commands:
[cache-repair profile](../../../runs/background-cache-profile-2026-10-08_05-42/report.md).
Candidate base `bab2342faeca7d0af2ac2f8227d36f5b8fafc7cf` includes the newer native consumer
repairs. An isolated source archive overlays the three owners' exact selected working files,
after verifying ancestry and unchanged base versions. This is not the entire release stack.
The same pinned upstream `f65fe98dd007f1ed7482bd5420392917c040c80d` and shared Release toolchain
are used. No maintained branch received copied patches or profiling instrumentation.

The build needed one owner repair: `EvaluationPipeline.cc` must include `openscad.h` for
`commandline_commands`. That include is now present in the hierarchy owner's working file.
The application then built successfully and all four listed focused regression cases passed
through the desktop profile runner. This does not establish full-release acceptance.

With Inspector preparation off, five measured processes per condition plus warm-up give:

| Preview | Upstream | Fixed candidate | Remaining regression |
| --- | ---: | ---: | ---: |
| Initial | 4.622 s | 4.905 s | 6.1% |
| Unchanged | 2.124 s | 2.694 s | 26.8% |

All 72 main-series Previews have identical CSG hashes and no detected contention. Instrumented
and uninstrumented timings differ by roughly 1–2%. The prior pair was 2.42x on unchanged
Preview; the new pair is 1.27x, but the newer base means this is not a controlled before/after
of only two patches.

Verified repair effects: **13 reused libraries, zero warm library reparses; zero strict binding
validation calls during publication**. Strict source-action checks still pass their regression
cases. Cache-wrapper copying costs only 0.14 ms in a separate detailed series.

Remaining work, ordered by measured evidence:

- Language instantiation is approximately 235 ms slower. Sampled captured-library lookup
  explains approximately 129 ms of that, nested within instantiation. The remaining language
  gap needs finer attribution. Inspect the extra path-map lookup in `SourceFileCache::lookup`.
- Agent inspection snapshot preparation plus retention costs approximately 93 ms even with
  Inspector preparation off and HTTP access disabled. HTTP publication itself is negligible.
  This is separate from optional Inspector provenance; demand-driven snapshots are a potential
  improvement if their API/annotation behavior is preserved.
- Exact-byte capture/checking costs approximately 55 ms for reuse eligibility, 32 ms at worker
  completion and 31 ms in the asynchronous pre-publication validator. Include/use lookup
  validation adds approximately 15 ms. They cover different race boundaries; removing one
  blindly would reintroduce stale-publication or cache-reuse errors.
- Root parsing and CSG generation are already close to upstream. Semantic discovery/finalization
  is approximately 15 ms. Do not prioritize geometry cutting/rendering based on this profile.

Phase timers are inclusive and median observations; do not sum nested values. Raw
`libraries_reused.ms` is a numeric count gauge, not milliseconds. The separate detail series
excluded one contended warm-up and waited for an unrelated Visual Studio compiler to finish;
the user application was not stopped.

Inspector-on follow-up: three measured processes per build plus warm-up, 24 matching Previews.
Candidate first/repeated Preview is **5.616 / 2.829 s**, paired upstream **4.529 / 2.111 s**.
The primary Inspector-off profiled series is **4.976 / 2.637 s**: enabling preparation adds
approximately **0.64 s initially and 0.19 s on repeat** on this model. These are separate
series with about 1% upstream drift, not a precise interleaved on/off experiment. All 13
libraries are still reused, with no strict GUI publication validation. This measures the
always-prepare setting, not on-demand activation or Inspector interaction. Across main,
detail and Inspector-on series, 120 accepted Previews have identical CSG hashes.
