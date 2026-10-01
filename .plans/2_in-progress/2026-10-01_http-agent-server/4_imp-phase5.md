# Phase 5 — Evidence, camera control and fresh capture

Status: implemented and committed as b6461b511. Depends on phases 1–4. Covers R13–R20.

## Implementation

1. Complete annotation adapters over the native store and controller: list/search/detail, immutable original PNG and
   explicit historical-camera restoration. Preserve accepted unsaved evidence and published busy-time reads.
2. Share native camera conversion/operations between new API and existing annotation routes. Add standard views,
   projection and fit using actual OpenSCAD semantics. Preserve the public camera-angle convention and finite-value
   validation. Never introduce source writes or a private camera model that disagrees with the viewport.
3. Validate server/document/window/viewport, expected displayed result and view revision at admission and dispatch.
   Apply each camera operation as one guarded GUI action; notify existing consumers correctly. If native Animate or
   script-camera behavior produces later reevaluation, report the resulting state and require fresh capture preconditions.
4. Use the existing post-paint frame-ready mechanism for capture. Bind camera/result/size at request execution,
   invalidate on intervening changes, copy detached image data, then encode/hash away from GL ownership. Do not use
   fixed sleeps, recursive grab calls or another window's cached framebuffer as proof of the requested frame.
5. Register draft/modal/compile locks centrally. Camera changes, restore and fresh captures reject blocked states;
   historical evidence remains readable. A timeout or Stop invalidates pending callbacks; encoding may finish but
   cannot revive stopped work or publish into another server session.
6. Report the actual capture policy. Core excludes interactive annotation controls and historical marks while retaining
   its existing renderer policy; phase 7 must adopt navigation's helper-free capture boundary when integrated. Do not
   silently change viewport preferences to get a screenshot. Captures use native dimensions with explicit DPR metadata.
7. Keep legacy `/v1` adapter behavior compatible. New stricter view preconditions apply to `/v2`; enforce available
   native result guards for legacy requests without requiring fields its unchanged client does not send.

## Validation

- Read/checksum accepted evidence before save, during drawing and after geometry changes. Restore against current
  geometry and verify source/store content, active tab and historical PNG remain unchanged.
- Compare each standard camera/projection/fit action to native UI results; test invalid numeric values and source/
  Customizer dirty-state preservation. Race a user orbit with an agent request and expect explicit stale behavior.
- Native capture matrix: preview, F6 result, empty result, old model after failure, resized viewport, DPI changes,
  minimized/unavailable target, two windows and close during capture. Unsupported redraw returns an honest error.
- Inspect actual PNGs for correct model, angle, content, dimensions and excluded UI. Check returned hashes and result/
  view IDs against recorded state; a changed include must not be verified using the preceding image.
- Exercise draft marks/undo-all, modal comments, compilation, Stop/restart and cancelled frame callbacks. No blind retry
  during busy interaction; no late camera motion or restoration into a newly opened document.

## Exit evidence and handoff

Retain original/fresh PNGs and metadata, native test logs and concise visual observations. Do not replace visual
verification with checksum tests alone. Phase 6 receives a complete core HTTP workflow; any navigation-only behavior
remains explicitly absent until phase 7, without weakening existing annotation locks.
