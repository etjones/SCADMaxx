# HTTP agent server — implementation evidence

Status: phases 1–3 committed; phase 4 in progress. User requested sequential implementation and phase commits.

## Checkout and prerequisites

- Dedicated source: `D:/openscad/wt-openscad-http-agent-server`, `codex/http-agent-server`.
- Starting baseline: `464e25dad0c01af5488375c15aa6734190531eb5`; clean source and initialized submodules verified.
- Reviewed annotations input: `d670fad09`, base `612e684c2`; six committed reconstructed phases, matching that
  feature's verified palette-fixed implementation. The other worktree's dirty Clipper2 state was not copied.
- Prerequisite merge: `a2a79091342630611c874abfadd9b5bc928aa03a`. Preserves original annotation ancestry, including
  its separately identified Windows compilation/link repairs. No conflict or submodule revision change.
- Future composition must use the HTTP-only delta after the annotations prerequisite, not reapply annotation content.
  Navigation is separately in progress and remains required only for phase 7.

## Phase 1 working record

The shared service retains the existing `AgentAnnotations::Bridge/Transport` class/file names to minimize native
integration churn. They now own both access modes on one listener; there is no second HTTP server. Proposed design
names in the overall plan were descriptive, not required public symbols.

Implemented so far: broad/legacy access distinction, global access dialog, compatible discovery, v2 info/status,
monotonic request deadlines, running transitions, queued cancellation, bounded persistent idempotency receipts,
expiry and browser-request guards. V2 capabilities advertise only implemented operations.

Evidence root: `runs/http-agent-server/phase1/`. `build.ps1` records reproducible shared-dependency configure/build/test
commands and logs. Configuration succeeded with MSVC 19.51/Qt 6.11.1 and the existing vcpkg installation. No packages
were installed or upgraded. Separate protocol tests passed after the initial implementation; rerun after final edits.
Full Windows GUI build and incremental rebuild passed. Protocol tests: 2/2. Native tests: 6/6, including unchanged Python client; evidence native-20261001T153059 and visually inspected annotation-window.png. Unit test executable exited 0; JUnit retained. Source commit: a638ae7d3.

Source schemas/route adapters will be extended in their implementation phases. No API or requirement completion is
claimed for phases 4–7. Workspace planning moved to `2_in-progress`; unrelated control edits are preserved.

## Phase 2 — source commit 195a3be74

Added live document/editor revisions, bounded immutable disk/editor source snapshots with cached Unicode-safe pages,
bounded evaluation attempts/successful results, and typed diagnostics whose context is captured before GUI delivery.
Disk reads detect available metadata changes without claiming filesystem transactions. Snapshot read/hash is bounded
and synchronous on the GUI thread; no widget or file access happens on the HTTP worker. No background hashing is
needed for the 4 MiB root budget. Retained source pages have a separate estimated 32 MiB budget.

Windows incremental build passed. Protocol suites: 2/2; native suite: 8/8 in
`runs/http-agent-server/phase1/native-20261001T160437` (shared runner retained in phase1).
Checks cover Unicode filename/BOM/CRLF, distinct disk/editor data, stale revision, read-only state preservation,
failed compile without a new successful result, two windows sharing a path, active untitled vs displayed owner,
closed-window handle invalidation, and the unchanged legacy client/reload tests.
The two-window test exposed live-list iteration in the GUI test runner; copying its initial window list fixed the
test-harness lifetime failure. Source dependency records remain explicitly unknown until phase 3 captures them.

## Phase 3 — source commit 8fa5edcbf

Added isolated native parsing with bounded captured include/use inputs, typed syntax DTOs, ordered statement retention,
disabled/overwritten syntax, dependency handles, pagination, tree retention and worker-side expiry. Native parser
semantic-value destructors repair malformed-input cleanup; scoped output preserves native handler/suppression state.
Expressions expose const inspection via one observer friendship, avoiding a Qt dependency in core expression types.
In addition to planned budgets, inspection has an 8,192-token admission bound, 64-deep includes and a cooperative
two-second token-boundary deadline. No filesystem call or executing native operation is claimed interruptible.

Windows full/incremental builds passed. Native tests 9/9 in `runs/http-agent-server/phase3/native-20261001T164112`:
120 malformed parses, injected dependency-read exception/restoration, 500/100 child-page boundary, Unicode byte
columns, limits, include/use/missing/cycle cases, unchanged native roots/renderer/camera/output state and later preview.
Protocol tests 2/2 including expired cached inspection while heartbeat remains live. Unit executable exited 0.

Broader parser/echo regression selection: 27/28 executed tests passed; two existing tests are disabled. The infinite
recursion fixture `echo_recursion-test-function3` overflows the Windows native stack (0xc00000fd). Reproduced against
the pre-feature annotations artifact with the same exit code; see `baseline-recursion-exit.txt` and output under
phase3. This is a pre-existing native evaluation limitation, not exposed by the parse-only operation. Initial CTest
attempt lacked the adjacent `.com` launcher; staged the already-built winconsole launcher beside openscad.exe and
reran. One attempted relink overlapped CLI execution and hit a Windows executable lock; rebuilt after tests exited.
