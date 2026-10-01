# Phase 2 — Cube geometry, input and camera motion

Status: completed, source commit `ea9427744`. Depends on completed [phase 1](4_imp-phase1.md).
Primary requirements: R02–R08, R24–R26 in [requirements](2_requirements.md).

## Outcome

Deliver the compact live cube with correct 26-target snapping, arrows, roll, free orbit and configurable transition
engine. Native rendering and input work before popup/persistence complexity is added.

## Work

- [x] Add a pure chamfered-cube geometry model with stable face/edge/corner IDs and target directions. Parameterize
  chamfer width and sizes in logical pixels; clamp invalid experimental values without collapsing required targets.
- [x] Project from the actual camera basis, cull back-facing facets and order visible polygons. Paint outline/fill,
  labels, XYZ letters and hover state from a shared geometry snapshot. Do not render cube orientation independently
  of hit testing or draw all 26 targets as if simultaneously visible.
- [x] Add upper-right anchoring for the cube/arrow group and a separate triangle placeholder. Maintain minimum useful
  hit areas; changing scale or DPI recomputes polygons, labels, positioning and hit regions together.
- [x] Implement exact axis faces, 45-degree bisector edges and true isometric corners. Use the accepted standard up
  rule, preserve all nonorientation camera fields, and retain the old Diagonal action's exact target separately.
- [x] Add screen-relative directional arrows and view-axis roll. Baselines are 15 and 90 degrees respectively;
  dispatch one step per click through the shared camera boundary. Do not add hold-repeat/modifier controls.
- [x] Implement click/drag input states: idle, pressed, dragging, released/cancelled. Use pointer capture and a logical
  threshold; once a gesture becomes a drag it cannot become a click again. Disabled drag-orbit suppresses moved-click
  snapping and propagation. Free orbit tracks a virtual trackball without changing position, projection, pan or zoom.
- [x] Add interruptible transitions for discrete camera targets. Interpolate orientation, pan, positive distance and
  FOV as planned, switch projection once when required, and assign the exact final pose. Coalesce visual notifications;
  preserve one final operation notification and existing manual-navigation behavior.
- [x] Retarget from the displayed pose on a second command. Manual input, script camera updates, owner replacement,
  capture and closing invalidate stale transition callbacks. Store an operation generation, not raw delayed pointers.
- [x] Implement resting/active opacity interpolation and stop timers when complete/hidden. Keep hover/focus/drag
  activation independent of opacity, and expose tunable values through the settings model prepared for phase 3.

## Validation

- Test all 26 target IDs and independent expected orientations. In orthographic corner views, verify equal projected
  axis lengths; verify 45-degree edges and deterministic poles. Check bounds/shared-edge hits and hidden facets.
- Verify unchanged translation/distance/FOV/projection after each orientation-only operation. Four 90-degree rolls
  and full directional cycles return to the start within a documented tolerance.
- Native tests cover press jitter, dragging through target boundaries, release outside, focus loss, orbit disabled,
  resize during a gesture and repeated clicks. Geometry selection and source state must remain unchanged.
- Transition tests cover rapid reentry, projection-changing recall targets, script updates and close. Assert exact
  endpoints, bounded notifications, no delayed camera overwrite, no new per-frame model compilation.
- Native images compare light/dark, enlarged fonts and scaled DPI with the approved compact visual direction. Confirm
  that dragging moves the camera, not the widget, and that fading does not leave trails or defer click recognition.

## Exit and evidence

Capture target-grid images, input/transition test output and event/compile observations in the phase-2 run record.
The cube must remain synchronized after existing menu/mouse/script changes. Known experimental appearance values are
recorded, not treated as final calibration. Phase 3 exposes live tuning and replaces the triangle placeholder with
the accepted popup. No claims about saved-view lifecycle or final metrics are made at this phase.
