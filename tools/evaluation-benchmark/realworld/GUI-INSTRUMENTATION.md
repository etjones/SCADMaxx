# Native GUI timing boundary

The CLI stages in this harness are implemented and runnable. Native opening/first-display and warm edit latency
are not yet instrumented. This document defines the next adapter boundary without asserting measurements exist.

Use a matched, optional instrumentation patch on both baseline and candidate source revisions. Keep the
performance optimization delta separate. Never compare an instrumented candidate with an uninstrumented
baseline and attribute all of their difference to the optimizer.

Each JSON event should contain run ID, model ID/hash, build ID/hash, document ID, operation ID, monotonic
timestamp, stage name, start/end, thread ID, cache policy, and preview/full-render mode. Optional counters:
source bytes, expanded nodes, primitive/triangle counts, cache hits/misses/evictions and peak memory.
Write events to a buffered run-local stream outside critical sections. Measure instrumentation overhead.

| Operation boundary | Start | End |
| --- | --- | --- |
| Native open | Explicit open request accepted | Editor contents and Customizer initialization ready |
| Parse | Parser entry | AST available, including includes/use resolution |
| Instantiate | SourceFile::instantiate entry | Complete expanded geometry-operation tree available |
| Preview preparation | CSG/leaf geometry preparation starts | CSG normalization and GPU upload ready |
| First result frame | Explicit preview/render request accepted | First frame of that operation is presented |
| Full geometry | GeometryEvaluator entry | Evaluated geometry available |
| Serialization | Export starts after geometry availability | Stream closed and output validated |
| Edit response | Source/parameter change accepted | First matching-result frame presented |

Include causal operation IDs so a queued paint from an older model cannot satisfy a new request. GPU submission
is not completion/presentation. Record the actual presentation callback and renderer/GPU/driver identity.
Elapsed stages can overlap across threads; report inclusive durations and critical-path wall time separately.

Test cold application open, warm document open, no-change re-evaluation, a declared parameter edit, a source edit,
and restore independently. Arbitrary online files do not share a meaningful editable parameter: edits need
per-model cases and expected geometry effects. Do not manufacture a universal edit by changing `$fn`.

Use the same frozen corpus and correctness comparator. A first-frame image does not certify export geometry,
and STL equality does not certify preview correctness. Retain diagnostics, stale-result detection, cancellations,
timeouts and invalid geometry explicitly. Until these hooks are implemented and validated, native GUI metrics
must remain unavailable in reports rather than borrowing CLI wall times.
