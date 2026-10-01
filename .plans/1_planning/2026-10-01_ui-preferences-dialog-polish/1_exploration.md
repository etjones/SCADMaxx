# Preferences and secondary-dialog polish

Status: planning. Apply the accepted Customizer's restrained hierarchy to other existing surfaces.
Delivery: part 4 of 4, after Customizer validation, on `codex/ui-visual-polish` in
`D:/openscad/wt-openscad-ui-visual-polish`. No separate branch or worktree for this part.
Shared evidence: [UI visual polish](../2026-10-01_ui-visual-polish/1_exploration.md).
Dependencies: [Qt/font foundation](../2026-10-01_ui-qt-foundation-typography/1_exploration.md), including #6776,
and [shared icon treatment](../2026-10-01_ui-icon-system/1_exploration.md).

## Outcome

Make Preferences and secondary windows coherent through typography, spacing, artwork and appropriate Qt states,
while preserving native chrome, control order and existing workflows.

## Targeted improvements

| Observed issue | Proposed treatment | Limit |
| --- | --- | --- |
| Preferences' strong selected category tile | Evaluate native QTabBar in the same location/order; compare native selection behavior. | Current toolbar buttons genuinely convey current page; don't remove the cue or repaint it arbitrarily. |
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

Tab-bar and flat-group-box treatments are implementation candidates to compare, not accepted visual guarantees.
Validate current-page visibility, keyboard access, translations, font changes, light/dark states and DPI. The earlier
window-frame/dock-chrome observations remain out of scope. No source edits or builds started for this brief.
