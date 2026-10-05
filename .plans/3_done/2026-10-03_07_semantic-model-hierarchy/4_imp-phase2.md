# Phase 2: evaluated instances, parameters and geometry ownership

Covers SH02-SH06/SH10-SH13/SH18/SH19. Requires phase 1's metadata and owned definition index.

1. Implement SemanticCollector/Scene and session RAII stack around native ModuleInstantiation/UserModule evaluation.
   Resolve callable once, evaluate Component metadata once, require a marked target, prohibit Components inside Parts
   and record the returned GroupNode. Exceptions must pop the stack and leave no installable partial snapshot.
2. Add optional binding observation to Parameters::parse/UserModuleContext without changing native matching/default
   rules. Clone final bound Values and capture winning argument/default source spans and ambiguity. Use 06 invocation
   records to count every execution of a call site, including hidden/root-excluded instances, for future edit guards.
3. Build full escaped paths, sibling uniqueness checks and parent/definition links. Traverse the final evaluated tree
   to accumulate local-to-parent/world transforms, prune root-excluded display entries and map nodes to deepest Parts.
   Do not use node indices/evaluation order for durable IDs or invert singular matrices to recover local placement.
4. Validate boundary-crossing operations and Assembly anonymous output. Keep the normal CSG tree untouched; identify
   maximal residual roots and finished Part roots for later mesh/export jobs. Collect diagnostics at operator/call
   spans. Invalid semantic topology cannot replace a current usable index; stale UI must be explicit.
5. Add SemanticCollector_test.cc / SemanticParameters_test.cc / SemanticScene_test.cc, tagged [semantic-evaluation]
   and [semantic-partition]. Build the CLI and GUI using the same core collector.
6. Implement currentScope and the finalization/placement-pass hooks from the
   [extension contract](../../1_planning/2026-10-03_00_source-first-cad-overview/semantic-extension-contract.md). Test a fake rigid
   correction on one repeated Component: consistent CLI/GUI/default-job dispatch once, updated provenance, preserved
   Part-local root and atomic failure. No Anchor/Attachment implementation or imports belong in this owner.

Run the accepted bracket/pair and nested rack fixtures. Assert exact IDs, parent paths, node owners, parameter Values,
origins and source spans: /pair/right width 45, nested rack has eight Parts and four pair Assemblies. Reorder loop keys
without path changes; add/delete/duplicate keys; keys containing / and ~ round-trip through escaping. Rename labels
without ID changes. Ordinary models yield no inferred Parts; mixed geometry produces a residual partition.

Compare finished Part geometry/bounds with an equivalent unannotated module call through GeometryEvaluator. Test
rotations, mirrors, nonuniform and singular placement, nested helper calls, positional/named/default arguments,
duplicate native arguments, expression defaults and arguments with observable echo/rands evaluation. Capturing values
must not evaluate expressions twice. An if(false) Component and disabled * call are absent. Test include/use lexical
defaults and two libraries with the same module name but distinct IDs; actual native callable resolution must win.

Boundary fixtures: difference wholly inside a Part succeeds; difference/explicit union/hull enclosing Components
diagnoses unsupported composition; loose geometry in an Assembly fails; ordinary unannotated equivalents retain
native behavior. Test ! within a Part, %/# roles and exceptions during nested instantiation.

Exit: source geometry equivalence, explicit IDs and lexical argument binding are proven by discovered tests. Do not
continue to UI/export if duplicate handling, local geometry or source ownership depends on a guessed node mapping.
