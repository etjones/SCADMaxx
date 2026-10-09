# Background evaluation requirements

Status: proposed implementation requirements, 2026-10-07. The requested outcome is a responsive window with
cancellable evaluation. Scheduling and quantitative targets below are recommended defaults, not measured results.

## User-visible behavior

1. Startup/open-triggered evaluation, F5 Preview and F6 Render run parsing, dependency loading, language
   evaluation and CPU geometry/CSG preparation without blocking the GUI event loop.
2. Editing, camera navigation, tab/window switching and Cancel remain usable. Retain the last successful model
   during work, failure and cancellation, visibly identifying its owner and outdated state. First evaluation
   shows an empty usable viewport. An empty successful model deliberately replaces the previous result.
3. Show queued, current stage, cancelling, succeeded, failed and cancelled states. Show numeric progress only
   when meaningful. A superseded job has a distinct internal terminal outcome and never appears successful.
4. A cancelled or obsolete job cannot publish geometry, camera changes, Customizer state, diagnostics into
   another attempt's console, source indicators, completion data or feature metadata.
5. Cancel immediately acknowledges the request and removes the same document's pending replacement. Actual
   stopping is cooperative. Display "Cancelling" while an indivisible library call or I/O operation finishes.
6. Preserve existing preview triggers, presets, dynamic parameter behavior, `$preview`, `$t`, camera variables,
   command-line definitions, backend selection, hard warnings and source diagnostics. Source edits alone do
   not enable automatic Preview. Existing automatic-preview, reload and animation requests use the service.

## Recommended scheduling rules

| Event | Required policy |
|---|---|
| Several native jobs | One active native evaluation per process; other windows remain interactive. Independent OpenSCAD processes are unaffected. |
| New explicit F5/F6 for the same document | Latest explicit intent wins, including a mode change; cancel the active older job and keep only its newest replacement. |
| Timer-triggered Preview while explicit Render is queued/running | Do not displace Render merely because a timer fires. Changed actual inputs invalidate old work; any new request follows the existing trigger policy. |
| Repeated automatic requests | Coalesce by document and input/configuration identity; no unbounded frame or slider queue. |
| Different documents/windows | FIFO among ready documents; replacing a pending request keeps its queue position. Explicit work precedes automatic work; round-robin automatic work prevents one animation monopolizing the service. |
| Tab switch | Do not publish into another document's viewport. Let work finish for its owner and retain at most one deferred completed result per window; validate again on activation. Evict older deferred results without starting work automatically. |
| Edit/preset/dependency/configuration change | Invalidate affected results and cancel obsolete computation. Preserve current triggers rather than scheduling an unsolicited replacement. |
| Explicit Cancel | Cancel the targeted document's active/queued work. Suppress automatic retries for that unchanged request; a new explicit request or genuine input change permits a later request. Pause that document's animation on Cancel. |
| Close document/window | Drop queued work, signal active cancellation, detach delivery and retire deferred results. No late callbacks may touch destroyed UI. |
| Exit application | Stop admission, cancel all jobs and finish worker cleanup before exit. Keep a responsive shutdown state while an uninterruptible operation finishes. |

Navigation after submission must not cause the finished job to restore an obsolete camera. If the script sets a
camera, apply its requested camera only when the user has not navigated since submission. Captured camera variables
remain part of the evaluated input; navigation does not by itself start another evaluation.

## Correctness and resource requirements

- Each job owns immutable root/open-editor snapshots, stable document/window identities and generations,
  parameters, render variables, options, and its cancellation token. Worker code never reads live editor widgets.
- Capture dirty include/use buffers and canonical source identities through the existing captured-input system.
  Discover disk dependencies in the worker, retain the exact bytes consumed, and seal the set before publication.
  Preserve existing import/font/resource behavior; do not claim source snapshots make external resources immutable.
- Publish geometry, backing AST/context lifetime, result/configuration identity and feature metadata consistently.
  Stale visible geometry cannot authorize picking, source edits, exports or draft commits against newer inputs.
- Failed and cancelled work must unwind parser/native scopes, restore settings/logging, and leave caches usable.
  The next ordinary model must succeed after cancellation in every supported stage.
- Bound pending jobs, retained results and diagnostic queues. Batched UI output may summarize a diagnostic flood
  with an explicit count; preserve error/warning totals and the job's outcome independently of UI delivery timing.
- Use the shared native gate until all relevant state is demonstrably independent. The event loop must never wait
  for that gate, a running worker, filesystem hashing or a blocking worker-to-UI callback.
- Preserve optional build configurations. Audit Python-enabled execution separately before claiming its cancellation
  coverage; Python callbacks/locking are not covered by native SCAD checkpoints. Never silently run it synchronously.

## Acceptance targets and limits

On the agreed Windows reference machine, target a 50 ms GUI heartbeat with p95 delay below 100 ms and no gap above
250 ms during controlled CPU fixtures; target visible Cancel acknowledgement within 100 ms. Target worker stop
within 250 ms in instrumented parser/interpreter/normalization fixtures. These are initial engineering targets:
record the actual distributions and investigate misses rather than silently widening limits.

Measure native-library/I/O stopping separately, without a false hard deadline. Record GUI snapshot, publication,
GPU upload/first frame and shutdown times separately. No claim that background execution speeds computation up.
Use the performance suite's existing per-case policy for elapsed-time regressions and equivalent-output checks.

Guaranteed termination inside arbitrary library calls, concurrent independent evaluators, incremental evaluation,
GPU rendering redesign, and changing startup reopen policy are outside this first implementation. A worker-process
design is the escalation if measured cooperative stopping cannot meet the user's actual workflow.
