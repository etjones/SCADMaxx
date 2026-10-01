# Preferences and secondary-dialog polish

Status: implemented and verified; final handoff is in [implementation results](5_post-implementation-notes.md).
The feature remains in-progress pending the user's completion review. Final feature in the four-part UI plan.
Apply the accepted Customizer's restrained hierarchy to other existing surfaces.
Delivery: part 4 of 4, after Customizer validation, on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. No separate branch or worktree for this part.
Shared evidence: [UI visual polish](../../1_planning/2026-10-01_ui-visual-polish/1_exploration.md).
Dependencies: [Qt/font foundation](../../3_done/2026-10-01_ui-qt-foundation-typography/1_exploration.md), including #6776,
and [shared icon treatment](../../3_done/2026-10-01_ui-icon-system/1_exploration.md).
Icon implementation is complete at `67101788f`; reuse `Icons` and `StatusMessageBox` without another renderer.
Quiet Customizer is implemented through `b22167be9`; see its
[results](../../3_done/2026-10-01_ui-customizer-polish/5_post-implementation-notes.md) for native styling,
font/spacing and palette evidence. Review this feature's own scope before implementation.

## Outcome

Make Preferences and secondary windows coherent through typography, spacing, artwork and appropriate Qt states,
while preserving native chrome, control order and existing workflows.

The foundation part supplies the shared application font and dialog font inheritance first. This part reuses that
foundation for per-dialog hierarchy and layout corrections; Console and editor content fonts remain independent.
Foundation is now implemented and Windows-verified, including removing fixed sizes from axis/update-status labels
and preserving experimental-feature emphasis without fixing its font family/size. Avoid duplicating these changes.

## Targeted improvements

| Observed issue | Proposed treatment | Limit |
| --- | --- | --- |
| Preferences' strong selected category tile | Replace with an approved native QTabBar in the same location/order. | Preserve current-page indication and native rendering; no custom selected fill. |
| Glossy/mismatched category artwork | Use shared Tabler/custom SVGs with consistent optical size. | Owned by icon-system work; don't create a second icon loader. |
| Bold/dense headings and uneven forms | Apply accepted regular/medium font hierarchy, aligned label/control edges and consistent row/group gaps. | Preserve explicit font preferences and existing control order. |
| Oversized or dominating group outlines | First remove inherited QSS effects; evaluate QGroupBox flat property with native rendering and better title spacing. | Retain native outlines if flattening obscures grouping; no hand-painted replacement borders. |
| Inconsistent field heights | Remove accidental fixed sizes/margins; use size hints and common font inheritance. | Native differences between control types are not automatically defects. |
| Sparse pages dominated by empty frames | Use content-driven layout sizing and restrained native group presentation. | Don't invent content or relocate settings to fill space. |
| Dense build-information/status text | Use clearer label/value emphasis and paragraph/row spacing; shared status icons. | Preserve content, copying behavior and native dock/status chrome. |

## Delivery and validation

Prototype Preferences first with the existing captured pages (3D View, Advanced, Editor, 3D Print and Dialogs).
Follow with export, information and other dialogs only after their actual appearance has been inspected; they are
audit targets, not all confirmed defects. Use separate patches by surface, not one sweeping dialog rewrite.

The native tab bar is approved. Flat group boxes remain a per-surface implementation candidate, not a blanket rule.
Validate current-page visibility, keyboard access, translations, font changes, light/dark states and DPI. The earlier
window-frame/dock-chrome observations remain out of scope. No source edits or builds started for this brief.

## Readiness review — 2026-10-01

Source baseline is the completed Customizer head `b22167be9`; source worktree is clean. Reviewed the current
Preferences screenshot, category construction in Preferences.cc, native group boxes in Preferences.ui and remaining
dialog styling. Foundation font inheritance and all icon replacements are already delivered and must not be repeated.

Confirmed findings:

- Category selection uses QActionGroup and checkable toolbar actions. Current-page indication is meaningful here;
  merely clearing checked state would be wrong. The user approved replacement with a native QTabBar.
- Categories vary with updater/experimental compile flags and the live AI feature flag. Any replacement must preserve
  order, conditional visibility, action-triggered page selection, accessible labels, keyboard access and overflow.
- Advanced contains numerous native group-box borders and uneven form alignment. Use style-derived gaps, content
  sizing and inherited normal/medium typography; evaluate native flat groups per surface, not a global replacement.
- Welcome still calls setStyleSheet; AI DiffDialog has styled apply/discard buttons; About HTML fixes paragraphs at
  9pt. These are concrete audit targets beyond Preferences, not evidence that every dialog needs rewriting.
- Standard OS file/font/color dialogs and window/dock chrome remain native. Editor/Console content typography,
  code/diff syntax colors, viewport output and user-authored data are outside the visual-polish scope.

The user approved native tabs and the full application-owned UI audit, including Welcome and optional AI surfaces.
No unresolved product decisions remain. See [requirements and inventory](2_requirements.md) and
[sequential plan](3_overall-plan.md). No build, prototype or source modification was performed during this review.

The expanded source audit also found stylesheet calls in AI chat/bubbles, input calibration/status widgets and the
word-search field. Include those in the final inventory rather than treating Welcome/DiffDialog as an exhaustive list.
Inspect actual rendering before deciding fixes; preserve semantic status information and code/content colors.

Acceptance must include actual Windows11 light/dark screenshots, simulated 100/125/150/200% scales, enlarged UI fonts,
long/translated labels, conditional categories, page selection, focus/default/escape behavior and live palette/font
changes. Test optional surfaces offline where constructible; record unavailable configurations instead of claiming
runtime coverage. Preserve setting semantics, button order and content copying. Complete the final cumulative UI
handoff only after this feature and its regression checks pass; do not enable build readiness during planning.
