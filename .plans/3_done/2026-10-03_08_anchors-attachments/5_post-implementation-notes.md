# Anchors and attachments: local implementation evidence

Locally complete and verified, 2026-10-04. Feature 12 follows this handoff.

Source: `D:/openscad/wt-openscad-anchors-attachments`, branch `feature/anchors-attachments`, retained HEAD/base
`6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Run: `D:/openscad/runs/20261004-anchors-attachments`.
Source changes are uncommitted; the source patch and affected-file hashes identify the implementation.
No staging, commits, promotion, push, readiness/stack change or integrated distribution is part of this handoff.

Final feature-only patch SHA-256: `474b690a175d2ea4eb6d6e6c096968494e1c76d3f96809055130c5ce92736676`.
Complete input: `61a07718bbca47e5ec09270b4b0ca9db49dd03a75e5898dc3fe1d0311e5a926e`.
`final-source-evidence.json` independently replays the feature delta and verifies all 246 affected working files.
[Acceptance evidence](../../../../runs/20261004-anchors-attachments/acceptance-evidence.json), SHA-256
`a96043f42fce502b15827f58acadccee27a8a0a193796e72834b738a8e330949`, binds exact source, native reports and package.
All 205 original 07 handoff files remain unchanged. The generated Clipper version header is retained separately and
its original working bytes restored; indexed submodule revisions and shared dependency bytes are unchanged.

## Behavior and requirements

| Requirements | Implemented behavior and evidence |
| --- | --- |
| AN01–AN03 | Strict Anchor/Point/Axis/Plane collection with actual scoped owner identity. Points, axes and planes expose their own typed world values; incomplete orientation never becomes an attachment frame. Core schema/collection and native typed helper cases. |
| AN04 | Proper canonical owner/drawing frames and explicit up projection. Core frame/resolver cases and default-definition native resolution. |
| AN05–AN06 | Parametric named declarations and fixed owner-local captured coordinates use 14's source Records and resolver states. Source/input/result freshness includes changed/closed included owners. Native transient capture, Save, Undo/Redo and reopen. |
| AN07–AN08 | Shared frame capture and rigid Mate/Align placement. The installed SCAD helper maps bounded pinned BOSL2 anchors to ordinary Anchor data. Native and 26 independent installed-launcher cases compare the implemented bridge with actual BOSL2 attachment transforms. |
| AN09–AN12 | Source-only authority, explicit owner namespaces and default contexts. Capture/cancel has no source change. Save and supported literal adjustments use one 02 transaction; computed base expressions remain intact. Shared edits explicitly list declaration uses. |
| AN13–AN15 | Containment plus attachment DAG, one driver per child, lexical deterministic order and pre-publication validation. Missing/cyclic/multiple relations fail without usable wrongly placed export. Native preview/render and both CLI launchers use the solved tree. |
| AN16–AN17 | Corrected tree, semantic placement and provenance retain the same scoped paths. Independent reused Assemblies support equal local IDs. Hide/Solo/clipping do not change graph or export. Duplicate IDs fail within the exact owner. |
| AN18–AN19 | Inspector reference list, declaration navigation, transient Pick/Save/Cancel, label/translation/quaternion and Attachment adjustment controls. Native shared, read-only, stale, include-owner and source/annotation joint undo cases. |
| AN20 | Nonuniform/mirrored capture and proper orientation, inverse-transpose normals, rigid distance preservation, conditioning rejection and honest unavailable frames. Core numerical fixtures and affine native surface capture. |

The attachment transform is `Ft * T(offset + adjustment) * Rz(spin) * MateRy(pi)/AlignI * inverse(Fc)`.
Offsets use the target's unspun axes. Corrections wrap the existing native tree without deforming the child's world
shape. Declaration-owned parameters are collected from their actual evaluated scope. Invalid relations abort the
native publication driver before geometry consumers receive a current scene.

Source/API documentation is `doc/anchors-and-attachments.md`. The installed helper is
`libraries/SCADMaxx/bosl2-anchors.scad`; its descriptor contract is `bosl2-adapter.json`.

## Prerequisite boundaries

The feature uses 03/07/14 and their 02/06/OEP8/Customizer closure. No 04/05/09/10/11/12/13/15 implementation is
required by the minimal checkout. The exact 07 complete input is
`7da00d78d6886e7d984067bdcaf01f5363bd674d42d5ac6cf8b05c0c37aff904`.

`inputs/manifest.json` locks separate owner follow-ups: 07 consumer result/default context, 14 rejection before
value evaluation, native literal duplicate proof, consumer draft/literal field previews, preview isolation/comma
coalescing and 03 renderer restoration. These generic inputs are independently replayed and excluded from 08's
feature-only patch. Original owner checkouts and the completed 07 handoff remain unchanged.

03's renderer fix captures the newly installed native renderer synchronously before a queued consumer releases the
previous inspection request. A fake-consumer desktop regression reproduces the release ordering. The Inspector
scroll sizing follow-up is also generic and separately retained; it does not contain Anchor types.

## Executed checks

- Windows Release application/console/unit build on the shared profile, with experimental features and Manifold
  Minkowski enabled. CTest discovery confirms the requested cases; 156 affected cases pass.
- Full unit discovery: 222 cases; full-process JUnit: 321 parameterized rows, zero failures/errors. Four parser/import
  checks pass. The pure frame, graph, solver, resolver, evaluator, source edit and real BOSL2 checks are included.
- Native Anchor: 12/12, Selection 19/19 before the sizing follow-up, Design 10/10. Full minimal native suite: 112
  rows across eleven classes, zero failures/skips, including actual HTTP/annotation/navigation workflows.
- The extracted verification package repeats the full 112-row native suite with clean PATH. Extracted Anchor
  checks at 150% and 200% scaling each pass 12/12.
- Both extracted launchers pass ten solved CSG/STL checks: original and changed target parameters agree, and a
  missing reference fails without usable export. Bounds change only for the parameter-dependent assembly.
- The clean-PATH BOSL bridge suite passes all 26 checks. BOSL2 is external, pinned at 2.0.766,
  `e173fa0ae45f9e2082e0d8c0382dae98621b7c20`; API/source hashes remain unchanged. It is not bundled.

The final extracted package after the generic Inspector sizing correction passes 113 native rows in eleven classes,
including Selection 20/20. Both extracted Anchor DPI runs repeat 12/12, both launchers repeat ten CLI checks and the
bridge repeats 26 cases. Package SHA-256: `d121e8a2bb62b3355aaddc6ea2720fe71f3450608811756a39700cda2444e8f0`.
Installed executable/console, seven shaders, helper, manifest, example and documentation match the source/build.

The optional verification composition in `wt-openscad-anchors-composition-check` combines exact 08, selected #6878,
04 and 05 inputs. Its Release build and all 175 affected cases pass. Native Anchor 14/14 includes two real interaction
cases: a Section framed by an Anchor on a placed Component follows a target parameter change and clips actual picks;
hidden/clipped STL export preserves the full original placed geometry. A Vim insertion and an Anchor literal edit
form separate Undo/Redo steps. Composition-only test code remains outside the 08 feature delta.

The final combined native run exercises 142 rows across thirteen classes. All behavioral checks pass; its one clipping
frame-time failure occurred while the fresh 12 prerequisite build was compiling (eight-plane p95 43.05 ms).
The unchanged focused Clipping suite, rerun with that build idle, passes 14/14: 102,396 triangles at 1280×720,
one-plane p95 12.23 ms and eight-plane p95 11.65 ms, below the unchanged 33 ms limit. Both reports remain retained.
The earlier complete combined run passes 141/141 before adding the generic sizing regression.
`composition-check/final-inputs.json` binds the final merged files; the two additional native Anchor interaction
tests have separate SHA-256 `28cd4ce50ffd82ba5c39bfd45ef28a247d41c6a46d76d0c6338335017fdc3980`, excluded from the
minimal feature patch.

## Retained failures and limits

Early failures and diagnostic attempts remain in the run. Corrections included the native duplicate-object evaluator,
consumer preview ownership, renderer release ordering, clean-PATH DLL deployment, source serializer assertions,
fixture isolation from previous Eye/Solo state and annotation cleanup before tab close. The earlier incomplete
joint-undo native run was stopped after an unsaved annotation stranded its cleanup; the corrected run verifies the
complete undo sequence and returns annotation state clean before closing. Failed reports are not counted as passes.

MSVC 14.51.36231, Windows SDK 10.0.26100.0, Qt 6.11.1/QScintilla 2.14.1 and existing shared vcpkg are unchanged.
OpenGL evidence: 4.6 NVIDIA 616.92, GeForce RTX 3070 Ti, QOpenGLWidget, 24-bit depth/8-bit stencil.
Other platforms, Qt5/headless builds and clean-machine portability remain unverified. Arbitrary BOSL2 descriptors,
automatic surface rematching, general constraints and downstream authoring tools remain outside this bounded feature.
Definition-default descendant token paths report Unsupported rather than inventing an instance identity.

A later requested integrated build must select the exact handoff inputs and run release acceptance. The portable
archive here is development verification staging. Promotion remains a separate user decision.
