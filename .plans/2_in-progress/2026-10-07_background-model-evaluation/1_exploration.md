# Background model evaluation and cancellation

Status: in progress. Source investigation and implementation planning expanded on 2026-10-07;
implementation has not started. See [requirements](2_requirements.md) and [implementation plan](3_overall-plan.md).

## User intent

Evaluate the model in the background both when opening it at startup and on subsequent Preview/Render requests,
so the UI remains responsive and the user can cancel expensive work. Record this as a separate feature.

The following design is the analysis requested for this feature, not a completed implementation or measured speedup.

## Current behavior and evidence

Inspection of the semantic-hierarchy checkout found:

| Stage | Current execution |
|---|---|
| Parsing, loading dependencies and evaluating SCAD code | UI thread |
| Generating and normalizing F5 preview CSG products | UI thread |
| Computing F6 final geometry | Existing `GeometryWorker` thread, after synchronous initial evaluation |
| Installing the result and drawing the viewport | UI/OpenGL thread |

Consequently, F6 can block before its worker starts, and F5 can block throughout most computation. Calls to
`processEvents()` offer intermittent responsiveness and reentrancy hazards; they do not provide background execution.

Relevant source entry points, verified during the analysis:

- [MainWindow.cc](../../../../wt-openscad-semantic-model-hierarchy/src/gui/MainWindow.cc): `compile`, `compileDone`,
  `instantiateRoot`, `compileCSG`, `actionRenderPreview`, `cgalRender`, `report_func` and `consoleOutput`.
- [GeometryWorker.cc](../../../../wt-openscad-semantic-model-hierarchy/src/gui/GeometryWorker.cc): existing F6 worker,
  including cancellation exceptions and forcing deferred Manifold evaluation before result delivery.
- [NativeExecutionGuard.h](../../../../wt-openscad-semantic-model-hierarchy/src/core/NativeExecutionGuard.h): shared
  recursive lock for parser/evaluation/cache state.
- [progress.cc](../../../../wt-openscad-semantic-model-hierarchy/src/core/progress.cc): process-wide progress callback,
  counters and userdata. Current GUI callback accesses the progress widget; this is not a suitable worker-job contract.
- [EvaluationBinding.h](../../../../wt-openscad-selection-model-inspector/src/gui/selection/EvaluationBinding.h):
  captured inputs, retained result ownership, document/revision stamps and strict freshness checks.

See [the performance investigation and repair history](../../../experimental/repairs/gui-freshness-performance.md).
Repeated GUI freshness checks and Customizer dependency ordering have committed, unvalidated fixes. Background work
complements those fixes; it does not replace them or justify restoring the diagnostic freshness bypass.

## Recommended design

Use one serialized background evaluation service, shared by initial preview and subsequent evaluations. Reuse the
native execution gate initially; concurrent independent evaluators are outside the first scope.

1. On the UI thread, capture editor buffers (including dirty dependencies), parameter values, settings and request
   identity. Capture data without retaining worker access to mutable widgets or `MainWindow` fields.
2. In the worker, parse, resolve dependencies, evaluate the language and prepare the CPU-side preview products or
   final geometry. Preserve the captured source/semantic/provenance information needed by the current features.
3. Keep the last successful model visible. Allow editing, navigation, tab switching and cancellation. On initial
   startup, show an immediately usable window with an empty viewport until the first successful result arrives.
4. Deliver progress and diagnostics through queued messages carrying document and job identities. Publish completed
   results on the UI thread only if the owner still exists and the request, inputs and parameters remain applicable.
5. Supersede obsolete work: signal cancellation and retain only the newest pending request for that document.
   Explicit Cancel removes its pending replacement as well; it must not immediately restart the cancelled work.

The recommended request policy is specified in the requirements, including arbitration across documents/windows
and Preview versus Render. Source edits invalidate results but do not introduce a new automatic-preview loop.
Snapshot capture and final publication must stay short; hashing dependencies or destroying large obsolete results
must not simply move the freeze to a different UI callback. Keep retired computation-owned data cleanup off the UI
thread where safe. Qt widgets and viewport OpenGL installation/drawing retain their appropriate thread ownership.

## Main implementation difficulties

- **Shared native state:** parser state, caches, settings, progress and diagnostics must have explicit ownership.
  A worker holding `NativeExecutionGuard` is insufficient if Customizer or another UI action blocks acquiring it.
  Queue evaluation-dependent work; navigation, editing and cancellation must not wait on that gate. Cancellation
  must also work while a job is waiting for the evaluator, rather than getting stuck in an uninterruptible lock wait.
- **Customizer coupling:** separate computation of parameter metadata/reactive values from widget construction and
  application. Preserve `use` dependency ordering, captured dirty buffers, presets and parameter application order.
- **Lifetime and identity:** closing a tab/window, replacing a document, changing an included file, or requesting a
  newer evaluation must not publish stale geometry, diagnostics or Inspector metadata into the wrong document.
  Preserve strict action validation; an old model can remain visible without authorizing edits against stale input.
- **Cancellation coverage:** replace GUI-widget polling with a thread-safe job cancellation token. Add bounded
  polling to parsing, interpreter loops, dependency work and CSG preparation where necessary. Emit progress without
  touching widgets from workers, and prevent unbounded queued console messages from saturating the UI.
- **Result handoff:** build CPU data in the worker, then install the renderer and associated feature snapshots as one
  consistent result. Avoid discarding the old renderer at job start. Account for peak memory while both results exist.

## Cancellation guarantees and process alternative

Responsive cancellation and immediate termination of computation are different guarantees. The UI can acknowledge
Cancel immediately, retain the previous model and reject the cancelled result. The worker stops at its next safe
cancellation point. Long indivisible Manifold/CGAL or other library operations may delay the actual stop and therefore
delay a queued replacement job. Measure and report cancellation latency separately from UI acknowledgement.

Do not forcibly terminate a thread that may own native locks or partially modified caches. If a later requirement
demands guaranteed termination during arbitrary library calls, investigate a separate worker process. That allows
discarding the process, but requires an explicit transport for geometry, source/provenance and semantic metadata,
dirty buffers, progress and errors, plus worker restart/cache policy. It is substantially more work than a thread.

Recommendation: begin with a worker thread and cooperative cancellation, with clear coverage and latency limits.
This is a medium-to-large architectural feature, requiring several implementation/validation stages. It improves
responsiveness; it does not inherently shorten evaluation time or fix slow viewport GPU drawing.

## Proposed implementation stages and ownership

1. Extract immutable evaluation request/result types and computation from `MainWindow`, preserving synchronous results.
2. Route startup/F5 evaluation through the serialized worker and atomic result publication; adapt Customizer and logging.
3. Add cancellation, supersession, close/shutdown handling and shared scheduling with the existing F6 path.
4. Integrate downstream consumers and validate correctness, responsiveness, cancellation latency and memory behavior.

Create a dedicated source branch/worktree when implementation is requested. Determine its base from the maintained
dependency DAG, using the captured-evaluation owner as a foundation rather than an integrated all-features branch.
Generic changes to existing foundations belong in their owners and arrive through normal forward merges. Dynamic
Customizer and semantic/provenance/persistence consumers need explicit integration coverage without adding circular
dependencies. Do not copy prerequisite implementations or cherry-pick fixes across owners.

This does not depend on the unfinished evaluator-speedup experiment or reopening the last-used model. If startup
reopening later requests Preview, it should call this same evaluation service. Include the committed freshness
and Customizer fixes before implementing overlapping changes; separate prior validation is not a prerequisite.

## Acceptance scenarios for later validation

Use the [integration performance regression suite](../2026-10-07_render-performance-regressions/1_exploration.md)
to establish a baseline before validating this refactor. Keep total computation time, first-frame latency, UI
responsiveness and cancellation latency separate so moving work to a thread cannot conceal extra computation.

- Startup/open, F5 and F6 keep the window responsive during parsing, language evaluation and geometry computation.
- The real `module_plus.scad` case and synthetic long interpreter/CSG cases exercise more than the final mesh stage.
- Cancel works in each supported stage and while queued; cancelled jobs never publish partial or obsolete results.
- Repeated Preview requests coalesce; editing, parameter changes and dirty include/use buffers preserve exact inputs.
- Tab/window closure, switching documents, new requests and dependency changes during completion reject stale delivery.
- Old geometry stays navigable during computation; failed/cancelled jobs preserve it with correct stale-action guards.
- Customizer, annotations, HTTP evaluation requests, Inspector, model structure and cross sections remain consistent.
- Source warnings, errors, provenance, semantic metadata and resulting geometry match the synchronous baseline.
- Long library calls have measured cancellation latency; diagnostics/progress and result installation do not freeze UI.
- Shutdown does not deadlock, leak live jobs or silently publish after cancellation; repeated runs have bounded memory.

No source edits, new worktree, build, tests or selected release-stack changes are part of this planning item.

## Source investigation — 2026-10-07

Read-only inspection used the captured-evaluation owner at `335a5762cc2fa18124b1ced717e60771c6164c5b`,
dynamic Customizer owner at `306c92d39c4cbb7fe82981e179161aa85d44774e`, and semantic consumer at
`49b30bae3cac3d148a1fefc0604c13e089b4c8d6`. All had pending changes at inspection; these SHAs identify their bases,
not a frozen identity of the inspected working files. No source checkout was changed by this investigation.

The freshness/Customizer repair handoff remains relevant as historical evidence. The subsequent committed
checkpoint is recorded in the implementation plan; include it ahead of overlapping background-evaluation changes.

| Verified source boundary | Consequence for implementation |
|---|---|
| `MainWindow::compile`, `parseDocument`, `instantiateRoot`, `compileCSG` | Parsing, language execution, parameter setup and preview preparation currently call into widgets and shared window fields. Extract computation before scheduling it. |
| `instantiateRoot` and `cgalRender` clear renderer/tree members | Retaining the old model requires separate candidate ownership, not just moving the existing function to a thread. |
| `GeometryWorker::start` stores `const Tree*`; its destructor calls `wait()` | Existing F6 worker is not a reusable document-independent job. Replace its mutable-window lifetime dependency and avoid joining a running worker in window destruction. |
| `NativeExecutionGuard` uses a blocking recursive mutex | Cancellation cannot interrupt waiting for this lock. Use one scheduling owner and cancellable acquisition for remaining external native workers; UI callbacks must never wait on it. |
| `progress.cc` keeps global counters/callback/userdata; `report_func` reads `ProgressWidget` | Progress and cancellation must become job scoped. Checking Cancel must be independent of progress throttling and widget access. |
| `printutils.cc` and `ScopedOutput` use shared mutable handlers and warning state | Serial native jobs alone do not isolate UI logging. Establish thread/job-local routing and pass immutable diagnostic context in queued batches. |
| `EvaluationBinding::capture` copies editor contents; `inputsCurrent` hashes editors and reads disk | Reuse source ownership, but audit capture cost and move large hashing/disk validation off the event loop without weakening strict action guards. |
| Dynamic `ParameterWidget::setParameters` constructs `CustomizerContext`; `updateParameterStates` evaluates attributes | Split parameter computation from widget updates, including slider edits with automatic preview disabled. A QWidget method must not remain the native evaluation entry point. |
| `AnnotationController::finishEvaluation` runs `inspectModel` in `NativeEvaluationScope` | Prepare detached inspection/provenance data inside the job, before publication. Otherwise the completion callback can still block on native work. |
| `parse()` has explicit lexer/scope cleanup for captured-input exceptions | Add cancellation through a cleanup-safe path. Simply throwing from the lexer can leave global parser state or allocations behind. |
| Interpreter loops and CSG normalization have no general job cancellation contract | Instrument language loops, tail calls, dependency reads and normalization, not only geometry progress callbacks. |
| Semantic mesh/export jobs already acquire the native gate | Bring these jobs under shared arbitration or cancellable acquisition; do not let them strand Cancel or make UI actions wait. |

`StackCheck` is already thread-local in this owner; retain initialization and sufficient worker stack size.
The current HTTP interface exposes inspection/history but cannot trigger evaluation. Its parse path also calls
native parsing from the GUI bridge. Migrate that path to asynchronous completion; do not assume an evaluation
HTTP endpoint exists or add one solely to make a benchmark easier.

The [performance suite's CLI phase](../2026-10-07_render-performance-regressions/5_post-implementation-notes.md)
is now implemented and verified; native GUI measurements remain open. Use its maintained fixtures/runner and
add native lifecycle measurements rather than reviving the removed diagnostic GUI probes.

Qt's [thread ownership rules](https://doc.qt.io/qt-6/threads-qobject.html) require widget operations on the GUI
thread. [QThread](https://doc.qt.io/qt-6/qthread.html) provides queued delivery and cooperative interruption;
`quit()` alone does not interrupt a long-running function. A cancellation slot queued behind that function
would also arrive too late. Use an atomic token set directly by the controller.
