# OpenSCAD UI visual polish

Status: foundation done; icon system in progress from 2026-10-01. Customizer and dialog polish remain planning.
Direction constrained to native Qt styling after user review.

Prerequisite update: original upstream PR #6776, head `aab4aed030dd61b80c5f850177f2af93e067eb7d`,
is committed in the existing UI worktree. Four integration conflicts were resolved while preserving newer
upstream changes. Foundation is committed through `1d498d864`; no push. Icon-system preparation is in progress.
The existing MSVC Settings stream-declaration repair `c577f934adade4b762fba095abbad79a3b13df30`
is also applied and committed at the user's request, alongside the other recorded Windows baseline repairs.
See [integration evidence](../../../artifacts/ui-visual-polish/2026-10-01/pr-6776-integration.md).

## Accepted reference and focused follow-up parts

The user accepted the quiet Customizer preview, including its improved typography, as the visual reference.
Use the compact geometry, normal/medium type hierarchy, neutral open/closed headers, sentence case and discreet
help icons as the target. The earlier AI-generated full-window concepts remain superseded.

Reference fragment: [preserved HTML](../../../artifacts/ui-visual-polish/2026-10-01/customizer-quiet-preview.html),
copied byte-for-byte from the original Codex visualization during the readiness review.
Rendered evidence: `artifacts/ui-visual-polish/2026-10-01/customizer-preview-light-qa.png` and
`customizer-preview-dark-qa.png`. These are mockup renders, not OpenSCAD screenshots.
Segoe UI at 13 CSS pixels with normal/medium weights is the accepted Windows visual starting point. Calibrate its
Qt equivalent under display scaling, respecting explicit user font settings and other platforms' font conventions.
Do not silently discard the accepted typography by simply retaining the current defaults.

Foundation scope confirmed: apply shared font defaults to the UI and dialogs, with Customizer as the first
label-weight/spacing implementation. Customizer inherits the application font unless separately overridden.
Console and editor content keep independent defaults and settings. Foundation acceptance targets Windows only;
Linux/macOS runtime checks are optional future work. Detailed requirements and the implementation sequence live
in the foundation plan; the later Customizer/dialog parts reuse its result.

Four focused briefs own the work. This file retains the shared evidence and historical discussion.

1. [Qt foundation and typography](../../3_done/2026-10-01_ui-qt-foundation-typography/1_exploration.md)
   (done): #6776 applied; font inheritance, Segoe UI 10 pt Windows default and native Customizer spacing implemented.
   Native Windows light/dark captures and regression results are recorded in its implementation notes.
2. [Icon system](../../2_in-progress/2026-10-01_ui-icon-system/1_exploration.md)
   (in progress): Tabler, custom CAD gaps, size and state-aware coloring.
3. [Customizer polish](../2026-10-01_ui-customizer-polish/1_exploration.md): implement the accepted reference.
4. [Preferences and dialog polish](../2026-10-01_ui-preferences-dialog-polish/1_exploration.md): extend its hierarchy,
   spacing and control-state principles to secondary windows.

User-confirmed delivery: implement all four parts sequentially in the existing `codex/ui-visual-polish` branch and
`D:/openscad/wt-openscad-ui-visual-polish` worktree. Do not create separate branches or worktrees for these parts.
Apply #6776 first, then #1 foundation/typography, #2 icon system, #3 Customizer, and #4 Preferences/dialogs.
The separate briefs are organizational boundaries within one cumulative implementation, with reviewable commits.
This sequencing decision does not itself start implementation.

## Intent and boundary

Improve OpenSCAD's visual coherence: toolbar icon scale, Customizer headers, light/dark icon treatment,
Windows Qt style integration, and the appearance of secondary windows. Begin with evidence and patterns.
Keep button order, pane arrangement, menus, parameter order, keyboard behavior and workflows intact.
User-approved scope extension: replace inline Customizer explanatory text with a discreet help icon and tooltip,
and capitalize displayed labels. Preserve access to the explanations for keyboard and assistive-technology users.
Improve typography, hierarchy, whitespace, consistent icons and correct use of existing theme colors and widget states.
Keep Qt's selected platform style and native chrome. No custom window/dock chrome, global reskin, replacement style,
fixed light/dark palette, or bespoke control borders/radii. Navigation redesign is excluded.

The original generated concepts exceeded these constraints. Retain them as historical exploration only; their chrome,
border and control-skin changes are not proposals for implementation. Screenshot observations remain valid evidence,
but noticing a native-style difference does not authorize overriding it.

## Workspace and reproducibility

- Worktree: `D:/openscad/wt-openscad-ui-visual-polish`.
- Branch: `codex/ui-visual-polish`; push remote `origin`; nothing pushed.
- Base: freshly fetched `upstream/master`, `464e25dad0c01af5488375c15aa6734190531eb5`.
- Shared clone: `D:/openscad/openscad-master`; main checkout and occupied worktrees preserved.
- Recursive submodules initialized and matching; source was clean before applying #6776. No checkout-local AGENTS.md found.
- Managed worktree creation targeted the workspace control repository and failed on missing `upstream/master`.
  Used the workspace's explicitly prescribed Git worktree workflow against `openscad-master` instead.
- Submodule initialization required adding Git's existing `usr/bin` and `mingw64/bin` to this command's PATH.
- Plans and evidence remain outside the upstream-facing checkout. PR #6776 compilation checks are recorded separately;
  no commit, published PR or recurring task created.

## Evidence

[Open visual review gallery](../../../artifacts/ui-visual-polish/2026-10-01/index.html).
All originals and generated concepts are under `artifacts/ui-visual-polish/2026-10-01/`.
B01-B10 are original JPEG captures, not generated reconstructions. Context captures duplicate some dialog views.
B11 is the user's supplied PNG reference from the last release, with exact version/style unverified.

| ID / file in baseline/ | Build and surface |
| --- | --- |
| B01 `01-main-light.jpg` | Running 2026.09.27, git `cc19000e`; user's filament rack; Customizer and Console |
| B02 `02-preferences-3d-context.jpg` | Same build; Preferences in context |
| B03 `03-preferences-3d.jpg` | 3D View Preferences |
| B04 `04-preferences-advanced.jpg` | Advanced Preferences |
| B05 `05-preferences-3d-print.jpg` | 3D Print Preferences; no service credentials entered |
| B06 `06-preferences-editor.jpg` | Editor Preferences |
| B07 `07-preferences-dialogs.jpg` | Dialogs Preferences |
| B08 `08-experimental-main-light.jpg` | Latest staged experimental build; controlled bracket fixture |
| B09 `09-build-info-context.jpg` | Experimental build information in context |
| B10 `10-build-info.jpg` | Experimental build information dialog |
| B11 `11-release-customizer-user-reference.png` | User-supplied last-release Customizer; reference for visual restraint |

The experimental binary is
`artifacts/20261001-shared-rebuild/attempt-1/staging/openscad.exe`, version
`2026.10.01-experimental-20261001-shared-rebuild`, git `31b1430530c295c4b24662b2d5a4b989bbbabc7d`.
The running dialog confirms Windows 11 (10.0.26200), Qt 6.11.1 and QScintilla 2.14.1.
This composition includes prior shortcut and dynamic-theme work; it is not the new feature's upstream base.

Fixture: `artifacts/ui-visual-polish/2026-10-01/ui-study.scad`. Open it, Preview (F5), then View All.
The editor was already hidden in the user's stored layout and remains hidden in the study.
No user design was edited. Original Preferences tab was restored and the dialog closed.
The user ended Computer Use and requested finishing with existing screenshots. No further captures were attempted.
The study application remains open. An empty installed OpenSCAD window opened by the launch helper may also remain;
cleanup was interrupted, so it is not recorded as closed.

Both captured application themes are light. A dark viewport is a separate setting, not evidence of dark widgets.
The exact runtime QStyle object name and monitor scaling were not instrumented. The user's `windows11` diagnosis
remains an investigation lead; appearance alone does not establish the active style or its root cause.
Initial occluded capture was rejected and not retained. The cursor glow is capture/input feedback, not a UI defect.

## Concrete visual issue inventory

Observed items below are visual judgments grounded in the named captures, not claims of measured accessibility failures.
Priority H means address early; M means polish after the shared foundation.

| ID | Evidence | Concrete issue | Pattern / priority |
| --- | --- | --- | --- |
| V01 | B01, B08 | Toolbar symbols occupy a small optical area compared with text and available window space. | Icon metrics / H |
| V02 | B01, B08 | Cube, magnifier, axis and document symbols have noticeably different stroke density. | Icon family / H |
| V03 | B01, B08 | STL/DXF lettering is compressed into tiny document symbols and loses clarity at viewing scale. | Small-size glyph design / M |
| V04 | B01, B08 | Selected view toggles combine dense dark glyphs with saturated blue tiles. | Foreground/state pairing / H |
| V05 | B03-B07 | Glossy illustrated Preferences icons clash with the main window's monochrome line icons. | Shared icon family / H |
| V06 | B03-B07 | Preferences category icons have inconsistent optical size and silhouettes. | Icon metrics / M |
| V07 | B01 | Black header text and black disclosure triangles on dark blue have weak visual contrast. | State/contrast / H |
| V08 | B01, B08 | Every expanded section receives a strong blue fill, making expansion look selected. | State semantics / H |
| V09 | B08 | Header text is white, but the disclosure chevron remains dark against blue. | Foreground/state pairing / H |
| V10 | B01, B08 | Section headings sit in shallow rows with little vertical breathing room. | Header metrics / H |
| V11 | B01, B08 | Dock title bars use grey boxed strips that differ from the rounded fields below. | Surface/border consistency / M |
| V12 | B01, B08 | Dock close glyphs and titles are very small and crowded against the pane edges. | Chrome metrics / M |
| V13 | B01 | Long Customizer descriptions crowd the next parameter or section boundary. | Spacing rhythm / M |
| V14 | B01, B08 | Label, description, slider and next-row gaps lack a consistent visual rhythm. | Component spacing / H |
| V15 | B01, B08 | Description text has nearly the same visual intensity as parameter values. | Typography hierarchy / M |
| V16 | B01 | Adjacent numeric fields are tightly stacked, forming a striped grid with little separation. | Field metrics / M |
| V17 | B01, B08 | Thin full-width grey slider rails dominate compared with small knobs and labels. | Control balance / M |
| V18 | B01, B08 | Preset plus/minus/ellipsis buttons have weakly drawn symbols and faint boundaries. | Small control/icon states / M |
| V19 | B04-B06 | Dark group-box outlines draw more attention than their section titles and fields. | Border hierarchy / H |
| V20 | B04-B06 | Spinboxes, editable fields and dropdowns have visibly different border/height treatments. | Shared control metrics / H |
| V21 | B03-B07 | Selected category blue blocks are much stronger than the quiet selection in lists. | Selection vocabulary / M |
| V22 | B07 | One dark outline encloses nearly the entire empty dialog, making framing the dominant feature. | Border hierarchy / M |
| V23 | B01, B08 | Console title, content boundary, toolbar edge and status edge stack multiple horizontal rules. | Separator policy / M |
| V24 | B10 | Dense information text has little line separation; label/value emphasis varies with wrapping. | Typography/vertical rhythm / M |

The sparse Preferences pages and varying form alignment were also noticed. Moving controls, replacing the category
toolbar with a sidebar, or inventing preview content would be UX work and is deliberately excluded here.

## Reported issues and untested states

- Dark-mode icons: reported by the user, not reproduced in a captured dark application session.
  Current upstream already contains `resources/icons/chokusen-dark/index.theme` and `icons-chokusen-dark.qrc`.
  `src/openscad_gui.cc:135` selects `chokusen-dark` or `chokusen` in `setGlobalTheme()`.
  Investigate coverage, direct resource icons, theme selection and refresh, rather than replacing everything blindly.
- `windows11` style: compare with Fusion under the same build, font, display scale and palette before assigning cause.
- Pending visual states: hover, keyboard focus, pressed, checked, disabled, inactive window and high contrast.
- Pending theme cases: dark startup, light-to-dark and dark-to-light, existing dialogs, multiple main windows.
- Pending DPI cases: 100%, 125%, 150%, 200% and moving between mixed-DPI monitors.
- Pending surfaces: visible editor/search, actual PDF/3MF/SVG export dialogs, Welcome, error/progress display,
  animation, Viewport Control, font/color dialogs and any newer AI UI. These are audit targets, not confirmed defects.

## Grouped design direction

1. **Typography and hierarchy.** Inherit the platform/user font. Differentiate headings through modest weight and
   whitespace before considering color. Preserve readable descriptions; do not misuse disabled/placeholder colors
   for enabled explanatory text. Prefer QFont APIs over font-only stylesheets.
2. **Whitespace.** Start from Qt layout/style spacing and size hints, then add deliberate section separation and
   description-to-field spacing. Avoid global fixed heights or a new radius/border system. Keep order and placement.
3. **Consistent icons.** Use Tabler SVGs, with OpenSCAD-owned matching icons for coverage gaps (user decision).
   Preserve complete semantic coverage of existing uses. Compare 20/24/28 logical-pixel sizes in native toolbars, with matched
   optical weight and light/dark/state coverage. Let Qt paint their buttons.
4. **Correct states.** Customizer expansion should not imply a selected/checked button. Aim for the same native
   resting appearance open and closed, with the disclosure arrow reporting expansion. Preserve keyboard behavior,
   saved state and accessible expanded/collapsed semantics. Preferences genuinely needs a current-category cue.
5. **Theme roles.** Prefer inherited Window/WindowText, Base/Text and Button/ButtonText pairs where appropriate.
   Highlight/HighlightedText belong together for actual selections; Accent is not a general section background.
   Do not override the application Highlight role to make one widget quieter. Keep the viewport palette separate.

## Native Qt investigation, following user review

Current feature-base source confirms:

- `src/gui/parameter/GroupWidget.cc:14` makes the header checkable; line 41 maps expansion to checked state.
  The same constructor explicitly sets group layout spacing and margins to zero (lines 18-22).
  These are OpenSCAD decisions, with direct opportunities for improvement without reskinning Qt.
- Preferences categories are checkable actions in `Preferences.ui:3245` onward, grouped in
  `Preferences.cc:249`; they are toolbar buttons rather than QTabBar tabs. The first category is checked at line 372.
  Removing selection indiscriminately would lose meaningful current-page feedback. A native tab representation in
  the same location would be a separate proposal, not an approved change or a guaranteed appearance improvement.
- Those category icons use direct PNG resources such as `:/icons/prefs3DView.png`, while the main icon theme has a
  dark variant. Replacing this mixed artwork and routing it consistently is an application-owned improvement.
- `OpenSCADApp.cc:116` applies the application font through a global stylesheet; `ParameterWidget.cc:472` applies
  a Customizer font stylesheet. Compare existing #6776 work before any cleanup; the experimental build differs.

[Qt 6.11.1 Windows 11 style source](https://raw.githubusercontent.com/qt/qtbase/v6.11.1/src/plugins/styles/modernwindows/qwindows11style.cpp)
uses an accent fill for checked tool buttons unless an explicit Button brush overrides it. This explains the likely
shared mechanism behind blue Preferences categories and rollup headers. Auto-raise alone does not remove checked fill.
Closed combo-box drawing clears the checked flag, so actual dropdowns require a separate investigation of closed,
focused and popup-selected states. The captured executable's active style still needs runtime confirmation.

[Qt palette roles](https://doc.qt.io/qt-6/qpalette.html#ColorRole-enum) provide semantic color pairs, not arbitrary design
tokens. [QWidget palette documentation](https://doc.qt.io/qt-6/qwidget.html#palette-prop) warns that styles may ignore
roles and that palette overrides should not be combined with stylesheets. A local palette override is a testable
option only where the control honors it and all states remain correct; copying theme colors once can freeze them.
Do not promise a muted selected-tab fill without establishing an acceptable native mechanism.

Reclassify V11/V12/V23 as native-chrome observations with no redesign proposed. V17/V19/V20/V22 are diagnostic:
first distinguish native rendering from application overrides or layout misuse. They do not justify custom painting.

## Additional findings and constraints, 2026-10-01

The Customizer rollup is OpenSCAD's `GroupWidget` composite, not a Qt checkbox or a stock Qt accordion. Its header
is a checkable QToolButton. `setExpanded()` calls `setChecked()`, so Qt receives a checked-button state and paints
the button surface accordingly. Checkbox indicator styling is not being reused. Use a normal disclosure button
with separately held expansion state as the first prototype, keeping native painting and accessible expansion.

Preferences likewise implements category navigation using checkable toolbar actions and a QStackedWidget.
`Preferences::addPrefPage()` registers action-to-page mappings; `actionTriggered()` changes the stack. This is an
OpenSCAD choice, not a requirement of Qt. Qt provides QTabBar/QTabWidget for actual tabs. Convenience as the original
author's motivation is unverified. A native tab-bar comparison may preserve category order and location, but its
keyboard behavior, labels, sizing and overflow need review before adopting it; no navigation redesign is authorized.

### Stylesheet-free foundation

No new `setStyleSheet()` calls or Designer `styleSheet` properties. Use QFont and widget/layout APIs, inherited
palettes, native size hints and style metrics. Moving a custom skin into C++ painting would still violate the scope.

[PR #6776](https://github.com/openscad/openscad/pull/6776) is the relevant cleanup/dynamic-theme foundation;
[#6796](https://github.com/openscad/openscad/issues/6796) is a policy discussion, not a removal PR. The captured
experimental build already includes #6776. Its committed local integration is
`8e4a30f86716c8a7cd93bcbff1cd33249bd110fa` on `codex/pr-6776-dynamic-dark-mode-switching`.
That integration still has the original checked GroupWidget implementation. Its worktree contains unrelated local
edits; do not incorporate those silently. In the visual-polish worktree, original upstream #6776 head
`aab4aed030dd61b80c5f850177f2af93e067eb7d` and the saved MSVC stream-declaration repair are now applied and staged.
All 13 changed C++ files plus InitConfigurator compile successfully. Full executable and runtime GUI verification
remain pending; see the integration evidence above. Typography implementation has not started.

The PR is not complete stylesheet eradication. A source search of the committed local integration still finds uses
in ColorLabel/ColorList, LaunchingScreen, QWordSearchField, input configuration widgets, ParameterCheckBox and AI UI.
Track that remaining cleanup explicitly instead of assuming the PR makes the application stylesheet-free.

### Proposed whitespace rules

Start with native horizontal/vertical layout spacing and content-margin metrics, not a universal fixed-pixel grid.
Let `S` mean the resolved native vertical spacing for the relevant layout; let Qt resolve control-specific spacing
when its style returns a sentinel rather than treating that value as a pixel count.

- Keep a label, its help icon and its control visually together: approximately half S within the parameter.
- Use S between distinct parameters and approximately twice S between sections. These are prototype targets.
- Give section headings modest font weight and symmetric vertical breathing room; expansion changes the arrow,
  not the resting background color. Inherit font family and size unless the user configured them explicitly.
- Apply outer native content margins once per container; avoid doubled nested margins and the current blanket zero
  spacing. Preserve deliberate zero margins needed for edge-to-edge native containers.
- Align common label/control edges and allow tooltip descriptions to wrap. Control heights follow native size hints and
  font metrics; no fixed-height clipping or blank space added to fill sparse pages.
- Recompute derived spacing when font/style changes; verify translations, scaling and keyboard focus later.

### Release-reference refinement: quieter rows and contextual help

User supplied B11 as the quieter appearance of the last release. Its compact rows, plain controls and pale header
fills keep attention on parameters. The expanded header is somewhat stronger than the closed headers, but much less
dominant than the saturated checked-button fills in the newer captures. Use its restraint as the design reference;
do not hard-code the old light-blue colors or reproduce a legacy control skin.

Confirmed design requirements:

- Move each option's explanatory text out of the persistent row into a discreet question-mark help icon beside its
  label. Show the full explanation in a native tooltip on hover. Only show the icon when an explanation exists.
- Use a small Tabler help symbol with theme-aware contrast and a usable interaction target; avoid an accent-filled
  button. Make the help available through keyboard focus/activation and accessible description as well as hover.
  Preserve full explanatory content, units and examples; long descriptions must remain readable.
- Capitalize displayed Customizer text in sentence case: `show doorframe` becomes `Show doorframe`, `swap boards`
  becomes `Swap boards`. Preserve existing acronyms, proper names and intentional casing beyond the initial letter;
  do not apply title case to every word. This is presentation formatting, not renaming SCAD variables, preset keys,
  user-entered values or enumeration values. Apply the same convention to application-owned Customizer captions.
- Keep section headers quiet in both states, use the disclosure arrow for expansion, and maintain readable label
  hierarchy without restoring large saturated backgrounds.

Review the existing `Show Details` modes when implementing contextual help so they do not duplicate inline text or
make the explanation inaccessible. Any broader removal/reorganization of that selector remains outside this change.
The #6776 prerequisite still applies before source implementation. This update records the design; no source changed.

### Existing icon-set investigation

Inventoried all 64 unique light Chokusen SVG names (dark mirrors excluded), Designer icon references and C++ icon
loads. Added 17 direct-resource/system-name candidates, including all ten Preferences artwork names, status/close/
stop icons and `emblem-unreadable`. Features and AI currently share Preferences artwork. Preserve OpenSCAD and
OctoPrint branding and native Qt window/dialog chrome rather than counting them as replacement glyphs.

The full per-name candidate map is in
[`icon-coverage.json`](../../../artifacts/ui-visual-polish/2026-10-01/icon-coverage.json).
All proposed Tabler filenames were verified against its official repository tree at
`74929e50416e2b7c0abb8368cdc74bdcb2560ab6` (5166 outline filenames), saved alongside as `tabler-outline-catalog.txt`.
This verifies existence, not optical or semantic suitability. Coverage counts for Chokusen are 33 straightforward
stock candidates, 13 requiring semantic review and 18 gaps requiring custom coverage. The user selected Tabler as
the icon family and authorized implementing our own matching icons for the gaps. Individual mappings still need
semantic and visual validation; generic placeholders are not approved replacements.

| Family | License / form | Assessment |
| --- | --- | --- |
| [Tabler](https://github.com/tabler/tabler-icons) | MIT; 24-unit SVG grid, 2-unit strokes | Selected by the user; extend with matching OpenSCAD-owned icons for gaps. |
| [Lucide](https://lucide.dev/license) | ISC; inherited Feather artwork has MIT notices | Coherent general application family; ruler-dimension-line exists. Full OpenSCAD coverage not established. |
| [Material Symbols](https://github.com/google/material-design-icons) | Apache-2.0; optical sizes and weight variants | Useful optical-size alternative; complete CAD-action mapping not established. |

Tabler gaps: no verified six-face camera family, distinct surface/edge/wireframe/thrown-together family, or dedicated
3MF/CSG/DXF/OBJ/OFF/POV/STL/WRL file-type symbols. PDF/PNG/SVG do exist. Generic cubes and export arrows in the map
are placeholders documenting collisions, not acceptable substitutes. Preview versus render and projection/reset
semantics also need visual review. Complete coverage will combine stock Tabler icons with our own gap icons, matching
its grid, stroke weight, line caps/joins and optical balance. Preserve distinct action meanings and retain the stock
icons' license notices and provenance. The gaps no longer block choosing the family; filling them is implementation
scope, after the #6776 prerequisite.

Icon selection must include enabled/disabled, checked/unchecked, light/dark and selected-background contrast.
An SVG using `currentColor` does not by itself establish Qt palette integration. Validate the QIcon loading/rendering
path and live palette changes; avoid merely baking one light and one dark foreground into unrelated call sites.

## History investigation: origin and intent of the Customizer appearance

Investigated Git history and upstream discussions on 2026-10-01. The evidence points to changed Qt rendering of
longstanding widget states, compounded by stylesheet interactions, rather than an OpenSCAD decision to make expanded
headers strongly accent-colored. The exact first affected nightly was not bisected, and B11's runtime style remains
unverified. Distinguish those limits from the source history below.

- `2db79cf7c41f1e6b6d29bd9c2a547174dd00b467` (2016-07-27) introduced parameter groups with a checkable
  QToolButton from the outset. They were never QCheckBox headers.
- `5c89af78a0a75304dff5862ebcde99e791bd847b` (2017-11-01), titled "removed the headline, make the button full
  width", deliberately removed the separate horizontal rule and borderless-button stylesheet. Adjacent commits
  explicitly aimed to minimize spacing. These choices predate the released appearance in the user's reference.
- The `openscad-2021.01` tag already uses a full-width checkable header, checked state for expansion and zero outer
  spacing. It contains no prescribed pale-blue header palette. The quiet released appearance came from the style
  rendering those controls, rather than an old OpenSCAD pale-blue theme that was subsequently replaced.
- `562d0b42a97eef28e7de8708bd52c0d532d22558` (2021-04-27) refactored the Customizer to persist per editor and
  manage named parameter sets. It retained the checked-button header and added explicit zero content-layout spacing.
  `1e9a3c4c8c3d3295b122154d654e368104a5a311` (2021-04-29) introduced typed parameter constraints and independent
  control widgets, including shared description widgets and four-pixel parameter side margins. These were functional
  refactors with layout effects, not a saturated-header color design.
- [Qt 6.7 release notes](https://doc.qt.io/qt-6/whatsnew67.html#qt-widgets-module) explicitly introduce Windows 11
  style as the default on Windows 11, with dark-mode support. Its checked tool buttons use accent fills.
- [OpenSCAD PR #6562](https://github.com/openscad/openscad/pull/6562), merged 2026-01-25, makes Qt 6 the default
  across all platforms. Commit `13de4908b3ee6aeff209e247235de86a9ebab57b` also switches Windows release script
  setup to Qt 6. The PR has no explanatory body or issue comments documenting a Customizer visual redesign.
- In [#6991](https://github.com/openscad/openscad/issues/6991#issuecomment-5503244638), Jordan Brown explains that
  OpenSCAD delegates presentation to Qt and that the color follows the Windows accent. The discussion treats the
  unreadable foreground as a bug, rather than defending strong header fills as a deliberate Customizer design.
- [The diagnosis](https://github.com/openscad/openscad/issues/6991#issuecomment-5532214677) identifies inherited
  stylesheets resolving ButtonText and bypassing Qt's checked-button foreground choice. Removing them via #6776
  fixes the label but exposes a separate arrow-color problem. Jordan Brown
  [confirmed the two stylesheet removals](https://github.com/openscad/openscad/issues/6991#issuecomment-5886043694)
  on 2026-09-29 and also observed an unexpected text-alignment change. Thus even font-only QSS has affected painting.
- [PR #6999](https://github.com/openscad/openscad/pull/6999) is an unmerged contrast repair, not the cause of the
  changed background. #6776 is a theme-inheritance repair, not a plan to reintroduce the old lighter header fill.

Descriptions and casing also predate the recent visual change: the 2021.01 source already supports descriptions as
tooltips when details are hidden and formats names by replacing underscores with spaces without capitalization.
The new help-icon requirement improves discoverability of an existing presentation option; sentence case is a new
requested polish rather than restoration of a removed capitalization rule.

Retrieved issue-comment evidence, including authors and direct links, is preserved in
`artifacts/ui-visual-polish/2026-10-01/customizer-history-issue-6991.json`.

## Historical image concepts

Historical concepts, superseded as implementation targets by the native-Qt constraints above.
Generated with the built-in image_gen tool from real captured references. Full prompts, including corrections,
are retained in `artifacts/ui-visual-polish/2026-10-01/prompts.json`.

| Concept | File in concepts/ | Intended evaluation |
| --- | --- | --- |
| A: light | `01-main-light.png` | Neutral section headers, consistent fields, restrained pane borders |
| B: dark | `02-main-dark.png` | Dark surfaces, light glyphs/text, coherent controls and neutral headers |
| C: Preferences | `03-preferences-light.png` | Unified icon language, softened group outlines and better heading hierarchy |

These are visual direction studies, not exact widget specifications. Generated toolbar glyphs, tiny text and log
content are approximate; do not turn them into replacement icon assets or copy altered text. Main-window studies
preserve the broad pane structure and parameter order but vary row spacing. Exact production geometry remains based
on the originals. The full-window concepts do not adequately settle the toolbar size decision: make a real
20/24/28-pixel icon comparison in the next design pass before implementation.

The first light attempt moved sliders inline and changed a value; it was rejected. The revised light image restored
slider placement but changed the viewport to white. `01-main-light-draft.png` retains that rejected intermediate;
the final `01-main-light.png` restores the dark viewport. No viewport scheme change is proposed.

## Related work and likely implementation boundaries

Read the existing investigation before implementation:
`openscad-6991/.plans/2_in-progress/2026-09-02_customizer-theme-behavior/1_exploration.md`.
It describes checked QToolButton headers, palette inheritance and dynamic theme work. Its root-cause findings are
historical context, not newly verified behavior of every build in this audit.

Do not merge or overwrite the occupied #6999 header-contrast or #6776 dark-mode worktrees. Compare their changes first.
Likely source areas are `src/gui/parameter/GroupWidget.*`, parameter control widgets, `src/gui/MainWindow.*`,
`src/gui/Preferences.*`, `src/gui/OpenSCADApp.cc`, `src/openscad_gui.cc` and `resources/icons/`.
No application source was edited during this exploration.

If implementation is requested, keep reviewable patches separate: icon metrics/assets; expansion-state semantics;
native font/palette inheritance; whitespace and typography. Capture the same fixture and
states before/after each patch. Check native keyboard and accessible expansion semantics when changing header paint.

## Next design pass

Use existing screenshots for constrained studies: typography/spacing only, icon artwork/size only, and rollup state
only. Leave native chrome and control painting intact in each comparison. Actual Qt prototypes will be needed to
validate palette/state behavior; generated images cannot establish what native styling can produce.
Further screenshot capture is deferred until requested. No application source was changed in this review.
Future work can fix forward, replan, restart a design attempt, or supersede it while retaining this evidence.
