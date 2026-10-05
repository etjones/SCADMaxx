# Semantic hierarchy requirements

All seven decisions accepted on 2026-10-03, including typed annotations on module definitions and calls.
The [technical design](3_overall-plan.md) and six implementation phases specify the implementation handoff;
they do not claim implemented syntax or runtime verification. Preserve [exploration](1_exploration.md).

## Definitions, instances and geometry

- SH01: provide language/UI-recognized Part, Component and Assembly kinds using the shared typed declaration
  mechanism. Part/Assembly annotate ordinary module definitions; Component annotates an ordinary module call.
  Section/View remain annotated object assignments. Free-form kind strings do not determine semantic behavior.
- SH02: Part and Assembly definitions are reusable templates and produce no displayed geometry on declaration.
  Explicit Component instances place them; an Assembly needs an explicit root instance to appear in the model.
- SH03: Part geometry describes one finished manufactured item, with its own local frame and source association.
  Cuts/unions defining that item belong inside its geometry. Semantic wrapping must not alter that geometry.
- SH04: Assemblies arrange Parts/subassemblies and retain component boundaries. The initial semantic assembly
  mechanism does not perform boolean cuts/fusions across Component boundaries or silently change Part geometry.
  A shared machining parameter can drive matching cuts in individual Parts. Diagnose unsupported composition.
- SH05: retain semantic hierarchy and component geometry before final composition merges geometry. The model tree
  presents intentional authored instances, not every internal CSG operation. No fabricated final-face ownership.

## Parameters and Customizer

- SH06: Part/Assembly definitions have parameter defaults; Components may override them. Instances of one definition
  can differ without duplicating it. Assembly-to-child values pass through explicit source arguments/expressions.
  Matching parameter names alone do not create inheritance or coupling.
- SH07: Customizer follows the selected semantic node and shows resolved parameters with their origins: default,
  instance override or parent expression. Support navigation to the parameter owner and an all-parameters view.
- SH08: editing an instance override affects that instance; editing definition defaults is a separate explicit
  action. Shared/default edits must communicate their wider scope. Never silently replace an expression by its
  evaluated constant. Unsupported/ambiguous derived values remain inspectable with source navigation.
- SH09: declaration/parameter source edits use the authoritative live source buffer, transactions, revision guards,
  normal undo and ordinary Save. Reject stale, read-only, closed or ambiguous targets before mutation. No implicit
  write to a library or hidden second model. Per-instance editing must not silently change all loop instances.

## Identity and references

- SH10: definitions have document-wide IDs; Components have explicit IDs unique within their parent, including the
  document root for root instances. Placed instances are identified by full ID paths. Labels are independently editable.
- SH11: repeated and loop-generated Components supply explicit keys. Never derive durable identity automatically
  from evaluation order, source offsets, labels or generated face/edge/node numbering. Duplicate sibling IDs and
  duplicate definition IDs produce diagnostics rather than first/last-winner behavior.
- SH12: label rename and sibling reordering preserve references. Changing an ID or reparenting changes the instance
  path and requires deliberate reference repair. Deletion becomes unresolved. No nearest-geometry retargeting.
- SH13: distinguish reusable definition targets from placed-instance targets. Retain definition references, actual
  parameter values and transforms for later drawings/anchors/BOM work. This feature does not implement a BOM system.
- SH14: register semantic-target resolution with 14 and consume 03/06's current result/provenance guards. Missing,
  stale, ambiguous or unsupported targets must be explicit; a refreshed node number cannot validate an old reference.

## Tree, inspection and output

- SH15: selection, eye visibility and solo are separate inspection operations. None suppresses geometry in the
  parametric program or silently changes source. Tree/viewport selection stays synchronized where a semantic owner
  is known, and exposes ambiguity where ownership is unavailable. Navigation and other tools remain usable.
- SH16: offer applicable selection/highlight, show/hide, solo, fit, transform inspection, definition/source navigation
  and targeted export actions. Sections use the shared 14 definition contract; drawing/anchor integrations are
  supplied by their later features and cannot become reverse build dependencies of 07.
- SH17: targeted Component export uses its resolved parameter values and defaults to its own local coordinates.
  Provide explicit As placed export retaining its transform in the full model. Assembly-local export retains all
  relative child placements. Definition export uses definition defaults. Export target is explicit and unaffected
  by transient hide/solo or live inspection clipping.
- SH18: ordinary models without semantic declarations retain existing geometry and Customizer behavior and show a
  single Model entry. Mixed models show their explicit hierarchy plus Other geometry for unassigned content.
  Do not infer semantic Parts for every module/boolean, convert source automatically or invent persistent identity.
- SH19: libraries/includes, nested Assemblies and repeated instances must have explicit scope/ownership rules in
  the technical plan. Library source stays with its owner; inspecting/instantiating a library does not authorize edits.
- SH20: build on 03/06/14 and the selected object/Customizer baseline, without 08/09/10/12 implementations. Own the
  semantic declarations/evaluation, tree, parameter binding and resolver. Keep attachments, drawing layouts, general
  viewport authoring, explosion, assembly machining, full BOM and new geometry/export backends outside this scope.

## Acceptance examples

1. Define one bracket and place it twice: exactly two solids and two Component instances, sharing one definition.
2. Use widths 30 and 40 on the same Part: each instance evaluates and exports at its own width. Changing one override
   changes one instance. Changing a shared default affects only uses that still take that default.
3. Pass width/2 from an Assembly: selecting the child shows the evaluated value and expression origin. A numeric
   control cannot silently replace width/2. Source edits/undo preserve other instances and untouched text.
4. Nest the same subassembly twice, each with a child ID bracket: full paths differ; a duplicate sibling ID fails.
   Loop keys survive sibling reorder; inserting another loop item does not retarget existing references.
5. Rename a label: references still resolve. Change an ID/reparent/delete: affected references become unresolved
   until explicitly repaired. No similar nearby object is substituted.
6. Two plates share a hole parameter defined in their Part geometries: isolated and exported plates retain the holes.
   An attempted semantic cross-component cut receives an explicit unsupported-composition diagnostic.
7. Export a rotated/translated instance locally and As placed: shape/parameters agree, placement differs as chosen.
   Export a subassembly locally: internal placements remain. Hidden siblings/clipping do not silently alter output.
8. Open an unannotated model, then a mixed model: geometry and existing Customizer behavior remain intact; the tree
   adds only the agreed Model/Other geometry entries and explicit semantic instances.
9. Change source/include contents or tabs during selection/edit/export preparation: reject stale targets and keep
   source/geometry ownership with the captured document. Invalid evaluation cannot masquerade as a current hierarchy.

The [accepted notation](source-authoring-proposal.md), technical design and phases freeze source, library/parameter
binding, records/resolvers, export/display algorithms and verification fixtures. Implementation waits for verified
03/06/14, including 03's shared inspection-presentation contract; it does not depend on implementing 04 or 08.
