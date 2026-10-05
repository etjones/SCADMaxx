# Viewport redraw freshness and camera publication

State: owner fixes committed and promoted on 2026-10-05 at the user's request.
See [promotion record](../promotion-20261005.md) for exact heads and validation limits.
Run: `D:/openscad/runs/20261005-viewport-performance`.

The 2026-10-04 integration at `c5d03a05c1f45ce8ada0538eeb4e6e36c8b9054d`
performs full dependency reads and SHA-256 checks during viewport drawing. The affected
housing model has 52 captured inputs but only 1,060 preview triangles. Camera signals
also synchronously republish the entire HTTP evidence snapshot. The selection freshness
check in `MainWindow::compile` additionally previews unsaved text during auto-reload.

## Owner changes

- Selection/model inspector: `current()` becomes a cheap display-state query. Editor signals
  and file watchers invalidate it. `validate()` and `scene()` retain exact-byte validation
  for actions. Auto-reload consumes a disk-change notification; an unsaved editor revision
  alone must never request preview. Consume the flag before the dependency-settle timer
  re-enters `compile`, otherwise the reload repeatedly restarts parsing.
  Refresh editor subscriptions after tab/window inventory changes. Watch disk paths even
  when their buffers are open so saving an included/used file can request reload. A disk
  notification validates outside painting; open editor overrides retain their semantics.
- HTTP server: separate camera-state signals and filter duplicate states. Publish only
  camera and view revision into the transport snapshot; retain document, result and source
  evidence. Full publication still handles actual state changes and the heartbeat.
  Queue the delta immediately: a 16 ms debounce allowed stale camera revisions through
  transport admission before the update arrived. The native `guardedViewport` test
  reproduces this; retain its immediate 409 expectation.
- Anchors, clipping and semantic hierarchy: prepare display geometry when controller state
  changes. Paint callbacks draw cached geometry and check cheap freshness only.
  Anchor's retained `References` resolver callback must explicitly check captured inputs,
  not just cached `current()`: `includedOwnerAndRetainedResolverGuards` checks a disk edit before watcher
  event delivery. Resolving an action target remains strict; drawing its prepared helper
  does not resolve it again.
  Preserve its existing model-only semantics (no added active-tab or draft-pixel restriction).
- Contextual insertion: `validateModel()` must explicitly call `inputsCurrent()` now that
  `current()` is cached. Preserve its intentional allowance for hypothetical draft pixels.

## Replay boundaries

`source-state.json` in the run records each owner HEAD, patch and SHA-256. Owner patches
are limited to `src` and `tests`; existing generated dependency changes and Python caches
are excluded. The later authorized promotion preserves those patches in owner commits;
the integrated adaptation is retained at `500441ff0` for reviewed replay.

The integrated verification patch is against the existing 2026-10-04 composition, with
no refetch or additional feature selection. The existing GUI verification build and shared
vcpkg packages are reused; the previous delivered ZIP/executable remain unchanged.

Selection's owner patch needs two explicit adaptations after the later source-first patches:

1. Watch `EvaluationInputs::validationInputs()` in the integrated sealed-input model, rather
   than only the older owner's `consumed()` set. Preserve sealed-input capture semantics.
2. Preserve `!hypotheticalPixels` in `validate()`. Add exact-byte validation to both
   `validate()` and `validateModel()`; do not weaken draft, owner or revision checks.

Do not overwrite the integrated EvaluationBinding files with the older owner files.
The full adapted delta is retained as `integrated.patch` in the run.

The fresh `20261005-scadmaxx-all-features` run reproduced this overlap at insertion
foundation `05deb09fd`. Its preserved conflict is under
`conflicts/insertion-foundation-followups/`. Resolve both predicates and watcher loops
as above. The final EvaluationBinding.cc matches verified `0a53d34ce` exactly.
The subsequent contextual-insertion strict-validation followup is already satisfied;
its three-way patch applies without removing those checks. All 22 entry checkpoints passed.

## Verification

Run evidence, executable identity and final native outcomes are in the run's `report.md`.
Regression cases cover unsaved edits staying idle, explicit preview, disk dependency reload,
cached display checks, strict rejection of changed bytes before file-watcher delivery,
and camera-only HTTP updates preserving existing evidence. The native suites also exercise
selection, semantic hierarchy, clipping, anchors and insertion together.
