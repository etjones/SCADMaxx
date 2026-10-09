# Core Vim editing requirements

The four product questions were answered on 2026-10-03. This specification incorporates those answers; remaining
engine/port verification is an implementation phase gate, not an unanswered product preference. See [exploration](1_exploration.md).

## Scope and settings

- VM01: Provide a persistent application preference to enable/disable Vim editing, default off. It applies to source
  editors in existing and newly opened windows/tabs. Toggling changes input behavior without changing text, dirty state,
  undo history or document identity. Enable starts in Normal mode; disable restores ordinary editor behavior/caret.
- VM02: Implement the bounded core in [the command matrix](command-conformance.md): Normal/Insert/Visual editing,
  motions/counts, delete/change/yank, text objects, paste, undo/redo, dot repeat, search and basic document commands.
  Characterwise and linewise operations retain their distinct behavior. Unsupported commands cannot fall through as
  source text in Normal/Visual mode or partially execute a different command.
- VM03: With Vim enabled and the source editor focused, supported Vim bindings take priority over conflicting
  QScintilla/application shortcuts. There is no hybrid-priority setting. Unrelated application commands remain usable;
  other focused controls, the viewport and modal dialogs retain their ordinary keyboard behavior.
- VM04: The only new behavior setting is enable/disable. No custom key mappings, `.vimrc`, Vimscript, compatibility
  layer, plugin system or configurable priority rules. Future shortcut customization is deferred.
- VM05: Exclude macros, named/numbered register selection, Visual Block and substitution commands. Paste/yank still
  require an ordinary unnamed register with characterwise/linewise metadata; this is core operation state, not named
  register support. No persistent user command/configuration files are read.

## Editing and interaction

- VM06: Use the existing authoritative QScintilla buffer, source revision/fingerprint signals and undo stack. Each
  completed modifying command is a logical undo action; change-plus-insertion is one action. Search/navigation/yank
  do not modify text or create undo entries. No independent shadow source or whole-document replacement.
- VM07: In Insert mode, one Escape dismisses completion and call-tip UI, ends the insertion/change action and enters
  Normal mode. It must not accept a highlighted completion, insert Escape text or require a second press.
  Escape also cancels pending operators/counts, Visual selection or the search/Ex prompt without applying an edit.
- VM08: Show the current mode and appropriate caret. Normal mode operates on characters, with a valid empty-line
  position; Insert uses the normal insertion caret. Visual highlighting must show the characters the operator affects.
- VM09: Preserve Unicode, LF/CRLF, ordinary indentation/completion and read-only behavior. Motions and deletion must
  not split encoded characters. Account for QScintilla byte positions separately from displayed character columns.
- VM10: Counts compose with motions/operators. Dot repeats the last supported completed change, including inserted
  text, at the current position. Cancelled or failed commands must not replace the last valid repeat operation.
  Repetition uses current text; it is not replay of stale absolute source ranges.
- VM11: Pending input cannot migrate between documents. On focus/document change, close transient prompts and cancel
  incomplete commands; finish any insertion undo group without undoing typed text. Document-specific cursor/selection,
  search/repeat context must not accidentally apply another editor's state or retain a pointer to a closed editor.
- VM12: Typed, Vim, Customizer, annotation and programmatic edits share coherent undo/revision behavior. Non-Vim edits
  must not be captured as Vim insertion for later dot-repeat. They invalidate pending context that no longer applies.

## Document operations and failure behavior

- VM13: Route `:w`, `:q` and `:e` through existing Save, close-current-document and open/reload operations. Bind the
  operation to its originating editor. Keep Save As for untitled files, dirty-close/reload choices and external-file
  conflict handling. A cancelled/failed Save must not be reported as success or cause the document to close.
- VM14: Command/search feedback belongs to the editor's status/prompt surface, including not-found and unsupported
  commands. Do not silently execute excluded substitutions, force writes, shell commands or remappings through a
  reused engine. Enabling a vendor engine must not expose all its commands automatically.
- VM15: Patch the Geany engine for the existing Qt/QScintilla/MSVC/shared-dependency setup, preserving selected
  shortcut and annotation features. The Vim implementation must have no GTK or GLib build/runtime dependency,
  including through its selected engine code. Replace toolkit APIs with direct Qt/C++ code; no GTK/GLib emulation
  layer, runtime installation or second editor. Preserve upstream attribution/licenses and record local patches.
  Verify dependency removal as well as real QScintilla command and native focus/shortcut/popup behavior.

## Acceptance and completion

The command matrix defines representative expected outcomes; extend edge-case coverage without expanding scope.
Required native cases: enable/disable persistence, priority versus QAction shortcuts, one-Escape autocomplete,
multiple windows/tabs, dirty save/close/reload, annotation undo and interleaved programmatic source changes.
02 is now a prerequisite for its pre-group external-edit notification; verify mixed undo on that actual base.
The [technical plan](3_overall-plan.md) and four phases specify the port and proof cases. Runtime proof remains
unexecuted; [the port investigation](port-investigation.md) retains its evidence and risks.
