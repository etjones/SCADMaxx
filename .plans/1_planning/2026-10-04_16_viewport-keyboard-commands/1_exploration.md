# 16 Viewport keyboard commands and focus switching

## Request and status

Created 2026-10-04 at the user's request to capture the viewport keyboard inventory and proposed focus behavior as a
separate feature. The user wants keyboard access to all viewport operations, including measuring and annotations.
Status: exploration captured; not implementation-ready. This does not start implementation or add work to batch 3.

Scope: command coverage, configurable bindings, discoverability, editor/viewport focus, and interaction with Vim and
active tools. Exact default bindings and the extent of completely mouse-free operation remain to settle. The proposed
behavior below is the direction discussed with the user, not a finalized keymap.

## Source inventory

Read-only inspection covered the delivered `D:/openscad/wt-scadmaxx-20261002` integration, separate 03/04/05/07
implementations, and 08/12 planning. These are source defaults, not a runtime keyboard audit or the user's personal
configuration. Feature-branch behavior is not necessarily in the delivered application.

| Operation | Observed support or gap |
| --- | --- |
| Measure distance / angle | D / A exist; rendered Manifold geometry is required. Point selection still uses the mouse. |
| Start annotation | No dedicated shortcut found. |
| Annotation colour, edit/delete comment, restore view, blank-view ownership, save owner document | Panel/palette controls without dedicated shortcuts. |
| Finish/cancel annotation; drawing undo/redo | Enter / Escape and standard Undo/Redo handled during drawing. |
| Six standard camera views; diagonal | Ctrl+4 through Ctrl+9; Ctrl+0 for diagonal. |
| Center / fit all / zoom in and out | Ctrl+Shift+0 / Ctrl+Shift+V / Ctrl+] and Ctrl+[. |
| Orbit / roll | Arrows and Q/E with navigation-cube focus; not uniform viewport bindings. |
| Cube face/edge/corner selection | [ / ] cycle targets; Enter snaps, with cube focus. |
| Pan camera | No dedicated keyboard commands found. |
| Perspective / orthographic; reset camera | No default shortcuts found. |
| Edges / axes / crosshairs | Ctrl+1 / Ctrl+2 / Ctrl+3. |
| Scale markers; viewport information, triangles, FPS, frame time | No dedicated defaults found. |
| Saved views: add, recall, rename, remove | No direct viewport shortcuts; list activation/editing works once focused. |
| 03 Select geometry / clear selection | Buttons/menu action without dedicated shortcuts. Escape cancels active picking. |
| 07 Hide/show, solo/clear solo, fit/export selected, go to call/definition | Tree/context-menu/Inspector controls without dedicated shortcuts. |
| 07 Create Section, retry target preparation, cancel target jobs | Context-menu/Inspector operations without dedicated shortcuts. |
| 04 Enable clipping; create/reset XY/XZ/YZ sections | No dedicated shortcuts. |
| 04 Select/enable section, pick point, pick-and-align, flip, helper visibility, delete, promote/save | No dedicated shortcuts. |
| 04 Section origin/offset/orientation | Numeric fields and slider support keyboard editing once focused. |
| 08 Anchors/attachments | In progress at inspection; inventory commands against its finished UI. |
| 12 Contextual insertion | Shift+A specified in requirements; not counted as delivered support. |

Source references (relative to the named checkout):

- Delivered integration: `src/gui/MainWindow.ui`, `MainWindow.cc`, `NavigationCube.cc`, `ViewportPopup.cc`,
  `ShortcutConfigurator.cc`, and `annotations/AnnotationController.cc`.
- `wt-openscad-selection-model-inspector`: `src/gui/selection/ViewportToolRouter.cc`.
- `wt-openscad-live-clipping-sections`: `src/gui/clipping/ClippingDock.cc` and `ClippingController.cc`.
- `wt-openscad-semantic-model-hierarchy`: `src/gui/selection/InspectorDock.cc` and
  `src/gui/semantic/SemanticController.cc`.
- `wt-openscad-vim-editor-mode`: `src/gui/vim/VimScintilla.cc` and `src/gui/vim/engine/Engine.cc`.

## Current focus and command model

Single-key commands exist, but handling is fragmented: measurement uses window actions, the cube handles its own
keys, and annotations/tool routing handle active-operation keys. Measurement does not establish a general
viewport-only command context.

Ctrl+J opens dock navigation; Ctrl+K / Ctrl+H cycle docks. The dock list includes Editor, Annotations and Viewport
Control, but does not explicitly include the 3D canvas. Viewport Control is the camera-settings panel, not the canvas.
Check dock traversal: the current ancestor loop compares the original focus widget instead of the traversed ancestor.
This is a source observation requiring runtime verification, not a reproduced bug.

The shortcut configurator discovers QActions. Buttons, transient context-menu actions and raw key handlers are not
automatically stable configurable commands. Reuse the existing action/configuration system and add missing command
registration and contexts rather than maintaining a separate hard-coded keymap.

## Proposed behavior

- A configurable editor/viewport focus toggle, with explicit focus commands available through the command menu.
  Returning restores the editor caret and preserves Vim mode; the shortcut remains reachable with Vim enabled.
- A visible focus border or label. Moving the mouse alone does not change keyboard focus.
- Viewport letter commands operate only in the viewport command context. Editor typing and enabled Vim retain
  priority inside the editor; text/numeric fields keep their normal input behavior.
- Define the viewport focus group: canvas, cube and tool controls cooperate without stealing text input or cancelling
  a tool merely because its own controls receive focus.
- Escape cancels the current viewport tool and stays in the viewport; the focus toggle switches panes. Preserve
  accepted one-press Vim Escape behavior inside the editor.
- Every supported operation becomes a stable named configurable command. Frequent operations get defaults;
  a searchable command menu exposes everything else without requiring a unique key for every operation.
- Show the active tool and confirm/cancel hints. Preserve enabled/disabled reasons, renderer restrictions, undo owner
  and document targeting whether invoked through a key, button or menu.
- Cover navigation, measurements, annotations, selection, semantic visibility/targets, sections, saved views,
  anchors/attachments and insertion using the existing feature services.

## Boundary still to settle

Keyboard-triggered tools can still use mouse picking and drawing. Completely mouse-free operation additionally needs
object/face/point traversal, numeric point entry, camera panning and a keyboard alternative to freehand annotation.
Preserve both needs; do not claim shortcuts alone deliver mouse-free operation or silently invent those interactions.

Before requirements, settle that boundary, the focus-toggle key, frequent-operation defaults, command-menu key, and
focus-transfer/cancellation rules for tool panels. This capture step does not ask the user to decide them now.

## Branch ownership and sequence

Implement on a separate feature branch/worktree with recorded prerequisite inputs, followed by later integration.
Preserve occupied owner checkouts; do not add this to the running third batch automatically.

The command/focus foundation can be developed against existing shortcut, navigation and annotation support and
verified 03/05 behavior. Existing 04/07 and source-backed 14 services supply operations; consume verified handoffs
instead of reimplementing their models or persistence. Respect 03's insertion focus-group refinement where applicable.
Complete 08/12 coverage follows their stable implementations. The graph's 12 -> 16 edge means completion of all tool
coverage, not that preliminary command/focus work must wait. No dependency on postponed 09/10/13 is introduced;
08/12 must not depend on 16.

## Verification direction

Create a command matrix: stable ID, context, default/configured key, enabled condition and owning feature. Test actual
Qt shortcut dispatch and focus, editor/Vim/text-field isolation, explicit focus transfer, tool cancellation, correct
undo ownership, floating docks, conflict detection and saved bindings after restart. Verify keys invoke the same
actions as menus/buttons. Audit complete supported-operation coverage on the final prerequisite composition, with
separate acceptance for mouse-free use if selected. No tests were run for this exploration.
