# Phase 3: expression-preserving edits, drafts and lifecycle undo

Covers DO-03, DO-06, DO-12 through DO-16 and the source-only limitation in DO-02.

1. Implement DesignSourceMap's bounded lossless field scanner and DesignEdits::prepare returning 02 requests.
   Verify annotation/assignment ownership and unique fixed keys; computed/helper/ambiguous definitions are read-only
   to numeric GUI edits. Add tests [design-source-edits] for comments, whitespace, Unicode, LF/CRLF, trailing commas,
   nested adjust, string keys, duplicate/computed keys, multiline strings and truncated/invalid source.
2. Implement DesignDocument transient/draft/commit/cancel/promotion lifecycle. Offset/pick/rotation updates touch only
   literal adjustment terms, preserving origin/normal/up expressions. Reject stale/read-only/closed editor targets.
   Add the generic consumer lifecycle adapter from the
   [scoped extension contract](../2026-10-03_00_source-first-cad-overview/semantic-extension-contract.md). Use a fake
   consumer to test two owners with the same local ID, promotion/rebinding by opaque key, owner destruction and
   source/lifecycle undo. Never resolve a consumer draft through the global document-ID map alone.
3. Add EditorUndoRegistry and the optional participant in SourceEditing transactions; refactor existing annotation
   container dispatch to the common registry. Append metadata and text to one native undo group after prevalidation.
4. Native TestDesignObjects: promote a referenced transient Section, undo/redo, rename, explicit delete and undo;
   interleave ordinary typing and annotation undo. One ID survives promotion/undo; manual deletion reports Missing.
   Failed transaction leaves source, lifecycle, register tokens and history unchanged. Clear history and close editor
   tests must release callbacks without use-after-free.
5. Test height/2 remains exact source text after offset drag, rotate, Save/reopen and parameter change. An expression
   in adjust.offset makes that numerical edit unavailable; it is never replaced with its current result.

Register TestDesignObjects and `OPENSCAD_DESIGN_OBJECT_TESTS_ONLY`. Run [design-source-edits], 02 transaction tests,
TestDesignObjects and annotation undo tests. Exit: expression/lifecycle preservation passes with actual undo events.
