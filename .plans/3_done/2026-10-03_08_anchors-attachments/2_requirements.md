# Anchor and attachment requirements

All six scope/behavior decisions accepted on 2026-10-03. The source contract, numerical design and implementation
phases refine these choices. Retain [the exploration](1_exploration.md); source/runtime verification remains required.

- AN01: Represent a meaningful modeling location with owner/instance identity, local position and orientation, optional
  semantic name and spin around its normal. Distinguish instance-local anchors from definition-wide anchors.
- AN02: A geometric hit can create a transient anchor without source edits. Normal gives two orientation degrees of
  freedom; spin supplies the remaining placement degree. Explicitly define local/world and parent/child frames.
- AN03: Initially support oriented anchors, points, axes and planes. Profiles and multi-feature interfaces are deferred.
  A point/axis/plane without a complete orientation cannot silently become a fully constrained attachment frame.
- AN04: Provide deterministic canonical drawing frames for semantic targets and a section up direction. Drawing up
  changes 2D presentation while leaving a clipping half-space unchanged.
- AN05: Prefer explicit named parametric anchors. A saved click is explicitly a fixed owner-local position/orientation;
  it follows placement but does not promise to track a changing surface/hole. Raw geometric picks remain result-bound.
  Automatic geometric rematching and persistent generated topology IDs are deferred. Missing owners stay unresolved.
- AN06: Use 14's generic persistence/resolution states and 07's semantic owner contract. This branch provides the
  named-feature resolver, without causing either foundation to import its consumers.
- AN07: Resolve parent/child attachment frames into explicit placement transforms for consumers 10/12. Keep normal
  flips/spin/local transformations reproducible; reject incompatible or unresolved references before source mutation.
- AN08: Support general OpenSCAD anchors/transforms and include a bounded BOSL2 adapter for verified standard/custom
  named anchors and basic parent-child placement against a pinned revision. No arbitrary library introspection or
  requirement to use BOSL2 for ordinary SCADMaxx anchors. Adapter operations must not introduce boolean/tag side effects.
- AN09: Deliberately persisted modeling anchors/attachments use 02 transactions and normal Save; merely clicking,
  inspecting or moving a temporary clipping origin must not author source or modify model CSG.
- AN10: Placement preference is a meaningful named relation, a suitable custom/BOSL2 anchor, a relative source
  transform, then an explicit absolute transform. Generated source stays readable and reflects the selected strategy.
- AN11: Keep provider catalogs, insertion menus, drawing layout and complete manipulation controllers outside this
  service. Expose stable values/results that consumers can use without importing one another's UI.
- AN12: Reusable reference declarations are annotated objects inside Part/Assembly module bodies and evaluate from
  their actual parameters. Definition anchors resolve separately for every instance. Explicit instance-owned
  declarations do not rewrite the shared definition. Storage remains ordinary .scad source.
- AN13: An attachment is a live directed placement relation. One placement relation per child is allowed; chains
  work, self/cyclic and multiply driven placement fail. No general assembly constraint solver is included.
- AN14: Mate is the default: coincident anchor origins and opposed facing directions. Align matches facing directions.
  Both support offset and spin; attachment translation/rotation preserves the child's existing size and shape.
- AN15: Apply successful attachment placement before preview/render/export consumers use the evaluated scene.
  CLI and GUI agree. A missing/invalid live relation cannot silently leave the child at its unrelated base position.
- AN16: Preserve semantic instance paths, Part-local geometry and source provenance when applying attachment placement.
  Definition export uses its defaults; instance export uses actual parameters/solved internal placement. Selection,
  hide/solo and inspection clipping do not alter the attachment graph or export target.
- AN17: Reference IDs are unique within their declared owner; labels are separate. Equal local IDs on different
  definitions/instances are valid. Reject ambiguous duplicate IDs within one owner, including instance additions
  colliding with inherited definition anchors. Do not create implicit anchor overrides.
- AN18: Source UI actions must preserve parametric expressions and communicate shared declaration scope. Use 02/06
  byte/revision/lifetime guards and one undo group; no automatic library edit, Save or hidden attachment authority.
- AN19: Inspect/show references, create a transient anchor from a current hit, explicitly save a fixed anchor and edit
  supported literal attachment offsets/spin. Expose resolver/placement operations for later 10/12 authoring controllers.
- AN20: Verify nonuniform/mirrored owner frames, reject singular/ill-conditioned frames where inversion is required,
  and make unavailable orientation/ownership explicit. No silent deformation or approximate fallback placement.

## Acceptance cases

1. Parent rotated/translated, child nonuniformly transformed: resolved point/orientation and placement round-trip agree.
2. Same definition instantiated twice: local named anchor resolves separately; one instance does not move the other.
3. Normal flip and spin produce the documented orientation without moving the anchor point unexpectedly.
4. Rename label versus delete owner: identity survives label change; deletion becomes unresolved, never nearest-match.
5. Change tessellation/boolean topology: a parametric named anchor remains defined; a saved fixed anchor retains its
   local coordinates without pretending to track a surface; a raw pick becomes Changed.
6. Plain OpenSCAD and a pinned BOSL2 fixture yield equivalent intended placement using their different source forms.
7. Persist/reopen through 14; undo an explicit source-backed attachment through 02; transient creation changes no source.

8. Change a named target parameter: a live chain moves on reevaluation, with identical preview/render/CLI placement.
   Cyclic or missing references produce a diagnostic and no usable incorrectly placed current result.
9. Solve against scaled/mirrored owners: placement preserves the child's pre-attachment world-space distances.
10. Two instances of a reusable Assembly get independent relative attachment graphs and equal local anchor IDs.

## Implementation specification

Use [the source contract](source-contract.md), [technical design](3_overall-plan.md), six phase files and the
[BOSL2 investigation](bosl2-investigation.md). 07/14's generic extension hooks must be verified owner prerequisites;
08 contributes concrete reference/attachment behavior without reverse dependencies. The BOSL2 probe verifies the
existing library's selected frame mapping; it does not prove unimplemented native Anchor/Attachment behavior.
