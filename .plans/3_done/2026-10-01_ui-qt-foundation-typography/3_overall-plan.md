# Qt foundation and typography — implementation plan

Status: all four phases implemented and verified; see [results](5_post-implementation-notes.md).
Implements [requirements](2_requirements.md). Product questions are resolved.
Use `D:/openscad/wt-openscad-ui-visual-polish`, branch `codex/ui-visual-polish`, throughout.

## 1. Establish the native baseline

- Recheck source/index/submodule state and preserve the staged #6776 and stream-declaration repair.
- Complete a Windows Release build using the existing shared vcpkg installation. Apply already recorded baseline
  repairs only when applicable; record each separately from UI behavior changes. Do not import unrelated PR work.
- Save baseline native Windows11 light/dark evidence using the existing UI study fixture and isolated test settings.
  Record the effective application, Customizer, Console and editor fonts, DPI, style and pane geometry.
- Keep the user's working settings intact. Store builds, fixtures and evidence in workspace artifacts, outside source.

## 2. Implement font defaults and inheritance

- Inspect `Preferences::init/getValue/removeDefaultSettings`, the existing font signals, OpenSCADApp's application
  font setter, ParameterWidget's font setter and Console/editor initialization together before changing defaults.
- Keep an independent platform-derived default for Console/editor. Resolve the application default to the calibrated
  Windows font only for the UI; retain platform conventions elsewhere. Preserve explicit saved overrides.
- Resolve Customizer overrides per property over the current application font. Ensure both its scroll content and
  surrounding controls have the intended relationship; update every open Customizer on application-font changes.
- Preferences should display effective inherited values without persisting them as choices. Keep explicit overrides
  distinguishable from inherited values going forward, including when their values happen to be equal.
  Preserve the existing reset/default mechanism and setting compatibility; no new settings workflow is required.
- Audit application-owned font assignments for interference with normal UI inheritance. Keep semantic fonts and
  independent Console/editor content intact. Scope repairs to font inheritance, not individual dialog redesigns.
- Start native size calibration near the existing integer point sizes that approximate the 13-CSS-pixel reference.
  Record the selected size and comparison; do not introduce fractional settings just to copy browser measurements.

## 3. Apply hierarchy and spacing to Customizer

- Use the effective inherited/overridden font as the basis for regular and medium roles; do not freeze its family
  or size in child widgets. Apply label/header emphasis without propagating that weight into input controls.
- Primary areas: ParameterDescriptionWidget.ui, ParameterVirtualWidget, GroupWidget and parameter control layouts.
  Replace blanket bold label treatment and accidental zero/doubled gaps with the shared compact spacing rules.
- Derive layout gaps from native metrics with proper sentinel handling, and recompute derived geometry after
  relevant font/style changes. Prefer normal Qt inheritance/layout invalidation over custom event machinery.
- Keep the current expansion state, descriptions, casing, icons and control locations. The later Customizer part
  reuses this implementation and adjusts only geometry required by its new help/header treatment.

## 4. Verify and record

- Use the repository's existing Qt test arrangements where available for focused inheritance tests. Exercise absent,
  family-only, size-only and combined Customizer overrides; application updates; multiple windows; restart;
  Preferences signal feedback; and unchanged Console/editor content fonts and zoom.
- Check font-derived layouts with long labels, enlarged fonts, each current parameter type and description mode.
  Keep tests focused on observable behavior rather than duplicating helper calculations.
- Build/link and launch the full GUI. Compare native light/dark output at the four agreed scales, documenting
  physical versus simulated DPI. Include representative Preferences/export surfaces to check shared font adoption.
- Verify keyboard/focus behavior, palette contrast and theme switching. An intentional later-phase header/icon
  defect is recorded separately; a new regression caused by this part must be fixed before completion.
- Update `5_post-implementation-notes.md` with calibration choices, source changes, verification and remaining
  limitations. Update downstream plans to consume the established font/spacing rules, without duplicate work.

Completion requires the requirements' acceptance evidence. The prerequisite's successful object compilation is
not a substitute for this feature's build and visual checks. No Linux/macOS runtime gate applies to this iteration.
