# Shared selection, picking and Model Inspector

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Planning review: [requirements](2_requirements.md), [technical design and four phases](3_overall-plan.md) are prepared.
The dedicated surface pass and native renderer proof are specified implementation work, not completed tests. See the
[readiness audit](../../1_planning/2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Original exploration status: planning. Sources: chats A/C/D in the [overview](../../1_planning/2026-10-03_00_source-first-cad-overview/1_exploration.md).

## Purpose and shared context

Provide one selection service for clipping, dimensioning, source editing and insertion. Model Inspector is the visible
surface: object/part selection, face/point picking, properties, source navigation and saved views.

Proposed hit context has independent layers:

- Geometry: world position, local position when available, surface normal, face/triangle and object identity.
- Evaluation: document/result revision and instance path, keeping repeated module calls distinct.
- Source: AST/source range, expression/module invocation and relevant parameters, when known.
- Semantics: component/assembly owner, parent and available anchors, when defined.

Keep missing information explicit. A geometric hit supports clipping without provenance; it does not imply safe
source editability. Guard hits against re-evaluation, document switches and stale displayed results.

## First delivery and follow-through

Inspect/reuse existing picking before adding a raycaster. The chat points to `MouseSelector` and off-screen/depth
picking; verify actual return values and backend coverage locally. Deliver position/normal picking first.

Support one-shot point and point-plus-surface picking, then restore normal navigation. Misses/cancellation leave
state intact. Expose an origin marker for manipulation pivots. Clipping depends only on this geometric slice.

The dependent [06](../2026-10-03_06_source-geometry-provenance/1_exploration.md) branch adds source navigation;
[07](../../1_planning/2026-10-03_07_semantic-model-hierarchy/1_exploration.md) adds the semantic tree/part context and Customizer
binding. Those integrations belong to their branches, not unfinished phases of this foundation. Tree and viewport
share selection through this feature's contract.
Properties stay observational until a supported source edit exists. Selected-node, inherited-assembly and
all-parameters Customizer views follow 07's parameter-ownership contract. Selection, visibility, solo and actual
model suppression remain separate operations.

Saved-view objects and their Inspector commands belong to the dependent
[14](../2026-10-03_14_design-object-persistence/1_exploration.md) branch. Personal camera/visibility state can stay
in the workspace; named views used to reproduce drawings or renders travel with the design. Do not create
incompatible inspection and drawing copies of the same reusable view.

Inspect integration with current right-click selection, navigation, measurements and annotations. Panel layout,
selection precedence, backend capabilities and saved-view storage are implementation-design decisions.

## Order and evidence

Base picking precedes [clipping](../2026-10-03_04_live-clipping-sections/1_exploration.md) independently of source and
semantic infrastructure. Later inspector slices must not block that delivery.

Check repeated/transformed instances, front/back faces, world/local conversion, transformed normals, misses,
cancellation, stale results and multiple documents. Report unavailable source context rather than guessing it.

## Branch boundary

Proposed source branch: `feature/selection-model-inspector`. Own geometric hit production, the basic Inspector,
small contribution interfaces and transient viewport overlay/tool routing. Existing navigation and annotations
must keep working; use those selected entries as recorded prerequisites. Clipping, source manipulation and insertion
register their own controllers without each taking over QGLView's input handling. This is a small shared seam, not a
new plugin framework. Compile/test with none of 06/07/08/14 present; no future-consumer headers or fake semantic data.
See [branch integration and handoff rules](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).
