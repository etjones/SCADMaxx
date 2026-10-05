# Phase 4: saved views, document lifecycle and consumer handoff

Covers DO-08, DO-14 through DO-20 and integrated requirements.

1. Refactor SavedViews camera entries to the shared View model, retaining distinct personal backing. Add source-backed
   view enumeration and Inspector contribution through 03, with Apply/Promote/Rename/Delete and clear backing status.
   Remove duplicated source-design authority; no importer, migration or automatic deletion of old user sidecars.
2. Verify camera pose roundtrip and parametric fit bounds, untitled creation/Save As, Save a Copy, reload, dirty close,
   read-only includes and external source/sidecar conflict. A canceled save keeps dirty source and object identity.
3. Exercise dependency closure across two open included files: successful saves, second save failure, cancel and
   retry. Report exact per-document outcomes. No hidden write to a closed file and no false atomic-save success.
4. Build/test without 04/06/07/08/09; run CLI declaration fixtures, [design-objects], [design-references],
   [design-source-edits], native TestDesignObjects, annotation/HTTP saved-view regressions and 02 source-save cases.
5. Record schemas/APIs, current source-only edit limits, actual test results and base/head handoff. Downstream 04/09
   consume these records; they cannot create a private Section store or runtime type hierarchy.

Use [the verification contract](../2026-10-03_00_source-first-cad-overview/verification-contract.md). Exit: all source,
identity, camera, undo and conflict acceptance cases pass; shared contracts are ready for dependent implementation.
