# HTTP agent server — implementation evidence

Status: all seven phases implemented and committed sequentially; final source retained and verified in the private origin.

Accepted as done by the user on 2026-10-02. This feature stays in the done lane; any future work belongs to a
separate fixup pass.

## Checkout and prerequisites

- Dedicated source: `D:/openscad/wt-openscad-http-agent-server`, `codex/http-agent-server`.
- Starting baseline: `464e25dad0c01af5488375c15aa6734190531eb5`; clean source and initialized submodules verified.
- Reviewed annotations input: `d670fad09`, base `612e684c2`; six committed reconstructed phases, matching that
  feature's verified palette-fixed implementation. The other worktree's dirty Clipper2 state was not copied.
- Prerequisite merge: `a2a79091342630611c874abfadd9b5bc928aa03a`. Preserves original annotation ancestry, including
  its separately identified Windows compilation/link repairs. No conflict or submodule revision change.
- Future composition must use the explicit prerequisite boundary below, not reapply annotations/navigation content.
  Navigation was required only for phase 7; the independent core checkpoint remains 9bb62939f.

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

Later phase records below supersede this initial checkpoint. Workspace planning moved to `2_in-progress` during
implementation and to `3_done` at completion; unrelated control edits are preserved.

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

## Phase 4 — source commit 42aacf037

Successful native publication now detaches instantiated hierarchies, typed common properties, source mappings,
effective roots, modifiers and observed dependency paths before native source lifetimes end. Result identity remains
separate from legacy generations. Current Customizer values include definition revision and stale-source status.
Geometry metrics and complete parameter metadata are explicitly omitted; HTTP.md freezes supported fields.
Inspection admits at most 12,000 evaluated nodes and shares the bounded tree cache. Serialization exceptions do not
turn successful native compilation into failure. Capturing bounded DTOs with access disabled allows first Enable to
inspect an existing displayed model; Stop still invalidates previously issued handles.

Windows Release build passed. Native suite 10/10, `runs/http-agent-server/phase3/native-20261001T165551`:
loop expansion/repeated spans, effective ! roots, disabled calls, retained tree after recompile, empty success,
stale Customizer definitions, and all preceding source/parser/legacy evidence/reload tests. Model property completeness
is deliberately false even with a typed adapter; geometry arrays and tessellation fields are not silently invented.

## Phase 5 — source commit b6461b511

Added v2 evidence reads/search/paging and native camera set/standard/projection/fit/restore, guarded by displayed
result and view revision at worker admission and GUI dispatch. Identical receipt replay precedes current-state checks.
Post-paint capture binds camera/result/owner/size/DPR, then encodes detached pixels through QtConcurrent. Stop invalidates
pending callbacks; modal/hidden/minimized targets fail honestly. Legacy request fields remain compatible.
Windows build passed, native tests 11/11 and protocol suites 2/2. Native evidence:
`runs/http-agent-server/phase3/native-20261001T170600`. Visually inspected `agent-v2-capture.png`: correct cutout cube
at the requested oblique orthographic camera, no annotation controls/strokes, native guides retained as advertised.
Tests include all seven standard views, receipt replay, user camera race, invalid camera, current capture hash/identity,
draft rejection, and historical reads during interaction, plus unchanged legacy client and reload coverage.

Workspace evidence commit 9718358 also included concurrent staged UI plan moves. Their file contents were preserved;
no source implementation was mixed. Subsequent workspace commits use explicit path-scoped commit arguments.

## Phase 6 — core delivery 7aee39c7e and capture-verification follow-up

Delivered stdlib client, skill, contract/schema and explicit identity/capability/request handling. CLI stderr retains
request IDs before sending; no implicit retry, instance replacement or redirect. PNG output validates SHA-256, chunks,
CRCs and dimensions and exclusively creates the explicit path. Redirected output is UTF-8 on Windows.
Native attempts include duration; status exposes busy reasons/capture availability. Global diagnostics are separate;
histories, Customizer context, dependency manifests and v2 JSON output have additional byte caps.

Windows GUI Release builds passed using shared vcpkg. Staged GUI uses copied existing runtime dependencies plus
Qt6Concurrent.dll; PATH restricted to that runtime and Windows. New and unchanged legacy clients run outside the
checkout. Native suite 12/12, no skips, in `runs/http-agent-server/phase6/native-20261001T173208`; packaged CLI executes
18 real commands covering disk capture, explicit parsing, syntax/model traversal, diagnostics, camera and checked PNG.
Native F6 capture passes identity and nonblank-pixel checks. Both top-view images inspected at full resolution.
An inline preview initially appeared blank; direct file hashes prove original and updated F6 images are identical
and valid. Removed redundant GL_FRONT selection but do not claim it repaired a reproduced image defect.
First staged attempt found and fixed Windows code-page output; the following full run passes both clients.

Protocol suites 2/2, including queue capacity, immutable evidence while busy, strict v2 guards and receipt replay.
Python client suite 5/5, including two live mock instances, stale discovery, redirects, uncertainty/deadline and PNG
failures. Unit executable exits 0 (JUnit has zero errors/failures). A 13,000-node fixture verifies the 12,000-node
admission bound and absence of dangling child edges. Earlier parser regression baseline limitation remains above.
Skill-validator invocation is unavailable because PyYAML is absent in both Python runtimes; reviewed required plain
frontmatter, naming, length, placeholders and linked files directly. No Python/runtime packages were installed.

Coverage limits: physical mixed-DPI monitor movement, other OS/Qt5/headless and a clean-machine installation are not
claimed. The staged run is on this development machine. Optional geometry metrics and full parameter metadata remain
unadvertised. Core source and staged evidence are independent of navigation; phase 7 uses only its reviewed committed
revision. Private-origin retention/readiness is finalized after phase 7; no GitHub publication or stack build ran.

## Phase 7 — native navigation integration

Source implementation: 0ec17f2a2; final composition/handoff: 498c4774d26e7235fbc4cbb9b34f56afb39ca645.
Navigation prerequisite: 0947b9e3a840209153d0ad791df27f38ec86858c, including its click-jitter and unchanged-reload
transition fixes. Native saved records, dirty flags, naming and companion persistence remain owned by SavedViews.
Added opaque document-scoped library revisions, list paging and guarded add/rename/remove/recall. Camera operations
use CameraNavigation; add/capture freezes the displayed transition pose. Native Save handles persistence; HTTP never
saves. Integrated captures omit guides/controls/statistics and preserve live preferences. Normal native exports retain
annotation composition; ModelOnly captures bypass it. This hook and exact annotated-pixel comparisons are retained
from the independently tested annotations/navigation composition d16b0001993cddfe7c020e67eca3f71996dee6fa.

Windows Release builds pass. Final native HTTP/annotation run: 13/13, zero skips,
`runs/http-agent-server/phase7/native-20261001T182715`. It includes 23 actual packaged CLI commands, unchanged legacy
client, real F6 result/capture, native save/reopen, duplicate mutations, concurrent native edits, wrong displayed owner,
draft locking, mid-transition add and complete orthographic recall after aspect change. Simulated 150% run:
`native-20261001T182401`, 13/13 (before restoring the export-composition hook); final combined navigation suite at
150%: `navigation-final-scale150`, 15/15. Native clean and F6 PNGs were visually inspected; model-only output has no
guides, cube, statistics or annotation strokes. Native navigation persistence/lifecycle tests cover Save As/copy,
untitled/metadata-only saves, external conflicts and companion behavior.

The first combined click probe failed twice, then passed with tracing. Navigation concurrently delivered its committed
reload-cancellation repair with stronger window-routed click tests. Integrated that exact fix, removed tracing and
passed both expanded navigation runs. No separate speculative click repair was added to HTTP.
Protocol suites: 2/2; Python client regressions: 5/5; unit JUnit: zero failures/errors. Earlier parser-stack limitation
and physical monitor/OS/clean-machine coverage limits remain as recorded above. No tests are claimed beyond evidence.

## Retained source and build-input handoff

Private repository: `E:/Dropbox/bare_repos/scadmaxx.git`. Verified with `git ls-remote` after ordinary pushes:

- `refs/heads/codex/http-agent-server`: `498c4774d26e7235fbc4cbb9b34f56afb39ca645`.
- `refs/heads/codex/http-agent-prerequisites`: `85829fa71870c4aa6945d3cd4abbc932faeab392`.

The latter is an ancestor of the delivered head, containing only the reviewed native annotations/navigation
composition plus navigation fixes. The build delta is exactly `85829fa7..498c4774`, with earlier selected dependencies
`navigation-cube` and `annotations`. Do not use auto-merge-base or squash-merge the complete feature head onto earlier
squashed dependencies. Preserve the binary-capable patch in `runs/http-agent-server/phase7/http-only.patch` and compare
the selected prerequisite heads before integration. Review the small CMake optional-Cairo correction and Windows GUI
test plumbing in this delta against separately applied repairs; they are not additional selected features. QGLView
and TabManager contain no residual changes against the prerequisite boundary. No submodule gitlink was changed.
Generated Clipper2 build text, Serena metadata and Python caches are excluded from commits. Dependency commits are the
original native feature inputs; source origin retains their ancestry. Detailed submodule identities and build recipe
are in the phase-7 run material.

Core-only and integrated staging remain separate under `artifacts/http-agent-server`. Their manifests identify source,
runtime provenance and executable hashes; integrated executable About metadata can show the pre-commit build hash,
while `matchingSourceCommit` records the exact committed code it was built from. This is a developer-machine validation
package, not a claim of a clean-machine release or an experimental full-stack composition.

Workspace handoff sets HTTP readiness true only after verified retention. Other selected features keep their own
readiness; this does not imply the entire SCADMaxx stack is ready. All subsequent workspace commits scope paths or use
a temporary index for owned changes within shared metadata files, preserving concurrent staged plans.
