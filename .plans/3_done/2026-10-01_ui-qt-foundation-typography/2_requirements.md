# Qt foundation and typography — requirements

Status: implementation authorized; user decisions incorporated on 2026-10-01.
Visual reference and source findings: [exploration](1_exploration.md).

## Scope and ownership

| Surface/work | This part delivers | Later owner |
| --- | --- | --- |
| Main UI, menus, toolbars and dialogs | Shared default font and reliable inheritance, honoring saved preferences | Individual dialog hierarchy/layout in part 4 |
| Customizer | Inheritance, regular/medium hierarchy, compact spacing and font-responsive geometry | Header expansion appearance, help icons, casing and description modes in part 3 |
| Console and editor content | Preserve independent defaults, chosen fonts, zoom and existing behavior | No typography redesign in this UI feature |
| Icons | Preserve current assets and metrics | Tabler/custom artwork, sizing and state colors in part 2 |

All work stays sequential on `codex/ui-visual-polish` in the existing worktree. PR #6776 and the saved MSVC repair
were staged before implementation and are now committed separately from typography. Preserve their provenance.

## Font behavior

1. Use the approved Segoe UI, 13-CSS-pixel preview as the Windows visual target. Select an appropriate Qt point size
   through native comparison; exact browser pixels are not a requirement. Respect display scaling and font fallback.
2. Saved application font settings override the new defaults. Do not overwrite settings to force the preview.
3. Customizer inherits application family and size when each respective setting is absent. Its saved family-only,
   size-only or combined overrides remain effective. Application changes update all inheriting open windows live;
   newly opened windows and a restart produce the same effective settings.
4. Console and editor remain independent even when they have no saved font settings. Updating the application font
   must not change their content font or zoom. Dialogs containing their preferences still use the shared UI font.
5. Keep body/control/description text regular; Customizer labels and section headings use restrained medium emphasis.
   Preserve semantic text styling and font-preview content where an individual font is the purpose of the widget.
6. Keep existing font controls and setting keys. Viewing/updating Preferences must not create unintended overrides.
   Absent legacy keys are treated as defaults; do not infer lost historical choices or rewrite saved fonts by name.

## Layout and native styling

- Implement the first use of shared spacing rules in Customizer. Keep label/control groups compact, separate rows
  consistently and give sections more breathing room. Use native layout metrics and font-dependent size hints.
- Begin with approximately half a native gap within a field, one between fields and two between sections;
  calibrate against the approved reference. Apply container margins once and preserve necessary zero margins.
- Update geometry after font/style/DPI changes. Avoid fixed heights that clip text or excessive empty space.
- Keep parameter order, values, preset behavior, checkbox/dropdown positions, focus order and keyboard operation.
  Exercise all current description modes; their replacement/help treatment belongs to part 3.
- Use Qt font/layout/palette APIs. Add no QSS, fixed theme colors, custom native-control painting or replacement chrome.
  Native checked-header colors remain until the later header-state change; they do not fail this typography part.
- This part does not require removing unrelated remaining application stylesheets. Fix font/layout interference
  only where necessary for the affected surfaces, and record remaining cleanup with its owning part.

## Acceptance

- A complete Windows executable from this source state builds and launches with the shared dependencies.
- Native Windows11 light/dark comparisons cover 100/125/150/200% scale. Record Qt/font/style/scale and whether a
  scaling case is simulated. Compare the same fixture, pane width, description mode and UI state before/after.
- Normal text, emphasis and density visibly approach the reference while native controls remain intact.
- Clean settings, saved/partial overrides, live font changes, multiple windows and restart behave as specified.
  Console/editor independence is covered explicitly.
- Enlarged fonts, long translated labels, disabled controls and keyboard focus show no introduced clipping,
  overlap, inaccessible controls or loss of contrast. Check representative Preferences and export dialogs for
  font-inheritance regressions; broader dialog polish is deferred.
- Focused automated regression checks cover the changed inheritance/settings behavior and relevant geometry.
  Record any remaining warnings or verification limits alongside native visual evidence.
- Acceptance is Windows only. Preserve portable APIs and other platforms' default conventions; Linux/macOS runtime
  checks may be undertaken later and do not block completion.

The user subsequently requested all phases of this feature be implemented sequentially in the existing branch.
No publication or automatic commit was requested during implementation. The user subsequently requested grouped
commits; their hashes are recorded in the implementation notes.
