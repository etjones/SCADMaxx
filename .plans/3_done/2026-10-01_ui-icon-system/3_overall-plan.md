# Consistent icon system — implementation plan

Status: all four phases completed on 2026-10-01, with a separate commit after each sequential phase.
See [implementation results](5_post-implementation-notes.md) for commits, evidence and validation limits.
Implements the accepted [requirements](2_requirements.md).
Keep all phases sequential in `D:/openscad/wt-openscad-ui-visual-polish`, branch `codex/ui-visual-polish`.

## 1. Complete the inventory and visual specification

Reconcile the 64 theme names and 17 auxiliary candidates with actual resource/action/pixmap consumers, including
optional UI. Resolve the 13 provisional semantic mappings and 18 custom gaps without conflating distinct actions.
Pin Tabler provenance/license. Produce a complete contact sheet and 20/24/28 toolbar comparisons at the 10 pt
foundation font, using the approved size targets. Verify the Qt-native status colors used by mode 3 and document
a deterministic source/fallback; do not treat arbitrary SVG currentColor as automatic widget inheritance.

## 2. Implement rendering, state handling and the preference

Use the existing Qt icon/resource infrastructure where practical, with centralized palette/state-aware rendering
and a shared status-icon provider. Keep native control painting. Cache by every relevant rendering input and
invalidate on theme/palette, mode and DPI changes. Supply all required QIcon modes/states and direct-pixmap updates.

Add the three-value persisted preference and native-status default in the existing User Interface group. Cover
missing/invalid settings, reset, restart, existing windows/dialogs and newly created consumers. All-monochrome mode
must also affect application-owned message-box symbols; changing only toolbar resources is insufficient.
Preserve message-box categories and behavior, including iconless/question dialogs, default and escape buttons,
modality and return values. Native OS-owned dialog contents stay outside this setting.

## 3. Integrate artwork and sizes across existing consumers

Replace ordinary action/category/compact icons and custom CAD gaps. Route warning/error/information icons in
dialogs and the compile banner through the selected status treatment. Keep other symbols monochrome and retain
branding/native chrome. Audit direct PNG/pixmap consumers and dialog factories, avoiding stale per-widget copies.
Preserve names, actions, order, shortcuts, focus/accessibility and fonts. Supply help artwork for the next feature.

## 4. Verify and record

Build/link the full Windows application. Run focused tests and native visual checks for all three modes, both
themes, four scales, checked/disabled/inactive controls and live switches across multiple windows. Exercise actual
warning/error/info dialogs and compile banners, Preferences categories, animation and compact/menu controls.
Check custom symbols and export-format distinctions at their actual displayed sizes. Record runtime/platform limits.
Include high-contrast fallback and message-box behavior checks. Audit optional consumers even when their runtime
dependencies are unavailable; record those validation limits rather than treating them as exercised.

Write `5_post-implementation-notes.md`, link authoritative screenshots and update downstream plans to consume the
new icon/status provider. Keep plans/build artifacts outside source. Commit only when requested, grouping work by
logical phase. The user explicitly authorized implementation and commits for all four phases on 2026-10-01.
