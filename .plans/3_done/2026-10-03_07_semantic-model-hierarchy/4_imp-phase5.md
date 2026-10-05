# Phase 5: selection-driven Customizer and source transactions

Covers SH06-SH09/SH12/SH19. Requires current semantic snapshots, 02 source-edit handoff and 06 validated spans.

1. Add SemanticParameterPanel to the existing Customizer dock, selected-instance/defaults/all-parameters navigation
   and visible origin/expression/owner. All parameters is a grouped inspection view; existing global Customizer remains
   separately available. Reuse value widgets through an adapter; never store instance values in global preset JSON.
2. Implement editable-literal classification and every guard in the overall plan: exact open writable owner, fresh
   snapshot, unambiguous native binding and unique call occurrence across the full invocation map. Expressions,
   repeated call sites and unsupported Values are read-only with precise source navigation/reason.
3. Implement SemanticSourceEdits for literal expression replacement, omitted named-argument insertion and safe named
   override removal. Use token/span boundaries, preserve all unrelated bytes/comments/newlines, reject ambiguous
   trivia. Default edits are a deliberate separate action with visible affected scope. Never implicitly open/save or
   patch a library. Do not make per-instance override dictionaries or flatten expressions.
4. Apply via 02 EditRequest and synchronous prepareExternalEdit before the undo group. On success invalidate controls
   and use normal reevaluation/selection rebinding. On rejected guards change neither source nor undo history.
5. Add [semantic-source-edits] unit cases and native panel/undo tests to TestSemanticHierarchy. Keep UI state keyed
   by document/result/semantic path, not raw ParameterObject pointers surviving widget rebuilds.

Exact fixtures: bracket() inserts width = 40 for a unique call; bracket(30) replaces only 30; bracket(width = 30)
updates that span; comment-heavy/multiline calls preserve comments; width + 10 remains an expression and cannot be
numerically overwritten. UTF-8 names/strings, CRLF/BOM, empty argument lists, trailing commas and unsupported removal
trivia have explicit expected byte results or rejection. Undo/redo reproduces original bytes in one action.

Nested rack fixture: /rack-a width is editable, its shared pair call's literal gap is not single-instance editable,
and child width expressions remain read-only. Two root instances of one Assembly make its internal call shared even
when one root is hidden or root-excluded. Definition default edit changes only default-inheriting uses; literal
overrides remain. Global Customizer changes reevaluate and refresh scoped values without persisting a second copy.

Native cases: tab switch/revision/include change before apply, stale widgets after rebuild, closed/read-only library,
explicitly opened library default editing, external edit/annotation undo interleaving, selection and source jump sync.
On a composition with 05, repeat the external-edit case during a Vim insert session and verify separate undo groups;
minimal-base tests use 02's actual synchronous hook without a 05 dependency.

Run [semantic-source-edits], native semantic tests and affected 02/06/Customizer regressions. Exit only when no
single-instance action can modify a shared call accidentally, no expression is flattened, and rejected edits leave
both bytes and undo history unchanged. Do not expand this phase into general source refactoring from feature 10.
