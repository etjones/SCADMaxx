# HTTP agent server — overall implementation plan

Status: core phases 1–6 committed; phase 7 navigation integration in progress. Implements [2_requirements.md](2_requirements.md).
Core phases 1–6 precede independent phase 7. See [execution evidence](5_post-implementation-notes.md).

## Checkout and prerequisites

- Source: `D:/openscad/wt-openscad-http-agent-server`, branch `codex/http-agent-server`.
- Planning baseline: `464e25dad0c01af5488375c15aa6734190531eb5`; source was clean with initialized submodules.
  Recheck HEAD, branch, status, submodules and local instructions before edits; preserve concurrent work.
- The annotations implementation was inspected in its separately owned worktree. Phase 1 must identify a reviewed
  committed annotation revision and its precise delta/base before integrating or extracting transport. Do not commit
  the other feature's work, copy its whole dirty tree, include unrelated baseline repairs, or invent a dependency SHA.
  If none is available, report this concrete prerequisite; standalone DTO/protocol work can proceed where independent.
- Choose the smallest reviewed prerequisite delta. Record ancestry and stack overlap so annotations are integrated
  once. Reuse the existing clone/worktree; do not base this branch on a composed experimental build.
- Navigation is required only for phase 7. No root dependency graph existed at planning time; keep sequencing here.
  Its current plan is [navigation](../../2_in-progress/2026-10-01_navigation-cube/3_overall-plan.md); implementation
  began in that separately owned chat during this planning pass. Recheck its actual committed state when needed.
- Proposed build directory: `build-http-agent-server` within the dedicated checkout; verify it is available first.
  Evidence: `D:/openscad/runs/http-agent-server/<attempt>/`; local staging, when requested/needed for validation:
  `D:/openscad/artifacts/http-agent-server/<attempt>/`. Use fresh attempt directories.
- Follow the [Windows profile](../../../experimental/profiles/windows-x64.md): shared installed packages at
  `D:/openscad/openscad-6991/build/vcpkg_installed`, toolchain `D:/vcpkg`, manifest mode/install disabled. Record actual
  toolchain, package-status hash and build options. Do not install dependencies or create a private dependency tree.

## Inspected integration points

Paths are relative to the dedicated source checkout unless marked annotations reference. Proposed new classes below
are design names, not assertions that those classes already exist.

| Existing area | Evidence and planned use |
| --- | --- |
| Annotations `AnnotationTransport.*`, `AnnotationBridge.*` | Worker listener, snapshots, discovery, GUI dispatch, receipts; extract into shared service without duplicating listener |
| Annotations `AnnotationController.*`, `AnnotationStore.*` | Native evidence, result identity, busy guards, camera/capture adapter |
| `src/gui/MainWindow.*` | `rootFile`, `absoluteRootNode`, `rootNode`, `csgRoot`, `renderedEditor`; lifecycle hooks must distinguish attempt and displayed-result success |
| `src/gui/TabManager.*`, `Editor.h`, editor implementation | Document IDs, text/dirty revisions, close/reopen and explicit buffer snapshots |
| `src/core/parser.y`, lexer/parser settings | `parse` mutates shared parser globals; serialization and restoration are mandatory |
| `src/core/AST.*`, `SourceFile.*`, `LocalScope.*` | Syntax locations, definitions, assignments, instantiations, include/use information |
| `src/core/Expression.*`, `ModuleInstantiation.*`, `UserModule.*` | Structural expression/argument/scope adapters |
| `src/core/node.*`, `Tree.*`, node subclasses | Evaluated hierarchy; indices reset per compile and `modinst` points into syntax lifetime |
| `src/utils/printutils.*` | Typed `Message`, global output-handler state; attributed fan-out must preserve original console |
| `src/gui/QGLView.*`, `src/glview/Camera.*` | GUI-thread frame readback and native camera conversion/fit |
| `src/RenderStatistic.*`, parameter widgets | Optional existing summaries, never additional rendering |
| `CMakeLists.txt`, `src/guitests`, existing unit tests | Register focused GUI/protocol/logic tests without GUI dependencies in headless core |

AST/CSG text dumps are useful comparison fixtures, not the public structured representation. `LocalScope` separates
lookup maps from print-order storage; do not serialize unordered maps as source order. Add narrow const visitor/access
surfaces where needed. Do not reconstruct syntax by parsing pretty-printed dumps.

## Architecture and ownership

1. **AgentService**, one process owner, holds access mode, target registry and adapters on the GUI thread.
2. **AgentTransport**, derived from the annotation transport, owns sockets, published immutable data and job receipts
   on its worker. It never accesses widgets, AST/node pointers, parser globals or GL contexts.
3. **DocumentRegistry/InspectionStore** owns runtime IDs, source snapshots, attempts, bounded detached tree records,
   diagnostics and result provenance. Public identifiers are opaque UUIDs, scoped as below.
4. **ParserInspection** uses the native parser under an application-wide parse/evaluation gate. Initially dispatch on
   the GUI thread only while native compilation is idle; do not move the non-reentrant parser onto an HTTP worker.
5. **EvaluationObserver** records normal evaluation lifecycle and creates bounded detached DTOs before source/node
   lifetimes end. No serialization on every read or paint. Serialization truncation must not break normal evaluation.
6. **AnnotationAdapter/ViewportAdapter** preserve native evidence, locks and frame-ready capture. Phase 7 supplies
   **SavedViewsAdapter** against navigation's native library and camera boundary.

Use ordinary Qt JSON/networking, standard C++ and existing dependencies. GUI-independent DTO/serialization code may
live in a small inspection library; service/UI code remains GUI-only. Avoid retaining full AST/node trees indefinitely.
Any short-lived native ownership must retain both nodes and source/module lifetimes, never `AbstractNode` alone.

## Identity and data contract

- `server_id` changes on every service start. Document/window/viewport UUIDs die with their objects. Paths label a
  target but are not its identity. Keep legacy IDs valid within their documented lifetimes.
- Document `source_revision` tracks editor text changes. Explicit source snapshots carry `origin`, path, captured
  revision, content hash and encoding/normalization description. Compare disk/editor normalized text separately from
  raw disk bytes; never compare differently normalized hashes as equal-content evidence.
- A parse gets `parse_id`; every native evaluation gets `attempt_id`; a successful displayed model gets `result_id`.
  A failed attempt may publish diagnostics while leaving the previous displayed-result ID intact. Empty success is
  its own successful result, not failure or a leftover model. Record effective root selection and parameters when known.
- `view_revision` changes for relevant camera/display-size state; `state_generation` changes on published state,
  independently of heartbeat. Capture checks identity/result/view before dispatch and immediately around readback.
- A tree has `tree_id`, `kind` (`syntax` or `evaluated`), source/attempt/result references, root IDs, completeness and
  expiry. Nodes carry local ID, kind, name, source span, typed attributes, ordered edges with roles and child count.
  `node_id` is valid only with its `tree_id`. Root/background modifiers and synthetic nodes have explicit attributes.
- Define source spans as 1-based lines and documented UTF-8 byte columns, with inclusive start/exclusive end; adapt
  native locations after Unicode fixtures confirm conversion. Missing locations are null plus a reason. Do not guess.
- Encode SCAD undefined/non-finite values with explicit tagged forms; JSON numbers remain finite. Separate expression
  syntax from evaluated property values. Large values and unsupported node kinds are explicit, bounded omissions.
- Diagnostics carry ID, attempt/parse identity, severity/category, text, nullable source span and truncation status.
  Unattributable messages are labelled global. No backfilling provenance for messages emitted before observation.

## Source/parse and evaluation lifecycle

An explicit parse request selects `disk` or `editor`, names the open document and supplies its expected revision/hash.
Snapshot editor text on the GUI thread; read disk bytes through a bounded, canonicalized document/dependency resolver.
Resolve includes/use using native path semantics, without overlaying other buffers or evaluating imports. An isolated
dependency resolver records bytes/hashes where read; handle cycles and changes without claiming cross-file atomicity.
Untitled source can parse with the existing native base context, identified explicitly; never change global cwd.

Prototype native parser-state restoration first, including lexer state, diagnostic handlers and warning settings.
Do not invoke `instantiate`, geometry construction or global `SourceFile::handleDependencies` cache mutation as an
inspection shortcut. Use scoped restoration and independent SourceFile ownership; failures destroy partial state.
Prefer no partial AST publication in v1. A parser failure produces diagnostics and no tree.

If safe isolation requires a narrow parser refactor, complete and test it in phase 3 before enabling parse capability.
Never silently fall back to compiling the document or spawning another OpenSCAD process. Wall-clock queue deadlines
do not interrupt a running synchronous parser; use input/structural bounds and cooperative checks where possible.
If the prototype cannot safely enforce them, retain the phase as incomplete and record the necessary technical repair.

Observe normal compilation through explicit begin, parse/evaluation completion, renderer publication and failure hooks.
Never assign a new successful `result_id` merely when `renderedEditor` changes during instantiation. Freeze typed tree
data while the native ownership is valid; retain an older detached snapshot within budgets for stale-result inspection.
Publish provenance and diagnostics together as a consistent generation; transport reads never see half a transition.

## HTTP and client design

Keep existing `/v1` annotation endpoints, headers, response shapes and discovery directory for the legacy client.
Expose the broader API under `/v2` on the same listener. Keep legacy discovery fields compatible and add a supported
agent-version/capability field. New client verifies `/v2/info`; old client remains on `/v1`. Do not alias new parse
operations into the legacy contract. The version denotes our service API, not upstream OpenSCAD's version.

New requests use `X-OpenSCAD-Agent: 1` and `X-OpenSCAD-Agent-Server: <id>`; initial info discovery needs only the
protocol guard. Validate Host, Origin/fetch metadata and JSON content type using the retained transport protections.
Legacy headers remain accepted only on legacy routes. Identity headers are protocol checks, not secret credentials.

| Route group | Planned operations |
| --- | --- |
| `/v2/info`, `/documents`, `/viewports`, `/status` | GET versions, targets, generation/heartbeat and availability |
| `/v2/documents/{id}/source-snapshots` | POST explicit bounded disk/editor snapshot, no arbitrary supplied source text |
| `/v2/source-snapshots/{id}` | GET captured text/provenance in bounded pages |
| `/v2/documents/{id}/parse` | POST parse an identified retained snapshot; reject expiry/wrong document |
| `/v2/documents/{id}/dependencies`, `/attempts`, `/results` | GET observed provenance/lifecycle records |
| `/v2/trees/{id}`, `/nodes/{node}`, `/nodes/{node}/children` | GET revision-bound metadata/node/pages; node routes nested under tree |
| `/v2/documents/{id}/diagnostics`, `/parameters`, `/geometry-summary` | GET attributed messages and advertised optional data |
| `/v2/annotations`, `/annotations/{id}` | GET document-targeted legacy evidence through the shared store |
| `/v2/viewports/{id}/view`, `/capture`, `/annotations/{id}/restore` | POST guarded camera/capture/restore operations |
| `/v2/requests/{id}`, `/requests/{id}/cancel` | GET outcome; POST queued cancellation or honest running status |
| `/v2/documents/{id}/saved-views[/{viewId}]` | Phase 7 only: GET list; POST explicit add/rename/remove/recall actions |

Relative names in the table are within `/v2`; publish exact full routes and JSON schemas in the source contract during
phase 1. Every POST has UUID `request_id`, correct server/document identities and operation-specific expected versions.
Camera/capture additionally require window, viewport and expected result/view; source snapshot needs no rendered result.
Parse consumes a retained immutable source snapshot, so a later editor change does not change its inputs; report it
as an older snapshot rather than silently reparsing the new buffer.

Return structured `code`, `message`, context and retry guidance: 400 invalid, 403 guard, 404 unknown, 409 stale/busy/ID
conflict, 410 expired, 413 limits, 429 capacity, 503 unavailable. Unsupported capability is 409 with `unsupported` code.
Retain legacy response contracts independently. Accepted jobs return 202; terminal polling contains execution-started
state and original target IDs. Repeated exact requests return receipts; changed payload conflicts.

Store full results for five minutes with LRU budgets; keep bounded request tombstones until restart to prevent reuse.
At tombstone capacity reject new POSTs, never evict evidence needed for idempotency. Stop closes the listener and
invalidates the server ID; detached running work cannot publish into or mutate a replacement server session.

## Initial engineering budgets

These are implementation starting values, to be verified with fixtures and adjusted explicitly in phase records.
Expose actual values in info; do not silently change legacy wire limits or weaken truncation/identity semantics.

| Resource | Initial bound |
| --- | --- |
| HTTP headers/body | 16 KiB / 256 KiB; source comes from bounded snapshot operations, not request-body uploads |
| Connections / queued jobs | 16 / 32; reject excess; incomplete-request idle timeout 5 seconds |
| Queue start deadline | 10 seconds default, maximum 120; distinct from execution/capture completion |
| Native capture wait | 10 seconds; timeout invalidates pending callback, without claiming native render interruption |
| Source snapshot | 4 MiB root, 32 MiB total parsed dependencies, 256 files; explicit over-limit outcome |
| Tree | 100,000 nodes, traversal depth 256, 500 nodes/page, 1 MiB non-image response |
| Retained inspection data | 8 trees and 64 MiB process total for trees/source/diagnostics; evict with explicit 410 |
| Diagnostics | 1 MiB per attempt, truncation flag and dropped-count where known |
| PNG/results | 32 MiB PNG, 128 MiB aggregate job results, 128 retained full outcomes |
| Idempotency receipts | 10,000 per server lifetime, then reject new operations until deliberate restart |

Cap snapshot creation, not just response encoding. Hash and serialize bounded detached data off the GUI thread where
safe. Report missing/evicted history, never pin every past revision. Poll status no faster than needed; the CLI uses
bounded backoff and reports busy/disabled reload instead of looping indefinitely. No event streaming is needed initially.

## Ordered phases and requirement coverage

| Phase | Deliverable | Prerequisites | Coverage |
| --- | --- | --- | --- |
| [1](4_imp-phase1.md) | Reviewed dependency boundary; service/protocol foundation | Committed annotations boundary for integration | R01–R05, R17–R18, R24 |
| [2](4_imp-phase2.md) | Target/source/result registry and diagnostics | 1 | R04, R06, R08, R11–R12, R19–R20 |
| [3](4_imp-phase3.md) | Isolated parsing and structured syntax tree | 1–2 | R06–R09, R11, R17–R18, R20 |
| [4](4_imp-phase4.md) | Evaluated tree and bounded optional summaries | 2–3 | R08, R10–R12, R18, R21 |
| [5](4_imp-phase5.md) | Evidence, native camera and verified capture | 1–4 | R13–R20 |
| [6](4_imp-phase6.md) | CLI/skill, regressions and core delivery evidence | 1–5 | R01–R24, especially R22–R24 |
| [7](4_imp-phase7.md) | Saved-view adapter and combined validation | Core + reviewed navigation implementation | N01–N03; R05, R14–R16, R20 |

Keep phase 7 pending after core completion if navigation is unavailable. Later preview/render, parameter writes and
export are not phases in this implementation. Record each implemented phase's evidence and deviations in
`5_post-implementation-notes.md` when execution begins/completes; do not create fictional results now.

## Validation and review discipline

Use unit/protocol tests for identities, serialization, budgets and receipt semantics; native GUI tests for source/
render lifecycle, camera/drawing locks and actual framebuffer images. Inspect actual PNGs. Phase plans specify the
fixtures and exit evidence; do not replace behavior checks with tests that repeat implementation details.

Run appropriate tests after each coherent change and broaden at phase boundaries for identified integration risks.
Build only with the shared dependency policy. Compare source/dirty/undo/camera/result state before and after read-only
operations. Exercise legacy and new clients together. Cancellation, errors and Stop must unwind RAII ownership.

Before any later commit, apply git-workflow, stage only intended source or workspace changes in the correct repository,
and review outgoing ancestry. No commit/push is requested by this planning turn. Any later local retention uses the
Dropbox origin; GitHub publication and combined experimental builds remain separate user actions. Mark integration
ready only after a verified committed revision is retained and delta/dependencies are reviewed.
At feature completion follow the [source/readiness handoff](../../../workflows/update-and-build-scadmaxx.md#feature-completion-and-later-github-publication),
including usable committed source and verified private-origin retention. This is a future implementation completion
obligation, not a request to commit or push this planning turn.
