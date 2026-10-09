# Phase 3: Inspector navigation and guarded edit targets

Covers PV01/PV06/PV07/PV08 and integrated PV03/PV04 behavior.

1. Implement ProvenanceService::resolve and editableSpan. Validate all result/input/editor identities before exposing
   a mutable target; this method only prepares 02 preconditions and never edits source itself.
2. Register the source Inspector contribution and navigation actions. Reopen a library for navigation using normal
   document handling; never write it in the background. Display missing/ambiguous/stale provenance explicitly.
3. Add TestProvenance native class, CMake registration and `OPENSCAD_PROVENANCE_TESTS_ONLY`. Test preview picks on two
   instances, their definition versus call navigation, a final boolean face, dirty include/use edits, parse failure,
   changing tabs during navigation and closing the source document. Old spans cannot target another tab.
4. Build this feature without 07/08/10/12/14. Verify existing HTTP syntax queries, annotations and 02 undo/revision
   behavior. Record public records, supported mappings and final-geometry limits for consumer phases.

Run [source-provenance] and native TestProvenance using
[the verification contract](../../1_planning/2026-10-03_00_source-first-cad-overview/verification-contract.md). Exit: all ranges,
instance and stale-result fixtures pass; source navigation works; no unsupported graphical source edit is implied.
