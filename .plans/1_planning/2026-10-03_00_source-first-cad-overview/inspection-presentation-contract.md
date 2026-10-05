# Shared inspection presentation contract

Owner: feature 03. Required by independent consumers 04 and 07. This refinement was identified while specifying
07 on 2026-10-03; it is a planning contract, not a claim that the active 03 implementation already supplies it.
Implement and verify it in 03 before freezing bases for 04/07. If 03 has completed by then, make a focused owner
follow-up and record its new tested revision. Do not copy competing infrastructure into both consumers or add a
04 -> 07 / 07 -> 04 dependency. Recheck the actual 03 handoff, not just this document.

## Problem and ownership

04 prepares a merged inspection mesh for clipping. 07 retains individual Part meshes for visibility and ownership.
Independent replacement of the viewport renderer would lose one of those behaviors. 03 therefore owns one display
coordinator in EvaluationBinding/QGLView and the generic data below, without semantic or Section headers.

New `src/glview/InspectionPresentation.{h,cc}` and `src/gui/InspectionPresentationController.{h,cc}`; common renderer
`src/glview/InspectionMeshRenderer.{h,cc}`. Reuse PolySet/VBO drawing and SurfacePick, not a new geometry backend.
All names are proposed implementation APIs; reconcile them once with the 03 owner's actual headers.

```cpp
struct InspectionPiece {
  uint64_t drawId;                         // result-local, nonzero
  std::optional<size_t> nodeIndex;
  std::shared_ptr<const PolySet> mesh;      // local mesh, immutable, worker-owned until ready
  Transform3d localToWorld;
  Color4f color;
  enum class Role { Solid, Highlight, Background } role;
};
struct InspectionMeshSet {
  std::string resultId;
  uint64_t geometryGeneration;
  std::vector<InspectionPiece> pieces;
};
struct InspectionMask {
  uint64_t serial;
  std::set<uint64_t> visible;               // exact draw IDs, not source suppression
};
```

Qt-side controller holds the current Stamp and returns QObject-scoped RAII registration tokens:

- `registerMeshProvider(id, priority, lifetime, start(scene, stamp, completion))`: asynchronous provider callback.
  Completion returns Ready(shared immutable set), Empty, Unsupported(reason), Cancelled or Failed(reason).
  Start returns a cancellation handle. Highest priority enabled provider wins; duplicate id/priority fails.
  07 registers semantic provider at priority 100 only for a valid semantic scene; 04 registers root provider at 0.
  A higher active provider's Pending/Failed state never falls through to a lower provider and loses ownership.
- `requestMeshes(owner, lifetime)` returns an RAII request. One job for the selected provider/result; all consumers
  share its completed set. Provider change, input invalidation or closing cancels delivery; workers retain their data.
- `setMask(ownerToken, mask)` / clear: masks from active owners intersect. Empty visible set means show nothing.
  Missing owner mask means all visible. Validate IDs, result and generation; never persist result-local draw IDs.
- `registerMeshEffect(id, order, lifetime, factory)` takes a Renderer decorator factory wrapping a shared child
  renderer. 04 registers its clip decorator, carrying only core ClipState. Color, edges and SurfacePick all receive
  its same predicate. Effect tokens can update uniforms without rebuilding meshes or replacing the child renderer.

03's coordinator constructs a base InspectionMeshRenderer from the selected mesh set, then wraps it in deterministic
effect order. Never let a consumer install/restore a saved raw renderer independently. The default renderer is
retained by 03; restore it only when no active request remains. A provider does not itself activate inspection display.
07 requests display for a valid semantic model, including residual geometry alongside definitions, so ownership and
visibility are available even before a toggle. A valid empty scene yields Empty, not a provider failure.
04 requests while clipping is enabled. Unannotated documents without either request use the ordinary renderer.

Ready set installation, provider change and final restoration advance viewportGeneration under the same result ID.
Mask/effect-uniform changes advance presentation serial; camera has its own serial. A pick captures and validates all
three. Changes do not rerun source or mutate EvaluationInputs. Notify consumers to rebind transient geometric hits;
07 may retain its own semantic path selection but must obtain new ObjectKeys before selecting/highlighting surfaces.
Mask changes must not cancel 04's source-bound draft gesture merely because its own presentation serial changed.

Meshes preserve per-piece draw IDs, transforms, role and colors in every decorated pass. Backgrounds are excluded
from picking. Shared mesh objects can be instanced with different transforms and draw IDs. Final aggregate geometry
does not retroactively acquire per-face ownership: 07's separately prepared display is where exact ownership exists.
For coincident surfaces, use deterministic piece order for equal depth and report that displayed owner only.
Do not claim the hidden coincident instance is uniquely inferable from that pixel.
The common mesh draw path applies each localToWorld once through the existing VBOBuilder conventions before
recentering/upload. SurfacePick receives the same world normal/winding correction as 03's ordinary mesh path; do not
apply a second inverse-transpose or mirror correction in a decorator. Include rotated, mirrored and nonuniformly
scaled pieces in the native fake-provider point/normal fixtures.

## Clipping adaptation and gates

04's ClipMeshJob becomes its priority-0 provider: one root solid piece plus existing role/color groups. When 07 is
present, 04 consumes 07's pieces and never re-merges them. Its ClippedMeshRenderer decorates the common draw loop,
adding the common plane predicate to surface/edge/pick shaders. It preserves masks, draw IDs and per-piece transforms.
Use one bounds-derived recentering origin for the displayed set; SurfacePick adds it exactly once. Recompute uniforms
when bounds/set changes; hiding/solo changes draw masks only and cannot start CSG work or upload identical meshes.

Keep the source-bound last-good display while preparation is pending with explicit Preparing inspection / Cancel.
Disable unavailable semantic hide/pick controls during pending/failure; do not show checked controls with no effect.
Failure preserves ordinary navigation and the last-good model with clear status. No guessed ownership is supplied.

03 phase 2 must test a fake two-piece provider, mask hide/restore, registration teardown, stale asynchronous completion,
effect wrapping of both hit/color passes and selection invalidation. 04 phase 1 must test its clip decorator on that
fake provider without linking 07. 07 phase 4 must test its provider with a test-only pass-through/tint effect without
linking 04. Final composition must test actual 04+07: hide/solo while clipped, turn clipping off while hidden, switch
tabs during preparation, masked objects never hit, retained rear surfaces still hit with their correct Part identity.
