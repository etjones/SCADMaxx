# HTTP agent server — requirements

Status: core requirements implemented and validated; navigation adapter in progress. See implementation notes for evidence.
Core requirements R01–R24 define the first delivery. N01–N03 apply only to the later navigation adapter.

## Scope and service

### R01 — First-delivery boundary

Provide live document/source inspection, explicit syntax parsing, parsed and evaluated trees, diagnostics,
annotation reads, viewport control, fresh capture and outcome/status inspection in the running GUI instance.
Exclude source writes, document open/close/switch/save, forced reload/preview/render, parameter writes, exports,
annotation mutation, arbitrary execution, remote listeners, headless rendering and MCP. Saved views are later work.

Acceptance: a documented operation inventory and negative-route tests demonstrate this boundary. Reading state
never invokes excluded operations. Ordinary file tools remain the editing path.

### R02 — Enablement and lifecycle

Provide discoverable Enable, Stop and Copy connection info controls without requiring the Annotations dock.
Remember explicit broad-service enablement across launches. Existing annotation-only consent must not automatically
enable newly exposed source/tree inspection. One service lifecycle governs all exposed capabilities. Stop rejects
new work, invalidates the server session and prevents queued actions from starting; report running-work limits honestly.

Acceptance: disabled, enabled, restart, legacy-consent migration and Stop tests show the actual accessible capabilities.

### R03 — Local discovery and access

Listen on numeric loopback at an automatically allocated port, without a secret token. Publish per-instance local
discovery and verify it against live service information. Preserve protocol/Host/browser-request guards. Do not
follow redirects, enable CORS or silently choose a different process when discovery is stale or ambiguous.

Acceptance: two instances are distinguishable; stale discovery cannot establish identity; incorrect headers, Host,
Origin and browser fetch metadata fail without executing operations. Document the local-process trust model.

### R04 — Explicit targets and lifetime

Expose process/server, window, document and viewport identities. Distinguish the active editor from the displayed
model's owner, duplicate file paths and untitled documents. Reopening a document or restarting the server invalidates
old handles. Resolve actions against their submitted identities, never whichever tab later becomes active.

Acceptance: cross-tab/window, duplicate-path, close/reopen and queued-action races cannot retarget operations.

### R05 — Compatibility and capabilities

Publish API/schema versions and supported capability groups. Preserve the existing annotations client contract on
the consolidated listener, including discovery, evidence retrieval, capture, view/restore and outcome polling.
Capabilities reflect runtime availability; absent optional integrations return a structured unsupported result.

Acceptance: the unchanged bundled annotations client completes its existing workflow; the new client rejects
unsupported versions and distinguishes absent functionality from temporarily unavailable data.

## Source and model inspection

### R06 — Disk and editor provenance

Disk files remain authoritative for the file-based agent workflow. Explicitly select disk or editor origin for source
snapshots; never substitute one for the other. Return document/path, origin, revision/hash and dirty/divergence state.
Untitled documents report no disk version. Restrict server source access to explicit open-document/dependency context.

Acceptance: differing disk/editor text yields separately identified snapshots. Reads change neither text nor dirty
state; an untitled disk request fails clearly while explicit editor inspection works. Unicode text round-trips.

### R07 — Explicit parse-only operation

Parse a captured disk or editor snapshot on explicit request, without module evaluation, saving, viewport changes,
tab switching or contamination of normal compiler caches/state. Return that attempt's success/failure and diagnostics.
Reads of existing trees do not initiate parsing. A failed parse never returns an old tree as a fresh successful result.

Acceptance: valid, invalid and unsaved sources parse with unchanged live model/result, editor, camera and undo state;
a subsequent normal preview behaves identically to one without an intervening parse-only request.

### R08 — Dependencies and limits of provenance

Report known include/use/import dependencies with requested/resolved paths, kind, available source location,
origin and availability. Distinguish dependencies read by parsing from ones actually used by an evaluation. Do not
evaluate imported geometry to inspect syntax. Editor parsing must not overlay unrelated open buffers onto disk files.
Unknown hashes or dynamically determined imports remain explicitly unknown; do not claim atomic cross-file snapshots.

Acceptance: relative paths, library paths, missing/cyclic dependencies, changed includes and dynamic import expressions
produce truthful provenance and bounded outcomes. A matching root hash alone cannot verify a dependency edit.

### R09 — Parsed source tree

Expose a structured, bounded syntax tree with snapshot-scoped node IDs, node kind/name, available source spans,
named child roles and expression/argument structure. Cover module/function definitions, assignments, instantiations,
control constructs and expressions. Mark unavailable locations and omitted/truncated data explicitly.

Acceptance: fixtures with nested modules/functions, loops, conditionals and expressions can be traversed in pages;
old node IDs never resolve into a new parse. Unknown syntax kinds retain an explicit typed fallback, not fake structure.

### R10 — Evaluated model tree

Expose the instantiated geometry/CSG-operation hierarchy from actual completed evaluation, with result-scoped IDs,
ordered children, operation names, available evaluated properties and source mapping. Distinguish it from syntax and
lowered renderer-specific CSG data. Report synthetic nodes, missing mappings, root selection and incomplete data.

Acceptance: loop expansion, transforms, Boolean operations, repeated module calls and the root modifier are traceable
without reevaluation. Recompile cannot invalidate memory used by an in-flight read or reuse an old public node ID.

### R11 — Attributable diagnostics

Provide bounded errors, warnings, echo/assert output and available duration/location data, tied to the actual parse or
evaluation attempt. Separate unrelated/global messages. Preserve the normal GUI console and diagnostic behavior.
Report truncation and unavailable historical diagnostics instead of reconstructing them from unrelated console text.

Acceptance: interleaved windows, parse-only errors, normal preview errors and echoes retain correct attribution;
enabling/disabling the service neither swallows messages nor duplicates them in the GUI.

### R12 — Results and freshness

Distinguish source revisions, parse snapshots, evaluation attempts, successful model results and displayed-result
identity. Represent never-evaluated, busy, failed, empty-success and stale states separately. A newer failed attempt
may coexist with an older displayed model; that image cannot verify the newer source.

Acceptance: successful preview/render, empty success, parse failure, evaluation failure and dependency-only changes
produce the correct state transitions. Parameter/source context belongs to the actual result, not current UI values.

## Evidence, navigation and concurrency

### R13 — Annotation evidence

List/search/read accepted annotations and original PNGs, including unsaved evidence, through the native store.
Keep images immutable and reads available from published snapshots while the GUI is busy where supported. Reading
evidence never moves the camera or edits/deletes an annotation. Explicit restore changes only the live camera.

Acceptance: retrieval preserves checksums before/after model edits and during a draft; restored historical viewpoints
show current geometry without historical strokes. Wrong-document evidence is rejected.

### R14 — Camera operations

Support explicit camera values, standard views, projection and fit through native semantics. Validate finite values
and targets. Actions check expected result/view revisions, respect locks and return the resulting camera revision.
Preserve normal SCAD camera conventions and explain subsequent script/Animate reevaluation effects.

Acceptance: principal views and both projections match native actions; stale requests, invalid values and user races
do not overwrite a newer camera. Agent control does not edit source or create a saved-view entry.

### R15 — Fresh capture

Capture the explicitly targeted native viewport at its current pixel dimensions. Return PNG, checksum, dimensions,
camera, document, displayed-result and view revision plus the actual capture policy. Frame readback must correspond
to these identities. Reject unavailable targets rather than substitute desktop or offline-render images.

Acceptance: inspect pixels and metadata after camera changes, resize and failed compilation. Exclude palette/control
UI and historical strokes. When navigation is integrated, also exclude guides/statistics under its clean-capture
contract; retain surface/edge rendering and never rewrite historical images.

### R16 — Busy states and interaction

Respect native annotation draft/capture/modal guards and evaluation conflicts. Invalid operations return busy or
stale without secretly deferring until user interaction ends. Capture coordinates with camera transitions; no late
callback may subsequently overwrite the captured camera. Reads must not mutate GUI objects from transport workers.

Acceptance: marked/unmarked drafts, modal entry, active compilation, transition interruption, resize and close produce
documented outcomes, with no deadlock, nested render loop or accidental target change.

### R17 — Asynchronous outcomes and retries

Operations have caller-generated request IDs and queued/running/terminal outcomes. Acceptance is not completion.
Identical retries within a server lifetime do not execute twice; changed input under an ID conflicts. Expired results
retain sufficient receipts to prevent reexecution. Restart invalidates IDs; clients never automatically resubmit them.
Cancellation distinguishes never-started work from running work that cannot yet stop safely.

Acceptance: lost responses, retries, conflicting input, cancellation, expiry, capacity exhaustion and restart preserve
at-most-once dispatch per server/request ID. Partial execution cannot be reported as never started.

### R18 — Bounded work and retention

Bound input/header sizes, connections, queue depth, read/output sizes, tree traversal, retained snapshots, diagnostics
and image/results memory. Publish practical limits and truncation/expiry behavior. Reject over-limit input before
unsafe allocation; normal rendering must not copy an unbounded second model solely for inspection.

Acceptance: large/deep sources/trees, oversized bodies, slow/disconnected clients and retention pressure terminate
with bounded results. A GUI timeout is not falsely described as cancelling running native code.

### R19 — Status and change observation

Expose monotonic state generations, GUI-heartbeat age and busy reasons. Polling must not trigger evaluation, paint,
source writes or tab switching. Report disabled reload, unsaved-source conflicts and missing fresh results explicitly.

Acceptance: external root/include/use edits yield a new successful generation when normal reload works; disabled
reload and failed evaluation remain non-successful regardless of elapsed time. Idle polling causes no render loop.

### R20 — Native state and file ownership

Inspection does not clear undo, save files, enable reload or resolve disk/editor conflicts. View operations preserve
source/Customizer dirtiness and native undo semantics. File edits remain the agent's explicit filesystem operations,
with live-status and concurrent-file checks taught in the skill; the server is not a filesystem transaction manager.

Acceptance: snapshot text, dirty flags, source timestamps, active tab and undo availability before/after operations;
only explicitly requested camera effects and permitted native follow-on behavior differ.

## Delivery and optional inspection

### R21 — Optional metadata contract

If advertised, Customizer inspection reports available parameter names, types, values, descriptions, constraints and
presets with editor/result provenance. Geometry summaries report available bounds/dimensions/counts and backend/result
kind. Missing data is unavailable/not-applicable, never invented zero; SCAD coordinates have no assumed physical unit.
These capabilities may be omitted from core delivery with an explicit recorded reason, without weakening R06–R12.

Acceptance: advertised fields are tested for stale, 2D/3D, empty and unsupported cases; no implicit full render,
parameter mutation or new expensive geometry computation occurs. Facets and triangles are not conflated.

### R22 — HTTP, CLI and skill

Ship a versioned HTTP contract, Python standard-library CLI and self-contained agent skill. Cover explicit discovery,
targeting, source origins, parsing/tree traversal, diagnostics, evidence, cameras, captures and outcome polling.
Decode/check PNGs into explicit output paths. No MCP adapter, dependency, installation or follow-up is included.

Acceptance: a client used outside the source checkout completes the documented workflow without third-party Python
packages; stdout machine results, stderr diagnostics and exit codes are consistent. No automatic cross-instance retry.

### R23 — Validation baseline

Verify Windows x64 GUI Release with shared dependencies, meaningful unit/protocol/native tests and actual captured
image inspection. Include Unicode paths/text, multiple instances/windows, lifetime races and failure cases above.
Retain source/build/test provenance and distinguish automated, manual, unsupported and untested cases.

Acceptance: the core phase-6 matrix passes or documented failures are resolved before delivery. A compile-only success
is not sufficient. No claim of Linux/macOS or clean-machine validation without corresponding evidence.

### R24 — Independent delivery and integration ownership

Keep implementation on the dedicated branch/worktree and workspace planning/evidence outside upstream source changes.
Use reviewed committed annotations dependencies/extraction boundaries. Core delivery does not require navigation;
do not copy unfinished work or duplicate its saved-view store. Keep build selection and readiness honest.

Acceptance: reviewed diff/ancestry, exact prerequisite revisions and retained test records identify what was delivered.
No GitHub publication, combined experimental build or unrelated feature changes are implied by this work item.

## Later navigation adapter

### N01 — Native saved-view access

Once navigation is integrated, advertise list/add/rename/remove/recall using its native document-owned records.
Use stable record IDs, complete camera snapshots and optimistic library revisions. No parallel storage format.

Acceptance: native UI and API see the same entries; add captures the displayed camera; recall restores pose,
distance, FOV and projection at the current viewport size without auto-fit or overlay changes.

### N02 — Persistence and concurrency

Metadata mutations remain unsaved until ordinary native saving; source reload retains them. Respect native undo,
close, Save As/copy/all, conflict and backup behavior. Requests never silently save or bypass a conflicting user edit.

Acceptance: restart after native save, untitled first save, source reload, final-entry deletion and concurrent edits
match the navigation requirements. Copying does not rebind or clear the original document's dirty state.

### N03 — Integrated locks and capture

Share navigation/annotation camera guards and clean capture policy. Absent integration advertises no saved-view
capability. Adapter completion is separate from core readiness.

Acceptance: combined tests exercise marked drafts, camera transitions, clean pixels, stale library/view requests and
legacy annotations compatibility using reviewed committed feature inputs.
