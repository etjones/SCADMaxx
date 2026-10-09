# Background evaluation implementation plan

Status: Windows build and focused validation recorded, 2026-10-07; in progress, not integration-ready.
See [the implementation record](4_imp-phase1.md) and [handoff and remaining work](5_post-implementation-notes.md).
The source checkpoint does not establish that the phase exit criteria below pass.
Behavior and scheduling policy live in [requirements](2_requirements.md); inspected source is recorded in
[the exploration](1_exploration.md#source-investigation--2026-10-07).

## Architecture

Use an application-owned controller and one long-lived evaluation worker. The controller owns the job queue and
all UI/document associations; the worker accepts plain captured data and produces owned CPU results. Preview and
Render share this path, including their initial parse and language evaluation. Replace the old F6 worker path
once migrated; do not retain two independent production evaluators or a synchronous GUI fallback.

```text
GUI: capture request -> queue/coalesce -> show progress -> validate delivery -> install -> first frame
                           |                                 ^
worker: admit -> parse/dependencies -> parameters -> language -> CSG or final geometry -> detach metadata
           cancellation token checked throughout              |                    |
                  queued progress/diagnostics ----------------+------ owned result-+
```

Proposed types under `src/core` and `src/gui/evaluation` (final names can follow local conventions):

- `EvaluationRequest`: job/document/window IDs, lifetime and request generations, source snapshots, parameter
  values, explicit/automatic cause, Preview/Render mode, definitions, features, backend, time, camera and options.
- `EvaluationJobContext`: atomic cancellation token, stage/progress sink, bounded diagnostic accumulator,
  terminal status, timings and scoped native configuration. Cancellation has its own exception/outcome, never
  a synthetic parse error, empty-success result or generic failure.
- `EvaluationResult`: owned AST/library/context backing, absolute/effective root and Tree, sealed consumed
  inputs, CSG products or final geometry, plain parameter descriptors, source indicators/completion symbols,
  detached inspection metadata and optional script-camera request. No borrowed `MainWindow::tree` or QWidget.
- `EvaluationService`: one process-wide admission point; the GUI-side controller manages jobs while one worker
  computes. Existing semantic mesh/export/draft/HTTP parse tasks sharing native state must participate or acquire
  the gate cancellably in the background. Keep their domain-specific result and mutation contracts.

State transitions are `Queued -> Running(stage) -> Ready -> Installed/Deferred`, with terminal `Failed`,
`Cancelled` and `Superseded` paths. Cancellation may intervene in Queued, Running or Ready; the GUI publication
generation check resolves completion-versus-cancel races. Each admitted job produces exactly one terminal record.

## Capture, computation and publication

Capture plain editor text and identities on the GUI thread, once per snapshot. Existing source revision hooks
can support immutable document mirrors if whole-buffer copying exceeds the budget; verify every edit/undo/reload
path before trusting a mirror. Resolve/hash large source inputs in the worker. Capture settings explicitly rather
than reading live preferences during work. Serialize native settings/cache maintenance with jobs; rendering may
continue only against frozen data and rendering-safe settings.

The worker uses `EvaluationInputs`, a request-local `SourceFileCache`, and `NativeEvaluationScope`. Preserve dirty
dependency precedence and load `use` dependencies before constructing the dynamic Customizer context. Parameters
must be resolved and applied before root instantiation, in the same order as the accepted synchronous behavior.

Split the Customizer into a plain computation model and a GUI adapter. Evaluate defaults, types, dynamic attributes
and imported preset/captured values in the worker; return descriptors and effective values. The GUI builds/updates
widgets without evaluating ASTs. Slider changes update captured values immediately and schedule coalesced reactive
metadata work even when automatic geometry Preview is disabled. Apply a descriptor result only to its captured
source/parameter generation; it must never overwrite a newer edit or emit a recursive preview request.

Prepare inspection/provenance and immutable consumer data before handing the result over. Make all expensive
final geometry evaluation and CPU conversion explicit, including deferred Manifold work. Audit renderer construction,
tessellation, bounding-box calculation and first-paint preparation so they do not secretly repeat CPU computation.
Renderer/OpenGL resource creation, installation and destruction stay on the GUI thread with the right GL context.

Before delivery, compare consumed disk bytes in background validation and capture the live editor revision table
on the GUI thread. Publication rechecks cancellation, owner lifetime, latest request/configuration, editor revisions
and watcher epochs. If an epoch changes during validation, reject or revalidate asynchronously. Disk validation is
a sampled observation, not an atomic filesystem transaction; preserve exact strict action validation, including
its delayed-watcher checks. Where an action needs expensive validation, complete it asynchronously and recheck its
generation before mutation. Never substitute a display-only freshness check for action authority.

Install renderer, retained scene, identities, diagnostics summary and consumers through one controlled publication
boundary. Do not emit consumer notifications halfway through the swap. Navigation during work keeps the current
camera under the requirements' rule. If the owning document is inactive, defer CPU output within the stated budget;
install only after activation and revalidation. If another deferred result replaces it, retire the older one.

Retain the last good display until installation succeeds. Mark it stale on input changes or when it cannot satisfy
the current request, without calling disk hashing during paint. Clear only on a successful empty result or normal
document lifecycle. Release large obsolete CPU graphs away from the GUI where safe and under native ownership rules;
never transfer GL or QObject destruction to that cleanup path. Account for active, displayed and deferred memory.

## Cancellation, locking and diagnostics

Cancel sets an atomic token directly; it must not rely on a worker slot queued behind long computation. Keep token
polling independent of the throttled progress channel. Use a typed cancellation exception and RAII restoration.

Add bounded checks at lexer/input chunks (including long tokens/comments), dependency loops, function/module entry,
tail-call loops, comprehensions, control loops, costly vector/builtin operations, node traversal, CSG normalization
rewrites/product import, and geometry operation boundaries. Poll before and after external I/O/backend calls.
Audit existing `catch` clauses so they propagate cancellation rather than convert it to a warning or `undef`.

Parser cancellation must release lexer buffers/files, partially allocated semantic values and scope/root state.
Review generated Bison/Flex unwinding before selecting exceptions versus an explicit parser abort; do not assume
an outer `catch` releases the parser's internal allocations. Verify cancellation followed by a clean parse and
repeat cancellation memory behavior. Partially computed cache entries must not be published as completed values.

Eliminate GUI acquisition of the native mutex from parsing, parameter updates, syntax inspection, cache actions,
exports and completion callbacks. Non-evaluation interactions remain independent. Adapt the guard for cancellable
background waiting where external consumers still use it, preserving recursive entry and stack checks. Do not
busy-spin or require a queued UI response while holding the gate.

Replace global progress/diagnostic routing with scoped job/thread state and audit every read/write, including CLI
and non-worker UI logging. Thread-local state alone is insufficient if backend callbacks run on other threads:
pass job context explicitly to callbacks or marshal them safely. Preserve CLI output and warning semantics.
Progress is coalesced; diagnostics use bounded batches tagged by job/document and sequence. Completion carries
authoritative counts and a final sequence marker so a delayed message cannot change another attempt's success.

Replace per-window worker destruction/join with application-owned shutdown: refuse new work, cancel, disconnect
window delivery, keep the event loop alive, then destroy the stopped worker. Display a cancelling/shutdown state
for long library calls. No `terminate()`, unsafe detach, or process exit while caches/threads are still in use.

Qt references: [thread affinity and queued delivery](https://doc.qt.io/qt-6/threads-qobject.html),
[QThread interruption and lifetime](https://doc.qt.io/qt-6/qthread.html). Use APIs supported by the pinned Qt build;
newer documentation is not authorization to upgrade dependencies.

## Ownership and prerequisites

The [freshness/Customizer owner repairs](../../../experimental/repairs/gui-freshness-performance.md) are now
committed. On 2026-10-07 the user clarified that background-evaluation work can proceed before their validation.
Separate prerequisite validation is not an implementation gate. Include the committed fixes through normal
forward merges, retain their identities, and validate their regression cases with this feature when authorized.

Observed committed checkpoint:

- Inspector freshness fix: `b93c9c219198630a2fde3822f2b90c29d88d9180`.
- Customizer dependency-order fix: `13697aa98f18e1d1b26187d2cf5a253e8b6dce07`.
- Persistence with forward merges: `a004cbad1907664306d1aab0d0a1a38b6e3e991c`.
- Hierarchy with forward merges: `72730cb9b70a9c712ed91c3e7581c392f1d624c0`.

These commits are not claimed as validated. Retain a reproducible prerequisite-only source checkpoint so later
failures can be attributed to the prerequisites or this refactor; preserve the last validated runtime separately.
When implementation is requested, use a dedicated `feature/background-model-evaluation` checkout from the captured
evaluation owner, with the required dynamic Customizer owner merged normally. Resolve current pins from
`experimental/DEPENDENCIES.json`; the inspection SHAs are not a future base-selection instruction.

Generic captured-input/lifetime/guard changes belong in Inspector, generic dynamic parameter separation belongs
in the Customizer owner, and generic annotation/HTTP lifecycle hooks belong in the HTTP owner. New background
orchestration and cancellation behavior belong in this feature. Keep owner interfaces data/callback based so
HTTP does not gain a reverse dependency on Inspector, and foundations never depend on their new consumer.
Merge generic owner changes forward; no copied foundations, cherry-picks, or integrated-build ancestry as a base.

Provenance, persistence, hierarchy, anchors, insertion, clipping, Vim and geometry bounds are integration consumers,
not reasons to base this feature on the entire release. Add an actual prerequisite only when its interface is
needed. Source changes for consumer adaptation stay in the relevant owners and are composed explicitly.

The performance plan is a validation prerequisite: its CLI phase exists, while GUI lifecycle support is incomplete.
Add maintained native timing hooks that can measure the synchronous baseline before changing execution. Reuse these
hooks for the async candidate; there is no dependency on unfinished evaluator-speedup experiments.

## Implementation phases and exit evidence

| Phase | Work | Exit evidence when builds/tests are authorized |
|---|---|---|
| 1. Freeze baseline and contracts | Include committed prerequisite repairs without waiting for separate validation; capture exact source/build inputs; add lifecycle timestamps and request/result ownership. Extract compute from MainWindow initially with matching behavior. | When validation is authorized, compare prerequisite-only and refactored behavior; baseline includes native first-frame and event-loop observations; no borrowed window tree in request/result contract. |
| 2. Separate native and GUI state | Split Customizer computation, snapshot settings, scoped progress/logging and metadata preparation. Audit all native gate callers and renderer CPU work. | Fresh dirty `use` fixture, presets and reactive controls match; thread-affinity assertions pass; no UI method is needed from compute. |
| 3. Introduce shared scheduler | Move startup/open/F5 and F6 end to end; implement coalescing, explicit/automatic arbitration, result ownership and cancellation-aware native admission. Replace old GeometryWorker path. | Slow parser/language and final geometry keep UI interactive; cross-window requests serialize; cancellation while queued works. |
| 4. Complete cooperative cancellation | Instrument supported stages, parser cleanup, exception propagation, external call boundaries and shutdown. Retire obsolete processEvents-based evaluation paths. | Cancel-at-stage tests recover with a successful next job; latest-request races and window/application closure complete safely. |
| 5. Publish and integrate consumers | Atomic renderer/scene/metadata delivery, inactive-document deferral, strict freshness, camera behavior, annotations/HTTP parse jobs and downstream feature adapters. | No wrong-document/stale installation; old model stays navigable; feature interactions and dynamic Customizer work in the actual composition. |
| 6. Validate and hand off | Extend the shared performance runner with native responsiveness/cancel/first-frame metrics; compare baseline/candidate and inspect memory. Record exact source and evidence. | Acceptance matrix below passes within declared limits; cancellation gaps are measured; post-implementation notes distinguish local validation from promotion/release. |

Phase 1's synchronous extraction is an implementation checkpoint, not a retained runtime compatibility option.
Runtime evidence can be collected in a later authorized validation pass; its absence does not block source
implementation of subsequent phases. Preserve reproducible checkpoints rather than treating unrun checks as passed.
Do not ship partial async F6 while leaving parsing/language/Customizer work on the event loop.

## Validation matrix

- Deterministic scheduler tests: explicit F5/F6 supersession, automatic request coalescing, fairness, Cancel versus
  completion, input changes, queued native-lock contention, inactive results and owner destruction.
- Cancellation fixtures: huge parse/long token, nested include/use, recursion/tail recursion, list comprehension,
  large builtin work, CSG normalization and geometry. Follow every cancel with an ordinary successful job.
- Numerical/language comparison: same parameters and backend, semantic/ordinary models, diagnostic ordering,
  hard warnings, empty results and geometry bounds. Use both supported Manifold/CGAL configurations as applicable.
- Native UI: cold application open, warm F5, Customizer edits with auto-preview on/off, F6, repeated cancellation,
  navigation during work, two tabs/two windows, unsaved input closure, file replacement and shutdown during a job.
- Adversarial delivery: change bytes with preserved timestamps before watcher delivery; source edit/undo, preset,
  included dirty buffer or window closure between validation and install. Cancelled partial geometry never installs.
- Feature composition: annotations and HTTP syntax inspection, selection/provenance, model hierarchy, section
  display, source transactions, drafts/commit, exports and Vim editing. Every action still enforces its own guards.
- Performance: reuse `experimental/performance` corpus plus the explicitly configured local `module_plus.scad`;
  record parse/language/CSG/backend time, queue time, snapshot/publication/first frame, heartbeat latency, Cancel
  acknowledgement versus worker stop, peak memory and repeated-run retention. Separate indivisible-call latency.
- Flood and lifecycle stress: many echoes/warnings, rapid edits, large obsolete result cleanup, repeated open/close,
  cache flush requests and multi-window exit. All jobs terminate once, with no unbounded queue or retained graphs.

Keep source checks and documentation review separate from actual runtime evidence. Planning does not authorize a
build or test run. The next implementation request should explicitly include builds/tests if phase exit validation
is wanted in the same pass, as required by the workspace instructions.
