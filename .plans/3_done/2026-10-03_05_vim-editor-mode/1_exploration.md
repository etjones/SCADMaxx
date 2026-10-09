# Vim interaction mode for the QScintilla editor

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Planning review: product choices resolved on 2026-10-03; [requirements](2_requirements.md), the
[command acceptance matrix](command-conformance.md) and [technical design/four phases](3_overall-plan.md) are prepared.
The pinned source port, command behavior and Qt integration are specified; runtime verification is still required. See the
[readiness audit](../../1_planning/2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Original exploration status: planning. Sources: chats B/A in the [overview](../../1_planning/2026-10-03_00_source-first-cad-overview/1_exploration.md).
The user subsequently accepted core Vim editing and settled the behavior described below. They also selected a
patched version of the Geany engine without GTK/GLib dependencies. The port has not yet been compiled or verified.

## Architecture

An optional Vim layer consumes editor key events and performs ordinary operations on the existing QScintilla buffer.
It needs no geometry or AST knowledge and no separate document representation. Normal editor input and viewport
source changes continue to use the same buffer, change notifications and undo system.

Adapt Geany's `vimode` by patching its toolkit-dependent code to Qt/C++ and QScintilla. The user explicitly excludes
a GTK or GLib dependency: the Vim implementation must build and run without either. Replace their types, collections,
strings, event handling and widgets directly; do not add emulation headers or retain a second toolkit/runtime.
The pinned source and remaining port work are documented in [the port investigation](port-investigation.md).

Proposed pipeline: Qt keys/modifiers -> Vim engine -> consumed Scintilla command or pass-through Insert input.
Use a small backend interface for cursor/selection/text edits, line/position mapping and undo grouping so commands
can be checked without launching the whole CAD application.

## Accepted first version

Normal, Insert and Visual modes; movements, counts, operators `d/c/y`, text objects, paste, undo/redo, dot repeat,
search and basic `:w/:q/:e` document commands. The requirements and command matrix make this bounded core concrete.
The user explicitly excludes macros, named registers, Visual Block and substitutions from the initial version.
Full Replace mode and broad Ex/Vim compatibility are also outside this bounded core.

Expose one Vim enable/disable preference. When enabled, Vim takes priority inside the source editor. There is no
configurable priority policy or per-command mapping in this version. Possible future shortcut configuration is
deferred; do not build hidden mapping machinery now. No custom mappings, `.vimrc` support or compatibility layer.

## Integration details

- One Escape dismisses completion/call-tip UI and enters Normal mode, without requiring another press.
- Mode-appropriate caret (block/bar) and visible mode indication; exact preference/status UI remains to be designed.
- Account for Scintilla's between-character caret versus Vim's on-character inclusive selections.
- Preserve logical undo grouping, including change operators plus insertion; verify actual engine semantics.
- Route `:w`, `:q`, `:e` and similar commands through SCADMaxx's document/window operations.
- Vim command priority applies while the source editor owns focus, without changing viewport/other-field shortcuts.
- External graphical buffer edits must leave Vim cursor, selection and pending commands coherent.

## Order and evidence

This can proceed independently of geometry/provenance/assembly work. The technical review found a real dependency
on [02](../2026-10-03_02_source-editing-foundation/3_overall-plan.md): its synchronous external-edit notification must
finish a Vim insertion undo group before another source transaction opens a group. Later text notifications are too late.

Validate motions/operators/text objects/counts, Unicode and line boundaries, inclusive visual selection, folded lines,
undo/redo/repeat, popup Escape, dirty/save conflicts, multiple documents and interleaved graphical edits. Document
intentional Vim limitations. The chat's small-to-medium effort assessment is qualitative, not a delivery commitment.

## Branch boundary

Proposed source branch: `feature/vim-editor-mode`. Own key adapter/engine, mode preference/indicator, command tests
and its patched engine/build/license integration. Compile on 02 plus selected shortcuts and annotation undo.
Keep changes to common editor methods narrow and verify mixed undo on that actual prerequisite base.
Verify keys with viewport focus, application shortcuts and
annotation undo, not just isolated text motions. Reuse the shared Windows dependencies; engine research is not
approval to install GTK, GLib or a second editor/runtime. See
[branch integration and handoff rules](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Research update and next specification

The [Geany vimode README](https://github.com/geany/geany-plugins/blob/master/vimode/README), checked 2026-10-03,
documents the Scintilla/GTK boundary, GPLv2-or-later licensing, Normal/Insert/Replace/Visual/Visual Line modes,
operators/counts/repeat/search and a limited Ex surface. Named registers and Visual Block are missing, and its
Scintilla search semantics differ from Vim. This confirms a candidate, not a proven Qt port. The later source
inspection is recorded in [the port investigation](port-investigation.md), including the exact candidate revision
and concrete adaptation gaps.

Use the command matrix's initial mode/text/caret, keys, outcomes and integration acceptance cases. Expand its fixtures
for boundary/Unicode cases while preserving the accepted scope. Prove operator counts, inclusive selections,
dot-repeat after insert, one-press popup Escape, shortcut priority and document operations against the chosen adapter.
The technical plan isolates the selected vendor core from Qt event/document glue. Phase 1 builds the specified
MSVC-linked bridge and smoke fixtures; later phases verify full behavior. No port is claimed proven before those
checks pass. Do not transfer GTK runtime dependencies into the product.
