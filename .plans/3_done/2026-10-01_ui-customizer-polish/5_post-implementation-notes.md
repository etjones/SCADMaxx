# Quiet Customizer — implementation results

All four phases completed sequentially in `D:/openscad/wt-openscad-ui-visual-polish`, branch `codex/ui-visual-polish`.

## Commits and handoff

1. `eea6d92b7` — native quiet disclosure headers and accessible expansion.
2. `7c3ea4d9c` — default Help icons mode and hover-only native tooltips.
3. `accfd2d98` — conservative display capitalization and native checkbox metrics.
4. `b22167be9` — real-model native regression fixture and evidence.

Exact source head: `b22167be9ca2701c4d321ee9dc4b0172ee99ac92`. Source/index/submodules are clean.
Customizer-only delta: `67101788f..b22167be9`. Private origin
`E:/Dropbox/bare_repos/scadmaxx.git`, `refs/heads/codex/ui-visual-polish`, verified at that head.
The initial loose-object push encountered a filesystem permission error; a normal non-forced push using packed
objects succeeded. No ACL changes, history rewriting or GitHub publication.

The cumulative UI branch already includes #6776, baseline Windows repairs, typography and icons. Future composition
must not apply those twice. Preferences/dialog polish remains pending; do not mark the cumulative UI source ready yet.

## Delivered behavior

- Native headers have the same resting surface open/closed, with disclosure arrows and accessible state updates.
  Qt controls text alignment and native borders; the HTML mockup is a visual reference, not a replacement skin.
- Help icons is the initial default, in the former Hide Details position. The other three modes remain available.
  Icons only appear for nonblank descriptions, beside the parameter label. Mouse-hover-only tooltips; no Tab stops,
  clicks, keyboard activation or new shortcuts. Existing input navigation is preserved.
- Native tooltip text preserves literal punctuation, angle brackets, units and line breaks. Passive descriptive
  metadata is present without adding help actions. Icons use the shared palette/DPI-aware renderer.
- Display-only capitalization preserves mixed-case words and original variable/group identities. Group names that
  capitalize identically retain separate expansion state. No changes to preset names, enum values or author help.
- Existing font/spacing helpers are reused and the final checkbox stylesheet is removed. Native sizing remains in
  control; no new QSS, custom chrome, editor/Console content-font changes or viewport changes.

## Verification

Evidence root: `D:/openscad/artifacts/ui-visual-polish/2026-10-01/`.

- Windows Release executable and tests built using the existing shared Qt 6.11.1 dependencies; logs
  `customizer-phase1-build.log`, `customizer-phase2-build.log`, `customizer-phase3-build.log`,
  `customizer-phase4-build.log` and final fixture build `customizer-native-fix-build.log`.
- Per-phase combined checks: 534, 603 and 617 assertions, all passing.
- Full ordinary suite: **77,467 assertions**, zero failures/errors, `customizer-full-suite-tests.xml`.
- Final native matrix: **472 assertions**, zero failures/errors, under `customizer-final-native/<theme>-<scale>/`.
  All four modes, real compiled parameters, edited values, expansion after rebuilds, Expand all, preset
  creation/reset/reload, native help tooltip, 350px panel, 18pt text and live theme changes were exercised.
  Captures include `customizer.png`, `main-window.png`, `mode-0.png` through `mode-3.png`, `help-tooltip.png`,
  and `enlarged-font.png`. Final light/dark screenshots were visually inspected.
- The first native fixture forgot to show the dock in its clean profile; corrected the fixture and reran the full
  matrix. Use final evidence rather than `customizer-first-native`.

## Limits

Scaling is simulated; physical mixed-monitor movement and Windows high-contrast switching were not exercised.
Qt5/older Qt6 and Linux/macOS runtime remain untested. Screen-reader application behavior was not manually tested;
the Qt accessibility interface/state/action is covered directly. Translation catalogs were not regenerated; changed
English source captions follow the existing translation mechanism and may fall back to English until translated.
Large text in an unusually narrow panel can elide native combobox captions; no responsive workflow rearrangement was
introduced. The developer binary retains its earlier configured version suffix; commit identities here are authoritative.

No source implementation of the next Preferences/dialog feature was started. Reuse this feature's native controls,
shared font/spacing, icon provider and display-only casing rules where applicable.

## Follow-up — help alignment and activation

The user revised the original hover-only requirement: vertically align help icons with their labels, shorten the
hover delay, and display help immediately on left click. No Tab stops or keyboard activation are added.
The working-tree implementation centers the icon, uses a 250 ms hover timer, and opens the same native tooltip on
left press. Leaving/hiding cancels pending hover help. Text escaping, parameter values and focus behavior remain.

`help-interaction-full-tests.xml`: 77,593 assertions passed, including the pending measurement-icon fix.
`help-interaction-native/<light|dark>-<1|2>`: all four native runs passed, with tooltip capture via the click path.
The native fixture allows Qt's tooltip appearance animation; tooltip text is supplied immediately on click.
These follow-up changes are uncommitted and are not part of the original phase commits above.
The same preview executable was rebuilt successfully with both follow-ups; see `ui-followups-build.log`.
