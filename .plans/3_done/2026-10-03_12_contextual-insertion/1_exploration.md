# Contextual source insertion through the viewport

Planning review, 2026-10-04: all five choices accepted. [Requirements](2_requirements.md),
[technical design](3_overall-plan.md), source/preview contracts and six phases define the implementation handoff.
Native implementation and runtime checks remain outstanding. See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).

11's [provider/version contract](../2026-10-03_11_component-provider-adapters/provider-contract.md) now specifies its
catalog, typed fragments, scoped helper imports and bindings to separately installed libraries. Use that contract
when designing this consumer's preview and source transformations; 09/10 are postponed and remain unnecessary here.

Status: planning. Source: chat A in the [overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md).

## Requested workflow

Click a point/face, invoke a Blender-like Shift-A palette, choose a primitive/hole/thread/component, configure and
position a preview, then commit ordinary OpenSCAD text. The user frames this as a hybrid UI for easier text insertion,
not a fully visual CAD editor. The inserted result must immediately be normal editable source.

Core interaction: `pick -> Add palette -> select item -> configure -> placement preview -> commit`.
Example: click a cube face, choose an M4 threaded hole, set depth/direction, preview and commit.
Shift-A is the requested interaction reference; integrate it with SCADMaxx's configurable shortcut system.

## Context and palette

Use hit world/local positions, normal, selected source object, instance path, semantic parent and insertion context.
An extensible searchable/menu palette can group primitives, holes (plain/countersunk/counterbore/threaded), fasteners,
BOSL2, BOLTS standard components, NopSCADlib hardware and user/project entries. Registry content belongs to
[11](../2026-10-03_11_component-provider-adapters/1_exploration.md), not hard-coded UI branches.

BOLTS is the standards library corrected by the user. NopSCADlib remains another example, not its replacement.
11's accepted first catalog is cube, sphere, cylinder, plain hole, BOSL2 threaded hole and BOLTS screw/nut/washer.
The wider category examples above do not extend that initial catalog. Catalogs ship; vendor libraries do not.
Provider and placement/source adapters answer separate what/where/how questions.

## Proposed preview and placement behavior

- Show a temporary item plus a compact parameter inspector before modifying source.
- Appropriate controls may include size/standard, length/depth, tolerance, direction and rotation. Exact fields are
  provider-defined; the M4/12 mm/6H example is illustrative, not a fixed schema.
- Derive orientation from 11's item contact frame and 08's mating solver, with explicit Flip. A screw is additive but
  its shaft points into the surface; additive/subtractive operation alone cannot determine orientation.
- Move in the placement plane and spin about its normal. Accepted configurable defaults: G move, R spin, F Flip,
  Enter Commit, Escape Cancel; numeric offsets/spin and an inspector anchor selector. Tab cycling was not selected.
- Prefer meaningful semantic/BOSL2 attachments when available; otherwise use readable relative/ordinary transforms.
- Preview cancellation leaves source untouched. Enter/Commit applies one logical transaction to the live buffer.

## Boolean and source semantics

An added sphere/component is usually additive; a hole/threaded-hole mask is subtractive. Choose the intended parent
and update the appropriate boolean scope, including a suitable difference or supported BOSL2 tagged operation.
Do not merely append a positive cylinder and call it a hole. Preserve surrounding expressions/comments/formatting,
add required includes deliberately, and never modify a library definition or all instances by accidental targeting.

Commit through [02](../2026-10-03_02_source-editing-foundation/1_exploration.md), reparse and show the evaluated result.
Keep disk writes under normal Save. Re-resolve stale source/hits before commit; a tab or source change during preview
must not redirect insertion to another document or obsolete range.

## Dependencies and evidence

Needs geometric selection, source/instance provenance, source transactions and providers. Semantic placement adds
hierarchy and anchors. It shares foundations with [10](../2026-10-03_10_interactive-source-editing/1_exploration.md)
but does not depend on all existing-object manipulation actions being complete.

First demonstrate a primitive and a genuinely subtractive hole end to end, then a standards/component provider and
attachment-aware placement. This is a derived delivery sequence; initial providers are now frozen by 11.
Verify orientation, local/world frames, boolean target, include generation, comments, preview/cancel, single undo,
source changes during preview, repeated instances and multi-document safety. Reload the saved source independently
to prove the inserted geometry is fully represented in code.

## Accepted decisions, 2026-10-04

07 keeps cuts/unions inside Part geometry and arranges separate Components in Assemblies. Its initial contract
forbids cross-Component booleans. Therefore a hole in a semantic Part cannot be implemented by wrapping its placed
Component in a difference; a shared definition edit has wider scope and must be explicit. Primitives add Part geometry,
holes cut it, and hardware becomes a separate Component in the containing Assembly. Show destination and operation.
Shared edits require an explicit choice listing affected instances; no automatic definition cloning or loop expansion.

08's live Attachment places Components and is declared at file/Assembly scope, not inside Part geometry. The accepted
scope is fixed local placement for new Part geometry and live named attachments for separate Components. This is not
permission to bake an existing expression or silently degrade a live relation. Saved face picks follow owner placement,
not a changing surface, as already accepted in 08.

02 applies one transaction to one live document. Source rewrite design must keep imports/helpers, geometry and any
new reference declarations for an insertion within that document. Included definitions require an explicitly chosen,
open editable source document; disk-only or multi-document mutations are not provided by 02. Preserve scoped helper
imports from 11, including BOLTS isolation. These constraints require concrete source fixtures before implementation.

Show a movement ghost, then asynchronously evaluate the actual candidate model, including cuts and shared instances.
Only a current successful candidate can Commit; the live buffer stays untouched beforehand. Numeric controls and
the configurable shortcuts above apply in viewport context; editor/Vim priority remains. All five choices are settled.
Direct prerequisites and independence from postponed 09/10 are unchanged.

## Branch boundary

Proposed source branch: `feature/contextual-insertion`, with 02/03/06/08/11 as direct prerequisites. Own palette,
parameter/preview controller, provider-to-placement integration, include/name handling and boolean-scope source
transformations. 11 returns source fragments/metadata; this branch decides how they enter the document through 02.
Use 03's transient overlay/tool routing and 08's shared frames. Build without 09/10 and add no dependency on their
UI controllers. Test action/shortcut conflicts and interleaved source changes in the complete composition. See
[branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).
