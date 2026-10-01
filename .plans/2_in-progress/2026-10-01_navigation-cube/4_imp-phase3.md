# Phase 3 — Viewport popup, preferences and live tuning

Status: complete. Depends on completed [phase 2](4_imp-phase2.md).
Primary requirements: R10–R11, R17–R19, R21, R25 in [requirements](2_requirements.md).

## Outcome

Deliver the thin-framed resizable popup, shared projection/display/camera commands, persistent normal preferences,
and session-only developer controls with complete clipboard export. The saved-view list is completed in phase 4.

## Work

- [x] Implement the small unframed triangle with tooltip, accessible name and keyboard activation. Anchor popup
  placement to the viewport/triangle while clamping to the current screen; do not hard-code screenshot coordinates.
- [x] Build the titleless popup with a thin border and resize grip/edges. Explicitly implement outside-click dismissal,
  triangle-toggle behavior, Escape, focus restoration and resize capture. Consume dismissal events rather than
  forwarding them to geometry; descendants and inline editors must count as inside the popup.
- [x] Add exclusive Perspective/Orthographic radio buttons bound to the existing projection actions. Add the compact
  Center / View All / Reset row and Axes / Scale markers / Crosshairs / Edges checkboxes via shared actions.
- [x] Add Show information and individual Triangles / FPS / Frame time choices backed by settings. Preserve individual
  selections when the master switch is off. Do not present unavailable placeholder metrics as completed statistics.
- [x] Prepare an expanding saved-view-list area and explicit data-model binding points. Keep unavailable Add/Remove/
  Rename operations disabled until phase 4 supplies the document store; do not create a temporary second library.
- [x] Add ordinary Preferences for navigation visibility and camera animation on/off/duration. Persist popup size and
  normal choices using existing settings conventions. Restore hidden navigation without its popup; keep statistics
  independently visible. Synchronize new windows and action checked states through existing preference plumbing.
- [x] Add a dedicated dev build option and discoverable View-menu tuning entry. The dev window exposes overall scale,
  independent cube/triangle right/top insets, actual resolved coordinates, geometry/hit/label spacing, idle/hover opacity,
  fade delays/timings, camera duration/easing, step sizes and cube drag-orbit enable/disable. Changes apply live.
- [x] Keep session overrides separate from persistent baselines. Reset clears overrides; changing a normal preference
  clears any override for that same property so the change visibly takes effect. Restart drops all dev overrides.
- [x] Implement one Copy settings action from the settings model, not from currently visible widgets. Include all
  values, units, baselines/overrides, requested/clamped positions, viewport dimensions and DPR. Use stable formatting
  and short Copied feedback; do not copy the saved-camera library or add import/dev-file persistence.

## Validation

- Qt input tests exercise popup edges, resizing, clicking triangle twice, Escape/focus, outside click consumption and
  screen-edge/narrow-viewport placement. Verify no native title bar/close button appears on the tested Windows style.
- Each shared command reaches the same final camera/display state as its menu counterpart. Projection radios update
  when changed externally; world axes toggling does not erase the cube's XYZ labels.
- Isolated-profile tests restart the process to distinguish persistent ordinary settings from temporary overrides.
  Multiple windows show coherent choices without rebinding another viewport's transient interactions.
- Change each dev field and compare resulting layout/behavior plus copied text. Repeat after DPI/size clamping and
  with controls offscreen in a scrollable dev window. Include drag-orbit's enabled state in export.
- Inspect native light/dark, larger-font, translated-long-label and scaling screenshots; match the accepted popup
  structure while including the later Center / View All / Reset row.

## Exit and evidence

Record native screenshots with popup closed/open/resized, clipboard snapshots and persistence tests. Both production
and dev-option source paths must compile; only the dev build exposes experimental controls. Phase 4 consumes the
popup's real list/model interface. Empty/disabled saved-view placeholders are explicitly incomplete until then.

## Phase result

Thin-frame popup, shared actions, normal preferences and dev-only live tuning implemented. Both dev and production
configurations compile. Native popup dismissal, radio synchronization, resizing, tuning and clipboard tests pass;
123 unit cases pass. Evidence: runs/navigation-cube/phase3/native-1 and production. The corrected list layout was
visually inspected. Physical mixed-monitor, translated labels and process-restart checks remain final phase-6 QA.

