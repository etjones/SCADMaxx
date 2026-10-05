# Live clipping: technical design

Status: implementation specification prepared, 2026-10-03; renderer/performance fixtures have not yet been executed.
Branch `feature/live-clipping-sections`; direct prerequisites 03/14 and their closure. No 15 dependency.
Require 03's [shared inspection presentation contract](../2026-10-03_00_source-first-cad-overview/inspection-presentation-contract.md),
refined during 07 planning. Consume the verified owner revision; 04 and 07 remain independent branches.
Read [requirements](2_requirements.md), [selection](../2026-10-03_03_selection-model-inspector/3_overall-plan.md) and
[design objects](../2026-10-03_14_design-object-persistence/3_overall-plan.md). Audit source:
`4c325716b94e444637a80df3966197ce110b2b75`.

## Rendering decision and evidence

OpenCSGRenderer runs depth/stencil visibility before shading with GL_EQUAL. Discarding fragments only in its final
color pass cannot be assumed to expose deeper retained surfaces. Clipping its operands also changes the closed-solid
conditions of those passes. Do not implement live sections by adding an unverified discard to every OpenCSG shader.

Use a cached inspection mesh of the already evaluated tree. Final Manifold geometry already supplies PolySets;
CGAL has a conversion path; preview uses the existing GeometryEvaluator/GeometryWorker mechanism once when a
clipped inspection display is requested for a new evaluated result. Retain `$preview` and existing instantiated
parameters by evaluating that frozen preview tree, not rerunning the source in F6 mode. Plane movement then updates
GPU uniforms only. This adds an initial mesh-preparation delay, exposed as Preparing section view / Cancel; it does
not promise instant first use for expensive booleans. Record actual preparation and interaction latency separately.

Rendering never edits the model's CSG tree or source. A deliberate commit of a source-backed Section uses 14's
normal transaction, after the gesture. No geometry/CSG evaluation or disk write is allowed during the gesture.
No caps in this first implementation: the requirements explicitly made caps conditional. Capability reports mark
caps unavailable; do not display a working-looking cap toggle. Exact contours/export remain with 15/09/13.

## Source files and state ownership

New `src/gui/clipping/ClippingController.{h,cc}`, `ClippingDock.{h,cc}`, `SectionManipulator.{h,cc}`,
`ClipMeshJob.{h,cc}`; `src/glview/ClippingState.{h,cc}`, `ClippedMeshRenderer.{h,cc}`;
`shaders/ClippedSurface.{vert,frag}`, `ClipDiscard.glsl`. Extend 03 SurfacePick shaders to use the same discard
predicate when drawing a clipped mesh. Wire main-window dock/actions, resources and CMake lists.

14 owns Section definition/ID/drafts/persistence. The controller owns only inspection settings keyed by root document
and Section ID: enabled, helper visibility, selected row and global enable. Retain these through the existing
personal/workspace backing, independent of source; reopening a source Section does not imply it must start enabled.
No private Section serializer or second SavedSection object. Use 14 createTransient/beginEdit/updateDraft/commitDraft/
cancelDraft and DesignEdits fields exactly. Persisting is a deliberate action, not a consequence of naming while typing.

```cpp
struct ClipPlane { Vector3d origin, normal; double epsilon; std::string sectionId; };
struct ClipState { uint64_t generation; std::vector<ClipPlane> planes; }; // <= 8 enabled
struct ClipCapabilities { bool available, caps; unsigned maxPlanes; std::string reason; };
```

Keep ClipState core/renderer-only, without Qt or Design headers. ClippingController converts valid 14 records to it.
The initial scope clips the complete displayed root; a Section targeting an unsupported component subset reports
unavailable rather than cutting the whole model by accident. Named semantic targeting can extend this once 07 exists.

## Mesh preparation and renderer lifecycle

Capture 03's EvaluatedScene handle from the current binding and immutable camera snapshot.
ClipMeshJob constructs its own Tree cache and retains the scene until completion; do not hand GeometryWorker a pointer to MainWindow's
mutable Tree that can be replaced underneath it. Serialize geometry work through the existing evaluation lock/cache
discipline. Cancellation and result generation are checked before installing a result; stale jobs never replace a
new tab's display. Do not invoke QOpenGL operations in the worker; upload on the owning GUI GL context.

Register ClipMeshJob as 03's priority-0 root mesh provider and acquire an inspection request while clipping is active.
If a higher-priority semantic provider is registered, consume its immutable pieces without re-merging them. This uses
generic mesh data, not 07 headers. Register ClippedMeshRenderer as a mesh-effect decorator through the coordinator;
preserve draw IDs, transforms, roles and visible masks in color/edge/pick passes. Test this with a fake provider on
the minimal base. The decorator contributes the common plane predicate to the base mesh draw loop.

For the root provider in preview, evaluate the frozen root's solid geometry once, exclude `%` background from the solid and preserve
available colors. Build optional background/highlight overlays separately from their existing evaluated role data,
clipped with the same plane predicate; backgrounds remain excluded from picking. The mesh is a viewport derivative,
not an export/output result. When clipping is globally off or has no enabled planes, release its effect/request.
03 restores the ordinary renderer only when no consumer still requests inspection display; semantic hide/solo must
survive disabling clipping. Final root-provider rendering reuses evaluated geometry instead of a second boolean job.

03 coordinates at most one selected-provider mesh job per document and a current cached set per result/backend. Source/result
replacement invalidates/cancels the job and disables stale editing. Changing only a plane/camera never starts a job.
Preparing/cancel/failure keeps the last-good display with explicit status, not a partial incorrect section or a switch
from failed semantic meshes to an anonymous merged root. The mesh coordinator owns registration and restoration.
An empty valid mesh is an empty result, not a backend failure. Non-simple/unconvertible Nef or 2D diagnostic input
reports unsupported. Mesh generation may use existing geometry evaluation policy, but never silently repair a failed
result as a clipping-specific recovery step.

Install through 03's coordinator, preserving result ID and advancing viewport generation when the mesh set/provider
changes. Plane/mask changes advance presentation serial only. Pick normal/position comes from the actually displayed
clipped mesh. Preserve per-piece identity when supplied; provenance may be unavailable for merged root-provider faces
and must say so. Never reuse an old preview node ID to invent a source instance.

## GPU clipping and numerical convention

Maximum eight simultaneously enabled planes, independent of the number saved. Enabling a ninth refuses that action
with a clear limit; keep the earlier eight and never silently drop one. Global off preserves individual flags.
Draw all surviving mesh surfaces with depth testing and two-sided display, including interior/back surfaces revealed
by the cut. Opaque visibility is sufficient for picking even when visual materials are transparent.

For every solid/edge/hit fragment retain only `dot(worldPoint-origin,unitNormal) > epsilon` for all enabled planes.
Centralize this in ClipDiscard.glsl and compose it into surface/edge/pick fragment programs through ShaderUtils.
Keep matching vertex position transformation for color/depth/hit passes. Disable hardware early-depth assumptions
that would retain discarded fragments; the depth buffer must describe visible retained mesh surfaces.

Recenter mesh vertex buffers around the bounds center c before float upload. Send (origin-c) to shaders and compose
the camera matrix with translation(c). Set 03's SurfacePick positionOrigin=c so unprojected render-space hits add c
exactly once to recover world coordinates; world normals remain unchanged. Derive epsilon once per
plane update as max(8*FLT_EPSILON*D,64*DBL_EPSILON*M), where D is positive mesh bounds diagonal and M=max(D,|c|,|origin|).
Reject nonfinite/degenerate definitions. Recentring handles distant models but does not promise unlimited precision.
Record D/epsilon with diagnostics; features below the representable tolerance are a documented limit, not exact CAD.

Numerical fixtures must prove a coincident face disappears without consuming a separate wall at 1e-4*D on models
scaled by 1e-4, 1 and 1e4, including oblique/mirrored cases and translated bounds. If those cases fail, correct the
recentring/error bound before proceeding; simply increasing epsilon to hide artifacts is not allowed.
Helper plane depth bias is visual only: draw it after geometry with polygon offset/overlay layer; it never changes
the Section or the discard plane. Origin marker remains visible through 03's overlay layer as an editing aid.

## Dock and manipulation

Dock rows show name, enabled, source/transient status and validity. Actions: Add XY/XZ/YZ, rename, select, remove,
Promote/save definition, global clipping, Pick point, Pick + align, Flip, Reset orientation and Show plane. Use the
existing configurable QAction system, with no new global keybinding conflicts. Two angle controls use degrees,
azimuth [-180,180) and elevation [-90,90]; these are derived from the canonical normal, never independent state.

Presets start at current model bounds center with +Z/+Y/+X normal and deterministic orthogonal up. Slider range is
the min/max projection of all eight bounds corners onto the current normal relative to the plane's base origin;
allow numeric entry beyond that range and negative offsets. Moving after rotation always uses the current normal.
Numeric origin controls change 14's adjust.translation; normal drag changes adjust.offset. All source expressions
remain in the base origin/normal/up fields. Uneditable derived adjustment terms disable only the affected graphical
edit with source-navigation feedback.

The controller begins a 14 draft when a gesture starts and previews it through ClipState. Commit on release/Enter,
cancel on Escape or invalidation; a source-backed commit is one 02 undo group through 14, never per mouse move.
Transient commits stay transient. A source edit/evaluation/tab switch cancels a stale gesture rather than patching
an old source span. If a synchronous commit causes reevaluation, end the gesture before observing that event.

Pick point assigns the world point with orientation unchanged. Pick + align uses the outward geometric normal from
03 and retains its negative side by setting section normal=-hit.outwardNormal, exposing the interior behind that
wall. Transform the world target into the Section's resolved frame. Preserve drawing up by projection onto the new
plane; if degenerate choose the world/frame axis least aligned with the new normal, deterministically.

Normal gizmo drag: compute the closest point between mouse ray and the normal axis; delta from the initial ray gives
offset change. Near-parallel rays use the projected screen normal only when its length is sufficient; otherwise
disable that drag with feedback and keep numeric control available. Rotation rings use ray-plane intersection and
signed atan2 relative to the starting radial vector around the selected local right/up axis. Shift snaps rotation
to 15 degrees; otherwise continuous. Recompute from the initial gesture frame, not accumulated mouse deltas.
Rotate about the current origin: update adjustment rotation and translation together so offset*n changes cannot
move the pivot. Angle entry uses the same quaternion/frame calculation; pole azimuth is display-only, not another
stored geometric field. Flip rotates pi around up and adjusts translation to keep origin fixed.

Reset orientation restores the chosen preset normal/up while retaining origin. Delete a transient Section leaves
source untouched; deleting a source-backed Section explicitly removes its declaration through 14 and can leave
drawing references Missing. Do not silently replace referenced sections or erase a whole source file.

## Renderer coverage and phases

| Input mode | Clipped display |
| --- | --- |
| OpenCSG preview | Prepared mesh of the frozen preview-evaluated tree; initial preparation may be slow. |
| Manifold / PolySet final | GPU clipping of current evaluated mesh. |
| CGAL final | GPU clipping after valid Nef-to-PolySet conversion. |
| Thrown Together / 2D / nonconvertible geometry | Explicitly unavailable; original diagnostic view remains usable. |

[Phase 1](4_imp-phase1.md): cached mesh and GPU correctness/performance;
[phase 2](4_imp-phase2.md): controller/dock/source lifecycle;
[phase 3](4_imp-phase3.md): picks/manipulators/input integration;
[phase 4](4_imp-phase4.md): numerical/regression/package evidence.
This route is chosen to make correctness testable without modifying OpenCSG's boolean algorithm. Runtime evidence
still must establish the limits. No live-clipping success is claimed by this planning document.
