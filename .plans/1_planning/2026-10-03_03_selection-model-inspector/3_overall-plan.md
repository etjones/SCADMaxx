# Selection and Inspector: technical design

Status: source-reviewed implementation specification, 2026-10-03. No new code has been built or tested.
Read [requirements](2_requirements.md), [phase 1](4_imp-phase1.md) through [phase 4](4_imp-phase4.md), and the
[shared verification contract](../2026-10-03_00_source-first-cad-overview/verification-contract.md).
Branch: `feature/selection-model-inspector`; selected navigation/annotations/HTTP prerequisites, no new-feature prerequisite.
Later planning note, 2026-10-04: the original implementation now has a completion handoff. Feature 12 requires the
separate generic follow-up in [insertion foundation contract](../2026-10-03_00_source-first-cad-overview/insertion-foundation-contract.md).
Keep that delta and verification distinct; this note does not claim its draft/sealed-input/focus additions implemented.
Audit source: `4c325716b94e444637a80df3966197ce110b2b75`. Proposed APIs below are new.

## Source evidence and ownership

- `MouseSelector::select` renders RGB IDs to an FBO, reads no depth/normal and uses `height-y` (one pixel too high).
- `QGLView::findObject` invokes vertex/edge measurement picking and unprojects near depth -1; neither path is a
  surface-hit implementation. Preserve measurement behavior; replace ordinary object selection with the new hit API.
- `GLView::setupCamera` exposes modelview/projection including camera object translation. Do not apply it twice.
- `OpenCSGRenderer::draw` computes visibility with OpenCSG then uses GL_EQUAL for surface shading. Its subtraction
  states cull front faces. `VBOBuilder::create_surface` transforms vertices before deriving triangle normals.
- `PolySetRenderer` owns tessellated final geometry, but its selection pass lacks per-object ID assignment.
  `CGALRenderer::draw` ignores the supplied selection shader entirely. Both require explicit implementations.
- `AnnotationController` already owns document/result identity and renderer installation history. Extend/extract its
  result binding; do not create a second independent notion of the last successful evaluation.
- Native compilation reads includes with text-mode fopen and libraries through mtime-based SourceFileCache.
  `ParserInspection` has a separate callback reader, only for bounded HTTP syntax inspection. It is not a native
  evaluation snapshot. Source-consistent hit guards require a shared immutable input set, described below.

New files: `src/core/EvaluationInputs.{h,cc}`, `src/gui/selection/EvaluationBinding.{h,cc}`,
`SelectionTypes.h`, `SelectionService.{h,cc}`, `ViewportToolRouter.{h,cc}`, `InspectorDock.{h,cc}`;
`src/glview/SurfacePick.{h,cc}` and `shaders/SurfacePick.{vert,frag}`.
Change the named existing renderer/camera/input files, `MainWindow`, `QGLView`, annotation controller and CMake lists.
The small shared input/result binding belongs here; transactions remain in 02, syntax provenance in 06 and design
declarations in 14. Neither later branch implements another input snapshot or result-generation counter.

## Immutable evaluation inputs and guards

Core API, without Qt types:

```cpp
struct SourceInput {
  std::string fileKey, utf8, fingerprint; // fingerprint of these exact bytes
  std::optional<std::string> editorId;
  std::optional<uint64_t> editorRevision;
};
class EvaluationInputs {
public:
  const SourceInput& read(const std::filesystem::path& resolvedPath);
  const SourceInput& root() const;
  const std::map<std::string, SourceInput>& consumed() const;
};
```

At compilation start capture root and all open editor path/content/revision overrides on the GUI thread. Resolve
include/use with existing library search rules; for each resolved canonical file prefer that captured open editor,
otherwise read disk once in binary mode and retain exact UTF-8. Preserve CRLF and BOM bytes; reject invalid UTF-8/NUL
with a diagnostic. If two open editors own the same canonical file with different contents, fail the evaluation
explicitly instead of choosing one. Untitled root has a session fileKey and existing library-resolution base directory.

Thread a request-scoped reader through native parse/lexer and SourceFileCache. Includes use `yy_scan_bytes` and the
existing buffer/path/location stacks; preserve dependency registration and cycle handling. Cache library ASTs only
within the request initially; this removes mtime-only reuse from this path and prevents cross-request dirty-buffer
contamination. Keep existing unmodified consumers on their present cache path. Share the reader primitive with
ParserInspection while retaining its separate limits/disabled-node inspection semantics. This is a distinct native
source-loading path, not invocation of the HTTP inspection parser for normal compilation.

`EvaluationBinding` records the existing root editor ID/revision/fingerprint, existing result ID, consumed input
fingerprints and a viewport generation. Install it with the renderer only after a successful evaluation. Annotation
and HTTP result reports read that binding. Failure leaves last-good display visibly stale and unavailable for new hits.
Revisions, input edits/reloads, renderer replacement, tab close/switch invalidate selection/tools. On a pick, recheck
all consumed open revisions and disk hashes; if a dependency changed, mark the result stale and request ordinary
reevaluation. Do not call a pointer or an AST node number a persistent document ID.

Add an owned `EvaluatedScene` retained by EvaluationBinding: shared root AbstractNode, document path, captured
EvaluationInputs and request-local parse/evaluation backing needed by any node/context references. Publish it as
`std::shared_ptr<const EvaluatedScene>`; never expose a borrowed MainWindow preview-tree pointer as a job input.
`EvaluationBinding::scene(expectedStamp)` returns that shared handle only for the current successful result.
A geometry job constructs its own Tree from scene.root and scene.documentPath, since Tree's string/node caches are
mutable even through const methods. Keep the backing alive until all jobs release the scene; canceling/closing a
document invalidates delivery but must not destroy data still used by a worker. 04 consumes this ownership contract.

## Shared inspection presentation

Implement the [inspection presentation contract](../2026-10-03_00_source-first-cad-overview/inspection-presentation-contract.md)
as part of this foundation. It was identified during 07 planning on 2026-10-03 and must be checked against the active
03 implementation before declaring the owner handoff complete. If necessary, record a focused owner follow-up.
The common immutable mesh pieces, provider/request/effect registration, masks and renderer coordinator allow 04
clipping and 07 semantic visibility to compose without depending on each other. They contain no downstream types.
03 phase 2 verifies fake providers/effects; real semantic meshes and clip shaders remain in their owning branches.

## Selection API

Namespace `Selection`; Qt-facing DTOs:

```cpp
struct Stamp {
  QString documentId, resultId, sourceFingerprint, configurationFingerprint;
  quint64 sourceRevision, viewportGeneration;
};
struct ObjectKey { QString resultId; uint64_t drawId; std::optional<size_t> nodeIndex; };
struct Hit {
  Stamp stamp;
  ObjectKey object;
  Vector3d worldPoint, outwardNormal;
  std::optional<Transform3d> localToWorld;
  std::optional<Vector3d> localPoint;
};
enum class PickError { None, Miss, Cancelled, Stale, Unsupported, Busy, InvalidViewport, BackendFailure };
struct PickResult { PickError error; std::optional<Hit> hit; QString detail; };
struct State { std::optional<ObjectKey> object; std::optional<Hit> surface; };
PickResult SelectionService::pick(QPointF logicalPixel, const Stamp& expected);
bool SelectionService::selectObject(const ObjectKey& object, const Stamp& expected);
void SelectionService::clear(); // emits selectionChanged(State)
```

Configuration fingerprint covers compile defines, parameter overrides, $preview and backend-affecting options.
viewportGeneration changes on renderer/binding replacement, not every camera movement. Each individual pick also
captures camera and presentation serials, rechecking them before delivery; navigation while a pick tool is armed
therefore remains possible. A consumer's own draft overlay/plane updates do not cancel its source-bound gesture.

No face/triangle ID is promised by this pass. `drawId` is result-local. Preview nodeIndex can identify a CSG leaf;
final merged geometry may only identify the rendered root. Frame/local point are absent for singular transforms or
where a final mesh lacks an original instance transform. Enrichment never changes the geometric hit's identity.

## Two-pass surface picking

Use a non-MSAA framebuffer with depth/stencil. Pass A renders compact IDs (1..0xffffff, zero means miss) using the
actual renderer visibility and reads depth as well as RGB. Pass B repeats the same visibility in RGBA32F, writing the
normalized world normal to RGB. No MRT or primitive-ID shader extension is required. Fail capabilities if the needed
FBO formats are unavailable. Disable blending, dithering, sRGB conversion, lighting and multisampling for hit passes;
restore framebuffer, viewport, program, buffers, depth/stencil/cull and color masks through an RAII GL-state guard.
Do not render axes, navigation cube, annotation overlay, selection helpers or measurement decorations in these passes.

Map a logical Qt point to physical framebuffer pixel x=floor(px*DPR), y=H-1-floor(py*DPR), rejecting outside pixels.
Unproject the center (x+0.5,y+0.5,depth) using the inverse of the exact P*M used for this draw, with window depth in
[0,1] mapped to NDC [-1,1]. Depth=1/ID=0 is a miss. Perspective division and non-finite checks are mandatory.
Read ID/depth/normal under one captured camera/renderer generation; reject mismatched generations before delivery.
The renderer's SurfacePick draw context includes `Vector3d positionOrigin`, zero for existing world-space VBOs.
For a recentered mesh, the draw modelview includes translation(positionOrigin); add positionOrigin once to the
unprojected render-space point to recover worldPoint. Normal output stays world-space. This is the explicit seam
for 04's large-coordinate mesh display; test it with a nonzero origin rather than assuming unprojection removes it.

The pick vertex shader receives already-world-space VBO position/normal. Normalize in fragment output and multiply
by the renderer state's sign: subtraction polarity times mirror correction. VBOBuilder derives a normal from
transformed vertices but reverses mirrored draw winding separately without reversing that normal; for a negative
leaf-transform determinant apply an additional -1. Final mesh normals use their own established winding. Nonuniform
scale is already reflected by triangle construction; do not apply the inverse-transpose a second time.
Reject degenerate/zero normals. Required normal error in fixtures <=0.1 degree, point error <=max(1e-5*diagonal,
two depth-buffer quantization steps unprojected at that sample). Samples stay away from silhouette edges.

| Renderer | Required implementation / identity |
| --- | --- |
| OpenCSG preview | Add SURFACE_PICK shader mode; retain its exact OpenCSG depth/stencil visibility and position shader. Store draw token and subtraction polarity on OpenCSGVertexState. Root/highlight solids participate; background `%` objects excluded. |
| Manifold / PolySet final | Draw tessellated triangles with explicit draw tokens. Treat visible transparent surfaces as opaque for picking; no click-through policy in this version. |
| CGAL final | Cache a pick-only PolySet conversion of the same evaluated Nef geometry; draw its triangles with the surface shader. No repair and no selection of non-simple/nonconvertible Nef; report Unsupported there. |
| Thrown Together | Report Unsupported for solid surface tools because it is a diagnostic operand view. Ordinary navigation remains available. |
| 2D / empty | Report Unsupported / Miss respectively for 3D surface tools. |

Limit IDs to 0xffffff drawable groups; detect overflow before rendering, never wrap. Feature 04 may later install a
prepared mesh display with the same hit contract; it must advance viewportGeneration and retain the result binding.

## Exclusive tools, overlays and Inspector contributions

One router per QGLView; QObject ownership follows the view. APIs:

```cpp
enum class CancelReason { Escape, Replaced, FocusLost, DocumentChanged, ResultChanged, OwnerDestroyed };
struct ToolRequest { QString owner; Stamp expected; bool needNormal; };
using ToolToken = quint64;
ToolToken beginPick(ToolRequest, QObject* lifetime, std::function<void(PickResult)>);
struct DragCallbacks {
  std::function<void(QPointF, Qt::KeyboardModifiers)> move, release;
  std::function<void(CancelReason)> cancel;
};
ToolToken beginDrag(ToolRequest, QObject* lifetime, QPointF press, DragCallbacks);
void cancel(ToolToken, CancelReason);
bool route(QEvent&); // returns true only if the active owner consumed it
```

`beginPick` replaces/cancels the previous tool before activating another. Left click requests a hit; success returns
once and exits, Miss leaves the tool active with feedback, stale/unsupported failure exits with feedback. Escape,
focus loss, owner destruction and tab changes cancel once. Ordinary orbit/pan/wheel/navigation cube remain routed
to navigation outside the pick-confirm gesture; a drag beyond Qt's startDragDistance is navigation, not a pick.
During a consumer-owned drag it receives move/release until cancellation; expose `beginDrag` with the same token,
stamp and lifetime plus move/release/cancel callbacks. No two tools own one gesture.
Coordinates are view-local logical pixels; capture the originating button and deliver release or cancel once,
never both. Reject a stale begin request before taking capture; cancel with DocumentChanged or ResultChanged.

Adapt annotation drawing and measurement selection to acquire router tokens; annotation palette/modal input wins
inside its widget. Order: modal widget, active tool, navigation cube, existing navigation, ordinary click selection.
Ordinary click selection is available when Inspector selection action is active; preserve context menus.

Overlay registration returns an RAII token for a QObject owner, deterministic layer (WorldDepth, WorldOverlay, HUD),
and draw callback receiving immutable camera/stamp. Restore GL state after every callback. Consumers cannot draw in
the hit pass. Existing annotations/navigation retain their present visual order; helper pivots use WorldOverlay.
Expose `registerOverlay(QObject*, OverlayLayer, int order, std::function<void(const OverlayContext&)>)` returning
move-only OverlayToken. OverlayContext contains Stamp, modelview/projection matrices, logical viewport size and DPR;
draw on the GUI GL thread. Order is layer, numeric order, then registration sequence. Destruction unregisters safely.

Inspector is a dock listing geometric point/normal, available object/frame and evaluation freshness. Show unavailable
fields explicitly. Register `InspectorContribution {id, order, QObject* lifetime, build(State,Stamp)->QWidget*}`;
replace/destroy its widget on selection change, unregister on owner destruction. Register a selection-change
observer for enrichment; each consumer retains its own typed result keyed by Stamp/ObjectKey and contributes UI.
03 imports no semantic/source/design-object headers. Contribution IDs are unique; duplicates fail registration.

## Verification and phases

Fixtures and exact source changes are in phases 1-4. GPU verification requires a real Windows GL context; offscreen
math tests alone cannot establish OpenCSG visibility or shader parity. A failed backend invariant stops that phase
with evidence; it does not permit guessed normals, a mesh raycaster ignoring CSG, or a new source-edit capability.
