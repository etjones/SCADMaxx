# Consistent icon system

Status: in progress, moved at the user's request on 2026-10-01. User chose Tabler plus matching custom icons for gaps.
Delivery: part 2 of 4, after foundation/typography, on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. No separate branch or worktree for this part.
Shared evidence: [UI visual polish](../../1_planning/2026-10-01_ui-visual-polish/1_exploration.md).
Prerequisite: [Qt foundation](../../3_done/2026-10-01_ui-qt-foundation-typography/1_exploration.md), including #6776.
Foundation is implemented and Windows-verified; use its 10 pt UI baseline for icon calibration.

## Outcome

One legible icon family across main toolbars, Preferences, Customizer help and application-owned status controls,
with correct colors in light/dark, checked, disabled and inactive states.

## Scope and method

- Start from the existing complete candidate inventory in
  `artifacts/ui-visual-polish/2026-10-01/icon-coverage.json`: 64 Chokusen names and 17 auxiliary candidates.
- Use stock Tabler SVGs where the meaning fits. Implement the six camera directions, specialized export formats and
  CAD display-mode gaps in the same grid, stroke, cap/join and optical-weight conventions. Resolve the 13 provisional
  semantic mappings; generic cube/export placeholders must not erase distinctions.
- Prefer 24 logical pixels as the first toolbar comparison; compare 20/24/28 at real DPI before fixing defaults.
  Match optical size as well as bounding boxes; keep menu/helper icons appropriately smaller.
- Centralize palette-aware icon handling with ordinary Qt APIs. Determine foreground from the actual native control
  state and surface; do not assume HighlightedText always matches every checked button or that SVG currentColor
  automatically inherits the widget palette. Refresh existing icons after palette changes.
- Replace Preferences' mixed direct PNG artwork and weak preset/status symbols. Keep branding and native window/dock
  control artwork intact. Retain upstream license notices and record the vendored Tabler revision.
- Supply the discreet question-mark help symbol to Customizer; its interaction area can exceed its visible glyph.

## Validation and boundaries

Check every existing action mapping, distinct symbols side by side, live palette changes, native checked backgrounds,
disabled/inactive legibility and mixed DPI. Do not reorder actions or replace native toolbar painting.
No assets or application source changed for this brief; individual mappings remain to be validated.
