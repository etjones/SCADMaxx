# Preferences and secondary-dialog polish — implementation results

Four phases implemented sequentially on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. The final verification and private handoff are recorded below.
This is the last of the four UI features. Its lane remains in-progress pending the user's completion review.

## Commits

| Phase | Commit | Result |
| --- | --- | --- |
| 1 | `677442341` | Native Preferences category tabs, action/page synchronization and conditional fallback |
| 2 | `33f734dd7` | Native spacing, restrained Advanced/Dialogs groups and inherited heading font |
| 3 | `2e41da9f1` | Remaining stylesheet replacements, information readability and offline capture fixture |
| 4 | `8f5b3ae47` | Audit corrections, cumulative behavioral tests and expanded native captures |

## Surface audit

| Surface | Disposition and evidence |
| --- | --- |
| Preferences: 3D View, Editor, 3D Print, Advanced, Dialogs | Fixed shared tabs/metrics; flat native groups only on Advanced/Dialogs. All captured. Same names, category/control order and actions. |
| Preferences: Axes, Buttons, Mouse | Native status APIs replace QSS. Numeric axis badges retain readings even on styles that omit progress text. Pressed/dead-zone states retain palette-based emphasis. Captured without hardware. |
| Preferences: AI | Shared native tabs/metrics and inherited medium header. Category forced visible only in isolated fixture. Captured offline; conditional hide/show/fallback tested. |
| Preferences: Update / Experimental Features | Source-inspected; excluded by this build's compile flags. Common registration/metric paths apply, but runtime not claimed. |
| PDF, 3MF, SVG export | Inspected native light/dark layouts; no additional redesign needed. Existing PDF scroll area, group meanings, color content and standard buttons retained. |
| Print initialization / OctoPrint authorization | Offline widgets captured; native layout retained. No server authorization, request, credentials or print job exercised. |
| About | Paragraph font inherits the UI font. Branding/donation artwork and native browser retained. Captured. |
| Library/build information | Literal text with medium property labels and modest row spacing. Copyable `<`, `>` and `&` text regression covered. Captured. |
| Welcome | Native Window/list/button surfaces replace wave/background/button QSS. Logo, wordmark, content and controls retained. Captured. |
| AI chat, message/tool bubbles, diff | Native frames/palette/fonts/buttons; no hardcoded control skin. Code/diff content colors and fixed-font code family retained. Offline captures; dialog return values tested. |
| AI attachment preview / proposed-change banner | Stylesheet removed and inherited controls retained. Source-inspected; service-driven appearance and attachment interaction not runtime exercised. |
| OpenCSG warning / standard message boxes | Native warning captured; shared status message boxes rechecked by cumulative icon fixture. Semantics unchanged. |
| Progress | Native capture and Stop/cancel assertion; no presentation change needed. |
| Error Log | Native label colors plus shared warning/error icons fix yellow-on-light readability. Initial status column includes icon width. Captured; roles/icons tested. |
| Font list | Captured; inherited control text retained. Sample font/size is intentional content, not a UI font override. |
| Color list / swatches | Native channel sizing and palette/frame swatches replace QSS. Actual swatch colors unchanged. Selection size regression covered. Captured. |
| Viewport controls / animation | Native layouts inspected and captured; existing common icons/metrics retained. No camera, animation or rendering behavior changes. |
| Search field | Native text margins replace QSS. Counter expands with long numbers and font changes; zero clears reserved space. Focused test; main-window capture covers surrounding controls. |
| Main window / Customizer | Cumulative native fixture rechecks prior font/icon/quiet-header/help/preset work. No rearrangement. |
| Native OS file/font/color dialogs and window/dock chrome | Deliberately unchanged; Qt/platform-owned presentation. |
| Editor/Console content, viewport and user-authored data | Deliberately unchanged; font independence remains regression-tested. |

All Designer `.ui` surfaces were included in discovery. The source audit found no remaining `setStyleSheet()` calls
or Designer stylesheet properties under `src/gui`. HTML content styling is separate: branding and code/diff colors
are intentionally retained.

## Verification

Evidence root: `D:/openscad/artifacts/ui-visual-polish/2026-10-01/`.

- `dialogs-final-build.log`: Windows Release executable and unit-test build using shared Qt 6.11.1 dependencies.
- `dialogs-final-full-tests.xml`: 137 ordinary cases / 77,582 assertions; zero failures or errors.
- `dialogs-verified-native/<light|dark>-<1|1.25|1.5|2>/`: final dialog matrix, including 18pt text, long labels,
  overflow and live theme switching. Eight runs / 121,848 assertions; zero failures or errors. Each directory has
  PNG captures and JUnit/log evidence; assertion totals include repeated stylesheet checks over widget trees.
- `dialogs-regression-icons/` and `dialogs-regression-customizer/`: final light/dark at simulated 100% and 200%.
  Four runs each / 488 icon and 236 Customizer assertions; zero failures or errors. Earlier features additionally
  retain their own complete four-scale matrices.
- Representative final light/dark captures visually reviewed, including Preferences, enlarged text, exports,
  Welcome, About, library information, error status, swatches and AI surfaces.

Audit catches: corrected page registration versus presentation order; stable selected swatch sizing; top alignment
of the compact Dialogs group; status label room beside new Error Log icons. Initial failed builds/tests and
intermediate captures are retained; use the final evidence names above for acceptance.

## Composition boundary

Use the UI-only delta after **`be352f27972d570d61c9224a927079fa21055ac0`**, not the whole cumulative branch.
This base includes upstream #6776 integration `51acda1034a373d9be11b7118074ff47b4e79e04` plus the four previously
recorded MSVC baseline repairs. The UI entry depends on the separately selected `pr-6776` entry.
The reviewed PR input was `aab4aed030dd61b80c5f850177f2af93e067eb7d`; newer upstream/PR inputs require normal
composition review. The explicit boundary excludes replaying #6776 and those repairs. Obtain needed repairs
separately from the workspace repair catalog and verify applicability; do not replay the UI branch's base commit.

Source private origin is `E:/Dropbox/bare_repos/scadmaxx.git`, ref `refs/heads/codex/ui-visual-polish`.
Final source head: `8f5b3ae4707a8718db28722deb2fd723fd9415ab`. Dialog-only delta is `b22167be9..8f5b3ae47`.
Source/index/submodules are clean and aligned. The private origin was pushed without force and read back at this
exact head. The cumulative UI source is ready with the explicit delta/dependency above; the registry records it.
This feature does not start a new SCADMaxx composition or publish to GitHub.

## Limits

Windows-only runtime acceptance. DPI is simulated, not physical mixed-monitor movement. Qt5/older Qt6,
Linux/macOS, Windows high-contrast switching and screen-reader application use are not manually verified.
Long-label coverage uses a synthetic English label; it is not a full translated-locale audit. Large fonts retain
native scrolling/overflow instead of moving settings. Export/print rendering and external services/hardware are
not exercised by the dialog fixtures. Translation catalogs retain existing untranslated/fuzzy entries.
The shared build emits an existing Fontconfig configuration warning; tests pass. Its configured version suffix
still references an earlier UI development step; source commit identity in these notes is authoritative.
