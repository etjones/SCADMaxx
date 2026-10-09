# Quiet Customizer

Status: done; all four phases implemented and committed, moved to done at the user's request on 2026-10-01.
See [results and limits](5_post-implementation-notes.md). The accepted Customizer preview is the visual reference.
Delivery: part 3 of 4, after the icon system, on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. No separate branch or worktree for this part.
Reference and historical evidence: [UI visual polish](../2026-10-01_ui-visual-polish/1_exploration.md).
Prerequisite: [Qt foundation](../2026-10-01_ui-qt-foundation-typography/1_exploration.md), including #6776;
reuse [icon-system](../2026-10-01_ui-icon-system/1_exploration.md) help artwork and color handling.
Icon implementation is complete at `67101788f`: use `Icons::icon("help", widget)` and its palette/state handling.

## Outcome

Recover the release Customizer's quiet, compact character with the accepted preview's typography and help treatment.
Preserve parameter order, values, presets and section behavior.

## Scope and method

- Store expansion independently from QToolButton checked state so open headers no longer request the native accent
  fill. Retain Qt rendering, focus/keyboard operation, saved expansion and accessible expanded/collapsed semantics.
- Use the same resting surface for expanded and collapsed headers. The arrow carries expansion state; modest type
  weight and whitespace provide hierarchy. Start with native Button/ButtonText behavior, not a custom header painter.
- In Help Icons mode, show discreet label-adjacent help icons only for parameters with descriptions.
  Native tooltips contain the full explanation on mouse hover only. Icons do not take focus, add Tab stops,
  respond to clicks or provide keyboard activation/F1 behavior. Preserve existing parameter-control navigation.
- Render labels in sentence case without renaming variables, preset keys or enumeration values. Preserve acronyms
  and intentional internal casing. Labels/headers reuse the foundation's normal/medium type hierarchy.
- Reuse the compact row/group spacing implemented in the foundation part. Adjust only where the new help/header
  treatment requires it, keeping checkbox/dropdown positions and long-label readability.
- Remove the ShowDetails-only checkbox-indicator QSS (currently forces 20px), and evaluate native indicator sizing.
  The separate blanket-bold label correction belongs to the foundation part and must not be repeated here.
- Rename Hide Details to Help Icons and make it the initial default. Keep Show Details, Inline Details and
  Description Only with their existing meanings, without redundant help icons. Retain the selector and its order.

## Validation and boundaries

Compare native light/dark output against the accepted reference at matched scale. Check expansion, all parameter
types, presets, long help text, keyboard navigation, font settings, high DPI and accessibility. Contrast repairs must
include the disclosure arrow. Customizer polish is implemented; #6776 and its required MSVC repairs are already
committed in the shared feature tree. The user assigned the first Customizer typography/spacing pass to the
foundation part; this part builds on it. That foundation is now implemented and Windows-verified: reuse its
weight-only QFont roles, `UIUtils::layoutSpacing`, wrapping and per-property Customizer font inheritance.

## Readiness review — 2026-10-01

Reviewed source at `67101788f` and the preserved `customizer-quiet-preview.html`. Source worktree is clean.
The user resolved both product choices: Help Icons is the default and help is mouse-hover-only, with no keyboard
interaction. No unresolved product questions remain. Implementation is complete; requirements and phased plan
are recorded in [requirements](2_requirements.md) and [implementation plan](3_overall-plan.md).

Concrete implementation constraints:

- `GroupWidget` currently uses a checkable QToolButton for expansion. Decouple expansion from native checked paint,
  retain native hover/pressed/focus states, expose expanded/collapsed accessibility state and test keyboard toggling.
- `ParameterWidget::rebuildWidgets()` keys expansion by `GroupWidget::title()`. Keep the original group identity
  independent of display capitalization, including group names that become visually identical after capitalization.
  Preserve rebuild behavior and Expand/Collapse All; do not invent cross-session expansion persistence.
- Current labels replace underscores with spaces. Capitalize the first cased letter only when the first word has
  no uppercase letters; otherwise preserve that word. Never lowercase remaining text or split camelCase:
  `show_USB_port` becomes `Show USB port`; `iPhone` and `showUSBPort` remain unchanged. Preserve original
  variable/group keys, preset names, enum values and author help text. See requirements for application-owned captions.
- The four existing description modes are Show Details, Inline Details, Hide Details and Description Only.
  Show Details is the current first/default item; changing the selector rebuilds controls. There is no saved
  description-mode preference in the inspected implementation. The user approved Help Icons as the new initial
  default; do not add persistence or change how the other modes work.
- Remove the actual remaining checkbox-indicator stylesheet in `ParameterCheckBox.cc`; use native metrics.
  Reuse existing font/spacing and Icons helpers. No stylesheet, replacement chrome or hand-painted section skin.
- The HTML is a visual reference, not a literal widget specification: retain native sizing and existing positions,
  rather than copying its hardcoded CSS colors, borders, shadows or responsive control rearrangement.

Verification must cover all parameter types, all retained description modes, help absent/present/multiline/long,
narrow docks and enlarged fonts, light/dark at simulated 100/125/150/200%, live palette changes, unchanged parameter
Tab order and hover-only help, header accessibility, expansion across rebuilds, presets, auto-preview and unchanged
SCAD parameter identities/values.
Record simulated versus physical DPI coverage explicitly. Windows remains the acceptance platform.
