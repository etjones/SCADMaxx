# Consistent icon system

Status: done; all four implementation phases completed and committed, moved to done at the user's request on 2026-10-01.
User chose Tabler plus matching custom icons for gaps. See [results](5_post-implementation-notes.md).
Delivery: part 2 of 4, after foundation/typography, on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. No separate branch or worktree for this part.
Shared evidence: [UI visual polish](../../1_planning/2026-10-01_ui-visual-polish/1_exploration.md).
Prerequisite: [Qt foundation](../../3_done/2026-10-01_ui-qt-foundation-typography/1_exploration.md), including #6776.
Foundation is implemented and Windows-verified; use its 10 pt UI baseline for icon calibration.

## Outcome

Consistent Tabler artwork across ordinary controls, with a selectable status-icon treatment and correct colors
in light/dark, checked, disabled and inactive states. Native Qt status artwork is the default exception.

## Scope and method

- Start from the existing candidate inventory in
  `artifacts/ui-visual-polish/2026-10-01/icon-coverage.json`: 64 Chokusen names and 17 auxiliary candidates.
- Use stock Tabler SVGs where the meaning fits. Implement the six camera directions, specialized export formats and
  CAD display-mode gaps in the same grid, stroke, cap/join and optical-weight conventions. Resolve the 13 provisional
  semantic mappings; generic cube/export placeholders must not erase distinctions.
- Approved size targets: 24 logical pixels for main/editor/viewport and animation toolbars; native small-icon
  sizing (normally around 16) for menus and compact/help controls; retain 32 for Preferences categories.
  Compare 20/24/28 toolbar renders and adjust optical size without reordering controls or adding another preference.
  Preserve existing explicit size settings if discovered.
- Centralize palette-aware icon handling with ordinary Qt APIs. Determine foreground from the actual native control
  state and surface; do not assume HighlightedText always matches every checked button or that SVG currentColor
  automatically inherits the widget palette. Refresh existing icons after palette changes.
- Replace Preferences' mixed direct PNG artwork and weak preset/status symbols. Keep branding and native window/dock
  control artwork intact. Retain upstream license notices and record the vendored Tabler revision.
- Supply the discreet question-mark help symbol to Customizer; its interaction area can exceed its visible glyph.
- Add a persisted Status icon appearance preference: Monochrome, Native Qt status (default), Colored Tabler status.
  The choice covers application-owned warning/error/information symbols in dialogs and inline messages.
  Ordinary action and help icons remain monochrome in all three modes. See [requirements](2_requirements.md).

## Validation and boundaries

Check every existing action mapping, distinct symbols side by side, live palette changes, native checked backgrounds,
disabled/inactive legibility and mixed DPI. Do not reorder actions or replace native toolbar painting.
No assets or application source changed for this brief; individual mappings remain to be validated.

## Readiness review — 2026-10-01

Foundation commits through `1d498d864` are present and the source checkout is clean. Continue on the same branch.
This review concerns the icon feature; the Customizer interaction and dialog-layout features remain downstream.

- The inventory contains 33 stock candidates, 13 provisional mappings and 18 gaps among 64 theme names, plus
  17 auxiliary candidates. File-name availability does not establish semantic suitability or complete use coverage.
  Reconcile every actual action/resource use, including optional surfaces, aliases and direct pixmaps, before replacement.
- Current theme selection switches between Chokusen light/dark names. MainWindow reacts to ThemeChange;
  direct compile-result pixmaps bypass that mechanism. Updating only the theme assets would leave gaps.
- Cover existing and newly opened windows, standalone dialogs, shared actions, checked/unchecked, disabled,
  hover/active and inactive states. Refresh cached pixmaps on palette and device-pixel-ratio changes as well.
  Preserve Qt focus cues, native backgrounds, action text, shortcuts and accessible names.
- Retain distinct preview/render, surface/wireframe/edge overlay, projection, fit/reset, camera-direction and
  export-format meanings. Generic cube/export placeholders are not final artwork. Preserve native chrome,
  branding, editor/Console content fonts and viewport geometry/overlays.
- Use a pinned Tabler revision with its license/provenance and a small documented set of matching custom SVGs.
  Rendering/lookup details are implementation decisions, subject to the native Qt/no-QSS constraints.
- Windows-only acceptance carries forward: native light/dark at 100/125/150/200%, enlarged UI fonts, live changes,
  multiple windows and meaningful state/mapping tests. Clearly distinguish simulated DPI from physical migration.
- Produce a contact sheet of every replacement plus native toolbar comparisons, then verify actual controls.
  Help artwork is supplied here; tooltip interaction and description-mode changes belong to Customizer polish.

Size targets and all three status modes were accepted on 2026-10-01; the user explicitly chose Native Qt status
as the default. No unresolved product questions remain. See [requirements](2_requirements.md) and
[implementation plan](3_overall-plan.md).
Actual Qt Windows11 versus monochrome Tabler comparisons at 16/24/32 logical pixels are in
`artifacts/ui-visual-polish/2026-10-01/status-icons/light.png` and `dark.png` (rendered at 200% scale).
The subsequent user request authorized implementing and committing each phase sequentially; all four are complete.

Follow-up consistency review: reconciled the umbrella's stale foundation status and comparison artifact's pending
choice. Requirements now explicitly preserve message-box behavior and existing semantic categories, exclude
OS-owned dialog artwork, and cover high-contrast fallback. The three-mode decision and native-status default are
unchanged. Custom mappings, tint derivation and optical calibration remain phase-1 implementation work with visual
verification, not unresolved product decisions. This feature is ready; downstream Customizer/dialog briefs still
need their own readiness reviews when reached.
