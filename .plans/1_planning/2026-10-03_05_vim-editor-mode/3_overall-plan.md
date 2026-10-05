# Vim mode: Qt/QScintilla port design

Status: concrete port and phase specification, 2026-10-03; no port has yet been compiled. Product scope is settled.
Read [requirements](2_requirements.md), [command fixtures](command-conformance.md) and
[source investigation](port-investigation.md). Branch `feature/vim-editor-mode`; selected shortcuts/annotations base.
02 is a prerequisite for the synchronous external-edit boundary before another undo group opens. The first phase verifies the
port boundary; a failed assumption returns with evidence rather than letting Sol choose a different engine.

## Pinned adaptation and file set

Adapt Geany plugins vimode at `8d1838869cfdebbeb8469193119839f7ffae0052`. The pinned Makefile, command runner,
parameters, context, movement, text-object, edit, undo, mode-switch and utility sources were read through GitHub's API.
They use a small Scintilla message vocabulary but expose GTK/GDK/GLib and process-global state. This is a patched
source port, not linking the original plugin or implementing GTK-shaped substitute APIs.

Vendor adapted C++ under `src/gui/vim/engine/`, preserving per-file upstream notices and a LICENSE/origin record with
the pinned commit and source-to-adapted-file mapping. CMake uses an explicit file list, not a glob of upstream sources.

| Upstream source | Adapted responsibility |
| --- | --- |
| vi.c/.h, context.h | Engine.cc/.h, Context.h: per-editor state machine, dispatch, notifications; remove globals and settings beyond enable. |
| cmd-runner.c/.h, cmd-params.c/.h | CommandRunner.cc/.h, CommandParams.h: allowlisted tables, counts, operator/motion ranges. |
| cmds/motion.c/.h, motion-word.c/.h | Motion.cc/.h, WordMotion.cc/.h: only the command-matrix motions and find/repeat. |
| cmds/txtobjs.c/.h | TextObjects.cc/.h: word, parentheses/brackets/braces, single/double quotes; omit angle/backtick/WORD extensions. |
| cmds/edit.c/.h, changemode.c/.h, undo.c/.h | Edit.cc/.h, Modes.cc/.h, Undo.cc/.h: accepted edits and native history only. |
| sci.c/.h, utils.c/.h | ScintillaAccess.cc/.h and selected Search.cc/.h helpers, using real Qt/C++ ownership. |
| keypress.c/.h | Replace GDK translation with native QtKey.cc/.h; retain count/key-sequence semantics. |

Do not vendor backends/backend-geany.c, backend-viw.c, GTK excmd-prompt, generic excmd-runner/cmds/excmds, fold commands
or broad special-command tables. Replace search/Ex prompt handling with the bounded Qt host below. Remove excluded
substitution/Replace/case-conversion/indent/macro/register/mark/settings branches and their helpers from selected files.
Do not merely hide a menu while leaving an excluded command executable.

Replace GSList with owned std::vector/deque key sequences, allocated strings with QByteArray/QString, booleans with
bool and count arithmetic with checked uint64_t. Replace position/line fields with Scintilla pointer-sized signed
types (sptr_t/Sci_Position from the installed headers), never Win64 long/int casts. Use SendScintilla pointer-sized
overloads. Replace Unicode predicates with Qt Unicode classification; byte positions remain distinct from QString
indices. No g_*, gtk_*, gdk_* replacement namespace, shim headers or toolkit link libraries.

## Host API and ownership

New host files `src/gui/vim/VimEditorController.{h,cc}`, `VimScintilla.{h,cc}`, `VimPrompt.{h,cc}` and tests.
ScintillaEditor constructs VimScintilla, a small QsciScintilla subclass that can wrap actual native input dispatch.
It remains the same editor/document, with the same Scintilla buffer, lexer, completion and undo system.

```cpp
enum class Mode { Normal, Insert, VisualChar, VisualLine };
struct Key { int qtKey; Qt::KeyboardModifiers modifiers; QString text; };
enum class InputResult { Consumed, PassToEditor, PassToApplication };
enum class HostCommand { Save, Close, Reload, Open };
enum class HostResult { Success, Cancelled, Failed };
struct HostRequest { HostCommand command; QString path; };
class Engine {
public:
  InputResult key(const Key&);
  bool claimsShortcut(const Key&) const; // pure, no buffer/state mutation
  void cancelPending();
  void beforeExternalMutation();
  void setEnabled(bool);
  Mode mode() const;
};
```

Each controller owns one Engine/Context and a QPointer to its originating ScintillaEditor. Context owns mode,
pending keys/operator/count, character-find state, visual anchor, last search, last completed repeat description,
insert journal and undo-group depth. A process-level unnamed register contains only UTF-8 bytes and linewise flag,
allowing ordinary yank/paste between documents; it never holds an editor pointer. No named/numbered registers.

Focus/tab loss cancels incomplete operators/prompts and exits Visual/Insert to Normal, closing any undo group without
discarding entered text. Keep that document's last completed repeat/search; pending input cannot move to another
editor. Destruction cancels callbacks before freeing state. Disable restores native caret/key handling without
clearing history, source revision or dirty state; enable starts Normal. Read-only still permits navigation/search.

## Qt input and shortcut priority

Insert a Vim-first route before ScintillaEditor's Escape/number-navigation/block-move filters. On ShortcutOverride,
accept keys claimed by the current Vim state so matching QAction shortcuts cannot win. Normal/Visual printable
commands (including unsupported printable commands) and their pending arguments are consumed; unsupported input
shows feedback and resets pending state without insertion. Ctrl+R is claimed in Normal/Visual. In Insert claim
native text-entry/editing keys and Escape, allowing them to reach QScintilla instead of an application shortcut.
Pass unrelated function/application shortcuts through. Restrict this policy to the source editor and its popup;
dialog fields, the viewport and the command prompt have their own normal focus handling.

Use QKeyEvent::text for printable characters; Shift is reflected in that text. Handle arrows/Escape/Enter explicitly.
Recognize AltGr text before treating Ctrl+Alt as a shortcut. Do not convert non-BMP characters to one UTF-16 QChar.
Insert IME preedit/commit follows QScintilla's native inputMethodEvent; Normal/Visual do not insert IME text.

VimScintilla wraps keyPressEvent/inputMethodEvent and completion acceptance in a scoped input-origin guard; this
allows synchronous SCN_MODIFIED callbacks to identify native Insert edits after event filters have returned.
Escape is intercepted before the completion popup: send SCI_AUTOCCANCEL and SCI_CALLTIPCANCEL, finish Insert,
move caret to the preceding character on the same line when appropriate, and consume the event once.

## Command semantics, ranges and undo

Use only command-conformance.md dispatch entries. Preserve the vendor operator/motion structure, replacing range
math with explicit half-open UTF-8 byte ranges and a Linewise flag. Character motions use SCI_POSITIONAFTER/BEFORE,
never byte +/-1; CRLF is one line boundary. Normal horizontal motion clamps before EOL; empty lines have one valid
caret position. j/k use logical document lines, expand a folded target line and preserve desired character column.
Word classes are whitespace, Unicode letters/numbers/marks/underscore, and other punctuation; do not classify a
non-ASCII byte as a complete character. Combining sequences remain valid UTF-8; test their cursor/delete behavior.

VisualChar stores logical anchor and caret character starts; display/operator range includes the later endpoint via
POSITIONAFTER, independent of drag direction. VisualLine includes complete selected lines/EOL, handling final line
without an EOL. The displayed highlight and the actual operator range must match. Text-object scanners balance
paired delimiters and honor quoted escapes; an unclosed object reports failure without editing. They use textual
Vim-style boundaries, not OpenSCAD AST selection.

Counts compose with checked multiplication. Overflow fails before mutation; clamp motion to document boundaries
as defined by the command. Bound generated paste/repeat insertion to 64 MiB per command and report refusal before
editing if exceeded. This is an internal resource limit, not a user setting. Keep the last successful repeat.

Open one native beginUndoAction/endUndoAction per completed modifying command. For c/cc/change-object, keep it open
through following Insert until Escape/focus loss. Native insertion starts one group at mode entry. Yank/search/
navigation create none. u/Ctrl+R use the existing Scintilla history; never clear it or implement parallel undo.

Record repeat as an operator/motion/count description plus an insertion edit journal relative to the insertion
origin, never absolute old source positions or merely SCN_CHARADDED characters. Capture SCN_MODIFIED insert/delete
notifications during owned native Insert input, including completion, backspace and IME commits. Journal positions
use character-boundary offsets relative to the current insertion origin; preserve EOL style. On dot, resolve the
operator against current text, dry-run the journal on the affected temporary text slice, validate all boundaries,
then apply one undo group. A failed dry-run leaves text/register/repeat unchanged. Dot does not re-run completion.

Connect 02's synchronous externalEditStarting signal to close/invalidate insertion recording before the caller opens
another undo group. Engine-owned edits bypass that external entrypoint; native Insert changes carry the input-origin
guard. BEFOREINSERT/BEFOREDELETE notifications detect any missed unguarded mutation, but cannot substitute for the
pre-group hook. External edits are not journaled. Suppress recording during native undo/redo and dot. Verify ordinary
menus, programmatic transactions and annotation history all pass the hook; never block their normal notifications.

## Search, commands and settings

Search in this bounded core is case-sensitive literal UTF-8 text using Scintilla target search with flags=0; no Vim
regex dialect is exposed. Forward/backward search excludes the current match until wrapping once, then reports
wrap/not-found. n uses last direction, N reverses it; an empty submitted pattern reuses the last pattern if present.
Prompt cancellation restores original caret/selection; search produces no dirty/undo entry. The upstream broad regex
and substitute implementation is removed from this port. This resolves the search-dialect design question.

VimPrompt is an editor-local QLineEdit/status row, not a modal dialog or global widget. `/`, `?`, `:` open it with an
originating-editor QPointer. Accept exactly `w`, `q`, `e` and `e <path>`. The path is the remainder after command and
leading whitespace; preserve internal spaces and backslashes. Accept optional matching outer double quotes and
remove only those; no escapes, tilde/environment expansion, force suffixes, shell, ranges or command abbreviations.
Empty :e reloads an existing file; untitled reload reports unavailable. A malformed quote or unknown command fails.

Host callbacks call public TabManager::save(editor)/saveAs(editor). Add document-bound `closeDocument(editor)` and
`reloadDocument(editor)` returning a TabManager-owned DocumentCommandResult {Success, Cancelled, Failed}; the Vim
host maps it to HostResult without importing Vim headers into TabManager. Factor existing closeTabRequested/maybeSave
and refreshDocument code into these entrypoints, updating old UI callers. Resolve tab index after any modal prompt using the
captured QPointer, never a remembered index or current tab. Reload first uses normal dirty/save/cancel handling.
Closing the last document follows the existing window-close behavior. Open uses TabManager::open(path) in the
originating window; no synthetic keyboard shortcuts. Cancellation/failure never chains to close or reports success.

Add Settings::Settings::vimMode bool default false, an Editor-page checkbox, a mode label and brief supported-command
help. Follow existing Settings visitor/Preferences apply flow, update all open controllers on changes. No extra Vim
configuration pages. Restore original QScintilla caret/selection settings on disable.

## Implementation phases

[1](4_imp-phase1.md): exact file port/core bridge and compile/dependency boundary;
[2](4_imp-phase2.md): core operations, Unicode, undo/repeat conformance;
[3](4_imp-phase3.md): Qt focus/priority/prompts/settings;
[4](4_imp-phase4.md): native composition, dependency audit and packaging evidence.
Every architectural choice is specified above; the first phases verify it with the real engine/QScintilla, rather
than asserting that a GTK-free port already exists.
