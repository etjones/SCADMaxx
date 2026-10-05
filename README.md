# SCADMaxx

*OpenSCAD, with the sliders turned up.*

SCADMaxx is not a fork of OpenSCAD. It is a build of openscad-master with a collection of experimental patches. These
patches are PR's from OpenSCAD's Github as well as other features that (source code wise) aren't in a state to be merged
and are only to be taken as implementations to investigate in terms of functionality, usability and so on.

SCADMaxx makes no promises on language compatibility or what features will be in the next version.

That said, I personally use SCADMaxx for everything I do with OpenSCAD. Its agentic implementation details range from
'obvious' to 'still visible', but it's perfectly usable in terms of stability.

This repository holds the build recipes, tools, prompts and documentation used to assemble it.

<!-- Hand-maintained by the user. Agents must not regenerate or update this README unless explicitly asked. -->

Here is a list of what SCADMaxx has or does over OpenSCAD master (everything compares to the latest dev builds from
master since the regular release is so old and missing things that master has, that it's basically irrelevant at this
point):

<!-- Feature template: use ## for the three categories and ### for each user-facing feature.
Within each category, alternate the primary image left/right, starting left.
Keep linked thumbnails and finish each feature with <br clear="both"> before the next heading.
New screenshot slots stay commented out until real captures are available.
-->

## Agentic use

### Annotations

<a href="docs/screenshots/annotations.png"><img align="left" hspace="16" width="320" src="docs/screenshots/annotations.png" alt="Red annotation around a mounting hole that breaks through the bracket edge, with drawing tools and defect comment dialog visible"></a>

Ever found yourself going in a circle of having your agent change a model, previewing changes in OpenSCAD, 
describing what the issue is and where it happens on the model; or taking a screenshot, pasting into Paint, and
then pasting that back into your agent? Well, no more! Annotate your views straight in SCADMaxx itself!

- Draw directly on the viewport and attach comments to captured images.
- Browse, search and edit annotations, or restore an annotation's camera view.
- Save annotations alongside the SCAD document.
- Local agents directly access your annotations through an HTTP API, and remove it when the issue is fixed, if you want.

<br clear="both">

### Agent access

<a href="docs/screenshots/agent-access.png"><img align="right" hspace="16" width="320" src="docs/screenshots/agent-access.png" alt="Agent access connection dialog with enable, stop and copy connection controls"></a>

- Enable a local HTTP API for inspecting open documents and application state.
- Read source snapshots, syntax trees, diagnostics and annotations.
- Control the camera, capture viewport images and access native saved views.
- Work through external file edits and reloads; the API does not write source files or force evaluation.

<br clear="both">

### OpenSCAD skill

<!-- Screenshot pending: An agent reviewing an annotated model with the SCADMaxx skill.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/openscad-skill.png"><img align="left" hspace="16" width="320" src="docs/screenshots/openscad-skill.png" alt="An agent reviewing an annotated model with the SCADMaxx skill."></a>
-->

- Instructions on how to build clean models, how to do chamfers and fillets.
- How to work with Agent Annotations.
- Work with SCADMaxx specific language features.

<br clear="both">

## UI and UX improvements

### UI improvements

<a href="docs/screenshots/ui-after.png"><img align="left" hspace="16" width="320" src="docs/screenshots/ui-after.png" alt="SCADMaxx toolbar and Customizer with unified icons, quieter group headers and help icons"></a>

- Consistent typography and spacing that adapt to font sizes and display scaling.
- Unified icons with light/dark support and configurable status-icon styles.
- A quieter Customizer with restrained group headers, clearer labels and help tooltips.
- Native Preferences tabs and improved spacing and readability across dialogs.
- Independent editor and console content fonts.

<br clear="both">

<details>
<summary>Compare regular OpenSCAD and SCADMaxx</summary>

| Regular OpenSCAD | SCADMaxx |
| --- | --- |
| <a href="docs/screenshots/ui-before.png"><img width="400" src="docs/screenshots/ui-before.png" alt="Regular OpenSCAD toolbar and Customizer"></a> | <a href="docs/screenshots/ui-after.png"><img width="400" src="docs/screenshots/ui-after.png" alt="SCADMaxx toolbar and Customizer with the same bracket"></a> |
| <a href="docs/screenshots/preferences-before.png"><img width="300" src="docs/screenshots/preferences-before.png" alt="Regular OpenSCAD Advanced Preferences"></a> | <a href="docs/screenshots/preferences-after.png"><img width="300" src="docs/screenshots/preferences-after.png" alt="SCADMaxx Advanced Preferences with updated tabs, fonts and spacing"></a> |

</details>

### Navigation cube

<a href="docs/screenshots/navigation-cube.png"><img align="right" hspace="16" width="200" src="docs/screenshots/navigation-cube.png" alt="Close-up of the navigation cube and view rotation controls"></a>

- Click cube faces, edges and corners to select a view.
- Orbit freely, rotate in steps and switch between perspective and orthographic projection.
- Save, name and recall document-specific camera views.
- Additional (optional) viewport information overlays.

<br clear="both">

### Model inspection and source navigation

<!-- Screenshot pending: Selected surface with Inspector information and source navigation choices.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/model-inspection.png"><img align="left" hspace="16" width="320" src="docs/screenshots/model-inspection.png" alt="Selected surface with Inspector information and source navigation choices."></a>
-->

- Pick a surface in the viewport and inspect its position and orientation.
- Find the source call or module definition behind selected geometry and jump to it in the editor.
- See candidate source locations when a rendered surface has more than one possible origin.

<br clear="both">

### Live clipping sections

<!-- Screenshot pending: A model interior exposed by a clipping plane, with handles and Sections controls visible.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/live-sections.png"><img align="right" hspace="16" width="320" src="docs/screenshots/live-sections.png" alt="A model interior exposed by a clipping plane, with handles and Sections controls visible."></a>
-->

- Look inside a model with movable clipping planes, without cutting the actual geometry.
- Position and rotate planes with viewport handles, numeric controls or a picked surface.
- Combine up to eight planes and save named sections in the SCAD source.
- Move a clipping plane without reevaluating the model on every step.

<br clear="both">

### Contextual insertion

<!-- Screenshot pending: Insertion palette and an uncommitted component preview positioned on a model.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/contextual-insertion.png"><img align="left" hspace="16" width="320" src="docs/screenshots/contextual-insertion.png" alt="Insertion palette and an uncommitted component preview positioned on a model."></a>
-->

- Pick a surface and press **Shift+A** to add a primitive, hole or hardware component.
- Search the insertion palette, set dimensions, and preview the proposed geometry before committing.
- Drag, rotate or flip the placement, or attach a component to an existing named anchor.
- Commit generates editable SCAD source; one Undo removes the insertion.
- Optional catalog items use separately installed, matching BOSL2 and BOLTS libraries.

<br clear="both">

### Vim editor mode

<!-- Screenshot pending: Source editor with a useful selection and the Vim mode indicator visible.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/vim-editor.png"><img align="right" hspace="16" width="320" src="docs/screenshots/vim-editor.png" alt="Source editor with a useful selection and the Vim mode indicator visible."></a>
-->

- Enable optional Normal, Insert, Visual and Visual Line modes in the source editor.
- Use familiar motions, text objects, delete/change/yank commands and dot repeat.
- Search with `/` and `?`, and use a small set of `:` commands to save, close, reload or open files.
- Keep the usual editor undo history and application shortcuts.

<br clear="both">

### SCADMaxx Launcher

<a href="docs/screenshots/launcher.png"><img align="left" hspace="16" width="320" src="docs/screenshots/launcher.png" alt="SCADMaxx Launcher with regular OpenSCAD selected for .scad files and SCADMaxx selected for .scadmax files"></a>

- Manage multiple installed OpenSCAD and SCADMaxx builds in one place.
- Choose which build opens files for each configured extension.
- Useful if you regularly download development builds (or make them yourself) and want to configure what binary is used
  to default-open OpenSCAD or SCADMaxx files.

<br clear="both">

### Customizable keyboard shortcuts — [#6878](https://github.com/openscad/openscad/pull/6878)

<a href="docs/screenshots/shortcuts.png"><img align="right" hspace="16" width="320" src="docs/screenshots/shortcuts.png" alt="Keyboard shortcut preferences listing real file and editing actions and their assigned keys"></a>

- Assign keyboard shortcuts through the GUI.
- Handle shortcut conflicts and restore defaults.

<br clear="both">

### Dynamic dark-mode switching — [#6776](https://github.com/openscad/openscad/pull/6776)

<a href="docs/screenshots/dark-mode.png"><img align="left" hspace="16" width="320" src="docs/screenshots/dark-mode.png" alt="Bracket and Customizer in dark mode"></a>

- Much improved handling of theme awareness, including switching themes when the application is running and better use
  of theme colors.

<details>
<summary>Compare the matching light theme</summary>

<a href="docs/screenshots/light-mode.png"><img width="480" src="docs/screenshots/light-mode.png" alt="The same bracket, camera and Customizer layout in light mode"></a>

</details>

<br clear="both">

## OpenSCAD language additions

### Object literals and comprehensions — [#6081](https://github.com/openscad/openscad/pull/6081)

<!-- Screenshot pending: A short object-literal example and its evaluated output.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/objects.png"><img align="left" hspace="16" width="320" src="docs/screenshots/objects.png" alt="A short object-literal example and its evaluated output."></a>
-->

- Group named values in objects using `{key: value}` literals.
- Read members with dot or bracket notation.
- Build objects with comprehensions and computed keys, and derive updated objects with `object()`.

<br clear="both">

### Native Customizer attributes — [#6642 variant](https://github.com/openscad/openscad/pull/6642)

<!-- Screenshot pending: A reactive Customizer example beside the attribute declaration that drives it.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/customizer-attributes.png"><img align="right" hspace="16" width="320" src="docs/screenshots/customizer-attributes.png" alt="A reactive Customizer example beside the attribute declaration that drives it."></a>
-->

- Describe parameters with `@{key: value}` blocks directly above their assignments.
- Set groups, descriptions, ranges and numeric widget options in source.
- Use expressions to hide or lock parameters as other values change.

<br clear="both">

### Parts, assemblies and components

<!-- Screenshot pending: An assembly with named components in the Model tree and selected-part parameters visible.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/parts-assemblies.png"><img align="left" hspace="16" width="320" src="docs/screenshots/parts-assemblies.png" alt="An assembly with named components in the Model tree and selected-part parameters visible."></a>
-->

- Mark module definitions as Parts or Assemblies, and their placed calls as Components.
- Give instances explicit identities and browse them in the Model tree.
- Inspect and edit supported per-instance parameters or definition defaults through the Customizer.
- Hide or solo parts for inspection, and export a selected component or assembly in local or placed coordinates.

<br clear="both">

### Anchors and attachments

<!-- Screenshot pending: Two components attached through named anchors, with reference and placement controls visible.
Uncomment after adding the full-size image; keep the same file in href and src.
<a href="docs/screenshots/anchors-attachments.png"><img align="right" hspace="16" width="320" src="docs/screenshots/anchors-attachments.png" alt="Two components attached through named anchors, with reference and placement controls visible."></a>
-->

- Declare named points, axes, planes and oriented anchors in SCAD source.
- Mate or align components through anchor references, with offset and spin adjustments.
- Let parametric anchors move attached components when dimensions change.
- Pick a surface to create an anchor draft, then save its declaration into the source.

<br clear="both">

## Installation

Only Windows builds are provided at the moment. If there is demand, I can look into doing cross platform builds. If you
are on another platform and want to build it yourself, you can also tell your agent to clone this repo and execute the
procedures described.

Builds are date-based, there is no regular release schedule. Have suggestions for patches or functionality that would
fit in an experimental build like this? File an issue.

To install, give your agent this prompt:

    Download the latest release zip of SCADMaxx from http://github.com/roel-v/SCADMaxx. Unzip it in a suitable working
    directory, into a subdirectory thereof with a name derived from the downloaded zip file. Install the agent skill
    you'll find in that installation folder. Report where you installed it afterward.

Or specify where you want it to install, of course.
