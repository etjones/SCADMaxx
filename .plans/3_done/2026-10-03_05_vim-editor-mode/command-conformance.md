# Core command and acceptance matrix

This makes the accepted scope in [requirements](2_requirements.md) concrete. It is the target behavior for the port,
not a claim that the candidate engine already passes. No remapping/configuration language is part of this matrix.

## Required command families

| Family | Required keys / behavior |
| --- | --- |
| Mode entry | i/a/I/A, o/O; Escape to Normal; v characterwise Visual and V linewise Visual. |
| Basic movement | h/j/k/l and arrows; w/b/e; 0/^/$; gg/G with line counts. |
| Character find | f/F/t/T followed by a character; ; repeats the find and , reverses it. |
| Counts | Counted motions/operators; operator and motion counts compose, e.g. 2d3w. |
| Operators | d/c/y with supported motions or text objects; dd/cc/yy and their counts; x for character deletion. |
| Text objects | Inner/around word; inner/around paired parentheses, square/curly brackets, single/double quotes. |
| Paste | p/P, counted paste, unnamed characterwise or linewise contents. |
| History | u undo, Ctrl+R redo, . repeat the last supported completed change. |
| Search | / forward, ? backward; Enter executes, Escape cancels; n/N repeat/reverse. |
| Documents | :w Save; :q close current document; :e reload current file; :e followed by a path opens that file. |

Visual mode uses supported motions and d/c/y. Text objects apply after an operator or in Visual mode, not as standalone
Normal-mode commands. Full Replace mode, Visual Block, macros, named/numbered register selection, substitutions,
marks, broad Ex commands, force forms, shell escapes, Vimscript, plugins and custom mappings are outside this version.
Do not expose extra vendor commands just because they compile. Ordinary editing menus remain available.

The technical plan selects case-sensitive literal search with forward/backward, wrapping, not-found and repeat.
Regular expressions are not part of this bounded search surface; no user-selectable regex dialect is introduced.

The document command prompt recognizes exactly the listed short command names; no command abbreviation engine is
needed. File paths may contain spaces and Unicode; use the existing document-open machinery and define/test command
argument decoding in the technical plan. :w on an untitled file invokes Save As. :e with no current filename reports that
reload is unavailable. No force variant bypasses save/conflict protection.

## Text fixtures

All cases start in Normal mode unless specified. Text is quoted with literal `\n`/`\r\n` notation for line endings.
Caret coordinates are one-based (line, Unicode character column), independent of Scintilla byte positions. Reset
buffer, history and unnamed register between cases. Bracketed key names represent one key event, not typed text.

| ID | Input / caret | Keys | Expected text / caret / mode |
| --- | --- | --- | --- |
| VC01 | `one two three`, (1,1) | `w` | Same text; (1,5); Normal; no undo entry. |
| VC02 | `one two three`, (1,5) | `e`, then `b` | (1,7), then (1,5); text unchanged. |
| VC03 | `  cube();`, (1,6) | `0`, `^`, `$` | Columns 1, 3, 9 respectively; text unchanged. |
| VC04 | `one\n  two\nthree`, (3,3) | `gg`, `2G`, `G` | (1,1), (2,3), (3,1); text unchanged. |
| VC05 | `abcabc`, (1,1) | `2fc` | Same text; (1,6); Normal. |
| VC06 | `abc;def;`, (1,1) | `2t;` | Same text; (1,7); Normal. |
| VC07 | `one two three four five six seven`, (1,1) | `2d3w` | `seven`; (1,1); one undo restores original. |
| VC08 | `a\nb\nc\n`, (2,1) | `dd` | `a\nc\n`; (2,1); unnamed register is linewise `b\n`. |
| VC09 | `a\nb\nc\n`, (2,1) | `yyp` | `a\nb\nb\nc\n`; (3,1); only paste adds an undo entry. |
| VC10 | `one two`, (1,2) | `diw` | ` two`; (1,1); one undo restores original. |
| VC11 | `cube([1, 2, 3]);`, (1,9) | `ci[9,9,9[Esc]` | `cube([9,9,9]);`; (1,11); Normal; change plus insertion is one undo. |
| VC12 | `abcd`, (1,2) | `vld` | `ad`; (1,2); Normal; highlight included both b and c before deletion. |
| VC13 | `one two three`, (1,1) | `cwX[Esc]w.` | `X X three`; (1,3); Normal. One u restores `X two three`; next u restores original. |
| VC14 | `one two`, (1,1) | `dw`, `u`, `[Ctrl+R]` | `two`, original, `two`; ordinary undo/redo ordering retained. |
| VC15 | `one two one`, (1,1) | `/two[Enter]`, `n`, `?[Esc]` | First two finish at (1,5) with wrap feedback as needed; cancelled prompt leaves it there. |
| VC16 | `one two`, (1,1) | `2d[Esc]` | Original text/caret, Normal; no new undo or repeat entry. |
| VC17 | `é😀x`, (1,1) | `l`, `x` | `éx`; (1,2); one undo restores the complete non-BMP character. |

Use the [Vim motion reference](https://vimhelp.org/motion.txt.html) for count composition, line/character motions
and text-object boundary semantics, and [change reference](https://vimhelp.org/change.txt.html) for supported editing
commands. The fixtures above are project-specific acceptance examples. Correct a fixture if a verified reference
contradicts it; do not silently change the product behavior to accommodate an adapter bug.

Expand tests for every supported family: backward f/F/t/T, all paired text objects and nesting, forward/backward
Visual selection, cc and insert entry variants, count overflow, empty line/file, end-of-line/file, LF/CRLF, folded
lines, tabs and combining characters. Check malformed/unterminated text objects leave source unchanged.

## Native integration cases

- VI01 Settings: enable/disable with a dirty buffer and existing undo history; restart; open another tab/window.
  Text/history survive, the preference persists and all source editors obey it. No mapping/priority settings appear.
- VI02 Focus/priority: supported Vim binding wins even when a QAction has the same shortcut. Focus a dialog field,
  search field or viewport and confirm its normal behavior. Application compile/render commands remain accessible.
- VI03 Escape: show completion and separately a call-tip while inserting; one Escape dismisses UI and enters Normal.
  A highlighted completion is not accepted. Verify with real Qt event dispatch, not direct engine calls alone.
- VI04 Multi-document: start an operator/count/search in A, switch to B and type. Nothing pending from A edits B.
  Close A while a prompt is pending. There is no dangling pointer or later command applied to a different document.
- VI05 Undo: type, make an annotation change, use Vim change/insert, then apply a programmatic source transaction.
  Undo/redo follows the actual sequence. Non-Vim insertion is never recorded as text for Vim's next dot repeat.
- VI06 Save/close/reload: :w handles untitled Save As and external conflict; :q targets only its source document;
  cancelled dirty close/reload preserves it; :e opens a Unicode path with spaces. Failed Save remains visibly failed.
- VI07 Exclusions: macros/register selection/block mode/substitution/remapping are not enabled by vendor defaults.
  Unsupported command feedback leaves source and undo unchanged; no shell/configuration file is executed.
- VI08 Read-only: navigation/search work; operators/insert/paste cannot modify text or corrupt undo/repeat state.
- VI09 Dependencies: compile the patched engine using only the existing Qt/C++/QScintilla setup. Inspect the Vim
  target's include/link closure and binary imports; it must neither require GTK/GLib nor add their runtime DLLs.
  Run the extracted application to verify the feature works without any added toolkit installation.

Record real test discovery, commands, fixture results and native interaction evidence under the shared
[handoff standard](../../1_planning/2026-10-03_00_source-first-cad-overview/implementation-handoff.md). Zero discovered tests is failure.
