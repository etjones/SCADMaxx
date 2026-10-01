# Qt foundation and typography — implementation results

Implemented and verified on Windows on 2026-10-01. All four phases are complete.
Source is committed on `codex/ui-visual-polish` in `D:/openscad/wt-openscad-ui-visual-polish`.
No push or publication. Icons, neutral Customizer headers/help/casing, and per-dialog polish remain separate features.

## Delivered

1. **Baseline:** applied #6776 before typography work and completed the Windows Release build. Retained the saved
   Settings stream repair; applied the existing main-wrapper, Cairo-target and MSVC manifest repairs needed for
   this build. Their exact provenance is in the integration record linked below.
2. **Fonts:** Windows UI defaults to Segoe UI 10 pt. Customizer family and size inherit independently unless saved
   overrides exist. Updates reach existing and new panels, including the controls above the scroll area.
   Preferences blocks incidental QFontComboBox notifications during application font changes. Explicit UI font
   overrides survive default-settings cleanup, including choices equal to the default. Console retains its platform
   default and its own widget/document font and zoom; editor content and zoom stay independent.
3. **Hierarchy/spacing:** Customizer labels/headings use weight-only QFont::Medium overrides; inputs/descriptions
   remain regular. Native metric gaps provide half-gap field spacing, one-gap row spacing and two-gap separation
   following expanded sections. Group content owns its inset. Long labels wrap; preferred vertical size policies
   allow the layout to allocate their required height. Native metric sentinels have a font-based fallback.
   Font/style changes refresh derived spacing. Fixed 8 pt axis labels and the fixed-size update-status label in
   Preferences now inherit; experimental-feature labels retain bold emphasis without pinning their family/size.
4. **Verification:** native captures, regression checks, source/whitespace review and downstream-plan updates complete.

No new stylesheet, fixed palette, native-control painter or replacement window chrome was added.

## Calibration and evidence

Evidence root: [artifacts](../../../artifacts/ui-visual-polish/2026-10-01/).
Baseline source is branch HEAD `464e25dad0c01af5488375c15aa6734190531eb5` plus the staged prerequisites.
The typography commits follow the two prerequisite commits, keeping their provenance distinct.
Reviewable deltas are preserved as `foundation-typography-tracked.patch` and `foundation-typography-test.patch`
(the new Catch2 source); apply both over `foundation-baseline.patch` to reproduce the complete source changes.

Committed at the user's request on 2026-10-01:

| Commit | Group |
| --- | --- |
| `51acda103` | Phase 1: integrate upstream #6776, retaining Jordan Brown's authorship |
| `be352f279` | Phase 1: four existing Windows build repairs |
| `b3c4349c3` | Phase 2: font defaults, inheritance and independent content fonts |
| `e24ab1532` | Phase 3: Customizer hierarchy, wrapping and native spacing |
| `1d498d864` | Phase 4: regression coverage and CMake test support |

The source checkout is clean. SHA256 comparison verified that all 35 affected source files are byte-for-byte
unchanged by commit grouping, so the recorded build/test evidence still applies. No push was made.

- Native baseline: `foundation-baseline/`; final native captures: `foundation-final/`.
  Both use the same 480 x 600 logical-pixel Customizer fixture and Hide Details mode. The fixture instantiates the
  actual OpenSCAD parameter widgets with representative values; it does not load a SCAD file or render a model.
- Segoe UI **9 pt / bold labels** became **10 pt / medium labels**. At 96 logical DPI, 10 pt is approximately
  13.33 logical pixels, close to the accepted 13-CSS-pixel reference without introducing fractional preferences.
- Qt **6.11.1**, native **windows11** style; light/dark at **100%, 125%, 150%, 200%** all pass. These are simulated
  scale cases using `QT_SCREEN_SCALE_FACTORS`, not four physical monitor configurations. The measured DPRs are
  1, 1.25, 1.5 and 2; each capture includes `fonts.json` and JUnit results.
- Captured Preferences (3D View and Advanced) and PDF export at every scale/theme. Full MainWindow, including its
  OpenGL viewport, was launched and captured at 100% in both themes. Native widgets run in the linked unit-test
  host with temporary INI settings, keeping the user's OpenSCAD settings intact. The full `openscad.exe` links and
  its executable launch/version check passes; a separate interactive run against the user's profile was avoided.
- Theme switching on existing widgets passes. Existing disabled controls retain native rendering. Visual review
  found no new clipping in the comparison fixtures; deliberately oversized text scrolls normally.

## Tests and reproducibility

`src/gui/Typography_test.cc` uses the existing Catch2 target. CMake exposes generated UI headers to that target and
matches its language standard to the application (C++20 with MSVC, C++17 elsewhere).

- `suite-final-tests.xml`: **75,679 assertions, zero failures**, all 60 ordinary unit-test cases.
- Typography coverage includes absent/partial/combined overrides, live changes, multiple panels, Preferences
  feedback, settings reload, four fresh-process startup combinations, Console Ctrl-wheel zoom and editor zoom.
- Long-label geometry checks exercise all six parameter widget implementations, all four description modes,
  10/18 pt fonts, label/control weights, wrapping, containment, expansion and keyboard checkbox operation.
- `native-regressions/light-1` and `dark-2`: **542 assertions each, zero failures**, including stress screenshots.
- `foundation-final/`: eight capture runs pass (13 assertions each at 100%, 12 at other scales), including live
  theme changes. The early `foundation-native` main-window captures lacked test-host resource initialization;
  `foundation-final` corrects this and is the authoritative evidence.
- Initial tests reproduced the stale Customizer/Console inheritance bug. A geometry test exposed height limits on
  wrapping labels; correcting size policies resolved it. One initial suite command used `*`, explicitly selecting
  opt-in fixtures without their environment; the corrected ordinary-suite filter is `~[.]`.
- Existing compiler warnings (numeric conversions, unused exception variables and Eigen configuration) remain.
  No Linux/macOS runtime check, physical monitor migration, installer packaging or screen-reader audit was performed.

Reproduction scripts beside the evidence: `Invoke-FoundationBuild.ps1`, `Invoke-FoundationChecks.ps1`
(`-Capture` for the eight native reference runs), and `Invoke-FoundationNativeChecks.ps1` for native regressions.

## Follow-on ownership

- Icon-system work consumes the 10 pt UI baseline; toolbar artwork/metrics remain unchanged here.
- Customizer polish reuses `UIUtils::layoutSpacing` and the weight-only font roles. It owns blue checked headers,
  help icons, sentence casing, description-mode reconciliation and the remaining Show Details checkbox QSS.
- Preferences/dialog polish reuses the shared font. It owns category selection presentation, group outlines,
  dialog-specific whitespace and any remaining stylistic inconsistencies.

Follow-up choices remain fix forward for bounded corrections, replan for a different implementation strategy,
restart if the assumptions fail, or supersede this feature with a replacement objective.
