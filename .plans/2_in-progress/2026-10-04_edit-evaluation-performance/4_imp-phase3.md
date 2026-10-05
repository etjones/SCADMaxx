# Phase 3: transfer function parameter storage

Authorized by "Ok then do the first one": try the parameter-table transfer proposed after phase 2.
Continue feature/edit-evaluation-performance at base 9899c745e47dbf0f48b3ca23562eea31e66f9b82.
Comparison baseline: frozen phase-2 candidate in runs/20261004-evaluation-general-contexts.

## Implementation

A new function body has no lexical variables. Consume the already-built lexical parameter map by moving its
storage, and account for the transferred variables in one batch. Keep special-variable merging through the
existing setter, so inherited values, explicit overrides and accounting retain their behavior.
Leave argument evaluation order, parameter/default binding, tail calls, closures and diagnostics unchanged.
Do not change generic context merging or add argument-vector changes to this experiment.
Retain all geometry operations, including Hull and Minkowski.

## Acceptance

Add a native accounting/merge test and SCAD coverage for defaults, mixed/named arguments, special-variable
overrides, closures and exceptions. Run the unit suite and all configured echo cases against the phase-2
runtime, explicitly separating existing baseline failures. Compare alternating warm and fresh workloads;
validate matching CSG and indexed OFF geometry. Measure language time using separate profiling runtimes.
Keep only a useful, semantically equivalent change. Preserve prior inputs, failed attempts and artifacts.

Run: D:/openscad/runs/20261004-evaluation-parameter-transfer.
Source and run handoff remain local and uncommitted; no promotion or application replacement is requested.

## Outcome

Implemented and retained. Panel language instantiation falls from 720.228 ms to 671.300 ms (6.79%) against phase 2,
with unchanged context counts. All five paired language batches improve. Three alternating uninstrumented pairs
show 8.66% lower local and 3.69% lower global six-frame OFF batch medians; all paired sequences improve, but
sample variation is substantial. Fresh panel OFF medians improve 3.27-9.00%. Brackets show no useful gain: warm
medians regress 1.16-5.30%, and their sub-millisecond language phase increases about 34 microseconds.

All 120 unit cases / 75,789 assertions pass. All 128 echo differential cases match phase 2, including five known
baseline failures; the focused CTest set passes 36/39. Every paired CSG output and all 306 validated OFF meshes
match. New native coverage checks heap accounting, empty transfer and special-variable merging. Two new SCAD
fixtures cover binding, defaults, dynamic scope, closures, order and diagnostics.

The final engine delta against the original base is 36 inserted / 7 removed lines across Context.cc/.h,
ContextFrame.cc/.h and Expression.cc, including retained phase 2. Twenty-five source files and exact runtime
identities are frozen under the run. Temporary profiling code is excluded from the final working source.
See report.md and final-manifest.json for final build/cleanup evidence and replay instructions. This phase is
complete; broader GUI/incremental/GPU research stays in progress. No operation support was removed.
