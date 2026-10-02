# Icon system — implementation results

All four phases implemented sequentially in `D:/openscad/wt-openscad-ui-visual-polish`, branch
`codex/ui-visual-polish`, on foundation commit `1d498d864`. No separate UI branch/worktree was created.

## Delivered

- 83 semantic icon mappings: pinned MIT-licensed Tabler outline assets plus matching CAD, camera, format and
  animation artwork. Custom format labels are paths, not font-dependent text. Provenance is in
  `resources/icons/tabler/README.md`; license retained there and included in the application's About text.
- Palette/state/DPI-aware QIcon rendering, live label/model-item updates and native checked-button contrast.
  24 logical-pixel main/editor/viewer/animation icons, 32-pixel Preferences categories, native compact/menu sizing.
- Preferences > Advanced > User Interface > Status icon appearance: Monochrome, Native Qt status (default),
  Colored Tabler status. Stable stored enum; missing/invalid values default to native; changes apply live.
- Native status artwork or Qt-derived semantic tints for warning/error/information. Question/help/waiting/success
  glyphs stay monochrome. Information dialogs reporting success retain their existing information category.
- Compile banners, OctoPrint and application-owned message boxes participate. Qt message-box widgets retain
  their buttons/defaults/escape actions and native style/chrome; OS-owned file-dialog icons remain native.
- Real error-banner verification exposed stale warning content after syntax errors. Refresh the result on both
  normal completion and exception cleanup, without changing compilation or error-handling decisions.
- No new stylesheet, replacement Qt style, custom chrome, editor/Console font change or viewport color change.

## Commits

1. `258e9c4f3` — artwork, mappings and provenance.
2. `7883dcda5` — shared renderer, persisted preference and focused regression checks.
3. `9d50104f5` — native UI integration and checked-state contrast.
4. `67101788f` — final regression/native checks, live consumers, compile-banner correction and shipped license.

Final source head: `67101788f2a61e37d20febda760b2d08b0400c55`, verified at private origin
`E:/Dropbox/bare_repos/scadmaxx.git`, ref `refs/heads/codex/ui-visual-polish`. Source/index/submodules are clean.
Icon-only delta: `1d498d864..67101788f`. Cumulative UI branch base is
`464e25dad0c01af5488375c15aa6734190531eb5`; it includes #6776 and the previously recorded Windows repairs.

## Verification

Artifact root: `D:/openscad/artifacts/ui-visual-polish/2026-10-01/`.

- Full Windows Release executable and test target built with shared Qt 6.11.1 dependencies. Final build logs:
  `icons-delivery-build.log` (including About license) and `icons-settled-build.log` (final capture timing).
- Full ordinary suite: **77,384 assertions**, zero failures, in `icons-verified-suite-tests.xml`.
  Focused icon tests also cover every mapping at four DPRs, actual pixel output, palettes/alpha/disabled state,
  new action consumers, persisted settings/default/invalid values and fresh-process loading.
- Native Windows11: three modes × light/dark × simulated 100/125/150/200% scaling, two real main windows,
  live theme/preference changes, real warning and syntax-error banners, four message-box categories, Preferences,
  animation and 18 pt UI fonts. All eight runs passed 122 assertions each: **976 assertions**, zero failures/errors.
  Final evidence is `icons-release-check/<theme>-<scale>/`.
  Capture explicitly lets Qt settle after undocking/font changes; earlier transient captures are not final evidence.
- Source/resource audit finds no active old Chokusen/direct PNG icon consumers. Legacy branding and content images
  remain excluded. The obsolete entries were removed from `common.qrc.in`, the source of generated `common.qrc`.

## Limits and handoff

- Scale factors are simulated; physical mixed-monitor migration and Windows high-contrast desktop switching were
  not exercised. The high-contrast foreground fallback is implemented. Qt5/older Qt6 paths are source-checked only;
  Linux/macOS runtime checks remain deferred as agreed.
- OctoPrint network approval and physical input hardware were not exercised. Their icon paths were audited and
  integrated; rendering is covered independently. Optional Python/AI workflows were not run end to end.
- This is a developer build, not a packaged release. Its configured version suffix still names the earlier build
  configuration; source commits and these records are the authority for the tested changes. No GitHub publication.
- UI visual polish remains incomplete overall: quiet Customizer headers/help/casing and secondary-dialog polish
  are next. Do not mark the cumulative UI source ready for the combined build merely because this part is complete.
  The branch includes #6776 and Windows baseline repairs already; future composition must avoid applying them twice.
- Downstream work should use `Icons::icon`, `Icons::setLabelIcon`, and `StatusMessageBox`; it must not add another
  icon renderer or restore direct status PNGs. `help` supplies the Customizer's question-mark artwork.

## Follow-up — familiar Preview and Render silhouettes

The user found the overlapping-solids replacements too different from the originals and approved restoring their
recognizable shapes. Preview now uses the original dashed cube / fast-forward chevrons; Render uses the solid cube
/ hourglass. Both are redrawn on the 24-unit grid with round 2-unit strokes (1.5 for the hourglass detail), using
the existing palette-aware renderer. No action, shortcut or toolbar placement changed.

Evidence: `preview-render-light.png` and `preview-render-dark.png` compare original and redrawn assets at enlarged
and actual toolbar sizes. `familiar-action-icons-tests.xml` passed; all four native runs under
`familiar-action-icons-native/<light|dark>-<1|2>` passed. The resource library and test executable are rebuilt.
These artwork changes are uncommitted, alongside the previously tested measurement/help follow-ups. The GUI
executable remains open (process 80948 at this checkpoint), so its final relink is pending the user closing it.
