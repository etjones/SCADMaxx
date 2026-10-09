# Interactive source editing from the viewport

Planning review: product scope is unresolved. Establish the intended user workflow and its value beyond 07's
parameter editing, 08's attachment controls and 12's insertion before choosing edit policies or implementation phases.
The user challenged whether general interactive resizing was ever an agreed feature. See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Status: postponed by the user after reviewing the unresolved scope. Preserve this exploration and unaccepted
proposals; resume only when requested. The next decision review is 11. No other active feature requires 10.
Sources: chats C/A/D in the [overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md).

Review history: the user selected this feature after postponing 09. The six recommendations in
[the suspended decision questions](0_conversation.md) remain unaccepted proposals. Existing 07/08 rules
already require explicit shared edits, expression preservation and guarded source transactions; do not reopen those.

The user then questioned the usefulness and definition of the proposed tools, especially editing a length derived
from another variable. The six recommendations have not been accepted. Do not equate source-edit infrastructure
with an agreed general direct-modeling feature or implement a collection of literal-only controls by default.

## Scope provenance and current concern

The retrieved C discussion includes the user's question about an interactive-editing research prototype, followed
by agreement about live text buffers, formatting and external-editor save behavior. Those establish source-edit
principles, not the semantics of resizing arbitrary geometry. In A's synthesis, the assistant described parameter,
dimension and attachment manipulation as examples that could eventually be supported. A's concrete user proposal
was contextual insertion, now feature 12. The previous six-point first-delivery proposal was added during this
planning chat and must not be presented as an earlier user decision.

For length = width - 2*wall, dragging the length does not identify whether width, wall or the expression should change.
Even an invertible expression such as width/2 leaves the question of changing other uses of width. Derived properties
are not inherently uneditable: explicit driving-input selection or authored handle-to-parameter bindings could define
the operation, but neither mechanism has been accepted for 10. Existing parameter editing in 07 remains valid.

The user accepted postponing 10 and proceeding to 11. Before any future resumption, establish a concrete additional
workflow. No implementation phases or scheduling dependency on 10 should be invented from this review.

## Defining behavior

A viewport action modifying the model becomes a source-buffer edit. Select source-backed geometry, identify an
editable property, manipulate it and apply a minimal patch through the shared editing engine. Reparse/evaluate then
produces the next geometry. There is no hidden second editable model or deferred whole-file regeneration.

Proposed action families include parameter changes, source-aware translation/rotation/scale, editing an expression
represented by a displayed dimension, and attachment-argument manipulation. These are candidate families, not a claim
that arbitrary OpenSCAD programs have a unique inverse edit.

D's opening discussion adds optional actions starting from an inspection section: copy its position/normal, create
source parameters, generate a 2D projection or deliberate CSG cut, or create a construction reference. These need a
known target, local/world frame and explicit source transaction. They are later authoring actions, distinct from
saving the Section declaration through [14](../../3_done/2026-10-03_14_design-object-persistence/1_exploration.md), and must
not make ordinary clipping gestures rewrite geometry.

## Editing constraints

- Use source revision, instance path and provenance to identify the intended target before enabling manipulation.
- Distinguish edits to shared definitions, call-site parameters and instance transforms; never change all repeated
  parts unintentionally when the user selected one instance.
- Preserve expression semantics and meaningful parameterization. Replacing `width / 2` with an evaluated constant
  is not automatically a valid edit. Decide supported transformations and expose ambiguity rather than guessing.
- Preserve comments/formatting outside targeted spans and use normal dirty/save behavior.
- Group a gesture into a logical undo operation; keep typed, Vim and graphical changes coherent.
- Re-resolve or reject stale mappings and preserve source on cancellation or failed evaluation.
- Determine live preview versus commit timing during design, without creating permanent geometry outside source.

## Dependencies and boundaries

Consume [02](../../3_done/2026-10-03_02_source-editing-foundation/1_exploration.md),
[06](../../3_done/2026-10-03_06_source-geometry-provenance/1_exploration.md), shared picking,
[07](../2026-10-03_07_semantic-model-hierarchy/1_exploration.md), and
[08](../2026-10-03_08_anchors-attachments/1_exploration.md) for attachment-aware operations.

Clipping remains inspection state; drawing dimensions do not automatically edit parameters. New-code insertion is
separate in [12](../2026-10-03_12_contextual-insertion/1_exploration.md), sharing this source-action infrastructure
without depending on completion of every manipulation tool. Vim remains an independent editor interaction layer.

Research described in [06](../../3_done/2026-10-03_06_source-geometry-provenance/1_exploration.md) supplies precedents, not a
verified ready-to-integrate implementation. External editors interoperate through normal file semantics; no broker
is required by the final user decision.

## Suggested first slice and evidence

Begin with an unambiguous literal transform or supported invocation parameter, proving source preservation and
one-step undo end to end. Expand to expressions and attachments only when their edit policies are explicit.
This bounded start is a sequencing recommendation, not a previously settled exclusion of other actions.

Check typed unsaved changes, odd formatting/comments, named expressions, nested/repeated instances, included files,
stale results, cancel, failed evaluation, undo/redo and external file conflicts. Exact gizmos, supported inverse-edit
rules and cross-file scope remain design decisions. General constraint solving and fully visual CAD are outside the
direction established in the chats.

## Branch boundary

Proposed source branch: `feature/interactive-source-editing`, with 02/03/06/08 as direct prerequisites. Own existing-
object action policies, manipulation controllers and source transformations, using 03's tool routing. Keep shared
text transactions, provenance and anchor math in their owners. 12 owns new-item insertion and does not include this
feature's controller headers. Reusable low-level needs discovered here must be implemented in the appropriate
foundation before both consumers adopt them, not copied between branches. Verify interleaved Vim/Customizer/HTTP
changes, undo and wrong-document/stale-result rejection after composition. See
[branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Required edit-policy matrix

For each proposed first action, record selected source form, allowed target, preview behavior, commit boundary,
before/after source, undo and failure outcome. Cover a literal transform, width/2, a named parameter used twice,
a repeated module call, a loop-generated instance and an included file. Distinguish modifying an existing literal,
editing a call argument and adding a wrapper; do not treat those as interchangeable edits.
Specify whether evaluation failure rolls back a committed source change or leaves an explicit invalid edit, and how
that policy interacts with undo. Settle which operations are supported or unavailable in the first delivery, then
design controllers around concrete 02/03/06/08 APIs rather than general inverse-programming promises.
