# Phase 4: model tree, selection and composable inspection

Covers SH05/SH12/SH15/SH16/SH18/SH20. Requires targets and verified 03 inspection-presentation APIs.

1. Implement ModelTreeModel/Dock and SemanticController, separate instance/definition targets, empty/stale diagnostics,
   ordinary Model and mixed Other geometry rows. Use typed model roles containing IDs plus current result, not AST
   pointers in QVariant. Implement hierarchy actions with applicable states; no drawing/BOM/anchor placeholders.
2. Implement SemanticMeshJob from phase 2's partition, preserving finished Part meshes, transforms, color and roles.
   Publish priority-100 provider to 03 only for a valid semantic scene. Distinct actual parameterizations cannot share
   meshes solely because their definition ID matches. Geometry work never runs on camera/eye/solo changes.
3. Implement per-document hidden paths and solo, ancestor visibility and masks. Keep independent selection. Preserve
   keys through valid reevaluation and prune missing paths. Clearing solo restores eyes. Disabled preparation/failure
   controls must communicate why; do not pretend a hidden object disappeared before the provider is ready.
4. Map semantic draw IDs to deepest Parts and select parent Assemblies from tree. Rebind ObjectKeys after renderer
   generations change; retain path selection separately. Highlight/fit use the shared overlay/target APIs. Implement
   call/definition navigation via 06 and a semantic Inspector contribution; distinguish ambiguous ordinary merged hits.
5. Add transient Create Section action through 14 for valid target/frame/bounds. Register native TestSemanticHierarchy
   in guitests.cc with OPENSCAD_SEMANTIC_TESTS_ONLY, and [semantic-tree] / [semantic-visibility] unit labels.

Unit cases: exact accepted hierarchy/Definitions, ordinary model one row, mixed residual row, empty Part, duplicate
errors, source deletion/reorder, hidden parent/child, solo and restoring eyes, two document sessions, stale state.

Native desktop GL cases: pick two instances and assert exact paths; pick a cut wall and verify correct finished Part;
occluded/mirrored/transformed instance, Assembly highlight, hidden object never hit, Other geometry has no persistent
semantic target. Check eye/solo/source text independence, navigation cube/orbit/tool arbitration and Inspector sync.
Instrument 100 mask updates: zero new source evaluations, boolean jobs or identical mesh uploads after preparation.

On the minimal prerequisite base use a test-only mesh effect (identity/tint) to prove 03 composes color and pick passes
without linking 04. Cancel provider work, change input, switch/close tabs, destroy registration owners and complete an
old job afterward: it must never replace the current display. Test ordinary OpenCSG/Manifold/convertible CGAL inputs;
unsupported diagnostic/2D/conversion states retain ordinary rendering with explicit semantic inspection limitations.

Run named unit labels, native TestSemanticHierarchy and TestSelection. Exit: actual display, hit identity, masks and
lifetime guards agree. Final merged output with no mapping cannot be declared a semantic hit by proximity heuristics.
