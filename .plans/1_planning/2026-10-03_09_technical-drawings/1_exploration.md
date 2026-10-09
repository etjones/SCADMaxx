# Repeatable technical drawings from SCADMaxx models

Planning review: requirements are partial. Projection convention, first dimension types, repeatable layout rules
and per-format fidelity need a concrete first-release contract before phases. See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Status: postponed by the user after completing 08 planning. Retain this exploration; resume decisions only when
requested. Feature 10 proceeds independently and does not require drawings.

Sources: all ten exchanges in C and the A/D synthesis and section discussions in the
[overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md). The opening five C exchanges were recovered
from the local app cache on 2026-10-03.

## User intent and feature boundary

Generate complete 2D technical drawings and 3D views from a parametric design: front/top/left and other useful views,
saved sections, dimensions and sheets. The user's doorway fitness-device example should have its drawing rules
defined once, then regenerate after parameter changes without an AI having to decide the layout again.

Keep this feature separate from general viewport source editing. Drawing dimensions describe model geometry; they
do not implicitly become modeling constraints. Reproducible drawing definitions are part of the design. The user
selected typed, annotated objects in the main or an included `.scad` file through 14's shared mechanism. Drawing
schemas and layout rules still need technical design; the storage location is settled.

## Proposed document and view structure

- Drawing set -> sheets -> views, dimensions, notes and optional BOM tables.
- Targets can be a part definition, a component instance, an assembly or an explicit component subset.
- Support a general assembly sheet and reusable part sheets, with section/detail views where needed; examples in
  the discussion were a crossbar end section and bracket detail.
- Define projection, orientation, scale or fit rule, linked base view, sheet position, labels and title-block content
  as repeatable rules. Parameter changes update values and geometry while preserving intentional sheet arrangement.
- Keep view projection and visual style separate. Orthographic, isometric and section views are the core direction;
  perspective, detail and exploded views are candidate extensions. Styles include technical lines, hidden lines,
  shading, shaded edges and rendered imagery; use the existing renderer for initial 3D views where suitable.
- Per-view visibility/isolation is presentation state, distinct from suppressing a component in the model.

## Frames, sections and semantic targets

Consume typed Part/Component/Assembly identities from
[07](../2026-10-03_07_semantic-model-hierarchy/1_exploration.md). A part is a manufactured definition; a component
is its placed instance; an assembly supplies grouping and hierarchy. Preserve identities before geometry is merged
so drawing targets and cut components remain identifiable. Do not depend on a private ParametricDesigns manifest.

Define a canonical drawing frame for a part/assembly, with a clear local/world default. Front, rear, left, right,
top and bottom must derive consistently from that frame. Named points, axes, planes, profiles and interfaces in
[08](../2026-10-03_08_anchors-attachments/1_exploration.md) provide meaningful directions and attachment references.

Reuse the Section object owned by [14](../../3_done/2026-10-03_14_design-object-persistence/1_exploration.md) and also consumed by
[04](../../3_done/2026-10-03_04_live-clipping-sections/1_exploration.md): stable identity, target/frame, origin, normal and
an up direction defining the 2D section orientation. A section through an axis plus a named offset is preferable to
an unrelated world coordinate when that relationship expresses the design intent. A drawing must not make a second
independent copy of an inspection section. Section targets and component identity can support separate hatch
directions/spacing, component callouts and later BOM association.

## Three levels of dimensions

The opening proposal distinguishes these complementary approaches:

1. Automatic overall measurements: bounding dimensions and recognisable circles/holes where the geometry supports
   a reliable interpretation. Do not claim arbitrary feature inference from a merged mesh.
2. Model-defined dimensions: references to stable named anchors, axes, holes or other features; evaluate their
   geometry again when parameters change.
3. Interactive dimensions: the user picks references and saves an associative dimension. Store semantic/geometric
   references, not viewport pixels, and expose unresolved or changed references after model edits.

Prefer named semantic references, then a robust geometric description with owner/context, and only then weak
generated topology. Topological naming is an explicit design problem, not solved merely by assigning face numbers.
Dimension types, units, tolerances, formatting, placement and collision handling still need concrete requirements.

## Geometry and output pipeline

The proposed technical-output path generates projected silhouettes and visible feature edges, optional hidden edges,
exact section boundaries and hatching, then composes 2D primitives, dimensions, centre lines, text, notes, borders and
title blocks. SVG, PDF and DXF are the proposed output formats. Define which features each format preserves.

Live GPU clipping does not itself produce exact section contours. Consume reusable numerical sections/measurements
from [15](../../3_done/2026-10-03_15_geometry-services/1_exploration.md); own drawing-specific projection/edge styling and layout
here. Keep enough component information for vector drawings. Rendered/isometric images can supplement line drawings,
but a screenshot with overlaid arrows alone does not fulfil the repeatable technical-output intent.

## Persistence and editing

[14](../../3_done/2026-10-03_14_design-object-persistence/1_exploration.md) owns shared design objects, persistence closure and
reference resolution. Saving a drawing also persists its referenced unsaved sections/views without duplicating them.
Layout, dimensions, semantic references and deliverable notes must travel with the design and reproduce the output.

Graphical edits update the `.scad` buffer containing the declaration, with undo, dirty/save and ordinary external-file
conflict handling from [02](../../3_done/2026-10-03_02_source-editing-foundation/1_exploration.md). Expressions can refer to model
parameters and must retain their parametric relationships. Included files have explicit editor ownership and normal
save/reload protection. No VS Code broker, CRDT or separate drawing-sidecar grammar is required.

## Suggested delivery and evidence

First prove a repeatable single-part sheet with orthographic/isometric views, deterministic orientation/scale and
basic dimensions. Then add hierarchy-targeted and section views, named/interactive associative dimensions, and
validated exports. This sequencing is derived here; broader style, detail/exploded-view and BOM support can follow.

Use dimensioned reference models and a multi-part doorway-device-style example. Change model parameters and
regenerate without AI intervention: verify sheet arrangement, updated dimensions, section orientation/position,
component visibility, scale/units, missing-target diagnostics and reopen behavior. Inspect exported linework,
hatching, text and rendered views. Define renderer coverage and vector/raster behavior per output format.

Full interactive source manipulation is not a prerequisite. Drawings follow usable hierarchy, reference, section
definition, numerical geometry and persistence contracts. The clipping dock is not a build prerequisite: create
Section definitions through the shared document API for drawing fixtures even when 04 is absent.

## Branch boundary

Proposed source branch: `feature/technical-drawings`, with 08/14/15 as direct new-feature prerequisites. Own drawing
definitions registered with 14, projection/presentation, dimension UI, sheet layout, output adapters and resources.
Never include clipping-dock headers or add a drawing-only semantic tree/Section copy. Numerical kernel extensions
return to 15; target/reference extensions return to 07/08. Build with its declared prerequisite set and also verify
shared Section editing when 04 joins the full composition. Output backends, fonts and other resources need portable
install rules and extracted-package checks. See
[branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Required first-sheet contract

Specify an actual dimensioned part and assembly sheet, including projection convention, units, view orientation,
scale/fit, alignment rules, supported dimension types and reference fallback. Record what happens to layout when a
part grows or a referenced feature disappears. Define automatic versus user-placed dimensions separately.
Select the first output formats and make a vector/raster/text/font/hidden-line/hatching fidelity table for each.
Keep optional BOM/detail/exploded views visible as later scope instead of quietly calling them implemented.

The design must map that example into 14's storage and 08's references, 15's computed contours and the existing output
facilities. Prove linework/hidden-edge generation against actual tessellated geometry; screenshots do not establish
vector accuracy. Only then specify drawing primitive types, layout algorithms, export modules and visual fixtures.
