# Phase 2: remove the redundant initial function context

Authorized by "Ok then try the next thing". Continue the existing branch/worktree and frozen upstream base.
Preserve phase 1's source snapshot and binaries; compare the generalized evaluator against that candidate.

## Change and constraints

Replace the sin/cos special case with lazy ownership of the function evaluator's first context.
Built-ins and initial callable lookup use the caller directly. User functions still allocate their parameter/body
context, and tail calls/let expressions retain existing context replacement and dynamic-scope semantics.
Do not copy caller configuration variables on entry: default arguments can evaluate in a defining lexical context
while special variables come from the active dynamic stack. Copy them only when replacing an owned tail context.
Preserve shadowing, anonymous calls, closures, stack checks, exceptions and diagnostics.
Keep full geometry support including Hull and Minkowski. No GPU, approximation or dependency changes.

## Verification

- Add explicit default-argument dynamic-scope, closure, tail-call and general builtin regression cases.
- Compare deterministic language outputs against the preserved phase-1 candidate and original baseline.
- Build with the same Windows repairs, compiler and shared dependencies; reuse the incremental build directory.
  Frozen phase-1 runtimes and evidence remain untouched.
- Run unit and language checks, then alternating paired fresh/retained-cache workload measurements.
- Validate matching CSG and indexed OFF geometry. Report fresh exports separately from six-frame sequences;
  neither is a measurement of GUI edit/reparse latency.
- Keep only a semantically equivalent change with useful measured behavior; preserve rejected evidence.

Run: D:/openscad/runs/20261004-evaluation-general-contexts.

## Outcome

Complete and retained. The general evaluator replaces phase 1's per-name shortcut. Language time on the panel
falls from 786.500 to 705.726 ms (10.27%); contexts from 738,031 to 392,332 (46.84%). Uninstrumented six-frame
OFF sequences improve 2.76% locally and 4.14% globally versus phase 1. Every paired panel sequence improves,
but the shared host has substantial timing variation. Brackets have no consistent end-to-end gain.

All 119 unit cases pass. All 126 configured echo cases match phase 1; after generating one missing parser-stress
input, 121 exit successfully and five retain baseline failures (four stack overflows and one Unicode filename).
The focused CTest set passes 34/37 with the known three recursion failures. All 306 OFF meshes and paired CSG
outputs match. Two new semantic fixtures and golden outputs are retained; temporary profiling code is removed.

Final source/binaries, exact inputs, checksums, raw measurements and limitations are frozen in the run report
and final-manifest.json. Source remains uncommitted and unpromoted; full Hull/Minkowski support is retained.
