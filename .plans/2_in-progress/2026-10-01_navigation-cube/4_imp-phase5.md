# Phase 5 — Viewport statistics and clean captures

Status: complete. Depends on [phase 4](4_imp-phase4.md).
Primary requirements: R20–R23, R26 in [requirements](2_requirements.md).

## Outcome

Supply meaningful triangle/FPS/frame-time information without idle redraw overhead, and make every GUI viewport image
route exclude navigation and guides while retaining the model and applicable annotations.

## Work

- [x] Publish typed cached triangle statistics at model preparation/result boundaries. Count preview tessellated model
  instances once each, excluding repeated rendering passes and helpers. Use final triangulated geometry only when
  available; do not reinterpret arbitrary facet counts, parse logs or trigger a render just to obtain statistics.
- [x] Associate values with document/result generation and render mode. Label preview/final, unavailable and retained
  stale results accurately. Clear previous-document values when ownership changes; handle empty models as valid zero
  where the backend supplies a meaningful count. Invalidate caches when geometry or instance transforms change.
- [x] Measure elapsed intervals between completed viewport paints, keeping a bounded rolling sample window. Derive
  FPS and frame-time milliseconds from the same samples; label this as viewport cadence, not GPU execution time.
  Exclude capture paints, reset after inactivity and show Idle instead of a misleading retained active FPS.
- [x] Bind the existing popup master/individual choices to the real stats overlay. Refresh text at a bounded rate;
  statistics must not force continuous repainting. Stop hidden-overlay timers. Keep its visibility independent of
  navigation visibility and expose refresh/averaging/idle calibration values through the dev settings/export model.
- [x] Introduce a scoped clean-render policy at the shared framebuffer capture boundary. Suppress GL world axes,
  scale markers and crosshairs as well as widget navigation, triangle, popup, dev window and statistics. Preserve
  model edge shading, model/background appearance, camera pose and the ordinary visible preference state.
- [x] Route PNG export, Copy Viewport, animation-frame dumping and the existing AI ViewportGrabber through the clean
  capture policy. Audit caching so no caller receives a stale or guide-bearing frame. Do not redesign independent
  command-line rendering options or introduce a new agent endpoint.
- [x] Stop a camera transition at its currently displayed pose for capture, invalidating queued callbacks; use the
  same pose for readback and applicable annotation composition. Restore scoped rendering state on every return/error
  path, without emitting preference changes or restarting the cancelled transition.
- [x] Define the annotation policy/composition boundary so clean images omit strokes and annotated evidence adds them
  exactly once. Accommodate camera-lock and redo-invalidation hooks without linking the standalone feature to the
  annotation branch. Existing stored images are never retroactively changed.

## Validation

- Use known triangulated models and multiple instances to verify typed counts. Exercise available preview/final
  backends, empty/failed evaluations, retained stale results and switching documents/render modes. Unsupported counts
  must display unavailable, not an invented value. Extra draw passes must not inflate counts.
- Instrument repaint/timer activity with stats hidden, active and idle. Verify measured intervals against known
  controlled paint times and ensure capture paints do not corrupt samples. Record the measurement's practical limits.
- Native framebuffer image tests enable every excluded overlay, capture through each GUI route, and compare with a
  clean reference at the same camera. Include model edges enabled, clipboard image data and animation frame output.
  Check on-screen state and preferences after success and injected failures; inspect actual saved pixels.
- Capture mid-transition, after a document switch, with the popup open and at mixed DPI. Verify queued motion cannot
  alter the captured pose after cancellation. A full-window UI screenshot should still show controls normally.
- Test annotation hooks with an injected compositor/lock policy on the standalone branch. Verify clean versus
  annotated requests and exactly-once strokes. Real annotation-branch behavior requires the separate combined check
  in phase 6; mock results must not be presented as that evidence.

## Exit and evidence

Record exact count semantics/backend availability, timing behavior, all capture callers and representative clean image
comparisons. Include failure-path restoration evidence and idle activity observations. The feature remains independently
buildable; document the remaining real annotation-composition check explicitly.

## Phase result

Typed cached counts cover preview instances (deduplicated CSG leaves) and prepared PolySet final rendering.
Counts match VBOBuilder triangle/quad/center-fan tessellation; CGAL Nef renderer reports unavailable.
Cadence uses bounded paint intervals and a one-shot idle timer. Native no-idle-loop checks pass.
Framebuffer, clipboard and existing AI capture pixels match a guide-free reference with edges preserved.
Capture state restores after an injected compositor exception; model-only skips and annotated calls invoke the hook once.
Build, 123 unit cases and 11 native cases (including setup/cleanup) pass. Evidence: runs/navigation-cube/phase5/complete.
PNG and animation callers are audited at their shared grabFrame boundary; native animation dumping remains phase 6 QA.
Real annotation integration is not inferred from the injected composition tests.

