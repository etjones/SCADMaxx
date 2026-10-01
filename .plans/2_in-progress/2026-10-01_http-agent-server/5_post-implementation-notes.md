# HTTP agent server — implementation evidence

Status: phase 1 committed; phase 2 in progress. User requested sequential implementation and phase commits.

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
claimed for phases 2–7. Workspace planning moved to `2_in-progress`; unrelated control edits are preserved.
