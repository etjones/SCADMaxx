# Phase 6 — Integration, calibration and local handoff

Status: implementation and local handoff complete; platform matrix limits are explicitly recorded. Depends on [phases 1–5](3_overall-plan.md#ordered-phases-and-coverage).
Primary requirements: R01–R28 in [requirements](2_requirements.md).

## Outcome

Validate the complete feature, choose usable provisional appearance defaults, and provide a runnable local development
build plus evidence. Keep experiment controls available for the user's final visual tuning.

## Work

- [x] Review all R01–R28 against the final implementation and earlier phase evidence. Maintain a requirement-to-test/
  artifact matrix in `5_post-implementation-notes.md`, with pass, failure or unverified status and precise limitations.
  Remove disabled placeholders and reconcile docs with the actual schema, control names and supported backends.
- [x] Build the dedicated checkout using the shared Windows dependencies and a verified compatible build directory.
  Validate both dev-tuning-enabled and production-disabled paths, plus applicable Qt/headless compile guards. Keep
  build repairs separate and record source revision, diff, submodule/dependency fingerprints and configure commands.
- [x] Run the relevant registered Catch2 and Qt GUI tests and required existing checks. Exercise the integrated camera,
  popup, save/recovery, multiwindow, settings and capture workflows using isolated profiles and fixtures. Expand tests
  only for new failures, changed code or uncovered risks rather than repeatedly rerunning unchanged successful checks.
- [x] Inspect a native visual matrix: perspective/orthographic; face/edge/corner/rolled views; small/large viewport;
  light/dark theme; larger fonts; translated labels; representative Windows scaling and mixed-DPI monitor movement.
  Check focus/keyboard access, contrast, resize boundaries and hit targets, including visible small edge/corner facets.
- [x] Calibrate compact cube scale, independent cube/triangle placement, labels, hover opacity/delay/fades and motion
  duration/easing through the dev window. Compare against the accepted popup mockup plus the later action-row addition.
  Record provisional defaults and copied complete settings from the running app; preserve live tunability for feedback.
- [x] Compare repaint/timer activity and frame cadence with navigation/stats hidden, idle, hovered and animating.
  Confirm no continuous idle loop, source reevaluation storm or stale callback after tab/window close. Record scene,
  display and hardware context instead of claiming a universal FPS budget from one machine.
- [x] When an annotation revision is available, verify lock behavior, redo invalidation and clean/annotated capture in
  a separate isolated composition checkout with exact revision IDs. Follow workspace annotation instructions and avoid
  occupied worktrees. Do not merge annotation code into this feature branch. If unavailable, mark real combined evidence
  unverified and distinguish standalone readiness from combined readiness.
- [x] Stage a runnable local application with the required runtime files using the workspace's established Windows
  deployment approach. Launch that staged executable with isolated settings and verify cube, popup, save/reopen and
  Copy settings. Record its absolute path and source/build identity. No ZIP, publication, PR or stack inclusion is implied.
- [x] Update exploration, requirements deviations and post-implementation notes with actual outcomes, unresolved issues,
  evidence locations and local launch instructions. Move the whole planning item only when the workflow's completion
  criteria are met; do not mark failed or unperformed required checks complete.

## Acceptance evidence index

| Requirements | Required integrated evidence |
| --- | --- |
| R01, R27, R28 | Standalone source/build identity, dependency reuse, tests and launched local application |
| R02–R08 | All 26 targets, native camera invariants, steps/orbit and interruptible transition tests |
| R09, R14, R24 | Camera notifications, script/Animate behavior, ownership and teardown tests |
| R10–R11, R21, R25 | Native popup/shared-action tests, focus/input behavior and visual matrix |
| R12–R16 | Saved-camera round trips, full document save/copy/reload matrix and failure/recovery evidence |
| R17–R19 | Restart/multiwindow preference checks, temporary overrides and complete clipboard settings |
| R20, R26 | Known geometry counts, cadence semantics, unsupported/stale states and idle activity observations |
| R22–R23 | Every GUI clean-image route, annotation policy tests and separately labeled real combined evidence |

## Exit and handoff

Supply links to the requirement evidence matrix, screenshots/capture samples, copied tuning settings, relevant test logs
and runnable local build. State any remaining platform/backend/composition limits explicitly. Experimental visual
values can continue to be tuned; a missing functional requirement or failed required check is not a calibration issue.

This phase does not authorize publishing or upstream integration. At the end of implementation, offer the workflow's
four follow-up paths—fix forward, replan, restart or supersede—without automatically initiating one.

Validation limits: physical mixed-monitor movement, OS dark controls, translated new labels and Qt5/headless builds
were not verified. Windows Qt6 native tests cover simulated 100/125/150/200% DPI, dark viewport, large fonts and
small windows. These are platform follow-ups, not claimed passes. See the final evidence matrix.
