# Phase 2: Source inventory and geometry edits

Requirements: IN03, IN07-11, IN13-15, IN18. Read 3_overall-plan.md and both source/preview contracts first.

1. Implement SourceInventory over retained native AST/06 span records. Record exact scopes, direct geometry runs,
   imports, effective identifiers, source-frame provenance and invocation coverage. Scanner handles trivia only.
2. Implement target enumeration and explicit shared definition scope. Use 07 ownership for Part bodies. Ordinary
   statements require unique source effects and known positive CSG role/frame. Show an unsupported reason otherwise.
3. Implement exact byte splice planning per source-edit-contract.md: wraps, trailing comments, BOM/EOL, imports,
   collision-free helpers and one-document expected slices. Keep source untouched in this phase.
4. Apply patches to a byte copy, natively parse and evaluate the candidate through phase 1. Add target-specific
   intersection/removal checking for subtractive recipes using native geometry; do not import feature 15.
5. Add deterministic golden files plus native geometry assertions and rejection fixtures. Wire core tests into
   actual CMake sources/globs; no test is considered present until ctest -N discovers it.

Checks: insertion-source label. ordinary-cut retains bounds [0,0,0]..[20,20,10] and removes cylinder volume;
ordinary-add has bounds [0,0,0]..[20,20,40]. Existing width expression stays byte-identical.
Cover two direct solids cut together, nested difference, UTF-8/BOM/CRLF, comment after the final semicolon,
declaration interleaving rejected, duplicate-start patch coalescing, included target with original root evaluation,
read-only/unopened/vendor source rejected, repeated loop call rejected and explicit enclosing unique target.
NoIntersection leaves source unchanged and disables Commit. Provider/library/import conflicts return diagnostics.
A changed width between capture and candidate evaluation must never authorize a rewrite at old byte offsets.

Exit: accepted forms yield correct native geometry and preserve all untouched byte ranges. Unsupported forms have
specific reasons; no regex-generated approximate edit. If wrapping changes lexical binding/geometry unexpectedly,
stop and repair the eligibility rule or algorithm before adding palette UI.

Use the overview verification-contract.md with the actual isolated build path: build OpenSCADExe and
OpenSCADUnitTests, run ctest -N, then the named CTest labels. Native cases use the registered GUI harness selector.
No zero-test result counts as passing; retain commands, discovery and logs in the feature run directory.
