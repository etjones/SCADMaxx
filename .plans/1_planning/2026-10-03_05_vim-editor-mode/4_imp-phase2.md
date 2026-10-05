# Phase 2: command conformance, Unicode and repeat

Covers VM02/VM05/VM06/VM08/VM09/VM10/VM12. Depends on phase 1's real widget bridge.

1. Finish only the allowlisted command tables and native range/word/text-object behavior. Implement the unnamed
   register with linewise metadata. Validate counts/resources before edits; no partial unsupported command dispatch.
2. Implement inclusive Visual and complete-line VisualLine display/ranges, EOL/empty-file clamping and mirrored
   selection direction. Add read-only checks at all mutation entrypoints.
3. Implement native undo groups and repeat journal with input origins, before-change invalidation and dry-run replay.
   Backspace/completion/paste/IME edits inside owned Insert must replay their resulting edits, not physical key events.
4. Run every VC01-VC17 fixture; add each supported delimiter in both directions/nested/unclosed form, count overflow,
   Unicode/non-BMP/combining text, LF/CRLF, final line without EOL, folded j/k targets and long insertion beyond the
   old 131072-byte buffer. Keep no fixed truncating repeat buffer.
5. Add a change-plus-insert/undo/redo sequence interleaved with an annotation container undo and external insertion.
   Assert external text is absent from dot replay and each logical change has one native undo action.

Run [vim-engine]. Exit: complete bounded command behavior passes with expected text, caret, mode, register kind,
revision and undo outcomes. Do not loosen fixtures merely to retain vendor differences; use the documented scope.
