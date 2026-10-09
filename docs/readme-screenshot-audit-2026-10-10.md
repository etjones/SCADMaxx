# README screenshot audit, 2026-10-10

All 20 unique README image references, including commented slots and comparison baselines, were
checked against the coordinated UI integration. README prose and image-slot activation are unchanged.
The contact sheet and capture evidence are in `D:/openscad/runs/ui-consistency-2026-10-10`.
Current captures must use final integration `659f5abf0e8959bc03c62155b436b1b6b44a8aca`.

| Image | Finding / action |
| --- | --- |
| agent-access.png | Connection dialog still represents the feature; no changed dock title is shown. Retain. |
| annotations.png | Annotation demonstration remains valid; refresh recommended for current chrome/toolbar styling. |
| openscad-skill.png | Missing commented slot, already documented. Requires a real permitted agent demonstration; do not fabricate it. |
| ui-after.png | Replaced from final shipped integration: matched bracket/camera/theme, selected E dock/group hierarchy. |
| ui-before.png | Historical upstream comparison baseline. Retain its original provenance. |
| preferences-before.png | Historical upstream comparison baseline. Retain its original provenance. |
| preferences-after.png | Replaced: actual Advanced groups and category selection from final shipped integration. |
| navigation-cube.png | Tight crop still depicts the same controls. Retain. |
| model-inspection.png | Feature state remains illustrative; cosmetic refresh recommended for the new Inspector title. |
| live-sections.png | Direction/position controls remain illustrative; cosmetic refresh recommended for the new dock title. README text about removed rotation handles is stale. |
| contextual-insertion.png | Real preview remains illustrative; cosmetic refresh recommended for the new dock title. |
| vim-editor.png | Visual-line example remains illustrative; cosmetic refresh recommended for the new Editor title. |
| launcher.png | Separate application unaffected by this UI branch; displayed historical installation paths are stale. Recapture with current launcher registrations in a launcher task. |
| shortcuts.png | Replaced: real application actions plus complete preset Save as, Load, Import and Export controls. |
| dark-mode.png | Old Customizer/title palette. Refresh together with light-mode.png, preserving matched camera/layout. |
| light-mode.png | Old Customizer/title palette. Refresh together with dark-mode.png. |
| objects.png | Language example remains valid; cosmetic refresh recommended for the new Editor title. |
| customizer-attributes.png | Replaced: real reactive attribute declarations, housing/lid and selected E header hierarchy. |
| parts-assemblies.png | Component demonstration remains valid; cosmetic refresh recommended for the new Inspector title. |
| anchors-attachments.png | Anchor demonstration remains valid; cosmetic refresh recommended for the new Inspector title. |

The untouched images retain their original source/binary identities in `screenshots/sources.json`.
They are not represented as captures of this release. A screenshot audit is distinct from recapturing
every feature demonstration; only successful real application captures may replace repository images.

The five October 10 captures (including supplementary `preferences-3d-view.png`) are in
`D:/openscad/runs/scadmaxx-all-features-2026-10-09_22-34/readme-captures`. Native originals and previous
assets are retained there. Replacement crops remove window chrome only; matching comparison dimensions
remain 1280×820 and 865×860. User viewport palette was restored to Nord Light; no bindings or model sources
were changed. The matched older light/dark pair is retained as historical evidence, with its older palette
explicitly identified above; it has not been recolored or mislabeled as current.
