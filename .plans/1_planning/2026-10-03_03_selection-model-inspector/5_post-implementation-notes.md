# Selection and Inspector local implementation handoff

Feature 03 is complete in `D:/openscad/wt-openscad-selection-model-inspector`, branch
`feature/selection-model-inspector`. Base and unchanged HEAD: `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`.
This is the retained HTTP/annotation/navigation prerequisite composition, not a selected-stack integration.
Feature/repair changes remain uncommitted. Actual source identity is the frozen patch and file hashes below.
No staging, commit, push, promotion, enabled-stack change or integrated release was performed.

## Delivered behavior and frozen interfaces

`EvaluationInputs` captures exact UTF-8 root/include/use bytes once per native evaluation, preferring captured dirty
editors and rejecting conflicting canonical open buffers. Request-local source cache/lexer paths share that snapshot.
`EvaluationBacking` owns parsed root/library ASTs, evaluation session and contexts; `EvaluatedScene` retains the node
tree and immutable inputs. Workers retain this scene after document close or later compilation. Existing document,
attempt and evaluated-result IDs remain authoritative; no duplicate document/result store is introduced.

`Selection::EvaluationBinding` binds installed renderers and temporary presentation renderers to those identities,
source/configuration fingerprints and viewport generation. Current consumed editor revisions/hashes and disk content
are checked; source changes, close/replacement, active-tab mismatch and failed evaluation reject stale use. Parse
failure preserves last-good pixels. HTTP result metadata exposes captured dependency/configuration provenance and
retains the same result ID when a presentation renderer is installed or restored, including a null default renderer.

`SelectionService::pick(logicalPixel, Stamp)` returns visible world point/outward normal and an ObjectKey, with an
optional invertible local frame/point. Preview identifies CSG draw groups; final aggregate geometry identifies the
rendered root and has no fabricated instance frame or source provenance. OpenCSG visibility/depth/stencil is retained;
Manifold/PolySet and simple convertible CGAL final paths share tessellated surface picking. Transparent solids are
opaque to this picking policy, `%` backgrounds are excluded, 2D/Thrown Together report Unsupported, empty is Miss.
Camera, renderer/result generation and presentation serial are captured/rechecked before delivery.

Two non-MSAA passes use compact RGB IDs/depth and RGBA32F world normals. OpenGL 3 framebuffer support and the formats
are required; failure is explicit. Pixel centers use actual physical framebuffer dimensions at DPR 1, 1.5 and 2.
Recentered positions add one explicit origin. Renderer signs correct VBOBuilder's negative face-cross convention,
subtraction polarity and mirrored winding once; no second inverse-transpose is applied. GL framebuffer, viewport,
program, buffers, matrices, depth/stencil/cull and masks are restored by `ScopedGLState`.

`ViewportToolRouter` owns one pick/drag/external gesture. A miss remains armed; success/cancellation retires before
delivery. Escape, owner destruction, source/result changes, tabs and focus invalidate once. Navigation drag/wheel/cube
input remains available while picking. Drag captures its originating button and delivers release or cancellation.
Existing annotation and measurement handlers acquire exclusive external tokens. Input inside their palettes/modals
keeps its existing priority. Context-menu input remains on the existing route.

`ViewportOverlays` registers QObject-scoped move-only tokens in WorldDepth/WorldOverlay/HUD order, then numeric order
and sequence. Each callback receives a captured camera/stamp with GL state restoration. Helpers do not enter hit or
clean capture passes. `InspectorDock` provides Select geometry, observational point/normal/object/frame/freshness, and
explicit unavailable provenance/semantic fields. It shares a right-side tab group with annotations. Contributions
have unique IDs, stable order, QObject lifetimes and owned widget replacement/destruction. Enrichment consumers use
the existing `selectionChanged` signal with their lifetime; they own typed data keyed by Stamp/ObjectKey.

The shared inspection-presentation refinement is implemented by this owner. `InspectionPresentationController`
coordinates enabled providers, requests, masks, effects, preparation/cancellation and central default restoration.
Highest provider priority owns one shared job/result; Pending/Failed never falls through. Worker delivery is queued
through a retained GUI dispatcher and rejects stale tickets, source/result and lifetimes. Registration alone does
not activate display. Preparation retains last-good pixels/navigation and explicitly disables unavailable hits.

`InspectionMeshRenderer` preserves immutable per-piece local mesh, transform, color/role and unique nonzero 64-bit
identity through compact GPU tokens. Instances transform once before recentering/upload; backgrounds are not hit.
Masks from active owners intersect; missing means all, empty means none. IDs/result/generation and active mask serial
are validated. Mask/uniform updates advance presentation serial without CSG work, mesh rebuild or child replacement.
Effects wrap in order then ID and share color/edge/hit predicates. Ready/provider/default transitions advance viewport
generation under the same result ID. Equal-depth coincident pieces use deterministic display order only.

The actual headers and `doc/inspection-foundation.md` are the consumer contract. No 06/07/08/14 or Section/semantic
headers are imported. Features 06/14/04 may use this frozen input; their behavior has not been tested by feature 03.

## Exact source and repair ownership

Run root: `D:/openscad/runs/20261003-selection-model-inspector`.
`final-source-evidence.json` records 67 working file hashes (56 feature-owned changes, 11 repair-only files), raw and
canonical LF identities, submodule revisions and independently reconstructed HEAD/repaired/final layers. Applying the
feature patch to repaired material matches every final canonical byte. Strict reverse apply-check also passes.

- Feature-only `final-feature.patch`: `fc9f0e8da7fa019447700bee498b09a689f00152d8ae965a106341a0569290bb`.
- Complete input `final-complete-input.patch`: `40a0eb7d90c43be7da037079e0d79214a6d207547f59f49aef3b6a8b1e13df4c`.
- Windows repairs: `e842b3549e34b455170c36c6bf70bebb19f864241c15473fd788dcf3daedf602`.
- Native harness repairs: `96bdba31c9a02b4e9bb1b93c75e254f667da58a25dcab9181cdb4e99152e788b`.
- Verification record: `e5b3b2b4ff088ac331a9b0da3143b0c18189e11aa9c381ab2d915c02a007413d`.

Required-only ancestry and exclusions are in `inputs/manifest.json`; 02/15 feature patches were not imported.
The later navigation head `bfd009ef0047452c09e3629d0af25efd6af34700`, shortcut/theme/UI changes and OEP8/Customizer
changes remain separate later composition obligations. No full selected-stack build was started incidentally.
All six submodules are clean at recorded revisions. The configure-generated Clipper version header was retained
with its built hash `0d636f1599b09743496d5c15c7dcb5bc3101bd423d6745bf17e480edbffccdac`, then restored to the original
working content hash `93ba10e1bd3bf28dbd43aeda284ba5ff23e066594c64bb01cd87b2eac94ebbb1` after verification.
Generated `.serena`/`.clangd` state is excluded. Shared dependency status remains
`2983caf4494a3428f029553e921a862000477e8e1266a8b74846acde80c7c2e1`; no packages were installed/upgraded.

## Verification

- Supported MSVC 19.51, SDK 10.0.26100.0, Qt 6.11.1/QScintilla 2.14.1 Release application/unit targets pass.
- Actual CTest discovery lists all 15 cases: 6 evaluation-inputs, 3 surface-pick-math, 3 inspection-presentation,
  3 selection-router. All pass on the final linked source; no zero-discovery or offscreen-as-native claim.
- Native GPU: NVIDIA GeForce RTX 3070 Ti, OpenGL 4.6.0 NVIDIA 616.92/GLAD 2.0.4. Real depth24/stencil8/RGBA32F passes
  verify preview and both final backends, perspective/orthographic, subtraction, front/rear occlusion, transforms,
  mirroring, repeated instances, background exclusion, transparency, recentering, resize and all four pixel borders.
  Visible frame samples and physical frame dimensions are verified alongside point/normal tolerances.
- Final ordinary Windows harness from the deployed/extracted feature package with clean runtime PATH:
  `native-20261003T222209478Z`. 58 QtTest results, 46 behavioral slots plus 12 setup/cleanup; no failures/skips.
  Per class: Annotations/HTTP 13, MainWindow 4, ModuleCache 4, Navigation 15, Selection 18, TabManager 4.
- Final selection-only DPR 1.5: `native-20261003T221117751Z`; DPR 2: `native-20261003T220957025Z`.
  Each passes 18 results (16 behavior plus setup/cleanup). The DPR-2 window sizes were constrained by the existing
  monitor's height; tests use the actual resulting viewport/frame dimensions and two distinct widths.
- Native fake-provider fixtures prove rotated/mirrored/nonuniform piece point/normal/frame correctness, front/rear
  masks, no mesh restart, matching hit/color effect predicate, stale worker completion, QObject teardown and exact
  default/null restoration. Tool/Inspector fixtures prove misses, Escape, replacement, source/include invalidation,
  stale/closed/wrong-window requests, drag release/cancel, measurements/annotations, focus, owned contribution widgets
  and per-callback overlay state/order. Source text and visibility/suppression remain separate from selection.
- Extracted package's seven-case Unicode filename regression passes through each of `scadmaxx.exe` and `.com` with
  clean PATH, including supplementary characters, Unicode directories and include/use. Shader hashes match source.
  Screenshots were inspected; point/normal/frame/unavailable fields remain readable at native DPR 1.5/2.

The local feature verification ZIP is `portable-verification.zip`, SHA256
`4d55bc02fafa218b97ef7e381ac7ba6921a85e4a17a3ac5f15c58e3beaea6891`. It is a feature test package, not a selected-stack
release or clean-machine certification. Executable hash: `3ad17dc28601133f067cede314ddd206d8fc49f8938a0e1e1143dced8ea068a3`.
All phase/interim/failing evidence is retained. Native checks corrected lifetime/cache scoping, OpenCSG program entry,
normal sign convention and physical-size mapping. Hidden-launch exposure was a test-fixture repair. A plain CMake
install omitted Qt DLLs; the existing runtime-copy/dependency deployment recipe fixed the portable check. Duplicate
identical MSVC DLL copies were removed only from this test staging, with hashes recorded. Controls were not modified.

## Limits and next work

This verifies the foundation on the existing Windows/NVIDIA machine. Unsupported modes/capabilities fail explicitly;
no exact final-face source ownership or hidden coincident instance is inferred. Consumers mutate tokens/controller
state on the GUI thread and use QPointer/immutable values for callbacks that may outlive an owner. Later integration
must freeze reviewed committed inputs, review the later navigation and selected-stack overlaps, and test actual
consumer combinations. Local completion does not enable or promote the feature. The authorized queue continues with
05, then 06, 14 and 04 in separate source worktrees.

## 2026-10-05 fix-forward: visible selection and clear workflow

Inspector now adds a background-aware selection box and picked-point marker for ordinary geometry,
with bounds cached at selection time. Preview bounds belong to the picked CSG primitive; final merged
geometry uses final-result bounds. No semantic ownership is inferred. Model-only captures exclude
the overlay, and clearing/staling the selection unregisters it. Picking remains one-shot, with
explicit completion feedback and inline workflow help. Preparation status now refers to geometry
for model tools; the clipping owner clarifies that Inspector need not be closed.

Local owner base: `ced629047eaa725a319f0c5a6a3602330b033c6d`. The uncommitted feature delta is
`runs/20261005-inspector-selection-feedback/selection.patch`, SHA256
`294b428eaecb2e553b7ae8f199aa7b5ddcc25005754874abafb13d416ea22d4d` (container-relative).
The run report records exact owner/verification heads, patches, submodules, native tests and screenshots.
Combined verification preserves existing Inspector scrolling and provenance contributions in
`wt-scadmaxx-20261004`. No commit, push or promotion was made; the existing promoted source and
delivered ZIP remain unchanged. Future integration must commit/promote the owner changes when requested.

## 2026-10-06 fix-forward: inherit and update viewport colors

Inspection presentation now applies the viewport color scheme before effects prepare meshes and
when installing/restoring renderers. InspectionMeshRenderer marks colored buffers dirty when its
effective color map changes, and rebuilds them in prepare() with a current GL context. Explicit
piece colors survive theme switches; geometry providers are not reevaluated for recoloring.

The cumulative uncommitted owner delta against `ced629047eaa725a319f0c5a6a3602330b033c6d` is
`runs/20261006-inspection-colors/selection-owner.patch`, SHA256
`e8ae5a11a5aad03e97ca848214138115289625ef02c018d8886bb8259cb8fdbb` (container-relative).
It includes and supersedes the previous selection-feedback patch. Combined verification retains
the newer Sections usability changes in `wt-scadmaxx-20261004`. Exact source, tests, hashes and
limits are in that run's report. No commit, push, promotion or running-release replacement.
