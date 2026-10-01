# Phase 3 — Parse isolation and structured syntax inspection

Status: implemented and validated; source commit `8fa5edcbf`. See implementation evidence and baseline test limitation.

## Prototype before expansion

The inspected parser uses shared lexer/parser globals, SourceFile ownership and diagnostic state. Prove a parse-only
call can restore native state on success, malformed source and exceptions before exposing it to HTTP. Serialize it
with normal compilation; no HTTP worker may call the parser. Do not mistake queue timeout for interruptibility.

## Implementation

1. Build a bounded RAII parse service consuming a retained source snapshot, not live text at execution time. Recheck
   document/server lifetime; the immutable snapshot remains valid as historical input even if editor text has advanced.
   Record that relationship in the outcome. Reject expired snapshots rather than recapture silently.
2. Audit parser globals, lexer cleanup, path/base handling, warning state and output-handler restoration. Isolate parse
   results from `MainWindow::rootFile`, ModuleCache and renderer roots. Add narrow native refactoring only where needed
   for cleanup or bounded parsing; validate it against normal compiler fixtures.
3. Add bounded dependency resolution using native lookup rules. Include/use syntax can be parsed independently under
   the same gate without instantiating modules or mutating shared dependency caches. Track visited paths/cycles and
   captured content. Preserve unknown dynamic-import provenance; do not create imported geometry.
4. Implement a typed syntax visitor over SourceFile, LocalScope, definitions, assignments, ModuleInstantiation and
   expressions. Add const traversal accessors for retained source order where necessary. Preserve semantic child roles
   and original locations; unsupported constructs have explicit fallback kind/text, never parsed dump-string guesses.
5. Produce detached syntax DTOs with fresh `tree_id` and local IDs. Enforce node/depth/string/value budgets while
   traversing, with explicit truncation. Use an iterative walk where depth could otherwise exhaust the C++ stack.
6. Normalize native spans into documented public locations using Unicode/CRLF tests. Where exact conversion is not
   justified, return unavailable location instead of inaccurate ranges. Syntax expressions remain syntax values.
7. Wire parse jobs, tree/node/child-page routes and expiry. Failures publish their own diagnostics and no new tree;
   cached older trees remain separately identified. Pagination tokens bind to tree/parent/order and cannot cross trees.

## Validation

- Parse valid/invalid roots and nested includes, use libraries, missing files, cycles, Unicode identifiers/comments,
  multiline expressions, duplicate definitions, loops, conditionals, functions and module parameters/defaults.
- Compare structural fixtures and selected human-readable dump output; test source order separately from lookup maps.
- Run ordinary preview before and after parse-only success/failure; compare model result and diagnostics. Confirm
  parse-only invokes no evaluation, file save, editor replacement, camera movement or undo reset.
- Interleave native compile requests, source changes, Stop and document closure. Verify exclusive parser access,
  scoped restoration and no publication into replacement targets.
- Test large/deep input, dependency and output limits, page boundaries, evicted snapshots, stale cursors, duplicate
  request IDs and cooperative cancellation. Record actual worst-case GUI interruption on bounded fixtures.

## Exit evidence and fallback boundary

The mandatory result is useful structured syntax plus safe isolated parsing, not merely a text AST dump. Retain native
state-restoration tests and bounded-load timing. If safety requires more native parser work, document and finish that
repair within scope before advertising parse support; do not bypass via evaluation, external process or silent omission.
Phase 4 reuses the public node/value schema and retention machinery, not live parser pointers.
