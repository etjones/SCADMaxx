# Navigation cube — requirements

Status: planned, not implemented. Derived from the settled [exploration](1_exploration.md) and eight answered questions.
This document defines required behavior; [3_overall-plan.md](3_overall-plan.md) defines mechanisms and phase ownership.
The [approved preview](assets/viewport-popup-approved-v4.png) establishes appearance, not exact dimensions or defaults.
It predates the accepted Center / View All / Reset row and dev drag-orbit toggle; the requirements below include both.

## Scope and navigation

### R01 — Independent viewport feature

Implement on the dedicated navigation-cube branch without depending on annotations or another experimental feature.
Retain existing View-menu commands, shortcuts, render modes, model Animate and toolbar visibility controls. Do not
edit SCAD geometry/source, redefine world axes, introduce a new agent API or migrate annotation storage. Camera
navigation alone must not mark source, Customizer or the saved-view library modified.

Acceptance: the feature works on its own base; ordinary model evaluation and geometry exports remain unchanged.

### R02 — Cube appearance and target identity

Show a labeled, chamfered cube with six face, twelve edge and eight corner targets in total. Only visible targets
are interactive; no hidden facet can win a hit test. Face names, XYZ letters, distinct chamfers and hover feedback
must remain readable in both themes. Hit regions must agree with the drawing and have deterministic boundaries.

Acceptance: a target test enumerates all 26 identities; native screenshots verify visible facet labels and hover state.

### R03 — Placement and scaling

Anchor the compact cube and its arrows/axis letters in the viewport's upper-right area. Place one discreet unframed
menu triangle above/right of it, near the viewport corner. There are no persistent dropdown buttons below the cube.
Ordinary dragging never moves either control. Dev settings independently adjust their positions and navigation scale.
Keep controls usable on resize, enlarged fonts and supported display scales; clamp positions to the available viewport.

Acceptance: resize and DPI changes preserve the chosen anchoring without clipped controls, trails or accidental moves.

### R04 — Camera synchronization

The cube reflects the actual displayed camera after mouse navigation, shortcuts/menus, viewport numeric controls,
saved-view recall, reset/fit, script camera variables and evaluation. Updating its display does not itself change the
camera. Existing camera consumers continue to receive appropriate final changes without compile feedback loops.

Acceptance: each input route updates the cube and camera fields; changing tabs cannot imply a different rendered model.

### R05 — Snap targets and invariants

Face clicks select the existing principal orientations. Edge views bisect the two adjacent face directions; corners
are true isometric directions with equal axis foreshortening under orthographic projection. Snaps use standard upright
roll, world Z up where possible and deterministic top/bottom orientations consistent with existing standard views.
Preserve pan/target, distance/zoom, field of view and projection. Existing Diagonal retains its current orientation.

Acceptance: an asymmetric XYZ fixture verifies all 26 views, up direction, preserved camera fields and repeated clicks.

### R06 — Roll and directional arrows

Provide clockwise/counterclockwise roll and four directional orbit arrows. Initial steps are 90 degrees for roll and
15 degrees for directional orbit, independently adjustable in dev settings. One click produces one step. Preserve
pan/target, distance, field of view and projection. Hold-repeat, modifiers and a separate opposite-view button are
outside this version. Arrow direction is screen-relative; roll rotates around the current viewing direction.

Acceptance: full-step cycles return to the starting orientation within numerical tolerance without pan/zoom drift.

### R07 — Cube free orbit

Dragging the cube freely orbits the camera. The dev window can enable/disable this behavior live; clicks and arrows
continue working in both states. Distinguish clicks from drags with a movement threshold. Completing a drag never
also snaps, selects geometry, creates an annotation stroke or relocates the cube. Release outside remains safe.

Acceptance: enabled/disabled drags, click jitter, release outside and cancellation are exercised in the native viewport.

### R08 — Configurable camera transitions

Provide animation on/off and duration preferences; expose easing and duration for dev tuning. Discrete cube snaps,
arrow steps and saved-view recalls honor the setting. Manual/free-orbit gestures track the pointer directly.
Shared standard-view commands use the same orientation transition behavior; Center / View All / Reset retain their
existing final effects. A saved view reaches its exact full camera, including projection, with no automatic fit.

New camera input supersedes an old transition from the currently displayed state. Manual navigation stops a pending
transition; close, reload, script-camera evaluation and capture cannot leave callbacks that later overwrite the camera.
Disabled animation applies the exact final state immediately. Camera animation is independent of model `$t` animation.

Acceptance: rapid retargeting, orbit interruption, compilation and close never jump back to a stale target.

## Popup and saved views

### R09 — Navigation safety and existing workflows

Route all new camera operations through the same permission checks and final notification behavior as ordinary
navigation. No operation should compile solely to draw or move the cube. Preserve existing model Animate behavior,
including camera-dependent evaluations, without compiling once per visual interpolation frame. No popup action
implicitly switches editors/documents, changes source selection or takes ownership of another window's render result.

Acceptance: count evaluations during transitions and compare source/selection state before and after navigation.

### R10 — Resizable popup

The triangle opens one thin-framed popup over the viewport, with no title bar or close button. It is resizable,
remembers its size and remains within the visible screen area. Clicking outside hides it without acting on geometry
underneath. Clicking its triangle again closes it. Resizing or interacting with descendants does not dismiss it.
Changes apply live. Escape cancels active inline editing first, then dismisses the popup when not editing.

Acceptance: pointer and keyboard sequences verify resizing, dismissal, focus restoration and no click-through effects.

### R11 — Projection and shared camera actions

The popup has two exclusive radio buttons, Perspective and Orthographic, sharing state with existing projection
actions. It also has a compact Center / View All / Reset row invoking the existing commands. Reset is the current
OpenSCAD reset, not a configurable Home or an orientation-only snap. Controls remain synchronized after saved recall.

Acceptance: each popup action has the same final camera effect as its existing menu counterpart.

### R12 — Saved-view list editing

Show a small resizable list for the displayed document, with Add / Remove / Rename below it. Add stores the current
camera, creates a unique default name such as View 1, selects the new entry and begins inline name editing. Keeping
the default is valid. Rename affects the selected entry; Remove deletes the selected entry. With no selection,
Remove/Rename are disabled. Cancelled/empty name edits retain the old or generated name; hiding the popup does not
discard a newly added entry. A completed nonempty edit is retained. Stable entries survive duplicate display names.

Single-click selects without moving the camera. Double-click or Enter recalls and leaves the popup open. Enter while
editing commits the name instead of recalling. No Update/overwrite-camera button is required in this version.

Acceptance: Add/cancel, rename/focus loss, Remove-last, Unicode names and keyboard recall behave without unintended motion.

### R13 — Camera snapshot and recall

Save orientation, translation/pan/target, distance/zoom, field of view and projection. Restore all of them; do not restore
overlay choices, window/viewport dimensions, renderer state or auto-fit behavior. A different viewport aspect ratio
can change the visible crop. Add reads the displayed camera, not a pending transition destination. Merely selecting
or recalling an entry does not modify it or mark the library unsaved.

Acceptance: camera values round-trip in both projections, at a different viewport size, without source or overlay edits.

### R14 — Document and window ownership

Each document has its own saved-view library. The popup identifies the document whose model the viewport displays;
selecting another editor alone must not silently rebind the library. When no trustworthy displayed-document owner is
available, disable library mutations and explain why. A successfully evaluated empty model still has an owner.
Retained geometry after a failed compile keeps its original owner. Closed owners cannot receive delayed actions.

Acceptance: test mismatched active/rendered documents, empty and failed results, close/reopen and multiple windows.

### R15 — Persistence with document saving

Store views beside the SCAD file in a separate simple experimental companion, independent of annotation data.
Add/Remove/Rename change memory and metadata dirty state; ordinary Save/Save All/Save As/Save a Copy persist them.
Untitled documents retain views in memory until first Save. Include metadata in dirty indicators and close prompts.
Save As carries views to the destination; Save a Copy leaves the original identity and unsaved state intact.

Source-only reload preserves library contents and unsaved metadata. Metadata-only Save must not rewrite SCAD or
trigger compilation. Deleting the final view persists empty state so old entries cannot reappear. Manual copying
requires source and companion. Reading an untouched document does not create a companion.

Acceptance: real document lifecycle tests verify reopen, Save All, copy, untitled Save, source timestamps and reload.

### R16 — Persistence failures and recovery

Report source/companion partial-save failures truthfully and retain unsaved data. Do not overwrite unreadable,
unsupported or externally changed companion data with an empty or stale library. Detect destination conflicts for
Save As/copy and conflicting writers. Preserve recovery data; integrate saved views with existing document backup
and recovery behavior. Two separately written files are not promised to be one crash-atomic transaction.

Acceptance: simulate failed writes, malformed data, another writer, destination collisions and recovery after interruption.

## Preferences, tuning and overlays

### R17 — Persistent preferences

Remember ordinary overlay choices, popup size and camera-animation on/off/duration globally. Normal Preferences
provides camera-animation and navigation visibility controls. Hiding navigation hides cube, triangle and popup, with
a discoverable way to restore them. It does not hide independently enabled statistics. Ordinary preferences and
saved camera entries have separate ownership; saved views remain per-document.

Acceptance: isolated-profile restart and multiple-window checks verify persistence and restoration of hidden navigation.

### R18 — Temporary live tuning

Provide a separate temporary dev window with live controls for overall scale; cube and triangle position; inspectable
coordinates; idle/hover opacity; hover delays and fade timings; camera duration/easing; step sizes; and drag-orbit enable.
Include geometry/hit-area/label/arrow spacing controls needed to calibrate the compact cube. No rebuild is needed.
These experiments are session-only, including temporary overrides of otherwise persistent preferences.

Hover/focus/drag feedback remains stable across cube, triangle and popup. Opacity animation never postpones hit testing.
Initial size, opacity and fade values are experimental and must be tunable rather than treated as frozen requirements.

Acceptance: change controls live, resize the viewport, inspect positions, and restart to verify experimental overrides clear.

### R19 — Copy settings

One Copy settings button copies a readable description of every current tuning/control setting, including controls
not currently visible, to the clipboard. Include names, units, anchor/offset and resolved positions, scale, viewport
dimensions, display scale, animation/hover values, drag toggle, steps, projection and overlay toggles. Distinguish
effective temporary overrides from saved baselines. Give brief success feedback. The saved-camera library itself
need not be copied. Clipboard import and a persistent dev-settings file are outside scope.

Acceptance: copied text exactly describes the current experiment, including after resizing and display-scale changes.

### R20 — Statistics with explicit meaning

Provide independently selectable triangle count, measured viewport FPS and frame-time readouts under Show information.
Label preview versus final-render counts; preview counts describe submitted model geometry, not the final Boolean
surface or repeated GPU passes. Use a final triangle count only when available without forcing a new geometry render.
Do not call nontriangular facets triangles. Empty, stale, unsupported/2D and failed results must be distinguishable.

FPS measures viewport frames rather than requested playback FPS. Frame time states its measurement meaning. Idle
is distinguishable from slow rendering; no continuous redraw or per-frame mesh traversal is introduced for statistics.

Acceptance: known simple/overlapping models distinguish count semantics; idle and interaction tests verify the readouts.

### R21 — Display controls

The popup exposes existing Axes, Scale markers, Crosshairs and Edges settings through shared actions. Show information
hides statistics without clearing the individual metric selections. World axes visibility is independent of the cube's
XYZ letters. Popup/toolbar/menu states agree, and ordinary display changes do not edit source or saved camera entries.

Acceptance: toggle from each UI entry point; verify displayed results, state synchronization and retained metric choices.

## Capture, integration and delivery quality

### R22 — Clean images

Copy Viewport, GUI model PNG export, animation frames and annotation/agent viewport captures contain model content
and applicable annotation strokes only. Exclude navigation controls, popup, dev window, statistics, axes, scale markers
and crosshairs. Model surface/edge rendering is model content. Full-window screenshots naturally include visible UI.
Clean captures remain unannotated; an annotated capture includes its intended strokes once, not annotation tool UI.

Capture uses the correct displayed camera/result, cannot race a transition, and does not permanently change viewport
settings or saved preferences. Do not alter historical annotation images. The new GUI chrome never enters headless
output; this feature does not redesign explicit command-line rendering options.

Acceptance: inspect actual image pixels for every GUI capture route with all helpers enabled and during transitions.

### R23 — Annotation interoperability

In a later combined build, all camera-changing paths obey annotation draft/capture locks. Permitted navigation clears
stroke redo as ordinary navigation does; blocked operations cannot execute later through delayed animation callbacks.
Viewport UI cannot generate strokes. Saved views retain their separate companion. Standalone feature delivery does
not require the annotation branch, and standalone tests are not claimed as proof of combined integration.

Acceptance: use lock-policy tests on the standalone branch and real annotation scenarios when a combined build is tested.

### R24 — Lifecycle robustness

Preview, thrown-together and F6 rendering, empty/error results, source reload, document close, window close and multiple
windows leave the UI valid. Each viewport owns its camera interaction and transient popup/tuning state. Closing or
replacing an owner invalidates outstanding gestures, animations, metric snapshots and callbacks safely.

Acceptance: lifecycle scenarios produce no stale pointer access, wrong-document metadata or camera changes after close.

### R25 — Native UI quality and accessibility

Use theme-aware native controls, clear focus/hover feedback, tooltips/accessibility names and keyboard equivalents.
Preserve native font inheritance, translations, readable contrast and useful minimum hit areas. Verify light/dark,
100/125/150/200% scaling, mixed monitors where available, narrow/fullscreen windows and larger fonts. No repaint trails,
stale highlights, popup clipping or invisible recovery path for hidden controls are acceptable.

Acceptance: native screenshots and interaction evidence cover the matrix and distinguish simulated from physical DPI.

### R26 — Bounded overhead

Navigation and overlays introduce no idle camera/render loop, repeated geometry compilation, blocking per-frame
statistics work or dependency-heavy rendering subsystem. Fades/transitions stop their timers when complete or hidden.
Reuse cached geometry summaries and respond to camera changes without rebuilding the model.

Acceptance: compare idle/interaction behavior with the feature hidden and shown; record event/compile counts and timing.

### R27 — Build and workspace constraints

Use the dedicated checkout and existing shared Windows Qt6/MSVC/vcpkg packages, with manifest installation disabled.
Keep planning, machine-specific build/run records and image artifacts outside upstream-facing source changes.
Missing dependencies are reported rather than automatically installed. Separate baseline build repairs from feature
work. No experimental stack selection, publication or package release is implied by this feature plan.

Acceptance: configuration evidence identifies source/dependency/toolchain state and confirms use of the shared tree.

### R28 — Verification and handoff

Provide focused behavior tests plus native visual/interaction evidence and a local runnable Windows build for tuning.
Maintain coverage from these requirement IDs to phased work and evidence. Record failures, deviations, actual tuned
values and platform/integration limits in post-implementation notes. Do not claim unperformed checks or other-platform
runtime verification. Production source remains compatible with the repository's existing GUI/headless build choices.

Acceptance: every requirement has passing evidence or an explicit unresolved limitation; the feature is not declared
fully complete while required checks are missing. No implementation tests or builds have been run by this planning task.
