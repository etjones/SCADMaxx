# Vim engine investigation

Status 2026-10-03: user-facing scope settled; the user selected patching the Geany engine to remove GTK/GLib.
Source inspected, but no Qt/MSVC port compiled or verified.
This records technical evidence needed before a complete GPT-6.1 Sol implementation handoff.

## Pinned research input

Selected engine to adapt: Geany plugins `vimode`, research revision `8d1838869cfdebbeb8469193119839f7ffae0052`.
Retrieved through the official GitHub API after browser source fetches failed. This pins the research input; it is
not a claim that its unchanged build is usable. Source remains external and no code was installed or copied into
SCADMaxx. The implementation will retain only the accepted core and patch it for native Qt/C++ integration.

Inspected at this revision:

- [vi.h](https://github.com/geany/geany-plugins/blob/8d1838869cfdebbeb8469193119839f7ffae0052/vimode/src/vi.h)
- [vi.c](https://github.com/geany/geany-plugins/blob/8d1838869cfdebbeb8469193119839f7ffae0052/vimode/src/vi.c)
- [context.h](https://github.com/geany/geany-plugins/blob/8d1838869cfdebbeb8469193119839f7ffae0052/vimode/src/context.h)
- [keypress.h](https://github.com/geany/geany-plugins/blob/8d1838869cfdebbeb8469193119839f7ffae0052/vimode/src/keypress.h)
- [sci.h](https://github.com/geany/geany-plugins/blob/8d1838869cfdebbeb8469193119839f7ffae0052/vimode/src/sci.h)
- [excmd-prompt.h](https://github.com/geany/geany-plugins/blob/8d1838869cfdebbeb8469193119839f7ffae0052/vimode/src/excmd-prompt.h)
- [Makefile.am](https://github.com/geany/geany-plugins/blob/8d1838869cfdebbeb8469193119839f7ffae0052/vimode/src/Makefile.am)

Source headers state GPLv2-or-later. Preserve license/copyright obligations if adaptation is selected; inspect the
complete chosen file set and repository notices before vendoring. No third-party runtime installation is approved.

## Findings and required adaptations

| Evidence | Consequence for the port design |
| --- | --- |
| vi.h exposes GtkWidget, GdkEventKey, ScintillaObject and GLib types. | This is not a toolkit-neutral library to link unchanged. Define a Qt/native boundary and eliminate GTK imports. |
| keypress.h/context.h use GDK keys and GSList/string state. | Map Qt keys/text explicitly and account for GLib collection/string dependencies throughout the selected core. |
| sci.h includes ScintillaWidget.h and uses scintilla_send_message. | Replace the GTK Scintilla boundary with QScintilla's supported message API and pointer-sized positions. |
| vi.c defines global state and CmdContext. | Multi-editor/window ownership must be explicit; no process-global active buffer may redirect pending operations. |
| vi.c changes Visual caret/selection because of Scintilla's between-character caret. | Inclusive visual selection needs real acceptance proof; copying it does not establish VC12 behavior. |
| context.h keeps a fixed-size insert buffer; vi_notify_sci records SCN_CHARADDED. | Prove repeat for Unicode, backspace/paste/completion and programmatic edits; avoid truncated or unrelated replay. |
| ViCallback supplies save/save-all/quit, with no open/reload callback. | The approved :e behavior needs explicit host integration, bound to the originating document. |
| Vendor modes/options include Replace and an alternate Insert policy. | Expose only the accepted core and single enable switch. Remove excluded dispatch/settings from the adapted path. |
| excmd-prompt.h accepts GTK parent and CmdContext. | Implement the prompt with Qt; preserve focus, cancellation, feedback and existing Save/close/reload protections. |

These findings invalidate the assumption that replacing only a GTK event callback completes the port. The selected
approach is a maintained patched engine, with direct replacement of GTK/GLib usage. Finish the bounded investigation
below to specify its exact file set and adaptation boundary.

## Mandatory patch boundary

- Replace GTK widgets and prompt lifetime with Qt widgets bound to the originating editor.
- Replace GDK events/key symbols with an explicit Qt key/text/modifier representation.
- Replace GLib lists, allocation, strings and Unicode helpers with appropriate C++/Qt ownership and operations.
  Keep UTF-8 byte positions distinct from QString's UTF-16 indices; a type-name substitution is insufficient.
- Replace ScintillaWidget/scintilla_send_message with the supported QScintilla interface. Use pointer-sized position
  types where required and preserve Scintilla undo/container notifications.
- Replace global active-engine state with explicitly owned context appropriate to multiple editors/windows.
- Remove excluded vendor command paths and their dependencies. Keep upstream notices and a concise origin/patch record.
- Add no GTK/GLib shim headers, fake g_* APIs, pkg-config requirement, runtime DLLs or package installation. Other
  pre-existing application dependencies are outside this feature; the Vim code must not introduce or rely on these.

## Investigation outcome and implementation verification

The remaining selected command/parameter/motion/text-object/edit/undo sources were inspected on 2026-10-03.
[The technical plan](3_overall-plan.md) now fixes the retained file set, Qt/C++ replacements, ownership, input origins,
literal search, document commands and the 02 edit-boundary dependency. The checklist below is retained as evidence
of the port risks; its compile/conformance/dependency proof is now specified in implementation phases 1-4, not claimed
already executed. Sol is given the concrete algorithm and fixtures, not an instruction to choose a port architecture.

1. Inspect command runner, parameters, word/text-object, edit, undo and Ex implementations at the pinned revision.
   Inventory which files/commands the accepted core actually needs, GLib/GDK dependencies, integer-position widths,
   clipboard semantics and register storage. Do not retain substitution/remapping code merely because it exists.
2. Define the selected core state/context, Qt event normalization, QScintilla message bridge and host callbacks.
   Use real Qt/C++ types where required; do not introduce fake GTK/GLib compatibility headers or a second runtime.
   Decide state ownership and exactly what is cancelled or retained at focus changes, external edits and tab closure.
3. Inspect actual SCADMaxx settings, shortcut override/event filters, Scintilla notifications and document actions.
   Freeze named file/symbol changes. The earlier source audit already established editor revision/annotation undo;
   preserve those mechanisms and verify overlap with feature 02 rather than inventing another history layer.
4. Compile a minimal patched engine/adapter against the supported existing Qt/QScintilla/MSVC installation and exercise VC07,
   VC11-VC14, VC17 plus VI02-VI05. These probe counts, change/repeat, inclusive selection, Unicode, focus and undo.
   A compile alone is insufficient. Report remaining search-dialect/cursor/selection differences explicitly.
5. Verify the selected Vim source/include/link dependency closure contains no GTK/GLib requirements. Inspect build
   commands and final binary imports, then exercise the extracted application without additional toolkit DLLs.
   Record the exact selected vendor files, local changes, licensing, build registration and passed/failed fixtures.
   The prepared overall design and phases map these obligations to concrete edits and verification. Passing them is
   required before calling the port implemented; the existence of the plan is not runtime proof.

No further product question is currently open. Technical failures should be investigated with evidence; return to
the user only if the agreed behavior needs to change, not simply to choose C++ names or adapter implementation details.
