# SCADMaxx

*OpenSCAD, with the sliders turned up.*

SCADMaxx combines regular OpenSCAD with additional features and selected upstream patches.
This repository holds the build recipes, tools, prompts and documentation used to assemble it.

<!-- Hand-maintained by the user. Agents must not regenerate or update this README unless explicitly asked. -->

Click any screenshot to open the full-size image. The examples below use the first integrated SCADMaxx build;
the UI comparisons also show regular OpenSCAD with the same model and layout.

## New features

### Annotations

<a href="docs/screenshots/annotations.png"><img align="left" hspace="16" width="320" src="docs/screenshots/annotations.png" alt="Red annotation around a mounting hole that breaks through the bracket edge, with drawing tools and defect comment dialog visible"></a>

- Draw directly on the viewport and attach comments to captured images.
- Browse, search and edit annotations, or restore an annotation's camera view.
- Save annotations alongside the SCAD document, with undo/redo support.
- Give local agents access to annotation evidence through an optional API and Python client.

*Mark a defect on the model and explain what needs to change.*

<br clear="both">

### Navigation cube

<a href="docs/screenshots/navigation-cube.png"><img align="right" hspace="16" width="200" src="docs/screenshots/navigation-cube.png" alt="Close-up of the navigation cube and view rotation controls"></a>

- Click cube faces, edges and corners to select a view.
- Orbit freely, rotate in steps and switch between perspective and orthographic projection.
- Save, name and recall document-specific camera views.
- Adjust camera transitions and viewport information overlays.

*The cube follows the camera and provides direct view selection.*

<br clear="both">

<details>
<summary>See saved views and viewport controls</summary>

<a href="docs/screenshots/navigation-menu.png"><img width="480" src="docs/screenshots/navigation-menu.png" alt="Bracket viewport with navigation menu expanded, showing projection, display and saved-view controls"></a>

*Keep useful camera positions with the document.*

</details>

### Agent access

<a href="docs/screenshots/agent-access.png"><img align="left" hspace="16" width="320" src="docs/screenshots/agent-access.png" alt="Agent access connection dialog with enable, stop and copy connection controls"></a>

- Enable a local HTTP API for inspecting open documents and application state.
- Read source snapshots, syntax trees, diagnostics and annotations.
- Control the camera, capture viewport images and access native saved views.
- Use the bundled Python client and agent workflow instructions.
- Work through external file edits and reloads; the API does not write source files or force evaluation.

*Enable local access and copy connection information from the application.*

<br clear="both">

### UI improvements

<a href="docs/screenshots/ui-after.png"><img align="right" hspace="16" width="320" src="docs/screenshots/ui-after.png" alt="SCADMaxx toolbar and Customizer with unified icons, quieter group headers and help icons"></a>

- Consistent typography and spacing that adapt to font sizes and display scaling.
- Unified icons with light/dark support and configurable status-icon styles.
- A quieter Customizer with restrained group headers, clearer labels and help tooltips.
- Native Preferences tabs and improved spacing and readability across dialogs.
- Independent editor and console content fonts.

*SCADMaxx: clearer controls and a quieter Customizer.*

<br clear="both">

<details>
<summary>Compare regular OpenSCAD and SCADMaxx</summary>

| Regular OpenSCAD | SCADMaxx |
| --- | --- |
| <a href="docs/screenshots/ui-before.png"><img width="400" src="docs/screenshots/ui-before.png" alt="Regular OpenSCAD toolbar and Customizer"></a> | <a href="docs/screenshots/ui-after.png"><img width="400" src="docs/screenshots/ui-after.png" alt="SCADMaxx toolbar and Customizer with the same bracket"></a> |
| <a href="docs/screenshots/preferences-before.png"><img width="300" src="docs/screenshots/preferences-before.png" alt="Regular OpenSCAD Advanced Preferences"></a> | <a href="docs/screenshots/preferences-after.png"><img width="300" src="docs/screenshots/preferences-after.png" alt="SCADMaxx Advanced Preferences with updated tabs, fonts and spacing"></a> |

*Matched model, camera, window size and display scale. The Customizer shows each version's default presentation.*

</details>

### SCADMaxx Launcher

<a href="docs/screenshots/launcher.png"><img align="left" hspace="16" width="320" src="docs/screenshots/launcher.png" alt="SCADMaxx Launcher with regular OpenSCAD selected for .scad files and SCADMaxx selected for .scadmax files"></a>

- Manage multiple installed OpenSCAD and SCADMaxx builds in one place.
- Choose which build opens files for each configured extension.
- Discover builds in selected folders and review which ones to include.
- Switch builds from the system tray, with optional startup at sign-in.
- Set up file associations through Windows Default Apps.

*A separate Windows companion utility: choose which installed build opens each file type.*

<br clear="both">

## Included upstream PRs

### Customizable keyboard shortcuts — [#6878](https://github.com/openscad/openscad/pull/6878)

<a href="docs/screenshots/shortcuts.png"><img align="right" hspace="16" width="320" src="docs/screenshots/shortcuts.png" alt="Keyboard shortcut preferences listing real file and editing actions and their assigned keys"></a>

- Search actions and assign keyboard shortcuts through the GUI.
- Handle shortcut conflicts and restore defaults.
- Apply changes across application windows and retain shortcut settings.

*Find an application action and customize its keyboard shortcuts.*

<br clear="both">

### Dynamic dark-mode switching — [#6776](https://github.com/openscad/openscad/pull/6776)

<a href="docs/screenshots/dark-mode.png"><img align="left" hspace="16" width="320" src="docs/screenshots/dark-mode.png" alt="Bracket and Customizer in dark mode"></a>

- Respond to light/dark theme changes while OpenSCAD remains open.
- Update widget palettes without restarting the application.
- Provide the theme foundation used by the local UI improvements.

*The same model in dark mode, with a matching dark viewport background.*

<details>
<summary>Compare the matching light theme</summary>

<a href="docs/screenshots/light-mode.png"><img width="480" src="docs/screenshots/light-mode.png" alt="The same bracket, camera and Customizer layout in light mode"></a>

</details>

<br clear="both">

## Build status and documentation

The first integrated Windows x64 editor build includes annotations, navigation, agent access, UI improvements and PRs #6878/#6776.
Its source is branch `scadmaxx-20261001`, revision `bcf48145d`.
Screenshots use that integrated source with a documentation-only capture harness.

- [Screenshot sources and capture details](docs/screenshots/sources.json)
- [Workspace guide](docs/workspace.md)
- [Repositories, worktrees and push destinations](docs/git-layout.md)
- [Selected features and PRs](experimental/PR_STACK.md)
- [Update and build instructions](workflows/update-and-build-scadmaxx.md)
