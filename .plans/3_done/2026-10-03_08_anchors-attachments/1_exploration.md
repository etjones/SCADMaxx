# Shared anchors and attachments

Planning review: [requirements](2_requirements.md), [source contract](source-contract.md),
[technical design](3_overall-plan.md) and six implementation phases are prepared. The pinned BOSL2 frame mapping
has executed probe evidence; the native feature still needs its specified implementation/runtime proofs. See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).
All six initial-scope decisions were accepted by the user on 2026-10-03. 07's semantic definition/instance contract
is specified. Technical source/evaluation and adapter work follows these decisions; no implementation starts here.

## Accepted initial scope

1. Deliver oriented anchors, points, axes and planes. Profiles and interfaces combining several mating features are
   deferred; they are not required for this branch to complete.
2. Define reusable anchors as annotated object declarations inside Part/Assembly modules, evaluated with actual
   module parameters. An explicit Component-owned declaration supplies an instance-only anchor.
3. A clicked surface anchor stays transient until explicitly saved. Saving captures a fixed point/orientation in
   its owner's local coordinates, labeled as such. It follows placement but does not automatically follow changing
   faces/holes. Parametric named anchors provide that behavior; automatic surface rematching is deferred.
4. Attachments are live directed placement relationships with one placement attachment per child. Chains work and
   cycles fail. No general assembly constraint solver is included.
5. Mate is the default (coincident positions, opposed facing directions); Align matches facing directions. Support
   offset and spin. Attachment preserves child size/shape; transformed/mirrored owners need verified frame math.
6. Include a bounded BOSL2 adapter for standard/custom named anchors and basic parent-child placement on a pinned
   version, alongside plain OpenSCAD. Arbitrary library introspection and the full BOSL2 feature set are excluded.

Status: planning. Sources: chats A/C/D in the [overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md).

## Purpose

Separate meaningful modeling locations from raw selection. Selection says where the user clicked; an anchor gives
that location an orientation, semantic identity and owner. Reuse this across clipping origins, dimensions,
component insertion, attachment editing and section references.

Proposed anchor fields are position, orientation, spin, semantic name and owner. Define local/world frames and
identity explicitly. A hit position plus normal yields a transient geometric anchor; rotation around the normal
supplies spin. A clipping plane has only two orientation degrees of freedom, but component placement needs spin.

The recovered drawing discussion also proposes typed reference geometry: named points, axes, planes, profiles and
interfaces. These can support dimensions, section placement, annotations, snapping, measurements, camera frames,
exploded views and agent inspection. Share ownership/frame/reference machinery without treating every reference as
an interchangeable point anchor or adding every possible feature kind to the initial semantic-node vocabulary.

Provide a canonical drawing frame for a Part/Assembly so front/top/side directions are deterministic. Section views
also need an up direction within their plane: it changes drawing orientation although it does not change clipping.

## BOSL2 and general OpenSCAD

BOSL2 is a natural adapter, not the definition of the entire system. Its parent/child attachment model and custom
named anchors were identified as a strong fit. Verify exact APIs and the installed revision before generation.
Plain OpenSCAD geometry must still support transient/geometric anchors and ordinary source transforms.

The proposed placement preference is: existing semantic anchor, appropriate custom named/BOSL2 anchor, relative
source transform, then explicit absolute transform when no stronger relation is available. These are alternative
modeling strategies, not backward-compatibility layers. Generated placement must remain understandable source.

Anchor creation from a click does not itself change source. Persisted modeling anchors/attachments require an explicit
source action through [02](../2026-10-03_02_source-editing-foundation/1_exploration.md). A clipping origin does not
modify CSG geometry; reproducible section declarations share
[14](../2026-10-03_14_design-object-persistence/1_exploration.md). Drawing dimensions may reference semantic anchors
without turning them into constraints.

## Ownership and lifetime

Use [03](../2026-10-03_03_selection-model-inspector/1_exploration.md) for geometry and
[07](../2026-10-03_07_semantic-model-hierarchy/1_exploration.md) for owners/instances. Keep instance-local and definition
anchors distinct. Define how anchors follow source changes, transformed instances and topology changes; mark lost
references explicitly rather than silently attaching to a different surface.

The earlier exploration considered three reference strengths, including geometric descriptions and generated
topology identifiers. The accepted initial scope uses explicit semantic/named references and fixed owner-local
captures; raw picks remain bound to their evaluation. Geometry rematching/topology persistence is deferred.
A triangulated face index cannot be a stable design feature. Keep missing/changed/invalid diagnostics and persisted
dependencies consistent with 14 rather than adding separate recovery rules for each consumer.

Placement integration in [12](../2026-10-03_12_contextual-insertion/1_exploration.md) consumes this contract together
with provider metadata from 11. Do not bake provider-specific menus or complete library assumptions into the core
anchor service; 11 itself does not import this service.

## Order and acceptance direction

Stabilize semantic ownership before persistent anchors; transient geometric anchors can be prototyped with picking.
Basic clipping does not wait for this feature. Full semantic drawings, attachment edits and insertion consume it.

Validate parent/child frames, normals and spin, transformed/repeated instances, direction flips, named anchors,
plain OpenSCAD placement, and stale/deleted owners. The source contract and technical design now specify persistence,
frame math and live evaluation order. Automatic mesh-feature rematching is explicitly outside the accepted scope.

The initial review checked BOSL2's official [attachment overview](https://github.com/BelfrySCAD/BOSL2/wiki/Tutorial-Attachment-Overview)
and [attachment API](https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad): the documented model includes
parent/child placement, orientation/spin and named anchors. The subsequent [pinned investigation](bosl2-investigation.md)
verified the existing installed revision and executed six placement plus two anchor-position assertions. This proves
the selected library mapping, not the future SCADMaxx bridge or native Anchor/Attachment implementation.

## Branch boundary

Proposed source branch: `feature/anchors-attachments`, with 03/07/14 as direct prerequisites. Own reference geometry,
frame/attachment calculations, named-feature resolution and its contribution to the shared persistence service.
The generic resolver interface remains owned by 14; it must not import this implementation. Expose placement results
for both 10 and 12. Provider metadata/source-fragment generation in 11 does not depend on this branch; 12 combines
the two contracts. Keep drawing layout and full manipulation/insertion controllers out of the shared anchor service.
See [branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).
