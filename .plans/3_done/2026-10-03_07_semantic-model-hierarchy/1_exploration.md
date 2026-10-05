# Semantic parts, components, assemblies and instances

Planning review: all seven decisions are accepted and recorded in [requirements](2_requirements.md), including
annotated module definitions/calls. The [technical design](3_overall-plan.md) and six bounded implementation phases
specify grammar, library binding, evaluation, display, source edits and export. See the
[readiness audit](../../1_planning/2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Status: planning. Sources: chats C/A in the [overview](../../1_planning/2026-10-03_00_source-first-cad-overview/1_exploration.md).
All ten exchanges of C were recovered, including the user's typed-node and hierarchical-selection decisions.

## Purpose and boundaries

Make parts and assemblies first-class across SCADMaxx, not merely inside drawings. The user proposed object-notation
syntax for semantic geometry and explicitly rejected free-form type strings because the UI must know the types and
their operations. They endorsed a hierarchical Model tree with visibility toggles as the natural replacement for
the flat Customizer `selected_content` convention, with possible Customizer integration at different layers.

The accepted initial vocabulary is deliberately limited to three typed nodes:

- Part: a reusable definition of one manufactured item, with geometry, local frame and named references.
- Component: an instance referring to a Part or Assembly, with its own transform and instance identity.
- Assembly: a reusable definition of a hierarchy of components/subassemblies. Two bracket components can refer to
  one bracket part.

Accepted on 2026-10-03: Part and Assembly declarations are reusable templates and emit no geometry on declaration.
An explicit Component instance produces their placed geometry; a displayed root Assembly requires a root Component.
Defining a bracket and placing it twice produces two brackets, not a third copy from the definition itself.

Use language-recognized types, conceptually an enum, rather than a free-form `kind: "assembly"` convention. The user
suggested a symbol plus object-style braces analogous to `@{}` Customizer metadata. The accepted spelling is now
`@{type: Part}` / `@{type: Assembly}` on modules and `@{type: Component}` on calls, with explicit IDs.
Earlier `&{}` examples were illustrative and are superseded by the accepted source contract.

The later storage decision in [14](../2026-10-03_14_design-object-persistence/2_requirements.md) establishes annotated
object declarations in `.scad` and a shared kind/identity mechanism. Reuse that mechanism for semantic kinds here.
The behavior below constrains instantiation and parameters; the technical design specifies geometry ownership
and binding through ordinary module evaluation, without introducing module-valued object expressions.

Semantic wrappers preserve identity without changing the CSG result. Maintain a semantic hierarchy alongside CSG
evaluation, keeping component geometry before final composition destroys its identity. The tree exposes intentional
author-defined objects, not every union/difference/transform node. Ordinary geometry need not declare an assembly.

Accepted on 2026-10-03: Parts contain their finished manufacturing geometry, including cuts/unions. Assemblies
place/group Parts and subassemblies; the initial semantic assembly mechanism does not perform boolean cuts or
fusions across Component boundaries. A hole through two plates is represented in both Part geometries, potentially
driven by shared parameters. A later assembly-machining feature would need an explicit effect-on-parts contract.

## Proposed responsibilities

- A lightweight semantic/evaluated hierarchy with stable explicit IDs where available and honest weaker identity
  for ordinary anonymous geometry.
- A model tree integrated with shared selection, properties, visibility, isolation and targeted export.
- Replace `selected_content` plumbing in new semantic models with generic hierarchical targets; do not require a
  model-specific `if (selected_content == ...)` chain. Existing project migration is separate scope.
- Shared targets for drawings, dimensions, anchors, insertion, assembly visibility and annotations.
- Later BOM support is an extension opportunity, not a requirement to build a complete parts-management system now.

Type-specific actions include show/hide children, isolate/solo, select/highlight, fit view, inspect instance transform,
find underlying part, export, create drawing/section and annotate. Assembly explosion/BOM and STEP export were future
possibilities, not requirements to implement a new geometry backend now. Hierarchical render/export targets such as
`/doorway_fitness/handles/left_handle` or its parent subassembly should work for UI and future CLI/API consumers.

## Targeted export and ordinary models

Accepted on 2026-10-03: exporting a selected Component uses its actual resolved parameter values and defaults to
its own local coordinates. An explicit As placed option retains its placement in the full model. An Assembly target
defaults to its own local frame and preserves all relative placements within it. Exporting a definition uses its
default parameter values. Inspection hide/solo and live clipping do not silently change export scope or geometry.

An ordinary model without semantic declarations retains its existing geometry and Customizer behavior, with one
Model entry in the semantic tree. Mixed models show declared semantic instances and an Other geometry entry for
unassigned geometry. Do not infer semantic Parts from every module/boolean or convert source automatically.
These anonymous entries provide inspection, not invented durable part identity. Semantic adoption can be gradual.

## Selection, visibility and parameters

Keep three independent concepts: clicking selects; eye toggles viewport visibility; solo temporarily isolates.
None removes geometry from the parametric program. Enabled/suppressed model configuration, if supported, is a separate
operation affecting evaluation. Do not recreate `selected_content` under a tree-shaped interface.

The Customizer follows selection rather than maintaining a second competing selector. Accepted on 2026-10-03:
Part/Assembly definitions provide parameter defaults; individual Components may supply overrides. Two instances
may have different dimensions without duplicating their definition. Assembly parameters reach children through
explicit source arguments/expressions, never implicit matching-name inheritance.

Selecting a Component shows its resolved values and where they originate: definition default, explicit instance
override or expression passed by its parent. Editing an instance override affects that instance; editing shared
definition defaults is a separate deliberate action and affects uses that still inherit those defaults. Preserve
expression-linked values and expose their source/owner; do not silently flatten an expression into its current value.
Tree navigation and Customizer controls remain available at different layers, with an optional all-parameters view.
The technical plan specifies parameter controls and source binding; the earlier `owner` field was illustrative.

## Identity

Accepted on 2026-10-03: keep persistent IDs separate from editable display labels. Part/Assembly definitions have
document-wide IDs; Components have explicit IDs unique within their parent. Full ID paths identify placed instances,
such as `/frame/left/bracket`. Root Component IDs are unique under the document root. Repeated/loop components supply
explicit keys rather than receiving identities from their evaluation order.

Renaming "Left handle" to "Left grip" or reordering siblings preserves references. Changing an ID or reparenting a
Component changes its instance path and requires deliberate reference repair. Deletion leaves references unresolved;
do not automatically retarget them to a geometrically similar item. Definition identity remains separate from its
instances' placement paths. Map those distinctions into 14's document registry/resolver without weakening its
duplicate-ID rules; the exact qualified record encoding is technical design.

Separate part ID from instance path: a manufacturing drawing usually targets the reusable Part, while an assembly
dimension targets two placed instances. Retain quantities and part references for later BOM output. Do not conflate
semantic identity, named feature/reference identity, and generated face/edge/vertex numbering; only the last has the
general topological-naming problem. The reference policy belongs to anchors and design-object persistence.

Reuse source/instance provenance from [06](../2026-10-03_06_source-geometry-provenance/1_exploration.md) and selection
from [03](../2026-10-03_03_selection-model-inspector/1_exploration.md). Anchors belong to semantic owners but have their
own contract in [08](../2026-10-03_08_anchors-attachments/1_exploration.md). Do not duplicate an assembly tree in drawings.

Model declarations remain source-defined. UI changes to declarations eventually use source transactions; transient
selection/visibility belongs to inspection state, and per-drawing visibility belongs to the drawing document.

## Accepted decisions and verification obligations

All seven decisions are settled: templates/placement, parameters, identity, finished-Part geometry,
local/placed export, ordinary-model presentation and annotated module definitions/calls. The technical plan specifies
executable grammar, parameter/source binding, nested/repeated evaluation, library boundaries and output targets.
Preserve generic semantics; the
ParametricDesigns and doorway-fitness examples motivate the feature without importing private project infrastructure.
Removal of obsolete product mechanisms must update affected consumers without unrequested compatibility layers.

Validate nested assemblies, repeated parts, source changes moving ranges, rename/deletion, visibility/isolation,
selection/Customizer synchronization, visibility versus suppression, targeted export and dangling references.
Establish the semantic contract before full drawing or semantic-placement work; it does not block basic clipping or Vim.

## Branch boundary

Proposed source branch: `feature/semantic-model-hierarchy`, with 03/06/14 plus selected OEP8/Customizer prerequisites.
Own typed semantic declarations/evaluation, the model tree, parameter ownership/Customizer binding and the concrete
semantic-target resolver registered with 14. 03 supplies selection/Inspector seams; it does not import this feature.
14 supplies persistence/reference interfaces; this branch supplies semantic rebinding. Keep named geometry/attachment
resolvers in 08, drawing logic in 09 and source-manipulation actions in 10/12.
Verify parser round trips, existing Customizer reactivity and tree/viewport selection on the declared base before
composition. See [branch integration and handoff rules](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Specification and implementation gates

The [accepted example](source-authoring-proposal.md) and technical design give exact trees, parameter origins,
repeated/nested instances, source ownership and registry encoding. Six implementation phases must prove these
behaviors, geometry equivalence and native composition before claiming implementation complete. No build was run
to validate these planning documents. The source review supports the route but cannot replace runtime evidence.

## Accepted source authoring form

Read-only source review at `4c325716b94e444637a80df3966197ce110b2b75`: `parser.y` currently attaches attribute_block
only to assignments. Named geometry modules are UserModule declarations with parameters/body and a separate
ModuleInstantiation call path. Ordinary object values are expressions; that parser has no anonymous module-valued
expression. `doc/customizer-attributes.md` confirms the existing annotation target is the next assignment.

The accepted authoring route extends annotation targets to ordinary module definitions and calls: Part/Assembly
metadata on module definitions, Component metadata on calls. This keeps existing geometry statements and parameter
lists, uses the known typed annotation vocabulary, and reuses 14's registry/resolver. Section/View remain annotated
object assignments. The user accepted this replacement for the earlier object-declaration idea on 2026-10-03.
It is new grammar to implement, not syntax supported in the inspected baseline. See the
[worked source example](source-authoring-proposal.md) and [implementation contract](3_overall-plan.md).
