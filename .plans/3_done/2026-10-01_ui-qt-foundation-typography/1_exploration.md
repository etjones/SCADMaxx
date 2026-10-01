# Qt foundation and typography

Status: implemented and verified on Windows on 2026-10-01. See [implementation results](5_post-implementation-notes.md).
Shared evidence and accepted reference:
[UI visual polish](../../1_planning/2026-10-01_ui-visual-polish/1_exploration.md).
Readiness review: all three product decisions resolved. See [requirements](2_requirements.md) and
[implementation plan](3_overall-plan.md).
The user subsequently authorized sequential implementation of all phases of this feature.

Prerequisite #6776 applied on 2026-10-01, original upstream head
`aab4aed030dd61b80c5f850177f2af93e067eb7d`. Foundation/typography is committed through `1d498d864`; no push.
The existing MSVC Settings stream-declaration repair `c577f934adade4b762fba095abbad79a3b13df30`
is also applied and committed at the user's request; see the implementation notes for the five commit groups.
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
  regular. Keep Console and code-editor font behavior independent, including their defaults and user selections.
- Define shared layout rules: tight label/control groups, consistent row spacing, greater section separation,
  margins applied once, and control heights from native size hints. Let font and style changes update geometry.
- Keep the platform QStyle, native chrome and inherited palette. Avoid fixed palettes, new stylesheets and a custom
  QStyle that reproduces a stylesheet skin. Mockup borders and browser control shapes are not implementation demands.

## Validation and boundaries

Validate font preferences, live light/dark changes, readability and clipping at 100/125/150/200% scaling and with
long translated text. Record native reference renders before dependent polishing. Verify differences caused by
removing QSS, including header alignment, rather than treating every change as intended.

Existing worktree belongs to the umbrella feature; #6776 is committed there. No additional checkout created.

## Consistency and completeness review — 2026-10-01

Reference: [preserved preview HTML](../../../artifacts/ui-visual-polish/2026-10-01/customizer-quiet-preview.html),
[light render](../../../artifacts/ui-visual-polish/2026-10-01/customizer-preview-light-qa.png),
and [dark render](../../../artifacts/ui-visual-polish/2026-10-01/customizer-preview-dark-qa.png).
The HTML uses Segoe UI at 13 CSS pixels, regular body/control text and weight 500 for labels/headers.
Its fixed control heights, browser borders, tooltip drawing and responsive rearrangement are not Qt requirements.
Keep the existing application control order and native painting.

### Source findings that affect implementation

- `Preferences::init()` seeds Application, Customizer and Console font defaults independently from
  `QTextDocument().defaultFont()`. `getValue()` falls back to this map when a setting is absent.
- After #6776, `OpenSCADApp::setApplicationFont()` uses QApplication::setFont; ParameterWidget sets a concrete font
  on its scroll area, while Console sets its document font. Separate font signals update each surface.
  Live Customizer inheritance from the application font must be implemented; Console remains independent.
- Existing font sizes and signals use integer point sizes. Calibrate the reference in Qt; do not copy CSS pixels
  directly into that setting or expand the public size model solely to reproduce a browser measurement.
- Preferences removes saved values equal to its defaults. Historical explicit choices matching old defaults cannot
  reliably be distinguished from unset choices. Preserve all saved non-default overrides; do not guess a migration
  from a font's name or size. Test family-only and size-only overrides independently, plus restart persistence.
- `ParameterDescriptionWidget.ui` explicitly makes parameter labels bold. GroupWidget and description layouts use
  zero spacing; ParameterVirtualWidget adds four-pixel side margins. Ownership of their first typography/spacing
  changes belongs to this foundation part. The later Customizer part reuses the resulting typography/spacing.
- Remaining checkbox-indicator, launch-screen, color-sample, search-field, input-configuration and AI stylesheets
  are separate surface work. No new QSS; this feature must not claim whole-application stylesheet eradication.

### Settled boundaries

- Apply the shared UI font throughout the application, including dialogs. Use Customizer as the first visible
  label-weight/spacing implementation; individual dialog hierarchy/layout polish remains part 4.
- Windows typography should visibly match the approved reference, calibrated at the same display scale.
  Preserve other platforms' font conventions and explicit preferences. Console and editor typography stay independent.
- Customizer follows application family and size when their corresponding override is absent, including live
  application-font changes. Preserve its existing independent overrides.
- Keep native window/dock chrome, QStyle, palette roles, selection/focus/disabled behavior and control positions.
- Icon assets/metrics remain part 2. Header expansion state, contextual help, label capitalization and description
  modes remain part 3. Preferences category controls and individual dialog layouts remain part 4.
- Shared spacing uses native layout metrics: begin with approximately half a native gap inside a field group,
  one gap between fields and two between sections. These are calibration targets, not fixed pixels.
  Resolve Qt sentinel spacing through layout APIs; apply outer margins once, preserve necessary zero margins,
  and let font metrics/native size hints determine control heights.

### Acceptance coverage

Windows-only acceptance is approved. Linux/macOS runtime verification is optional future work, not a completion gate.
Keep portable Qt APIs and platform font fallbacks; do not force the Windows font onto other platforms.

- A linked executable from this branch is needed for visual acceptance; object compilation alone is insufficient.
  Reuse shared dependencies and narrowly applicable saved build repairs, recording any additional prerequisite delta.
- Compare the same SCAD fixture before/after in actual Qt Windows11 light and dark, matching display scale.
  Exercise 100/125/150/200% scaling and record whether each check used real display scaling or a simulated scale.
- Check clean settings, existing application overrides, independent Customizer overrides, live updates,
  multiple windows and restart. Verify Console/editor defaults, settings and Console zoom remain independent.
- Validate controls/labels with enlarged user fonts and long translated text: no introduced truncation, overlap,
  inaccessible controls or unexplained fixed-height gaps. Handle missing font families through platform fallback.
- Check theme/style/font changes refresh inherited fonts and derived geometry without storing accidental overrides.
  Validate focus, keyboard operation, disabled states and palette contrast on affected surfaces.
- Add focused regression coverage for inheritance, persistence and geometry where behavior changes; screenshots
  provide visual evidence. Record actual platform coverage and any untested platform separately.

Requirements and implementation sequence are ready; no unresolved product questions remain.
Do not advance this feature to done based on the existing PR compilation result.
