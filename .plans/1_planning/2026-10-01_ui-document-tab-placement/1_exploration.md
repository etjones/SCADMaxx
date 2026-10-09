# Document tabs above the editor or 3D view

Status: planning at the user's explicit request on 2026-10-07; exploration recorded only.
Implementation is deferred until requested. This is a small additional feature on the existing `codex/ui-visual-polish` branch in
`D:/openscad/wt-openscad-ui-visual-polish`, not another branch or worktree.

## Problem and current behavior

Document navigation is currently inside the editor dock. Users working primarily with the 3D view and Customizer
lose visible access to documents when they hide the editor.

The current implementation has multiple source-document buffers, each with its own editor and Customizer state,
but only one shared viewport/rendered result per main window. The active document and last-rendered document can
be different. Switching editor tabs changes the active editor, Customizer and window title; it generally leaves
the previous geometry visible until F5. An initial preview can occur when no rendered document exists and automatic
reload is enabled.

File > Open File opens/selects a tab, reusing an untouched empty document where appropriate. It does not reveal a
hidden editor. File > New File explicitly reveals the editor before creating a tab. Separate New Window / Open in
New Window commands already exist. Thus opening another document with the editor hidden can change the active
document without exposing its tab or updating the displayed geometry.

Source inspected during discussion:

- `src/gui/TabManager.cc`: `actionNew`, `open`, `createTab`, `tabSwitched` and close handling.
- `src/gui/MainWindow.cc`: `on_fileActionOpen_triggered`, `onTabManagerEditorChanged`,
  `onTabManagerAboutToCloseEditor`, and `activeEditor` / `renderedEditor` ownership.
- `src/gui/MainWindow.ui`: existing file actions, editor dock and viewport arrangement.

## Agreed direction

- Add a dropdown under Preferences > Advanced > User interface:
  **Document tabs: Above editor / Above 3D view**.
- Above editor remains the default and preserves the existing editor-oriented behavior.
- Above 3D view places document navigation above the viewport, available while the editor is hidden.
  One visible document tab row in the chosen location; no duplicated document buffers or separate viewport per tab.
- Both placements select the same internal document. When viewport tabs select another document, the editor text,
  Customizer and window title follow, including when the editor is currently hidden.
- In the viewport placement, switching documents automatically recalculates a preview equivalent to F5.
  Do not trigger a full F6 render. Existing editor placement retains its current preview behavior.
- Preserve document names, modified markers, closing/save prompts and tab ordering. Changing placement must preserve
  open documents, unsaved edits, parameter state and current selection.
- Keep native Qt tabs, palette, fonts and chrome; reuse the completed UI foundations.

The suggested implementation is small enough for one implementation pass, but needs explicit checks around
preview ownership and document switching. No lengthy design round is required for the agreed basic behavior.

## Implementation considerations to resolve later

- Persist the placement preference using the existing settings mechanism; apply it without reopening documents.
  Choose the Qt ownership/synchronization approach after inspecting the existing QTabWidget. Avoid two independent
  sources of truth for selection, ordering or document identity.
- A slow preview must not leave the previous model looking like the selected document's completed result.
  Provide a clear updating state using existing native status/progress mechanisms; exact presentation is undecided.
- Define handling of rapid tab switches while compilation is running: avoid overlapping work, use the latest
  requested document, and prevent stale results from appearing under another document's tab.
- Check empty/new documents, parse/render failures, closing the active tab, closing the rendered document, and
  switching placement when the active document differs from the displayed result.
- Decide whether New File should keep the editor hidden in viewport placement. Its current explicit editor-reveal
  behavior is documented above; the new-mode behavior has not yet been agreed. Also verify Open/recent-file paths
  and single-tab visibility so this mode works consistently without the editor.
- Preserve native keyboard navigation, close behavior, long-name elision/overflow, drag reordering and accessibility.

## Boundaries and checks

Per-document cached geometry, separate cameras, retained F6 results and simultaneous 3D views are out of scope for
the initial version. Recalculation on switching is accepted; caching/view-state retention can be a later feature.
No editor redesign or unrelated panel rearrangement is intended.

Verification should cover both placements, editor visible/hidden, live preference changes, opening/new/closing,
unsaved documents, selection synchronization, Customizer values, preview errors and rapid switching during a slow
preview. Confirm the old default behavior remains intact. Use Windows native light/dark and representative scaling
checks consistently with the existing UI feature work.

Before implementation, inspect the current source/index and existing follow-ups: measurement-icon refresh and
Customizer help alignment/hover/click changes were rebuilt and tested but remain uncommitted as of this record.
Preserve that work and its evidence. Background context is in the
[UI program](../../3_done/2026-10-01_ui-visual-polish/1_exploration.md) and
[final UI audit / follow-up notes](../../2_in-progress/2026-10-01_ui-preferences-dialog-polish/5_post-implementation-notes.md).

This record authorizes no implementation, build, lifecycle move of other features, or publication.
