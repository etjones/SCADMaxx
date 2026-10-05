# Phase 1: annotated modules and declaration identity

Covers SH01/SH02/SH10/SH11/SH19/SH20. Start only after verified 03/06/14, selected OEP8/Customizer and 03's
[presentation refinement](../../1_planning/2026-10-03_00_source-first-cad-overview/inspection-presentation-contract.md).
Record actual base, prerequisite manifests, checkout-local instructions and clean/occupied worktree status.

1. Add SemanticKinds and immutable annotation metadata to UserModule/ModuleInstantiation. Refactor parser.y's
   module declaration production so annotated/unannotated paths share the same scope pushes/pops. Add the Component
   annotation on direct calls; extend 06 source ranges to include attributes, definition parameters and call delimiters.
2. Require 14's refined host enum/KindHandler/DeclarationKey in its verified owner handoff; register semantic kinds
   through those hooks. Keep valid Section/View syntax. Verify assignment edit/create/promote APIs reject module/call
   hosts; no partial body-as-object mutation. Missing hooks are a prerequisite failure, not a private 07 copy.
3. Implement syntactic type dispatch and exact field validation. Module id/label must be string literals; Component
   id/label may be caller expressions. Reject unknown kinds, duplicate fields, wrong hosts, local semantic definitions,
   supplied Component children and module redeclarations with semantic metadata. Ordinary helpers stay legal.
4. Add definition discovery over captured root/include/use ASTs. Deduplicate the same source occurrence; reject distinct
   definitions sharing IDs across files/kinds. Register definition metadata without executing unused library scopes
   or bodies. Keep source/AST ownership in the retained evaluation backing; no global pointer-keyed registry.
5. Add SemanticKinds_test.cc and fixtures under testdata/scad/semantic. Register [semantic-grammar] and
   [semantic-declarations] in real CMake discovery. Implement a scoped optional collector with no semantic input
   producing an empty result and ordinary CSG unchanged. Runtime instance collection follows in phase 2.

Required fixtures: accepted bracket/pair source parses; definition alone emits no geometry; ordinary object and
Customizer annotations still parse/evaluate; mixed Section/View/module metadata; variables named Part/Component
cannot change type dispatch; CRLF/Unicode/comment ranges slice exact bytes. Root/include/use definition inventory,
same library reached twice, colliding IDs with a Section, local definition, wrong type string, missing/empty ID,
unknown field, semantic redefinition and invalid annotation host each have expected source diagnostics.
An unused use-library containing echo and top-level geometry must not execute either during metadata discovery.

Run [semantic-grammar], [semantic-declarations], existing parser/object/Customizer tests and 14 typed-declaration
tests with the shared verification commands. Check Bison diagnostics against the recorded base. Exit only with
unchanged ordinary grammar behavior, zero new unresolved conflicts and exact source ranges. Stop if discovery needs
to run a body just to get its identity; implement the specified literal-ID route instead.
