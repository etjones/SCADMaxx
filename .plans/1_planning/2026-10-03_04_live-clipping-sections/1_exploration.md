# Live clipping and saved cross-sections

Planning review: [requirements](2_requirements.md), [technical design and four phases](3_overall-plan.md) are prepared.
The chosen renderer prepares a mesh once per result, then clips on the GPU; native correctness/performance remain to verify. See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Status: planning. Sources: all seven exchanges in D, C's shared-section discussion and A's synthesis in the
[overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md). The two earlier D exchanges and its original
[clipping-dock HTML mockup](assets/clipping-dock-mockup.original.html) were recovered from the local app cache.

## User decisions and canonical state

Clipping is a separate inspection feature in a dockable window. Save named planes for later activation. Moving a
clip changes the displayed cutaway, not the model's CSG geometry. The user explicitly requires that clipping
coincident with a model face removes that face cleanly instead of causing z-fighting.

Proposed inspection state: name, origin, unit normal, enabled, showPlane and display options. Use the same Section
object through unsaved and persisted states; stable ID, target/frame and drawing up direction come from
[14](../2026-10-03_14_design-object-persistence/1_exploration.md). Persist named planes across reopen and make sections
used by drawings reproducible with the design. The user selected typed, annotated declarations in the main or an
included `.scad` file. Saving a Section definition is distinct from changing the model's geometry.

Axis labels, angles and slider positions are UI representations, not independent geometric definitions. Flip
negates the normal. A section's drawing up direction does not alter the mathematical clipping half-space.

## Three levels of section feedback

The opening discussion distinguishes a translucent plane through an intact model, live renderer/GPU clipping, and
computed exact section geometry. Plane-only preview is useful for positioning, but live clipping is the intended
interactive inspection behavior. Slider motion must not repeatedly run CSG evaluation.

Exact contours, a filled section, measurements and SVG/DXF section export can be computed on release, after idle or
on demand. These are later geometry/output capabilities shared with drawings and agent tools, not a prerequisite
for every drag. A bounds-centred initial axis plane and a bounds-derived slider range were proposed; offsets may be
negative. Optional section outlines and filled/capped cuts depend on backend support.

## Dock and viewport design

- Global clipping toggle; create, name/rename, select, edit, enable/disable and delete saved planes.
- XY/XZ/YZ presets and free orientation; two angle controls with exact numeric entry.
- Position slider derives its range from model bounds and moves along the plane's current normal after any rotation.
- One-shot `Pick point` changes only origin; `Pick + align` also aligns to the selected surface.
- Show an origin marker and optional translucent helper plane; helper visibility is separate from clipping enablement.
- Drag along the normal; rotate with two-axis gizmo/rings around the current origin. Dock values follow immediately.
- Flip retained/discarded half and reset orientation. Rotation snapping at useful increments was proposed; exact
  keys and increments remain open.
- Multiple enabled planes clip simultaneously; visible geometry satisfies all enabled half-space tests.
- Render-side updates remain live while dragging, without rerunning OpenSCAD evaluation.

The recovered mockup illustrates a saved-plane list, add/name/enable controls, presets/free orientation, picking,
normal offset, rotation, flip/reset and helper/boundary/capping options. It is the original conceptual HTML widget,
not a production layout: its fixed slider limits and schematic geometry are illustrative. Textual requirements,
including global clipping and deletion, remain authoritative where the mockup omits controls.

## Coplanar-face invariant

Geometry on the boundary belongs to the discarded side. For a positive-distance retained-side convention, keep only
`dot(p - origin, normal) > epsilon`, using scale-aware tolerance. Choose the picked-face normal sign to reveal the
interior behind the clicked wall; a raw outward mesh normal may need negation. Flip reverses the retained side.
Tolerance must not consume nearby intended thin geometry.

Give the helper plane depth bias or a visual-only offset without moving the actual clip. Cut-surface highlighting or
capping is desirable if renderer feasibility permits; it was explicitly left conditional. Any cap must not fight
with the original coincident face.

## Seven workflows from the final exchange

1. Quick orthogonal section: open dock, add plane, choose preset, slide through bounds, flip if needed, name it.
2. Section through a point: select plane, pick once, preserve orientation, then offset or rotate.
3. Surface-relative section: pick and align, remove the clicked face, offset inward/outward, optionally flip.
4. Angled section: begin from preset/pick, rotate about its origin, move along the new normal.
5. Direct manipulation: select helper, drag normal handle or rotation rings while dock values follow.
6. Saved inspection: name and disable instead of deleting, reopen/re-enable, combine planes for a cutaway.
7. Temporary inspection: create, inspect and delete; no model-source edit is required.

## Later extensions from the opening discussion

A finite-thickness slab between two planes is a possible extension after single/multiple half-space clipping.
Optional "create from section" actions can copy parameters or deliberately create source parameters, a 2D projection,
a CSG cut or construction reference. They belong to explicit source authoring in
[10](../2026-10-03_10_interactive-source-editing/1_exploration.md), with a known target and coordinate frame.
Neither slab mode nor source creation is required for the first clipping delivery.

## Dependencies, technical design and evidence

Use [03](../2026-10-03_03_selection-model-inspector/1_exploration.md) for hits and the minimal lifecycle/persistence
contract in [14](../2026-10-03_14_design-object-persistence/1_exploration.md). Semantic anchors may enhance placement
later but are not prerequisites. Expose these same Section objects to
[09](../2026-10-03_09_technical-drawings/1_exploration.md) without combining feature ownership.
Exact drawing contours are separate from live display clipping.

Shared numerical section computation belongs to
[15](../2026-10-03_15_geometry-services/1_exploration.md). A later computed-section action can use that service;
the first live-clipping branch has no 15 dependency. Drawings depend on the Section definition in 14 and do not
need to link this dock or renderer implementation.

The [technical plan](3_overall-plan.md) selects prepared inspection meshes, eight enabled planes and explicit
unsupported/capping states, using 14's source lifecycle. Test all workflows and reopen persistence, helper/clip toggles, multiple planes,
oblique/transformed faces, small/large models and thin walls. Verify clean coplanar removal, no geometry-source
changes or model evaluation while dragging, and intentional saving through the shared document lifecycle.
Report backend/capping limits explicitly.

## Branch boundary

Proposed source branch: `feature/live-clipping-sections`, with 03 and 14 as its direct new-feature prerequisites.
Own dock/actions, clipping renderer/shader changes, plane manipulation and their resources/tests. Use 03's tool
routing and 14's Section objects; do not implement a private section store. Keep transient plane manipulation
usable without semantic hierarchy. Verify navigation/annotation overlays and coplanar clipping together in the
composition, including packaged shaders. See
[branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).
