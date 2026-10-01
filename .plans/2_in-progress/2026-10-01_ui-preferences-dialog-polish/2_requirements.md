# Preferences and secondary-dialog polish — requirements

Status: implemented; acceptance evidence and explicit coverage limits are in `5_post-implementation-notes.md`.
Final feature of the four-part UI plan.
Use the existing `codex/ui-visual-polish` branch/worktree after Customizer commit `b22167be9`.

## Native Preferences tabs

- Replace category toolbar presentation with QTabBar in the same top location and category order. Retain category
  names and the completed icon family; start with the existing 32 logical-pixel category icon size. Let Qt render
  native tabs, selection, focus and overflow; no QSS or custom fill, border, tab painting or window chrome.
- Preserve one selected page, existing action-triggered navigation and settings behavior. Conditional categories
  must follow compile flags and live feature visibility. Keep the current page when it remains available; if it is
  removed, select the nearest preceding available category, or the first available category if none precedes it.
- Use native tab keyboard/accessibility conventions. Tabs cannot be rearranged or closed. Preserve category order
  under overflow and long translations; no sidebar conversion or relocation of settings.

## Layout and typography

Reuse inherited application/dialog fonts, existing normal/medium hierarchy, native size hints and UIUtils spacing.
Correct observed alignment, accidental fixed dimensions, excessive empty frames and cramped spacing. Try native
flat groups only where grouping remains clear; retain native framed groups where they communicate relationships.
Do not flatten every group, suppress selection, relocate controls or reorder buttons to achieve the visual result.
Preserve explicit user fonts, mnemonics, focus order, default/escape actions, content and copying behavior.

## Full audit boundary and initial inventory

Every application-owned GUI surface is an audit target. Change only demonstrated visual/style defects; record each
surface as fixed, inspected with no change, or unexercised with the reason. Expand this inventory if discovery finds
additional surfaces. Optional service dialogs can be constructed with local fixtures; no credentials or requests.

| Surface | Initial evidence / audit focus |
| --- | --- |
| Preferences: every available page, including input and AI | Native tab replacement; form hierarchy, gaps, borders and overflow |
| PDF, 3MF, SVG export | Inspect actual native layouts, long labels, hints and buttons |
| Print initialization and OctoPrint authorization | Inspect labels/status/grouping offline; preserve actions |
| About, library/build information | About HTML fixes paragraphs at 9pt; inspect inherited font, wrapping and copying |
| Welcome | Existing stylesheet; inspect native replacement and preservation of branding/content |
| AI chat, bubbles and diff dialog | Existing hardcoded styles; inspect control/border/font/palette treatment offline |
| Input axis/button/mouse configuration | Existing stylesheet-driven status displays; retain distinguishable status meanings |
| OpenCSG warnings, message boxes, progress and error displays | Reuse shared status provider; inspect layout and semantics |
| Font/color lists, viewport controls, animation, search and other app-owned auxiliary panels | Audit remaining control styling, including QWordSearchField; avoid repeating completed work |
| Main window and Customizer | Regression audit of completed typography, icons and quiet Customizer |

Replace residual presentation stylesheets in audited controls with ordinary Qt APIs where applicable. Preserve
semantic indicators and code/diff content colors; do not equate all color with unwanted styling. No replacement
Qt style or custom skin. Native OS file/font/color dialogs, window/dock chrome, editor/Console content typography,
viewport rendering and user-authored data remain unchanged. Application-owned controls around those surfaces are
within the audit. Optional unavailable configurations must be reported, never silently treated as tested.

## Acceptance and completion

Windows11 light/dark; simulated 100/125/150/200%; enlarged fonts; long labels; keyboard/accessibility; live palette
and font changes; all tab selection paths and conditional visibility. Preserve setting values and dialog results.
Use focused behavioral tests and screenshots of actual widgets. Cross-platform runtime, physical mixed-monitor
movement and external service/hardware integration remain outside the agreed acceptance and must be identified.

No product questions remain. Per-surface visual decisions are implementation work within these rules. At completion,
record exact source/delta/dependencies, tests and screenshot coverage, private-origin retention and the cumulative UI
readiness decision. A finished audit requires a disposition for every discovered surface, not a claim of universal
runtime coverage. Do not mark the cumulative source ready before required checks and handoff are complete.
