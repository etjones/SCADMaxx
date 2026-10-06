# Split the toolbar into functional units

Status: planning only. Requested on 2026-10-06; implementation has not started.

## User intent

Split the toolbar into recognizable functional units so related commands are together and the toolbar is easier
to scan as SCADMaxx gains features.

## Proposed organization

Inventory the existing actions before assigning every command. Candidate groups:

- File and output: document operations and export commands currently exposed in toolbars.
- Model evaluation: preview, render and related evaluation controls.
- View navigation: fit, zoom, reset and standard viewpoints.
- Display: projection, rendering style, axes, scale and other viewport overlays.
- Inspection and tools: selection/inspection, measurements, cross sections and annotations where toolbar actions exist.

These groups are proposals, not a finalized command inventory or approved layout. Keep editor-specific commands
with the editor; do not duplicate menu commands merely to fill a group.

## Layout decisions to resolve

- Separate named Qt toolbars versus groups separated within one toolbar. Prefer separate toolbars if users should
  be able to move or hide each functional unit independently.
- Default group order and placement, including which commands belong beside the viewport versus the editor.
- Whether functional labels appear on screen or only in toolbar visibility menus and accessible names.
- Visibility, movement, locking and persistence behavior, with a clear way to restore the default layout.

## Implementation exploration

Inspect the maintained UI-polish branch, existing toolbar definitions, QAction ownership, toolbar context menus and
window-layout persistence. Reuse existing actions so shortcuts, checked state, enablement, tooltips and callbacks
remain consistent with menus. Preserve exclusive action groups and feature-conditional availability.

Keep theme-aware icon rendering and consistent visual weight from UI polish. Plan for narrow windows, DPI scaling,
overflow and multiple toolbar rows without obscuring the viewport or creating excessive unused space.
Reorganizing controls must not trigger model evaluation or change viewport state.

Choose the owning branch and necessary ancestry when implementation is requested. This is UI organization work;
it does not require merging every feature branch merely to reserve places for optional actions. No new sequencing
dependency between unfinished plans is established yet.

## Acceptance scenarios

- Related commands form clearly distinguishable functional units with a coherent default order.
- Every existing toolbar action remains reachable and retains its behavior and keyboard shortcut.
- Checked, disabled and mutually exclusive states stay synchronized between toolbars and menus.
- Layout remains usable at narrow widths and different DPI settings, in light and dark themes.
- Optional feature actions do not leave empty groups or dangling separators when absent.
- If independent toolbars are chosen, moving/hiding groups, restarting and restoring defaults behave consistently.
- Toolbar interaction introduces no extra model evaluations or viewport performance regression.

No source edits, worktree creation, builds, tests or release-stack changes are part of this planning item.
