# Phase 4: dependency removal and combined editor verification

Covers VM15 and integrated VM06/VM12/VM13. Use
[the verification contract](../../1_planning/2026-10-03_00_source-first-cad-overview/verification-contract.md).

1. Build the complete feature on its declared selected-source base, run [vim-engine] and native TestVimMode, then
   verify annotation undo and configurable application shortcuts with Vim disabled and enabled.
2. Verify implemented prerequisite 02: interleave typing, Vim ci/text/Escape, a SourceEditing transaction, annotation undo,
   u/Ctrl+R and dot. External transactions must end/invalidate insertion recording before their mutation; they must
   not enter the Vim journal or an open Vim undo group. The synchronous pre-group notification is mandatory; repair a
   missed entrypoint in its owning feature rather than relying on a notification after mutation has started.
3. Inspect the actual Vim compile/include/link closure and final binary imports using MSVC dumpbin /DEPENDENTS.
   Compare with the baseline: the Vim feature adds no GTK/GDK/GLib requirement, shim or runtime file. Search source
   for residual excluded dispatch and toolkit APIs, allowing only attribution text in origin/license documents.
4. Stage through the existing runtime deployment path and launch the extracted application. Verify setting, mode,
   one-Escape, basic editing and document commands without extra toolkit installation. Retain license materials.
5. Record selected upstream files/commit, local patch categories, real checks and known supported literal-search
   scope in completion notes. Do not claim full Vim compatibility or a runtime proof from dependency scanning alone.

Exit: bounded behavior, multi-document state, native UI and dependency removal are all verified. A failing toolkit,
selection, undo or focus invariant blocks completion; no extra dependency installation or scope reduction is implied.
