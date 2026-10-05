# Anchors and attachments: technical implementation plan

Status: source-reviewed specification prepared 2026-10-03; all six decisions accepted. The pinned BOSL2 probe passed;
native feature implementation/runtime checks remain outstanding. Read [requirements](2_requirements.md),
[source contract](source-contract.md) and [BOSL2 evidence](bosl2-investigation.md).
Branch feature/anchors-attachments; direct prerequisites 03/07/14 and their closure, including 02/06 and selected
OEP8/Customizer. No 04/09/10/11/12/15 requirement. Freeze a prerequisite-only base; do not use the moving full build.

## Evidence and files

Audited native source: wt-scadmaxx-20261002 at 4c325716b94e444637a80df3966197ce110b2b75. ScopeContext::init evaluates
assignments before body geometry; UserModuleContext applies Parameters::parse first. SourceFile::instantiate returns
the evaluated root before GUI/CLI find_root_tag and Tree setup. TransformNode exposes a Transform3d matrix, so a
placement pass can wrap a Component without changing its finished Part body. These are implementation seams, not
claims that 07/08 exist in that binary. Inspect actual owner handoffs before coding.

Require [the 14/07 extension contract](../2026-10-03_00_source-first-cad-overview/semantic-extension-contract.md) in
their tested revisions. New core src/core/anchors/: ReferenceKinds, ReferenceCollector, ReferenceScene, AnchorFrames,
AttachmentGraph, AttachmentSolver, AnchorResolver, AnchorOperations (.h/.cc and tests). New GUI src/gui/anchors/:
AnchorController, AnchorInspectorContribution, AnchorSourceEdits, AnchorOverlay (.h/.cc). New shipped SCAD helper
libraries/SCADMaxx/bosl2-anchors.scad, doc/anchors-and-attachments.md, testdata/scad/anchors fixtures and
src/guitests/TestAnchors.{h,cc}. Wire CMake/test/resource/library install paths explicitly.
Register kinds, resolver and placement pass through owner APIs at core application initialization used by CLI/GUI.
All frame/graph code is Qt-free. No consumer controller imports 04, drawing/provider/insertion or geometry-services code.

## Types, discovery and ownership

Register Anchor/Point/Axis/Plane/Attachment as assignment hosts with Consumer destination. Reuse existing @{type:...}
grammar; metadata contains type only, object fields in RHS. Decode the exact source-contract schemas. Copy native
evaluated Values once, including helper-returned objects; preserve source keys and expressions through 06/14 maps.
The direct semantic body scope requirement is verified using 07 currentScope, not the nearest arbitrary call stack.
An ordinary helper function may construct an object; an ordinary helper module is not a new declaration owner.

Core immutable records (names chosen for implementation):

```cpp
struct OwnerKey { enum class Role { Document, Instance, DefinitionDefault } role; std::string id; };
struct ReferenceKey { OwnerKey owner; std::string id; }; // ordered/hashable, labels excluded
struct Anchor { Vector3d position, normal, up; double spin; Vector3d adjustment; Quaterniond rotation; };
struct Point { Vector3d position; };
struct Axis { Vector3d position, direction; };
struct Plane { Vector3d position, normal; };
using ReferenceValue = std::variant<Anchor, Point, Axis, Plane>;
struct ReferenceRecord {
  ReferenceKey key; std::string label; ReferenceValue value;
  Design::DeclarationKey source; uint64_t invocation;
  bool fixedCapture, drawingFrame; // only Anchor supports these flags
};
struct Endpoint { OwnerKey component; std::string anchor; };
struct Attachment {
  OwnerKey declaringOwner; std::string id, label;
  Endpoint child, target; enum class Mode { Mate, Align } mode;
  Vector3d offset, offsetAdjustment; double spin, spinAdjustment;
  Design::DeclarationKey source;
};
```

Keep a result-owned ReferenceScene with source-input/configuration fingerprints, records, declarations-to-invocations,
diagnostics, graph and solved placements. Parameter Values remain in 07; do not add a second parameter authority.
OwnerKey::DefinitionDefault is for a separately instantiated default target, never an arbitrary live instance.
Resolve source-relative paths after all native instances exist, using the declaration's captured owner. Root document
is an explicit key, not an empty Component ID. Retain 07's path escaping; no filesystem normalization of model paths.

IDs across Anchor/Point/Axis/Plane share one namespace per owner. Attachments have a separate ID namespace per
declaring owner and a separate unique driven-child index. A definition anchor and explicit instance addition sharing
an ID invalidate both, not override. Definition/source label changes preserve keys. Missing/deleted owners or named
anchors remain missing. Invalid unreferenced metadata can remain a record diagnostic; an Attachment consuming it fails
the new geometry result. Duplicate placement drivers/cycles always fail; never leave a child silently unplaced.

## Frame convention and affine owners

Column vectors, 4x4 matrices, composition left-to-right as matrix multiplication applied rightmost first. Source
angles use degrees, C++ trigonometry uses radians. Normalize n; project up onto its tangent plane and normalize to u;
r=u cross n. R=[r u n] is right-handed. Reject zero/nonfinite inputs and normalized cross magnitude <=1e-10.
Anchor base orientation is R * Rz(spin). Apply normalized adjustment quaternion Q in owner coordinates on the left;
position is p+adjust.translation. Q rotates orientation about that anchor point, not the point about the owner origin.

For an affine owner W=[L,t], resolve point p'=L*p+t, normal n'=normalize(L^-T*n), and up
u'=normalize(L*u - n'*dot(n',L*u)); rebuild r'=u' cross n'. Store reflection parity separately for inspection, never
return a left-handed or scaled attachment frame. Axis direction uses normalize(L*d), not the normal formula. Plane
normal uses inverse transpose. Points need no inversion. Reject an inversion when sigmaMax is zero/nonfinite or
sigmaMin <=128*DBL_EPSILON*sigmaMax; reject nonfinite transformed results. This is an explicit supported-conditioning
bound, not a claim of unlimited precision. Local authored mirror/scale in Part geometry stays in that geometry.

The inverse capture of a world hit uses p_local=W^-1*p_world, n_local=normalize(L^T*n_world),
u_local=normalize(L^-1*u_world), with tangent projection/validation. Verify the round trip numerically. Choose the
transient up by projecting captured camera-up onto the hit tangent plane; if degenerate use the least-aligned world
axis, with fixed X/Y/Z tie order. Store this chosen up when saving; later camera motion does not rotate a saved anchor.
If semantic ownership is unavailable, expose a Fixed document point explicitly; never pretend it follows an anonymous
module. A singular owner cannot support inverse local capture and disables that Save target with a reason.

Only Anchor yields a complete rigid attachment frame. Point/Axis/Plane resolution returns its typed value. Callers
must supply missing direction/up explicitly to construct an Anchor; no type coercion that silently constrains spin.
Canonical drawing frame uses the owner's purpose=drawing Anchor, else its local axes. A non-rigid owner has no rigid
default drawing frame; use an explicit Anchor or report Unsupported. 14's rigid-frame rejection remains intact.

## Placement graph and algorithm

Run in 07's pre-publication placement pass after collection, before any CSG/provenance/render/export publication.
Graph vertices are all native Component instances plus fixed document root. Add containment edges parent -> child,
then attachment edges target owner -> driven child. Deduplicate equal edges. The child endpoint must belong to the
driven Component; target may be a sibling, ancestor, other branch or document anchor. Forbid self-target and descendants
driving an ancestor. A stable Kahn topological sort uses lexicographic full paths for independent nodes. Report a
concrete cycle path and each Attachment source on failure. Semantic containment/tree parentage never changes.

Process parents/targets before children. For an instance, first compute its base world Wc using finalized containment
ancestors and its source-authored relative transforms; do not include its own new correction yet. Resolve Fc, its
child anchor frame under Wc, and Ft, the target anchor frame under that target's finalized transform. With
o=offset+adjust.offset and s=spin+adjust.spin:

```text
M = identity (Align), or Ry(pi) (Mate)
Fdesired = Ft * Translate(o) * Rz(s) * M
Dworld = Fdesired * inverse(Fc)
Wsolved = Dworld * Wc
```

Dworld is rigid/proper; therefore distances in the child's already transformed geometry do not change. Offset stays
in Ft's unspun axes. Mate opposes normals and preserves up at zero spin; Align agrees in all three axes. Require
finite matrices, determinant/orthonormal residual <=1e-10 for Dworld rotation. Do not silently project a bad solution
back onto a nearby rotation. An unattached vertex retains Wc. A moving Assembly carries its descendants through the
containment edges; attached descendants then solve against their targets using that current base.

For insertion in the native node tree, let U be the finalized transform immediately outside the Component's returned
GroupNode (including intervening native transforms). Wrap that GroupNode in one TransformNode with
K=U^-1*Dworld*U. This may be locally affine under a scaled ancestor, but its world effect is exactly the rigid Dworld.
Keep the Part body/localRoot unchanged. Retain a synthetic flag-free ModuleInstantiation for each wrapper and link
its provenance to the original Component call/invocation; never duplicate root/highlight/background modifiers.
Rebuild 07 final transforms and 06 provenance after all placements; no in-place cached Geometry mutation.
An insertion/inversion/graph failure aborts the new result atomically. Fresh evaluations start from source matrices;
never reapply corrections from a previous result. Publish one finalized scene for all consumers.
If root-tag extraction cuts away a required placement wrapper, reject that root configuration explicitly rather than
publishing an unplaced result. Ordinary untruncated roots and Model tree Solo preserve the complete solved scene.

Every declaration is evaluated once. Anchor coordinates cannot query solved world placements through a new SCAD
function during native assignment evaluation: attachments use endpoint references resolved in the later pass.
This avoids accidental recursive reevaluation or an implicit numerical constraint solver. Loops of Component calls
work through explicit 07 keys; multiple Assembly instances each get their own relative graph.

## Resolvers and downstream APIs

Register domain anchor with token `{domain:"anchor",id:"mount",data:{owner:<07 semantic or document token>}}`.
Source shorthand component paths are expanded to these canonical tokens in the evaluated records. Definition tokens
resolve only through the owned default-target evaluation; instance tokens resolve in the current successful scene.
Use 14's Changed/Missing/Invalid/Unsupported states: stale input/configuration -> Changed, missing key -> Missing,
duplicate/malformed/cyclic -> Invalid, wrong reference kind or ill-conditioned required frame -> Unsupported.

`AnchorOperations::resolve(token, expectedResult)` returns a retained ReferenceScene plus typed local/world values,
optional rigid frame, source and diagnostic. The registered 14 resolver exposes a frame only for a valid Anchor.
Never synthesize a finite bounding box for an infinite axis/plane; GUI helper extents are separate. Point/Anchor bounds
may be degenerate points; 14 consumers requiring nonempty fit bounds report unavailable normally.
`solvePlacement(childFrame,targetFrame,mode,offset,spin)` is a pure numerical operation returning Dworld or an error.
`validateAttachmentDraft(draft,currentScene)` returns graph/ownership diagnostics and a candidate transform without
editing source. 10/12 consume these functions, then own their explicit source-edit/insertion workflow.

07 local/As placed export uses the finalized tree. A Component's own attachment wrapper is outside its local Part
root; Assembly local output includes solved internal placements. Definition-default evaluation runs the same pass
with its defaults and a synthetic root owner. Relative internal endpoints work; unresolved absolute external owners
produce an explicit dependency error, never a borrowed world transform. Hide/solo/clipping have no input to this pass.

## BOSL2 bridge and source generation

Implement the exact [pinned mapping](bosl2-investigation.md) in one shipped helper. Use _find_anchor only there and
assert BOSL_VERSION == [2,0,766]. Freeze the tested commit and API-file hashes in the adapter manifest/fixtures;
runtime evidence includes 03's actual captured library bytes. A different version is unsupported until explicitly
validated/repinned, with no alternative-call aliases. Normal user-written BOSL2 code remains outside this adapter gate.

Build B from position, direction and spin as verified. Apply the explicitly supplied shape placement to B's point,
normal/up using the same affine-frame rules, then emit ordinary Anchor object fields. Use BOSL2 matrix/vector helpers
for SCAD computation; parity/nonfinite/singular checks mirror the C++ convention and are tested against it.
Initial geometry descriptors are 3D cuboid/prismoid, cylinder/cone, sphere and explicit custom named anchors; reject
2D and path/VNF descriptors. Automatic capture of arbitrary attachable modules is outside this adapter. An explicitly
supplied supported geometry descriptor still uses BOSL2's own anchor lookup, including its stored override callable;
validate the returned anchor fields instead of attempting to introspect that function. These limits affect the
adapter, not ordinary native Anchor expressions.

The initial bridge gives semantic Parts meaningful BOSL2 anchors and uses the common native Attachment solver.
It does not wrap Component calls as BOSL2 child geometry or generate inside/tag booleans. No mandatory BOSL2 link,
runtime installation or library duplication is added to the native C++ core. Plain-source examples/tests compile
with no BOSL2 include path. Follow current library install rules when packaging the helper; package tests must
prove include <SCADMaxx/bosl2-anchors.scad> resolves and a missing BOSL2 gets a clear diagnostic.

## Inspection, source editing and lifecycle

AnchorController registers a 03 Inspector contribution and per-selected-owner reference overlays. Show names/types,
definition or instance origin, parametric versus Fixed local capture, local/world values and validity. Helpers use
03 overlay tokens and do not enter surface picking or model geometry. Keep the normal scene usable when helpers are
off. A reference list selects the owner/reference without changing visibility or authoring source.

Pick anchor uses 03's current hit and a transient 14-managed draft. Save anchor writes a new typed Anchor assignment
into the root live editor, with explicit absolute owner path (or document ownership), stable generated ID, captured
local values and capture=fixed. Choose a collision-free SCAD variable name; use 14's source insertion/undo lifecycle
and 02's transaction. Keep imported library definitions untouched. Undo promotion restores the transient draft through
14's joint source/lifecycle history. Cancel/source invalidation changes no source; raw result-bound drafts become stale.

Attachment Inspector exposes mode, target/child, offset and spin. Base expressions remain intact: numeric changes
edit literal adjust.offset/adjust.spin only. Read-only/computed RHS or expression adjustments offer source navigation.
One source declaration used by multiple invocations is explicitly shared: require the user to select Edit shared
declaration before enabling its controls, showing affected use count. An instance-only UI edit cannot rewrite it.
Named-reference label edits likewise use the declaration's honest scope; no hidden per-instance override map.

AnchorSourceEdits consumes 06 exact spans and 14 lossless field maps, checks 03 input/configuration freshness and
02 document/revision/expected bytes, then uses one pre-group-guarded transaction. Literal vectors/quaternions use
finite round-tripping SCAD serialization. Preserve comments/BOM/EOL and unrelated bytes. Never silently bake position,
normal/up/offset/spin expressions. Ordinary Save owns disk writes. Source/result/tab changes cancel stale edits and
rebuild the evaluated graph. One source authority supplies both UI and headless behavior.
Register 14's generic lifecycle adapter for the reference kinds, using an opaque encoded ReferenceKey to resolve
source records and locate promoted drafts. The adapter supplies source edit requests; 14 retains draft snapshots and
the joint undo participant. A local anchor ID alone cannot bind a promoted draft to another owner's same-named anchor.

## Verification and phase order

1. [Schemas, scoped collection and source cases](4_imp-phase1.md).
2. [Frames and graph solver](4_imp-phase2.md).
3. [Native placement and consistent output](4_imp-phase3.md).
4. [Pinned BOSL2 bridge](4_imp-phase4.md).
5. [Inspector, capture and guarded source edits](4_imp-phase5.md).
6. [Regression, branch composition and handoff](4_imp-phase6.md).

Use [shared verification commands](../2026-10-03_00_source-first-cad-overview/verification-contract.md).
Core math/graph tests need no GUI/BOSL2. Native pick/lifecycle checks require the desktop GL harness. A compiling
bridge or the planning probe alone cannot satisfy native requirements. Stop a failed phase with concrete evidence
before dependent UI work; never silently weaken source ownership, live placement or failure semantics.
