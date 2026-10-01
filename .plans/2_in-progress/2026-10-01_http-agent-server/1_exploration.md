# SCADMaxx HTTP endpoint / agent server

Status: exploration reviewed; requirements, overall plan and phased implementation plans are written.
Implementation was subsequently requested; see [current evidence](5_post-implementation-notes.md).

Planning entry points: [requirements](2_requirements.md), [overall plan](3_overall-plan.md) and its
[ordered phases](3_overall-plan.md#ordered-phases-and-requirement-coverage). Six phases deliver the core; phase 7
integrates saved views later. The requirements are the acceptance contract; this exploration retains decision context.

SCADMaxx — *OpenSCAD, with the sliders turned up.* The user wants a dedicated HTTP endpoint / agent server feature
with its own branch, worktree and pinned chat. This setup does not begin implementation or a build.

## Workspace

- Source: `D:/openscad/wt-openscad-http-agent-server`.
- Pinned chat: **SCADMaxx HTTP agent server**, ID `01a0f740-239c-79c2-a0cb-8611d0265757`.
- Branch: `codex/http-agent-server`, created through the existing `openscad-master` clone.
- Base: freshly fetched upstream master `464e25dad0c01af5488375c15aa6734190531eb5` on 2026-10-01.
- Local source origin: `E:/Dropbox/bare_repos/scadmaxx.git`; retain feature commits there.
- Workspace controls/plans stay under `D:/openscad`, outside upstream-facing source changes.
- The feature is selected in `experimental/PR_STACK.md` but not ready for integration (`ready: false`).

## Context for exploration

The feature lets an agent communicate with the running OpenSCAD instance through an HTTP API. The user accepted
the capability direction and resolved the completeness-review questions. The decisions below define the boundary
for requirements; no unresolved product question remains at the exploration stage.

Read the annotations exploration and inspect existing server/agent code in the annotations worktree to identify
reuse and ownership boundaries. At the reference review its implementation was uncommitted: treat it as a reference,
not a committed dependency or permission to copy its entire implementation. The Blender reference is
`D:/source/blender-annotations`, including `docs/owned-http-api.md` and its agent workflow documentation.

Use the existing in-process transport as the design starting point. The technical plan will specify GUI-thread
dispatch, asynchronous outcomes, snapshots and multi-instance targeting within the agreed local-access policy.
Declare actual committed feature dependencies explicitly before integration.

## Constraints and next work

- Read workspace `AGENTS.md`, `README.md`, `docs/git-layout.md`, `docs/worktrees.md` and checkout-local instructions.
- Keep the branch private/local. GitHub `publish` is used only when the user explicitly chooses publication.
- Keep the implementation independently reviewable against upstream; do not base it on the composed SCADMaxx build.
- Reuse the shared vcpkg packages in `D:/openscad/openscad-6991/build/vcpkg_installed` and toolchain `D:/vcpkg`.
- Preserve other feature worktrees and workspace edits. Do not start implementation or a build from this setup.
- Next work, when implementation is requested: execute the overall plan and phase 1's prerequisite checks.
- Whenever asking the user a question, stop and end the turn; resume only after an explicit answer.

## Agent use cases and accepted scope, 2026-10-01

The user clarified that this feature gives agents access to the running OpenSCAD instance. Reuse the annotations
and Blender work as references. Candidate capabilities explicitly raised were parsed-tree inspection, annotations
and screenshots, viewport control, and creating saved views through the navigation-cube feature. Blender Python
execution is not relevant to OpenSCAD. The user subsequently accepted this direction and requested a completeness
review. The resulting decisions and delivery boundary are incorporated below.

### Existing foundations

- OpenSCAD's annotations bridge already documents instance discovery, explicit document/window/viewport targeting,
  accepted annotation reads, immutable screenshots, fresh capture, camera set/restore and asynchronous receipts.
  It distinguishes the displayed model's owner from the active editor and checks the expected rendered-result ID.
- That feature deliberately excludes source editing, save, compile, document opening/switching and annotation
  mutations. A broader server may propose new capabilities, but must preserve those existing feature boundaries
  until its own scope is agreed.
- Blender's owned API provides the lifecycle reference: explicit targets, queued/running/terminal outcomes,
  idempotent retries, busy handling and fresh viewport evidence. Do not transfer its arbitrary Python executor.
- Navigation-cube exploration now includes document-owned saved camera snapshots: orientation, translation,
  distance, FOV and projection. Add/remove/rename change companion metadata; recall only changes the camera.
  Reuse that feature's records and persistence semantics instead of creating a second saved-view library.

### Capabilities and integration targets

| Capability | Useful agent task | Behavior |
| --- | --- | --- |
| Live document context | Establish what the user is actually viewing | List documents and viewports; report active editor, displayed root, dirty state, preview/render state and revisions |
| Source and dependency inspection | Explain a mismatch between disk, editor and viewport | Use disk files normally; explicitly inspect editor snapshots; report resolved include/use/import dependencies and available diagnostics |
| Parsed source tree | Find definitions, calls, arguments and source locations | Read a bounded tree/subtree with source spans and parse diagnostics; identify the exact source revision |
| Evaluated model tree | Understand what parameter values, loops and modules produced | Inspect the instantiated geometry/CSG hierarchy with available evaluated arguments and source mapping |
| Compilation feedback | Diagnose a failed or misleading preview | Structured errors, warnings, echo/assert output, durations and outcome tied to an evaluation/result |
| Annotations and images | Understand a reported defect and verify a correction | Reuse existing accepted evidence, camera restoration and fresh capture; preserve historical images |
| Viewport and saved views | Inspect several sides and leave a useful review angle | Core: standard views, explicit camera, projection and fit. Later integration: native saved-view list/add/rename/remove/recall |
| Customizer inspection | Understand the design's supported controls | Read parameter names, current values, types, descriptions, choices/ranges and presets |
| Geometry summary | Check gross changes without relying only on pixels | Bounds, dimensions, empty-result state and available mesh statistics, identifying preview versus final geometry |
| Change notifications | Wait reliably after an external file edit | Observe document/evaluation/result changes and request outcomes; start with polling or bounded waits |

Parsed and evaluated trees answer different questions. Offer both explicitly, with lazy children, depth/size limits
and IDs scoped to the source/evaluation revision. Do not promise durable node identity across recompilation or a
one-to-one mapping between source statements and generated geometry. Start with available source mappings and
report gaps. Existing CLI AST/CSG/term exports demonstrate useful dump machinery, not a ready structured live API.

### Source authority and explicit parsing

Disk SCAD files remain the normal source of truth for the agent's file-based workflow; the unsaved editor buffer
does not replace them as the authoritative design. Agents can read disk files using their existing file tools.
Source inspection and parse requests distinguish disk from editor explicitly and return origin, document/path,
revision or content hash, and available dependency provenance. Never silently substitute an editor buffer for disk
content or the reverse. Untitled documents have no disk version; report that absence.

Allow explicit parse-only requests for a captured disk or editor source snapshot, including unsaved editor text.
Return syntax diagnostics without evaluating modules, saving, replacing editor text or changing the displayed model.
Reading an existing tree does not trigger parsing. Cached trees retain their original source identity and revision;
they must not be labelled current merely because a filename matches.

The evaluated model tree and screenshots describe the actual completed evaluation, which can have used editor
contents different from disk. Report that provenance honestly: disk authority does not retroactively change what
OpenSCAD evaluated. Show disk/editor differences and source dirtiness; ordinary external edits must not discard
unsaved work. The API does not automatically reconcile conflicting versions or require every file read to pass
through the editor. Parse-only requests use isolated state and must not poison caches used by normal evaluation.

Scope source requests to an explicitly targeted open document and its known source/dependency context; ordinary
file tools remain available for other files. For a disk parse, use disk source; an explicit editor parse snapshots
that document's buffer without silently overlaying other open editors onto dependency files. Report what was read.
A failed parse returns its own diagnostics and any explicitly marked partial syntax data, not an old tree presented
as a new successful parse. Parsing SCAD dependencies does not evaluate imported geometry. A snapshot identifier does
not imply an atomic filesystem snapshot across all dependencies; changes and unknown provenance must remain visible.

Fresh captures should include the camera, dimensions, displayed document and result revision. Camera actions must
finish before capture, respect annotation locks and coordinate with navigation-cube animation. A failed new compile
must not cause an old visible model to be labelled as the new result. Dependency provenance is currently reported
as unknown by the annotations workflow; root hashes alone cannot establish that changed includes were evaluated.

### Operations worth adding after the inspection surface

Explicit preview and full render are especially useful: evaluate a specified live document, return an asynchronous
job, and associate diagnostics and captures with its completed result. This extends the annotation-only contract;
it should not implicitly save, discard editor changes or choose a different document. Cancellation must distinguish
queued cancellation from whatever running evaluation can actually interrupt.

Customizer writes and preset selection would let agents explore supported parameter variations without rewriting
SCAD source. They need native undo, explicit persistence behavior and revision checks. Later possibilities include
bounded parameter sweeps, selected animation times, geometry export, and viewport highlight/fit for a model-tree node.
Highlighting needs a separate source-to-geometry mapping investigation. Mesh validity, volume and component counts
should be exposed only where the selected backend can compute them reliably; never infer printability from a preview.

Keep ordinary source-file editing as the initial editing path. Reading unsaved editor content is still valuable.
An editor-write API can be considered separately if working directly on unsaved designs becomes a requirement.
There is no proposed arbitrary execution endpoint or annotation create/edit/delete API in the first scope.

### Accepted delivery direction and ownership

Prioritize an end-to-end inspect/edit/verify loop: discover the right live document, read diagnostics and model
structure, read annotations, edit externally, observe a new successful evaluation, and capture useful views.
Deliver this core first; saved views belong to the navigation-cube feature and do not block the core delivery.
Add an adapter to that feature's saved-view operations once its reviewed implementation is available. Advertise
saved-view capabilities only when integrated; do not build a substitute library in this feature. Add explicit
preview/render in later work, then parameter writes and export/batch operations. Read-only parameter and geometry
summaries can join the first scope where existing application data makes them straightforward.

This verification loop relies on ordinary automatic reload/preview already being enabled for the intended document.
Report when it is disabled, blocked by unsaved changes, or unable to produce a current result; do not enable it,
switch tabs, request evaluation or retry indefinitely as a hidden side effect of a read. A first-time document with
no evaluation has no model tree yet, although its source remains inspectable and explicitly parseable. Existing
geometry can still be inspected as a labelled older result after a failed attempt; it cannot verify a newer edit.

Parameter metadata and geometry summaries are capability-reported additions, not open-ended prerequisites for core
delivery. Define the supported fields in requirements and return explicit unavailable/not-applicable states for
missing data. Do not force evaluation to populate them. Distinguish current Customizer values from values used by
an older result, and preview bounds/statistics from final Boolean geometry. Do not report missing metrics as zero,
assume millimetres for unitless SCAD coordinates, or call every facet a triangle.

Prefer one process-level agent service with capability groups for documents, model inspection, annotations and
views. Factor or extend the existing annotations transport deliberately rather than starting a competing listener.
An in-process service is the natural initial design because live editor, render and viewport state belongs there;
GUI-owned operations must dispatch to the GUI thread. Keep capabilities discoverable so unavailable integrations
can be reported accurately. Exact extraction strategy, compatibility mechanisms and committed feature dependencies
belong in the technical plan; do not change stack ordering/readiness based on this exploration.

Retain the annotations local-access model: explicit Enable/Stop, remembered enablement across application launches,
numeric loopback only, automatic per-instance discovery and browser-request guards, without a secret token. This
trusts local processes; the guards do not authenticate them. Enabling the broader service is an explicit action,
not an automatic widening of old annotation-only consent. Keep bounded jobs and request IDs.

Deliver documented HTTP, a bundled Python standard-library CLI and an agent skill. MCP is explicitly excluded;
do not add an MCP adapter, dependency or planned MCP follow-up. Agents can use the documented HTTP directly or the
CLI. The client must retain explicit instance targeting, outcome tracking and image verification.

### References inspected

- `workflows/annotations.md` and the annotations exploration/post-implementation notes.
- `wt-openscad-annotations/contrib/openscad-agent-annotations/README.md` and `SKILL.md` (read as API references).
- Literal route/capability checks in `src/gui/annotations/AnnotationTransport.cc` and `AnnotationBridge.cc` there.
- `D:/source/blender-annotations/docs/owned-http-api.md` and
  `skills/agent-annotations/references/http-workflow.md`, revision `f8f84ed4de7efc34dce02b4fbb61cc44d62d1f4e`.
- Navigation-cube `1_exploration.md` and `2_requirements.md`, including saved views and capture integration constraints.
- Dedicated server checkout `src/openscad.cc`: CLI AST/CSG/term output options and geometry summary paths.

This was a documentation and bounded source-text review. No live server, compilation, tree serialization or new
API behavior was tested. Only this workspace exploration was edited; source worktrees and other plans were preserved.

## Consistency and completeness review, 2026-10-01

The next phase is testable requirements, not implementation. All four product questions were answered and their
decisions incorporated: disk remains authoritative with explicit editor parsing; core delivery does not wait for
saved views; retain the annotations local-access policy; HTTP/CLI/skill with no MCP. The resolved conversation file
was removed. No further product question is needed before requirements.

### Scope reconciliation

- The accepted first scope is live document/source context, parsed and evaluated trees, diagnostics, annotations,
  fresh screenshots and camera control. Saved-view access follows the navigation feature. Parameter metadata and
  existing geometry summaries are secondary inspection capabilities; unavailable data must be reported explicitly,
  never fabricated or computed by a hidden F6.
- Preview/render commands, Customizer writes, export, sweeps and model-node highlighting remain later work. Reading
  existing outcomes is distinct from requesting new evaluation. Source editing stays with ordinary agent file tools.
- No arbitrary script execution, document open/close/switch/save, annotation mutation, remote network listener,
  headless renderer, MCP adapter or new saved-view store is included. External changes must not discard unsaved work.
- Saved views must use the navigation feature's complete camera snapshots and document ownership. Add/rename/remove
  make metadata dirty; ordinary native saving persists it. Agent requests do not silently save source or companions.
  Navigation and recall do not change the saved-view library. Resizing can change framing without changing the camera.

### Behavior to carry into requirements

- Report active editor and displayed model independently. Explicit IDs distinguish windows, documents and reopened
  copies. Never silently retarget an action when the user changes tabs, closes a document or restarts the server.
- Distinguish editor revision, parse revision, evaluation attempt, successful model result and camera/view revision.
  Failed parse/evaluation, empty success, stale displayed geometry and never-evaluated documents are separate states.
- Separate parsed syntax from instantiated geometry and lowered CSG representations. Do not promise runtime values
  in an unevaluated AST, stable cross-evaluation node IDs or complete source mappings. Define the public tree schema,
  source ranges, supported node kinds and bounded traversal in requirements/design, rather than exposing C++ objects.
- State whether each dependency came from disk or an editor buffer, and whether it was actually used in a result.
  Report unresolved dependencies and unknown provenance. A list of paths or changed root hash is not proof of a
  consistent dependency snapshot. Handle include/use/import and unsaved root documents explicitly.
- Read-only inspection must not trigger compilation, save, tab switching or camera motion. An on-demand parse is a
  separate explicit operation on a captured source snapshot, with limits and no module evaluation.
- Diagnostics retain severity, message, available location and originating attempt/revision. Do not attribute a
  process-wide console's unrelated messages to a document. Limit retained output and report truncation.
- Fresh captures identify the exact document, model result and view. Finish or reject camera transitions before
  capture; respect drawing/modal/busy guards. Camera scripts may affect a subsequent evaluation. Avoid promising
  zero application side effects from camera changes where existing Animate behavior schedules reevaluation.
- Original annotation images stay immutable and readable while the GUI is busy where existing behavior permits.
  Captures exclude navigation/palette controls and historical strokes, following the annotation/navigation contracts.
  The navigation feature's newer capture contract also excludes statistics, axes, scale markers and crosshairs;
  preserve that contract when integrated without modifying stored evidence. Surface/edge rendering stays model
  content. A core build that precedes that integration reports its actual capture policy rather than claiming
  helper-free output it cannot yet provide. Use native viewport dimensions; custom-resolution offline rendering
  is outside this first scope. Never substitute another viewport or a desktop screenshot for an unavailable target.
- Use native camera operations and saved-view ownership; enforce revision checks for metadata mutations as well as
  camera operations. Concurrent user edits must conflict rather than be overwritten. Match native undo behavior and
  do not introduce a separate agent-only history.
- Read-only status distinguishes a responsive listener from a responsive GUI. Bounded results, queue limits,
  cancellation semantics, duplicate-request receipts, expiry and restart behavior must be explicit.
- Retain current annotations-client compatibility when consolidating the service, or supply an explicit versioned
  migration. One service lifecycle controls all capabilities; no competing listener or hidden fallback connector.
- Place discoverable agent-access controls outside reliance on the Annotations dock. Report capabilities and API
  version; preserve explicit instance choice. A broad service must not silently expand an old annotation-only consent.
- Ship maintained agent instructions and examples covering discovery, disk/editor divergence, explicit source
  selection, dirty-source checks, tree traversal, job outcomes and image verification through the agreed CLI/skill.

### Engineering and validation work for the next phases

Define read/operation contracts, ownership and failure behavior in requirements, then choose transport extraction,
GUI dispatch, immutable snapshots, parser/evaluator adapters and compatibility mechanisms in the technical plan.
Endpoint spelling, node schema layout, page sizes and exact resource budgets are engineering choices within the
product decisions above. No additional user decision is needed for routine implementation details.

Prototype tree/source mapping and capture lifecycle before promising implementation completeness. Validation must
cover unsaved and invalid source, expanded loops/modules, 2D/3D/empty models, stale results after failed compilation,
changed dependencies, multiple windows and duplicate paths, close/reopen, user/agent races, busy drafts, camera
transitions, large/truncated responses, expired jobs and server restart. Verify saved-view persistence when its
adapter is integrated. Verify existing annotation clients against the consolidated service and its stopped/disabled
state. Initial runtime validation is Windows x64 with the existing shared dependencies; other platforms remain a
separate verification claim.

Annotations and navigation remain separately owned worktrees. Their ownership contracts inform requirements, but
integration must use reviewed committed feature revisions rather than another chat's uncommitted work. Reusing the
annotations transport requires a reviewed dependency/extraction boundary before implementation. Navigation is a
prerequisite for its saved-view adapter only, not the core. This does not change the manually selected combined-build
stack or its readiness: a core delivery decision does not authorize omitting navigation from a SCADMaxx build.

The exploration is complete enough to write requirements. Technical design, prototypes and validation still follow;
this is not implementation readiness or a claim that the new APIs work. Stack readiness remains false. Review edits
are confined to this feature's planning and descriptive pending reason; other features and build selection are unchanged.

### Second completeness pass

Rechecked the complete exploration against the annotations client contract, navigation exploration/requirements,
and selected build sources. The four user decisions remain consistent. Clarified explicit disk/editor parsing,
parse failure and dependency provenance, the automatic-reload prerequisite, never-evaluated/stale models, optional
metadata/metric capabilities, units and count meanings, and the newer navigation capture policy. These refinements
implement existing decisions and introduce no new product questions.

First-scope acceptance must demonstrate: explicit live targeting; distinct disk/editor inspection; parse-only
success/failure without changing the displayed model; bounded parsed/evaluated tree traversal; attributable
diagnostics; accepted evidence retrieval; camera control and fresh capture; and reliable status/job handling through
the documented HTTP and CLI/skill workflow. Optional metadata and later saved-view adapters have separate coverage.
Validate Unicode paths/text, disk/editor divergence, source changes during inspection and disabled automatic reload
alongside the failure/concurrency matrix above. Long reads/jobs remain bounded; no idle polling should force repaint
or evaluation. Exact limits and test fixtures belong in the next phases.

Readiness is specifically for writing `2_requirements.md`. Public schemas, dependency extraction, prototypes,
implementation steps and executable acceptance evidence remain work for their respective later phases. Build-source
readiness remains false; its descriptive pending reason now refers to requirements and implementation rather than
an undecided feature scope.

## Planning handoff

The user subsequently requested requirements, an overall plan and phased implementation plans. These now exist as
linked above with requirement coverage, concrete source integration points, initial protocol/schema/resource design,
validation fixtures and phase exit evidence. Earlier review-readiness statements describe the preceding exploration
checkpoint. No requirement pass or runtime verification is claimed by writing these documents.

Navigation moved to `.plans/2_in-progress/2026-10-01_navigation-cube` during this planning pass; use that current
location for its requirements and implementation updates. Core delivery still does not wait for its adapter.
The annotations committed dependency boundary and parse-state isolation are explicit phase-1/phase-3 checks,
not unresolved product choices. Keep the current planning lane and source readiness false until implementation.
