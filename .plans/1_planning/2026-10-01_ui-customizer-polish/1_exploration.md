# Quiet Customizer

Status: planning; user accepted the rendered Customizer as the visual reference.
Delivery: part 3 of 4, after the icon system, on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. No separate branch or worktree for this part.
Reference and historical evidence: [UI visual polish](../2026-10-01_ui-visual-polish/1_exploration.md).
Prerequisite: [Qt foundation](../../3_done/2026-10-01_ui-qt-foundation-typography/1_exploration.md), including #6776;
reuse [icon-system](../../2_in-progress/2026-10-01_ui-icon-system/1_exploration.md) help artwork and color handling.

## Outcome

Recover the release Customizer's quiet, compact character with the accepted preview's typography and help treatment.
Preserve parameter order, values, presets and section behavior.

## Scope and method

- Store expansion independently from QToolButton checked state so open headers no longer request the native accent
  fill. Retain Qt rendering, focus/keyboard operation, saved expansion and accessible expanded/collapsed semantics.
- Use the same resting surface for expanded and collapsed headers. The arrow carries expansion state; modest type
  weight and whitespace provide hierarchy. Start with native Button/ButtonText behavior, not a custom header painter.
- Replace inline explanations with discreet label-adjacent help icons, only for parameters with descriptions.
  Native tooltips contain the full explanation; keyboard and assistive-technology access must remain available.
- Render labels in sentence case without renaming variables, preset keys or enumeration values. Preserve acronyms
  and intentional internal casing. Labels/headers reuse the foundation's normal/medium type hierarchy.
- Reuse the compact row/group spacing implemented in the foundation part. Adjust only where the new help/header
  treatment requires it, keeping checkbox/dropdown positions and long-label readability.
- Remove the ShowDetails-only checkbox-indicator QSS (currently forces 20px), and evaluate native indicator sizing.
  The separate blanket-bold label correction belongs to the foundation part and must not be repeated here.
- Reconcile existing description-display modes with help icons; preserve useful existing capabilities. The mockup's
  Hide details selection is illustrative and does not approve deleting modes or redesigning the selector.

## Validation and boundaries

Compare native light/dark output against the accepted reference at matched scale. Check expansion, all parameter
types, presets, long help text, keyboard navigation, font settings, high DPI and accessibility. Contrast repairs must
include the disclosure arrow. Customizer polish has not started; #6776 and its required MSVC repairs are already
committed in the shared feature tree. The user assigned the first Customizer typography/spacing pass to the
foundation part; this part builds on it. That foundation is now implemented and Windows-verified: reuse its
weight-only QFont roles, `UIUtils::layoutSpacing`, wrapping and per-property Customizer font inheritance.
