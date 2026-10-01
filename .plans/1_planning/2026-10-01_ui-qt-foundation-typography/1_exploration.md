# Qt foundation and typography

Status: planning. Shared evidence and accepted reference:
[UI visual polish](../2026-10-01_ui-visual-polish/1_exploration.md).

Prerequisite #6776 applied and staged on 2026-10-01, original upstream head
`aab4aed030dd61b80c5f850177f2af93e067eb7d`. No commit; foundation/typography changes have not started.
The existing MSVC Settings stream-declaration repair `c577f934adade4b762fba095abbad79a3b13df30`
is also applied and staged at the user's request.
See [integration evidence](../../../artifacts/ui-visual-polish/2026-10-01/pr-6776-integration.md).

Delivery: part 1 of 4, sequentially on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. Apply #6776 first. No separate branch or worktree for this part.

## Outcome

Provide reliable native theme/font inheritance and match the accepted preview's calmer, more readable typography.
This is the prerequisite for Customizer, icons and dialog polishing, not a new global skin.

## Scope and method

- Apply PR #6776 before source work in `wt-openscad-ui-visual-polish`. Record its exact revision and integration
  results; do not take uncommitted edits from its occupied PR worktree. This prerequisite is now applied.
- Audit remaining application/Customizer font QSS and use QFont/widget APIs. Other leftover QSS should be identified
  by affected surface and removed in its owning patch, rather than expanding this into an unrelated whole-app rewrite.
- Use the approved Segoe UI, 13-CSS-pixel, normal/medium-weight preview as the Windows calibration target. Convert to
  appropriate Qt font sizing and compare at actual display scale; do not equate CSS pixels with physical pixels or
  force Segoe UI on other operating systems. Preserve explicit application and Customizer font preferences.
- Prefer medium labels/section headings over the current uniformly bold parameter labels. Keep body/control text
  regular. Keep code-editor typography and user-selected editor fonts separate.
- Define shared layout rules: tight label/control groups, consistent row spacing, greater section separation,
  margins applied once, and control heights from native size hints. Let font and style changes update geometry.
- Keep the platform QStyle, native chrome and inherited palette. Avoid fixed palettes, new stylesheets and a custom
  QStyle that reproduces a stylesheet skin. Mockup borders and browser control shapes are not implementation demands.

## Validation and boundaries

Validate font preferences, live light/dark changes, readability and clipping at 100/125/150/200% scaling and with
long translated text. Record native reference renders before dependent polishing. Verify differences caused by
removing QSS, including header alignment, rather than treating every change as intended.

Existing worktree belongs to the umbrella feature; #6776 is staged there. No additional checkout created.
