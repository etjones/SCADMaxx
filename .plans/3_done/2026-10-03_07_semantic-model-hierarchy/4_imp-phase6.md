# Phase 6: regression, independent composition and handoff

Covers SH01-SH20. Requires all five functional phases and their recorded passing gates.

1. Run the complete semantic core/native suite and relevant object/Customizer, provenance, reference, source-edit,
   annotation, selection and export regressions. Confirm actual CTest discovery for all semantic labels; zero cases
   or a skipped required desktop GL case cannot be recorded as a pass. Record backend capability limits explicitly.
2. Verify the minimal 03/06/14 prerequisite composition builds with no 04/05/08/09/10/12 headers or linked objects.
   Review the feature delta against its recorded base and verify prerequisite changes stayed in their owning branches.
   The generic inspection contract belongs to 03; its follow-up must be included in the frozen base manifest.
3. Rehearse the feature-only delta in an isolated requested verification composition with earlier ready features.
   With 04 present, clip the bracket pair and a hollow Part; hide/solo while clipped, disable/re-enable clipping,
   select retained rear surfaces and check exact instance paths. Hide/solo never changes exported geometry. Test
   source changes/tab close while either preparation job is pending and resource teardown after repeated toggles.
4. With 05 present, test Vim insert -> scoped numeric source edit -> undo/redo; check one external source transaction
   after insertion is closed. Preserve navigation/annotations/shortcuts/themes and ordinary unannotated models.
5. Check packaged shader/UI resources in the feature's development staging area, using the existing build profile and
   shared vcpkg. Do not install dependencies, enable the selected stack, promote, push or publish a new distribution.
   Record integration checks blocked by an unavailable optional branch as deferred; never claim the combined behavior
   verified from a fake-provider test. Feature-local completion and integrated-delivery acceptance are separate.
6. Write 5_post-implementation-notes.md with actual base/head or uncommitted patch/hash identity, every requirement's
   evidence, passed commands/counts, backend/driver versions, known limits, exact touched shared APIs, independent-base
   result, composition results and pending delivery obligations. Follow the workspace local-handoff runbook.

Verification commands are the [shared native contract](../../1_planning/2026-10-03_00_source-first-cad-overview/verification-contract.md).
Labels: semantic-grammar, semantic-declarations, semantic-evaluation, semantic-partition, semantic-targets,
semantic-export, semantic-tree, semantic-visibility and semantic-source-edits. Native selector:
OPENSCAD_SEMANTIC_TESTS_ONLY. Test discovery and execution logs must identify the actual built inputs.

Acceptance matrix: definitions/no geometry; explicit instancing; lexical defaults/overrides; stable paths and collisions;
finished-Part booleans; nested/repeated/library ownership; ordinary/mixed models; exact current selection; independent
visibility/solo; local/placed/default export; source edits/undo; reference missing/stale states; clipping composition.
Do not call this feature complete if a required behavior is merely a UI placeholder or a guessed ownership mapping.
