# Preferences and dock consistency

## Scope and decisions

User notes and source exploration, 2026-10-10. Coordinate these changes before implementing the custom dock
title bar alone. The accepted visual baseline is [style-guide option E](../../../docs/ui-conventions.md):
16% Accent in Window for dock title backgrounds, 4% for resting Customizer group headers, neutral contents.
The user wants a custom dock title bar so docked and floating panels share that appearance.

Review Preferences as a whole: 3D View, Editor, Advanced, category navigation and Shortcuts. Experimental
appears acceptable to the user; include 3D Print in the consistency review, but no specific defect was reported.
Do not change settings semantics or introduce needless tint across entire pages.

## Source findings

Read the current integration `D:/openscad/wt-scadmaxx-20261006`, branch `scadmaxx-20261006`,
HEAD `f4f87a8eea11172037c459dd5ae9848b566fd044`. Findings are source-based, not new GUI validation:

- `src/gui/Preferences.ui`: 3D View's `horizontalLayout` explicitly gives a color-scheme column and an empty
  horizontal spacer stretch factors `1,3`. This explains substantial unused width. The expanding color list
  also competes for height with the settings below.
- `src/gui/Preferences.cc`: navigation controls and Always prepare Inspector data are appended directly to
  `page3DView->layout()`. The Inspector control is separate from the original page organization.
- Editor has a trailing horizontal spacer beside its settings. Enable Vim editor mode is appended directly
  to the outer page layout in `Preferences.cc`; it is not part of the existing editor groups. These are layout
  problems to resolve together, rather than simply removing either feature checkbox.
- `Preferences::updatePageMetrics()` explicitly makes Advanced and Dialogs group boxes flat. Advanced's
  different appearance is deliberate in the old implementation, not evidence of missing setting groups.
- Category navigation is a standard `QTabBar`, created in `Preferences.cc`; the former action toolbar is hidden.
  User reports insufficient hover and selected feedback. The source does not prove whether native style drawing,
  palette handling or another interaction is the runtime cause. Inspect the actual style path before changing it.
- `src/gui/ShortcutConfigurator.cc` persists edited bindings to the user-config `shortcuts.json`, and provides Reset.
  Its UI has no complete named presets or import/export controls. Automatic persistence of the active map is not
  a preset system. Presets are additional functionality, separate from visual polish.

## Coordinated design direction

1. Use one reusable, palette-aware dock title widget for SCADMaxx panels, not separate title implementations.
   Apply E to both docked and floating states. Keep title, close/float controls, accessible names, focus feedback,
   style metrics, drag and double-click docking behavior. Respect panel closable/floatable/movable capabilities.
   Let QDockWidget receive unhandled mouse events. Preserve layout save/restore and existing dock identities.
2. Reorganize 3D View into compact, top-aligned Appearance, Navigation and Inspector groups. Replace the oversized
   color-list region with a bounded chooser; use available width for coherent groups instead of a blank 3:1 spacer.
   Retain every color scheme and setting, including Inspector's performance explanation.
3. Make Editor group containers use the page's available width while keeping individual controls sensibly sized.
   Place Vim mode inside a named editing/mode group. Do not append feature settings after an expanding spacer.
4. Use consistent group-box treatment and spacing across Preferences, including Advanced. Group headings inside
   Preferences are static labels, not Customizer disclosure buttons; do not make them look clickable or mechanically
   apply the Customizer tint to every group. Keep dense pages scrollable at smaller windows and larger font scales.
5. Give categories persistent selected feedback, distinct hover feedback and visible keyboard focus. These states
   have different meanings from static dock hierarchy: selection can use Qt selection roles. Retain keyboard navigation,
   page/action synchronization and category overflow scrolling. Derive colors from the current palette, including
   inactive/disabled states, dark themes and high contrast.
6. Add complete shortcut presets in the shortcut owner: a named preset selector, save current bindings as a preset,
   and import/export for sharing complete sets. Preserve alternative bindings and explicit unbound actions.
   Use stable action identifiers and portable key-sequence encoding; report malformed files and conflicts before
   replacing the active map. Define handling of unavailable actions and new actions without silent data loss.
   Keep existing automatic persistence distinct from saving a named preset; do not add a general Preferences Save button.

## Ownership and implementation order

Use `codex/ui-visual-polish` in `D:/openscad/wt-openscad-ui-visual-polish` for shared visual/layout work.
It contains existing uncommitted branding/title changes and a dirty Clipper2 submodule; preserve them.
It does not contain every feature-specific preference addition present in the integration. Inspector settings belong
to `feature/selection-model-inspector`, Vim settings to `feature/vim-editor-mode`, and Customizer disclosure painting
to `codex/pr6642`. Shortcut presets belong with PR #6878's maintained input, not a new implementation hidden only
in the integration branch. Decide the maintained shortcut branch/ref before source changes to that feature.

Provide named insertion groups in shared Preferences first, then update feature owners to insert controls into them.
Avoid new reverse ancestry dependencies solely for UI placement; shared page organization may need to be owned in
the common prerequisite rather than making all owners depend on UI polish. Inspect actual dependencies before merging.
Use normal forward merges; never cherry-pick or merge the whole integration back into owners.
Separate reusable UI changes from shortcut-preset functionality in commits and handoff records.

This exploration records the coordinated direction; it does not claim the redesign or presets are implemented.
No source changes, build, tests, commits or pushes were made for this exploration. Builds and tests require an explicit
user request. When requested, verify category states, resizing/DPI, theme changes, dock drag/float/close and layout
restoration, plus preset round trips and rejection of invalid/conflicting input.
