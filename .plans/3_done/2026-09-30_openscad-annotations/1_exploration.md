# Native OpenSCAD annotations

## Intent and current state

Post-implementation decision: the OpenSCAD palette is fixed, with an arrow cursor over it. This supersedes the
movable-palette recommendation after the user reported repaint streaks while dragging. Blender behavior below
remains reference context, not a requirement to retain palette dragging.

Implement the behavior of the Blender Agent Annotations plugin in OpenSCAD: mark the displayed model, attach
optional context, retain the original image and viewpoint, let an agent inspect the evidence and change the design,
then inspect a fresh view. The user explicitly selected the Blender behavior as the reference on 2026-09-30.

This is an exploration informed by source inspection, not frozen requirements or implemented functionality.
The recommendations below distinguish direct behavior parity from adaptations to OpenSCAD's source-driven model.
Keep the feature independently reviewable and suitable for an upstream PR, with Windows validation first.

Development checkout: `D:/openscad/wt-openscad-annotations`, branch `feature/annotations`, based on upstream
`612e684c2cbbcdcb9a7a8307973f33fd910f9c17`. It is a worktree of `D:/openscad/openscad-master`; `origin` is the
existing user fork. No annotation implementation, build configuration, feature commit, push, or PR exists yet.

Review on 2026-09-30 reconfirmed the Blender behavior against the two source trees. It corrected four design gaps:
cross-tab save/undo targeting, ownership of blank or failed views, lexical hazards in embedded storage, and source
identity arriving too late in the implementation sequence. Storage and unified undo still need executable prototypes;
this source review establishes neither runtime parity nor build readiness.

The completeness review's user decisions are now settled: companion-file storage, drawing only, external agent
edits through ordinary file tools, and OpenSCAD's existing automatic reload. There is no editor-editing,
reload/compile, or document-switching API in this feature. The next planning deliverable is testable requirements,
followed by an implementation plan. Engineering mechanisms below remain subject to focused prototypes.

The user selected the existing undo-reset behavior on automatic source reload: clear source and annotation undo/redo
together, retaining current annotation contents and unsaved state. Do not add history-preservation machinery.

## Reference inspected

Blender source: `D:/source/blender-annotations`, commit `f8f84ed4de7efc34dce02b4fbb61cc44d62d1f4e`, runtime version
**0.3.3**. The working tree had only unrelated editor settings and `.serena` changes. This investigation read
documentation and implementation; it did not run Blender or repeat its recorded acceptance tests.

Primary reference files:

- [Usage](D:/source/blender-annotations/docs/usage.md),
  [storage foundation](D:/source/blender-annotations/docs/annotation-foundation.md), and
  [creation](D:/source/blender-annotations/docs/annotation-creation.md).
- [Owned API](D:/source/blender-annotations/docs/owned-http-api.md) and its maintained
  [HTTP contract](D:/source/blender-annotations/skills/agent-annotations/references/http-workflow.md).
- [Draft history](D:/source/blender-annotations/blender_annotations/drawing.py),
  [drawing controller](D:/source/blender-annotations/blender_annotations/drawing_ui.py),
  [palette](D:/source/blender-annotations/blender_annotations/palette.py),
  [record validation](D:/source/blender-annotations/blender_annotations/records.py), and
  [packed storage](D:/source/blender-annotations/blender_annotations/store.py).
- [Verification history](D:/source/blender-annotations/docs/verification.md): evidence is specifically for the
  tested Blender 5.2.1 Windows/OpenGL environment. Historical sections describe older releases; use 0.3.3 behavior.

## Blender reference behavior and agreed differences

### Creation and drawing

**Annotate issue** is a one-shot viewport tool. No selection is required. Orbit/pan/zoom remains available until
there is an active or completed stroke; thereafter the view is locked to prevent marks drifting relative to geometry.
Releasing the left mouse button finishes one stroke, not the annotation. Additional strokes may have different colors.

The movable viewport palette has twelve colors: red, orange, yellow, lime, green, cyan, blue, violet, magenta, pink,
white, and black. Yellow is initially selected. Colors affect future strokes only; the last color survives between
drafts within the running plugin session. Strokes have a contrasting outline. Palette controls never enter the PNG.
The palette remains usable when the annotations sidebar is hidden.

Ctrl+Z and Ctrl+Shift+Z undo/redo complete draft strokes with their original colors. Undoing every stroke permits
navigation again; actually changing the view clears stroke redo. Tiny clicks do not create strokes. Leaving the
drawing rectangle discards that active stroke without deleting earlier ones. Escape/right-click cancels the draft.
Status hints explain the current controls. The former modeling tool remains available after finishing or cancelling.

Enter/numpad Enter between strokes captures the view and opens a centered, immediately focused comment dialog.
Zero strokes and an empty comment are valid. **Add annotation** accepts; **Back to drawing** retains marks, history,
and entered text; **Cancel** discards. Returning from the dialog invalidates the old pending capture and the next
Enter captures again. Use native Qt dialog/input conventions; Blender's pointer warp and text-edit click quirks
are implementation details to avoid copying, while retaining equivalent keyboard access and immediate text focus.

**Annotate selection** is a separate action: it captures visible selected objects or mesh elements and descriptive
selection metadata. No selection creates no record. It does not change selection or mode. This part of the Blender
feature is explicitly excluded from OpenSCAD: the user chose drawing only.

### Review, persistence, and history

The list shows every annotation in the current Blender file, across its scenes, newest first. Selecting a row shows
the original fitted thumbnail and full wrapped comment; it does not move the live view or reselect geometry.
Comment search is case-insensitive. **Edit comment** changes only text. **Delete** confirms deletion and is the
completion mechanism. There are no issue statuses, resolve/reopen actions, or automatic deletion after an agent edit.

Each accepted record owns immutable PNG evidence and the original view/source metadata. Geometry changes, renamed
or missing source objects/scenes, and comment edits do not replace its image. Create, comment edit, and delete are
individual native undo steps, including when interleaved with modeling edits. Undo retains the image data needed
to restore a deleted record. The reference has an inline thumbnail, not a separate full-image viewer.

**Restore view here** is explicit and targets a particular current viewport. It restores a view of current geometry,
not historical geometry. It leaves selection, source model, frame, and shading alone. Missing or incompatible targets
produce an explanation. Size changes can change framing; the original PNG remains exact.

Blender stores validated JSON on packed image data inside the `.blend`. Save, Save As, and copying the file retain
annotations without a companion directory. Accepted but unsaved annotations are immediately readable by agents;
creating/editing/deleting an annotation never saves the model automatically. Saved evidence survives opening and
saving with the plugin disabled. OpenSCAD deliberately adapts this to a companion file, as selected by the user:
normal Save/Save As/Save a Copy handle both, while manual copying must include both files.

### Agent access

**Enable Agent Access** opts into an owned localhost server and future automatic startup. **Stop** rejects new work
and cancels queued work; it does not promise to interrupt work already executing. **Copy Connection Info** and
per-instance discovery identify the intended process. Consent and endpoint settings live outside model files.

The agent can list/read accepted annotations and retrieve original PNGs, enumerate viewports, capture a fresh view,
restore an explicit view, and execute Blender Python. Queued operations have request IDs and terminal outcomes;
an HTTP acceptance response is not completion. Instance/server/session identities and history epochs prevent stale
requests from acting on replacement contexts. Repeated identical requests do not execute twice.

Reads of accepted evidence remain available during annotation creation; model/view mutations and fresh capture
report busy while drawing, capturing, or editing annotation context. The agent examines full images, makes an
authorized correction, and verifies a fresh capture. The companion skill teaches this behavior.

## Existing OpenSCAD integration points

All paths below are relative to the annotations worktree and refer to the inspected upstream commit.

| Existing source | Observed capability | Proposed use |
| --- | --- | --- |
| `src/gui/QGLView.h/.cc` | QOpenGLWidget, mouse/wheel handlers, camera/resized signals, `grabFrame()` using `grabFramebuffer()` | Draft input, viewport capture, view invalidation |
| `src/glview/GLView.h`, `src/glview/Camera.h` | Renderer, camera, projection matrix, axes/edges/scale, projection and gimbal state | Capture provenance and explicit camera restoration |
| `src/gui/MainWindow.cc/.h` | Preview/render lifecycle, `renderedEditor`, `activeEditor`, node selection, PNG export | Bind evidence to the displayed model and coordinate busy state |
| `src/gui/TabManager.cc/.h` | Open/save/Save As/Save a Copy/close, reload signals, dirty prompts | Document ownership and annotation persistence |
| `src/gui/Editor.h`, `src/gui/ScintillaEditor.cc/.h` | Editor contents, content-change signals and native text undo | Source revisions, unsaved state and unified annotation undo |
| `src/gui/Dock.h`, MainWindow's dock list | Application dock widgets and persisted window state | Annotations panel integrated with existing layout controls |
| `src/gui/WindowManager.h`, `src/gui/OpenSCADApp.h` | Multiple windows in one process | One process-level service with explicit document/window/view IDs |
| `CMakeLists.txt`, `src/guitests` | Qt networking, libzip, Catch2 and GUI test infrastructure | Existing dependencies and focused regression tests |

Existing `src/gui/Network.h` is outbound networking infrastructure; an annotation HTTP server does not already
exist. Likewise, existing `core/customizer/Annotation.h` describes SCAD parameter annotations. Do not overload that
class with viewport evidence: use a distinct namespace such as `AgentAnnotations` and dedicated GUI components.

## Proposed OpenSCAD user workflow

Add an **Annotations** dock with **Annotate issue**, search, newest-first rows, inline
thumbnail, full comment, **Edit comment**, **Delete**, and **Restore view here**. Add the access controls in the same
panel. Register it through the existing dock/menu system, including layout save/restore and undocking.

Bind the store to the root SCAD document whose compiled model is displayed. Identify that document visibly in the
panel. Clicking a different editor tab does not transfer ownership of the viewport or its annotations. Viewing an
included library tab can coexist with a model compiled from another root document. Historical records retain the
root identity. The initial panel reviews the displayed model's store; no cross-document review selector is needed.
Do not silently switch the target because the active editor changed.

When no model is displayed, require a visibly identified open document as the owner before starting a blank capture;
an untitled document is valid. Freeze that identity for the draft. Closing the rendered root currently clears the
viewport in `MainWindow::onTabManagerAboutToCloseEditor`; cancel its draft and clear the panel's live target too.
Do not silently attach the resulting blank viewport to another tab. Review of another store is an explicit action.

Save and undo must target the same document as the user's action. With the annotation dock or its viewport focused,
route these commands to the displayed annotation owner and identify that owner in action labels. With a source
editor focused, preserve that editor's normal command target. Restore focus to the annotation context after accepting
a dialog. In particular, adding to model A while editor B is active must not make the next annotation-context Undo
undo B's text, or make Save silently save only B. This requires action routing as well as shared undo storage.

The end-to-end loop is: open and preview the intended document with automatic reload enabled, navigate, draw, add
optional context, and let the external agent retrieve the image and comment. The agent edits the SCAD files with its
existing file tools; OpenSCAD automatically reloads and previews the changes. The agent waits for that update and
captures the new view. The user reviews and deletes the original annotation when satisfied. Saving annotations
remains a normal user action; the agent's ordinary source-file writes are independent of annotation persistence.

## Drawing and capture design

Use an `AnnotationController` with explicit idle, drawing, capture-pending and comment states.
A draft binds to document/window/viewport IDs, a rendered-result revision, camera state, viewport dimensions,
device-pixel ratio, and a draft revision. Only acceptance publishes a complete record. Late callbacks carry the
draft token and cannot accept a cancelled draft or attach evidence to a newly opened document.

Camera binding is not frozen at tool entry: while no active or completed stroke exists, a permitted view change
updates the draft's camera baseline and clears stroke redo. The first active stroke locks that baseline. Undoing all
strokes unlocks it again. Keep the document/result identity fixed throughout; free navigation does not retarget it.

Use a transparent Qt overlay above the viewport for strokes and a fixed palette child widget. Intercept relevant
mouse/key events while active, and pass normal navigation through only while there are no marks or active stroke.
Suppress ordinary object picking, measurements, and context menus for consumed annotation input. Reuse the same
stroke painter for the visible overlay and final QImage composition, drawing the model framebuffer once and adding
the marks once. Do not capture the whole desktop or use an offline rerender as a substitute for the displayed view.

Prototype overlay stacking with QOpenGLWidget before committing to this design. An alternative is drawing strokes
after `GLView::paintGL()` with palette controls outside that capture path. Keep one rendering path for stroke shape,
outline, color and antialiasing; test pixel correspondence rather than assuming two painters look equivalent.

On Enter: validate the target and draft, request a redraw, wait for acknowledgment of the intended frame, copy the
framebuffer, compose marks, and open the dialog. Revalidate identities, revision and dimensions before publishing.
Copy the QImage returned by `grabFrame()`; do not retain a reference to its mutable member buffer. Encoding can run
off-thread on detached image data, while widget/OpenGL operations remain on the GUI thread. Do not rely on a fixed
sleep or recursively call a framebuffer grab from inside paintGL.

Store positions normalized to the PNG's top-left coordinate system, plus image dimensions, capture rectangle,
device-pixel ratio and explicit width units. Convert logical mouse coordinates to physical image pixels exactly
once. Scale the Blender palette/stroke measurements deliberately for Qt DPI behavior. Reject or cancel a draft
when resize, monitor-scale change, renderer replacement, tab/window closure, or document reload invalidates it.
Never stretch old strokes onto a changed image. Cache completed paths and thumbnails; avoid redraws or full-store
rescans on idle ticks, following the performance lessons from Blender 0.3.3.

Prevent navigation from every entry point while marked, including wheel, keyboard view shortcuts, viewport controls
and agent requests. Coordinate animation, auto-reload, Customizer changes and compilation with a scoped draft guard.
Unexpected source/evaluation changes invalidate the draft. Restore previous animation/reload settings on exit;
do not leave a global GUI lock held after cancellation. `GuiLocker` is process-global and currently guards several
compile actions; its semantics must be integrated explicitly rather than assumed to protect every mutation.

## Source and rendered-result identity

`activeEditor` and `renderedEditor` are distinct. In addition, `renderedEditor` is assigned during instantiation,
before all work has necessarily succeeded, and the displayed model can predate unsaved source edits. Therefore
neither the active tab, current file bytes, nor the pointer alone is sufficient capture provenance.

Introduce immutable rendered-result metadata, published when a preview/render result is actually installed.
Associate it with the renderer and a monotonically increasing result ID. Minimum metadata includes the owning
document/session, captured path, input source revision/hash, effective Customizer values,
animation time, relevant evaluation settings and renderer/backend. Capture camera/display state at capture time.
Bind evaluation input identity when the operation starts; do not infer it from `activeEditor` on completion.

Historical source text and complete dependency tracking are excluded from the initial version. Blender's record
stores source filepath/scene/view-layer descriptors, not historical project contents. Record reliable root-input
identity and report unknown dependency provenance explicitly. If dependency hashes are available, capture them
when their bytes are consumed, including cache reuse; rereading files at screenshot time cannot establish what
produced the image. Existing SourceFile dependency lists are not a complete immutable provenance service.
Do not copy source files, dependencies or binary assets into every record.

Permit evidence of an older still-displayed result with an explicit stale-source indication and both rendered and
current editor revisions. Failed recompilation must not relabel an old image as new source. Failure can also clear
the renderer: `instantiateRoot()` resets it before evaluation, so retaining the previous image is not guaranteed.
Track evaluating, installed, empty and failed/no-result states separately; stale provenance cannot outlive its
renderer. A successful empty model differs from a failed evaluation. Blank/no-model screenshots can follow the
zero-stroke workflow with an explicit owner and no fabricated successful-result identity.
Once marks exist, a changing rendered result cancels the draft rather than accepting a mismatched capture.

## Drawing-only scope

The user explicitly excluded picked objects for OpenSCAD. Provide no Annotate selection action, annotation picking
mode, object highlight, node/instance anchors or mesh-element metadata. Drawing works independently of picking
support in the current renderer. Normal OpenSCAD selection and measurement behavior resumes after the drawing tool
exits. Selecting an annotation row never invokes source navigation or changes the live model selection.

## View restoration

Store OpenSCAD-native camera data: projection, translation/rotation, distance, field of view, viewport size, and
effective matrices. Use Camera's user-space accessors consistently; Blender quaternion/lens fields are not an
interchange format for this camera. Record color scheme, renderer and display toggles as provenance.

Restore only to an explicitly selected live viewport of the matching document, using current geometry. Change
camera state only; do not edit `$vpt`/`$vpr`/`$vpd`/`$vpf`, Customizer values, source selection, animation time or
shading. Camera variables in SCAD can override the restored live view at the next evaluation; explain that behavior
rather than modifying source. Different viewport aspect ratios can change framing. Missing/closed documents,
stale IDs and incompatible camera state fail explicitly. The old PNG remains usable even when restoration cannot run.

Saved strokes belong to the original screenshot. They are not reprojected onto changed geometry during restoration
or included in a fresh verification capture. Fresh captures show the live viewport without annotation palette or
review UI; only a newly accepted annotation capture composites its current draft strokes.

## Companion-file persistence

The user selected a companion file: `model.scad` stores ordinary source and `model.scad.annotations` stores its
annotations. Keep both in the same directory. Save As and Save a Copy carry the annotations to the corresponding
destination companion; manual copying/renaming must include both. Stock OpenSCAD can edit the source while leaving
the companion untouched. A changed source does not invalidate historical screenshots or automatically erase them.
No image data or metadata comments are inserted into SCAD source, including unfinished source.

Use a versioned bounded archive containing a manifest and immutable PNGs; existing libzip is a candidate
implementation. Use an OpenSCAD-specific schema, UUID record IDs, UTC timestamps, comments, image dimensions/hashes,
normalized strokes, source/result metadata and native camera state. Historical root-source snapshots are excluded.
Blender schema-2 records are not an interchange format for OpenSCAD's source/view structures.

Acceptance changes in-memory annotations and dirty state only. Unsaved/untitled documents remain agent-readable.
Normal Save writes their companion alongside the chosen SCAD path. Include annotation changes in tab/window dirty
indicators, Save All, close prompts, backup/recovery and external-change handling. Annotation-only changes should
not rewrite the SCAD source or trigger geometry rebuilding. Reading records must not create or migrate a companion.

Integrate every lifecycle path: `TabManager::refreshDocument()`, ordinary save, Save a Copy, and
`MainWindow::writeBackup()` currently handle source separately. Save a Copy includes current annotations without
changing the original document's path or clearing its dirty state. Backups must retain both source and evidence.
Reload/discard must account for unsaved annotation changes and invalidate stale history/request tokens as needed;
an external source-only edit must not silently discard unsaved annotation work.

Keep source, Customizer and annotation dirty state distinct. Combine them for close/save indicators, but do not
make `isContentModified()` report an annotation-only change to `checkEditorModified()`: that would turn the normal
agent/reload loop into a source-discard prompt even when source has no unsaved edits. A source-only reload retains
accepted records, unsaved comment changes/deletions and annotation dirty state in memory. It does not reload an
older companion over them, save annotations implicitly, or mark them saved. Clear stale draft/action tokens while
keeping the open document's identity. Only explicit document close/discard or companion reload discards that state.

Detect companion changes made by another process before overwriting them. Preserve both the in-memory work and
external file and report a conflict instead of silently choosing one. Missing or incompatible companion data must
not prevent ordinary source preview. A new document with no annotations needs no companion; saving deletion of the
last record writes a valid empty store so stale saved records cannot reappear on reopen. Include empty state when
overwriting an annotated destination through Save As/Save a Copy.

Two QSaveFile commits are not one atomic transaction. Define recoverable partial-save behavior and track each
component's saved state. Do not report complete success or clear unsaved annotation state if the companion write
fails. Save As/copy must also account for an existing destination companion so old destination evidence cannot
accidentally become attached to new source. Test interrupted writes, low disk space, read-only paths, missing
companions, deletion of the last annotation and crash recovery before freezing the persistence mechanism.

Retain unsupported/corrupt companion data for recovery; never overwrite unreadable evidence as an empty store.
Enforce entry/size limits, validate image dimensions/checksums and read archive entries without arbitrary filesystem
extraction. Measure realistic multi-image sizes, load/save latency and undo memory. File copying may preserve record
UUIDs, so runtime document identity must still distinguish an original from its copy.

## Undo and lifetime design

There are three histories: draft strokes, comment-field text, and accepted document changes. Ctrl+Z during drawing
affects draft strokes; text entry uses Qt's normal editing; accepted create/edit/delete should interleave with source
edits as normal document undo steps. A separate invisible annotation stack would not provide Blender parity.

OpenSCAD currently routes TabManager undo/redo directly to its editor. The installed Qt6 QScintilla headers expose
`SCI_ADDUNDOACTION`, `SC_MOD_CONTAINER`, and undo/redo notifications. Prototype a document-command adapter using
container undo tokens so annotation commands share the source editor's history without inserting metadata into the
visible source buffer. This API presence is verified; correct behavior with OpenSCAD's editor is not yet tested.
Keep the adapter behind EditorInterface rather than exposing QScintilla throughout the annotation store.

Each command retains before/after metadata and references to immutable PNG bytes; delete releases data only after
both the live store and undo history no longer need it. Track source and annotation save points together, including
annotation-only changes. Validate interleaved source edit/create/comment edit/delete/undo/redo, history truncation,
Save As, external reload and close. If the container mechanism fails, investigate a coordinated document history;
do not silently ship independent histories as equivalent behavior.

Use the existing source-reload boundary for both histories. `TabManager::refreshDocument()` calls
`ScintillaEditor::setPlainText()`, which calls QScintilla `setText()` and resets source modified state. The installed
QScintilla header documents that `setText()` clears undo/redo history. Clear annotation history and its obsolete
command tokens at the same boundary; do not retain or reconstruct it across that reset. This clears history, not
current annotations: accepted in-memory records, edits/deletions and annotation dirty state survive. Test this using
the actual external-edit/automatic-reload path. An include/use-only preview update that does not reset editor history
does not require an extra history reset. No undo action writes an older SCAD file over external changes automatically.

Use process-scoped runtime services and document-scoped stores. Keep runtime window/viewport handles separate from
persistent record identities. A document reopen/replacement changes the session; history changes advance an epoch;
source edits and installed render results have their own revisions. Use guarded QObject references for live targets
and detached immutable records for background work. Closing a tab cancels its draft/jobs and releases its preview
cache; closing a source document does not erase evidence already owned by another root's store.

Use runtime document IDs, not paths or copied persistent UUIDs, for request routing. Save As keeps the live document
identity while updating its current path; historical capture paths stay unchanged. Opening a saved copy creates a
new runtime identity even if record UUIDs match. Requests qualify annotation IDs by document. Pending edit/delete
dialogs bind record ID, document session and content version at opening; switching a row or undoing must not redirect
or revive them. A dialog result that no longer matches is rejected without a mutation.

## Agent API mapping

Retain the reference's opt-in process-local server, automatic port, instance discovery, Stop, and Copy Connection
Info. Distinguish the product as OpenSCAD in discovery, and expose capabilities and protocol/schema versions. One
process can have several windows/documents; add explicit document IDs instead of assuming one Blender file session.
Never choose the first process or viewport automatically when multiple targets match.

Proposed route names for the agreed annotation/view bridge; this is not an already implemented protocol:

| Operation | OpenSCAD mapping |
| --- | --- |
| `GET /v1/info`, `/v1/documents`, `/v1/viewports` | Health, live targets, active/displayed document identities, dirty/auto-reload/busy state and installed-result identity |
| `GET /v1/annotations?document_id=...&q=...` | Detached records and diagnostics; no implicit tab switch |
| `GET /v1/annotations/<id>?document_id=...` | Full metadata and original PNG bytes/base64 |
| `POST /v1/capture` | Fresh native viewport PNG, no record creation and no automatic compile |
| `POST /v1/annotations/<id>/restore` | Explicit document/viewport target; camera-only restore |
| `POST /v1/viewports/<id>/view` | Set a live camera for inspection using validated OpenSCAD camera fields |
| `GET /v1/requests/<request_id>` | Queued/running/succeeded/failed/cancelled/expired outcome |

The external agent edits root and included SCAD files through its existing filesystem tools. No API reads or edits
editor-buffer contents, reloads, compiles, saves source, opens documents or switches tabs. Do not add an execution
endpoint, arbitrary shell or Python requirement. Annotation create/edit/delete remain native user actions.

Use the existing auto-reload path: `MainWindow::checkAutoReload()` acts on the active document and `compile(true)`
checks root-file changes, includes and used-library dependencies. It also respects unsaved-source confirmation.
The verification loop assumes the intended root is active, automatic reload is enabled, and file edits can be
loaded without conflicting unsaved editor changes. Report inactive targets, disabled reload, dirty buffers or
pending confirmation in status; never switch tabs, enable reload or answer a discard prompt through this bridge.
This also leaves untitled/unsaved documents usable for annotations even when file-based correction is unavailable.

After changing files, the agent waits for the normal reload/preview cycle to finish before requesting evidence.
Expose evaluation state and installed-result identity through read-only status. Include result ID, root-input hash
and actual renderer in captures; support an expected-result check to reject a replaced result. A fresh screenshot
alone does not prove that external edits have loaded. Test included-file changes even when the root hash is unchanged.
Auto-reload produces a preview; do not imply an F6 render or silently request one. Failed/blocked reloads must not be
reported as successful verification, and a busy or unchanged result must not be accepted merely after a fixed delay.

Queued captures and camera operations use explicit request IDs, target identities and expected state. A lost
response is polled or retried with the same ID and identical input. No annotation bridge operation saves the design.
The companion skill must respect dirty editor state before external writes and detect changes made concurrently;
the annotation server is not the executor or transaction manager for the agent's filesystem edits.
Check draft/busy state before starting file edits as well. The bridge cannot prevent independent filesystem writes;
if an external change invalidates a draft, apply the documented cancellation behavior rather than accepting
mismatched image/marks. An annotation-only dirty flag is not a source-edit conflict.

Qt Network is already linked. Prototype an owned HTTP transport with bounded parsing/requests and a GUI-thread
action queue; choose the transport implementation after checking Qt-version/build impact. Existing outbound
Network helpers are not an HTTP server. Keep OpenGL/widgets on the GUI thread and serve cached immutable accepted
evidence from the service without attempting off-thread scene access. Expose heartbeat/busy state so a responding
listener does not falsely imply that compilation has left the GUI responsive.

Carry over numeric-loopback binding, Host validation, browser-origin rejection, no CORS, body/image/queue limits,
and server/session checks from the Blender protocol. Start with its bounded-job semantics; adapt practical limits
after measurements. Revalidate targets when a queued operation starts. During drawing/comment/capture, return busy
for restoring/camera changes/fresh capture while keeping accepted-evidence reads available. Stop cancels queued
bridge work; it does not cancel unrelated user rendering or control filesystem work performed by an external agent.
Consent and discovery data must never be stored in the annotation companion.

Ship an OpenSCAD-specific companion skill/client describing discovery, evidence retrieval, source correction,
automatic-reload verification and capture. Reuse the conceptual contract and pure fixtures where useful, but do not modify the
Blender skill so its Blender-specific instructions accidentally operate on an OpenSCAD instance.

## Implementation sequence and validation

1. **Resolve architectural risks with small prototypes:** viewport overlay/capture at mixed DPI; companion storage
   through normal saves and partial-write recovery; interleaved container undo; provenance across tab switches and
   failed compiles. Establish the Windows Qt6 GUI build independently of experimental PR composition.
2. **Document model and persistence:** pure record validation, immutable image ownership, dirty/save/undo integration,
   corruption handling, untitled documents, Save As/copy and reopen behavior. Establish rendered-result ownership,
   root-input identity, failed/empty/stale states and cross-tab action routing here, before any capture can be accepted.
3. **Drawing and review:** dock, draft state machine, palette/history, native capture, comment actions, thumbnails
   and camera restoration. Validate a useful manual end-to-end workflow before adding server complexity.
4. **Agent access:** discovery, request outcomes, annotation reads, view/capture operations, read-only reload status,
   busy/stale checks, client and companion skill. Validate two instances, multiple tabs and external-edit/auto-reload.
5. **Windows delivery:** focused tests, GUI evidence, package smoke test, and a reviewable upstream-facing change.
   Add the feature to the experimental PR list only through an explicit selection when a feature revision is ready.

Use Catch2 for record validation, stroke history, normalized coordinates, storage failure handling and request
idempotency; use the existing `src/guitests` Qt infrastructure for document lifecycle and undo integration. Native
Windows/OpenGL checks are required for actual framebuffer/overlay behavior; headless tests alone cannot establish it.

Acceptance scenarios should include:

- Multiple differently colored strokes, tiny clicks, out-of-bounds strokes, undo-all/navigation/redo invalidation,
  Enter with no strokes, empty/Unicode comments, Back/Cancel, hidden dock, fixed palette/arrow cursor, and keyboard-only use.
- Pixel correspondence and no palette/dialog in captures at 100%, 125%, 150%, 200% and mixed-monitor DPI; resize
  invalidation; perspective/orthographic views; preview, thrown-together and rendered geometry.
- Active editor different from rendered root; unsaved source changes after preview; failed compile retaining an old
  image or clearing it; empty successful models; models using included libraries; animation
  and Customizer changes during drafts. Save/undo from annotation context target the owner even with another tab active.
- Save/reopen/Save As/Save a Copy, untitled and read-only documents, close/discard, unsupported/corrupt companions,
  external editor round trips, low disk space, crash recovery and no accidental annotation-only geometry rebuild.
- SCAD source remains untouched by annotation-only saves, including unfinished source; CLI/include/use and Customizer
  behavior unchanged; Save a Copy preserves annotations while leaving the original dirty state intact. Test partial
  two-file saves, existing destination companions, source-only external edits and deletion of the last annotation.
- Interleaved text and annotation undo/redo, including deleting the last record and restoring its original PNG;
  record selection and reads leave camera/source/dirty state unchanged.
- Accept/edit/delete annotations without saving, then externally modify the SCAD file and let it reload: annotation
  contents and dirty state survive, no source-discard warning occurs for annotation-only changes, and both undo/redo
  histories clear when editor text is reloaded. Companion conflicts and an explicitly saved empty store preserve evidence.
- Pending edit/delete during selection or history changes; original and copied files open simultaneously; closing
  the rendered root; blank capture with explicit ownership; undo-all then navigate and draw again.
- Restore after source changes, wrong-document targets, closed tabs, different viewport sizes and camera variables;
  never claim historical geometry or stable mesh anchoring.
- Duplicate/lost requests, Stop/restart, stale source revisions, busy drafts, queue/result expiry, bounded memory,
  and fresh-capture verification that identifies the result actually shown.
- External root/include/use edits picked up by automatic reload; unchanged root text with changed dependencies;
  disabled reload, dirty buffers, inactive root and compile errors reported without forced reload or tab switching.
- Many long strokes and many records: cached drawing/thumbnail work, responsive comments, no expensive idle polling.

## Readiness for requirements

The user-facing scope is settled: companion storage, drawing only, normal external SCAD edits, existing automatic
reload, and no editor-control or document-switching API. Drawing, immutable evidence, comment edit/delete, camera
restoration, unsaved annotation access, normal save behavior, unified undo and the agent review loop form the baseline.
Automatic source reload clears annotation undo/redo whenever it clears source undo/redo, as selected by the user.
All review questions are resolved. The exploration is ready for requirements; remaining engineering validation
belongs to the planned prototypes and does not require more product choices at this stage.

The agreed OpenSCAD adaptation excludes Blender's object selection and single-file storage. Those differences do
not make drawing-only companion-file delivery incomplete. Historical source retention and complete dependency
tracking are outside the initial scope. Validate companion recovery and undo integration before promising their
runtime behavior. Choose HTTP transport and exact operation schemas during technical design.

Engineering checks do not require the user to choose implementation mechanisms:

| Area | Evidence needed before the affected implementation is committed to |
| --- | --- |
| Windows baseline | Recorded Qt6/MSVC/vcpkg configuration and a passing baseline build in the annotations checkout |
| Persistence | Chosen format round trips, failure recovery, copy/reload/backup coverage, and unsupported-data preservation |
| Undo | Real QScintilla interleaving, save-point behavior, history truncation, and correct document targeting |
| Capture | Native overlay/framebuffer agreement, mixed-DPI handling, and cancellation of stale drafts |
| Automatic reload | Result ownership across tab changes, empty/failed previews and root/include/use edits on disk |
| Agent access | Explicit targets, revision checks, bounded request lifecycle, and mutation exclusion during drafts |

The requirements phase should turn these into concrete pass/fail criteria, including measured resource limits and
renderer capabilities. Prototypes can resolve mechanisms without reopening settled behavior; any necessary change
to the agreed user workflow must be brought back for a decision. No full feature implementation is ready to start
merely because the source review passed.

No issue-status system, mesh editing, surface-anchored markup, historical-geometry replay, full-image viewer,
standalone web UI, external service, or cross-platform release is added by this exploration. Those can be separate
decisions. This pass changes planning documents only; no OpenSCAD or Blender implementation has been modified.
