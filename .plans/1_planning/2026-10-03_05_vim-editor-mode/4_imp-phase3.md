# Phase 3: Qt priority, one Escape, document commands and preference

Covers VM01/VM03/VM04/VM07/VM11/VM13/VM14.

1. Construct VimScintilla in ScintillaEditor and wire the controller before existing event filters. Implement pure
   ShortcutOverride claiming, input-origin guards, popup Escape and focus/tab teardown according to the design.
2. Implement literal search and bounded Ex parser in VimPrompt. Connect document-bound host callbacks to the actual
   TabManager save/open/close/reload entrypoints, retaining Save As/conflict/dirty-close behavior.
3. Add the single persistent enable setting, Preferences checkbox, mode display/caret restore and command help.
   Enabling/disabling updates all windows without touching source/undo. Preserve AltGr/IME behavior in Insert.
4. Add TestVimMode native class, CMake/runner registration and `OPENSCAD_VIM_TESTS_ONLY`. Implement VI01-VI08, plus
   competing QAction Ctrl+R, completion/call-tip one-Escape, keypad arrows, quoted Unicode paths with spaces, failed
   Save, pending prompt's editor closing, modal field focus and a QAction source edit while in Insert.

Run [vim-engine] and native TestVimMode on Windows. Exit: real Qt dispatch meets focus/priority/popup requirements;
direct Engine calls alone cannot pass this phase. Text fields outside the source editor retain normal bindings.
