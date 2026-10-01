# Consistent icon system — requirements

Status: implemented and Windows-verified on 2026-10-01; see [results and limits](5_post-implementation-notes.md).
Build on foundation commit `1d498d864` in the existing `codex/ui-visual-polish` branch and worktree.

## Artwork and scope

- Use Tabler outline icons plus matching custom artwork where stock symbols do not preserve the action's meaning.
  Cover ordinary application-owned toolbars, menus, Preferences categories, compact controls and status indicators.
- Audit actual uses against the candidate inventory; no unresolved generic placeholders may silently ship.
  Preserve distinctions between preview/render, camera directions, projection/display modes and export formats.
- Keep branding, native window/dock chrome, control order, shortcuts, focus behavior and accessible names intact.
  Editor/Console content fonts and viewport geometry/overlays are outside this feature.
- Supply Customizer help artwork; its placement, tooltip interaction, casing and description-mode changes belong
  to the next feature. Preferences category layout/selection redesign remains in dialog polish.
- Pin the upstream asset revision, retain its license and record custom asset provenance.

## Size targets

- Main/editor/viewport and animation toolbars: 24 logical pixels.
- Menus, compact controls and help: native small-icon sizing, normally around 16 logical pixels.
- Preferences category icons: retain 32 logical pixels.
- Compare 20/24/28 toolbar renders and tune optical size without changing control order or adding a size setting.
  Respect existing explicit size preferences if found. Verify high DPI without relying on fixed physical pixels.

## Status icon appearance

Provide one application-wide preference in the existing Preferences > Advanced > User Interface area.
Use stable stored values, translated display labels and the existing settings/reset conventions.

| Mode | Warning, error and information symbols | Ordinary action/help icons |
| --- | --- | --- |
| Monochrome | Tabler shapes using the appropriate Qt foreground | Monochrome Tabler |
| Native Qt status — **default** | Native QStyle warning/error/information icons, retaining their colors | Monochrome Tabler |
| Colored Tabler status | Tabler shapes using the corresponding native Qt status-icon colors | Monochrome Tabler |

- Missing or invalid saved values resolve to Native Qt status. Preserve explicit choices across restart.
- Changes apply live to existing application-owned dialogs, inline messages and all open main windows;
  newly created widgets use the current selection. Refresh materialized pixmaps as well as QIcon consumers.
- Include the compile warning/error banner in the 3D view; the choice is not limited to modal dialogs.
  Apply the selected treatment consistently to application-owned message boxes and equivalent status indicators.
- Only warning/error/information semantics receive the three colors. Help/question, waiting and success glyphs
  remain monochrome; do not introduce an additional green status color or color ordinary action buttons.
  Preserve the existing message category: an information dialog reporting success still uses its information
  symbol; a dedicated success checkmark stays monochrome. Do not infer categories from translated message text.
- Application-owned QMessageBox question symbols use monochrome Tabler in every mode; iconless messages stay
  iconless. Preserve buttons, default/escape actions, modality and return values when routing message-box icons.
  Windows-owned file-dialog contents, shell icons, third-party branding and native chrome remain outside the setting.
- Mode 3 is an explicit exception to palette-only foregrounds. Its colors must correspond to the native Qt
  warning/error/information artwork; QPalette does not supply dedicated semantic roles. Record the derivation
  and fallback, and verify the resulting contrast in both themes. Do not invent an unrelated color scheme.
- Preserve native control/dialog painting and window chrome in every mode. No new stylesheet or global style skin.

## State behavior and acceptance

- Select foregrounds for the actual surface/state: normal, hovered/active, checked, unchecked, disabled and inactive.
  Recompute cached rendering after theme/palette, preference and device-pixel-ratio changes.
- Native Windows11 acceptance: light/dark, 100/125/150/200%, all three modes, multiple windows, runtime changes,
  clean/persisted/invalid settings, enlarged UI fonts and disabled/focused controls. Label simulated DPI clearly.
- Show all action mappings and custom gaps in a contact sheet; verify legibility in actual native toolbars/dialogs.
  Audit menus, optional surfaces and direct pixmap paths so no old asset accidentally bypasses the selected treatment.
- Add focused settings/mapping/state/cache regression checks, build the full Windows executable and record native
  visual evidence. Linux/macOS runtime acceptance is deferred; keep portable Qt APIs and sensible fallbacks.
- Retain meaningful shape and text cues: color is supplementary, never the only distinction between statuses.
  In Windows high-contrast mode, prefer system foreground contrast over decorative status tint where necessary;
  document that accessibility fallback and retain recognizable status shapes.
