# Phase 2: visible surface position and normal

Covers SI01/SI02/SI08. Depends on phase 1's binding; use [the exact picking algorithm](3_overall-plan.md).

1. Add SurfacePick FBO/state guard/shaders and SelectionService; replace the old y conversion in the new path.
   Add [surface-pick-math] unit tests for projection/unprojection, pixel centers, DPR, nonzero positionOrigin and invalid viewports.
2. Extend ShaderType and OpenCSG/PolySet draw dispatch; assign remapped IDs and explicit subtraction polarity.
   Preserve OpenCSG's matching position transformation between visibility and shading passes. Add CGAL pick-mesh
   caching using existing Nef conversion; never call general repair as an attempt to make picking succeed.
3. Freeze a camera before each two-pass pick; validate binding/inputs before and after readback. Handle FBO failure,
   empty geometry, unsupported diagnostic/2D views, too many IDs and degenerate normals explicitly.
4. Test native TestSelection fixtures under both preview and final renderers:
   - cube([10,10,10],center=true), front center: exact selected face point and outward unit normal;
   - difference of centered cube(10) and translated smaller cube: pick an internal subtraction wall and verify sign;
   - rotated and nonuniformly scaled cube, mirrored cube, two repeated cubes, overlapping front/back objects;
   - orthographic/perspective, 100%/150%/200% DPR, resize, all four viewport borders and miss outside geometry;
   - highlight included, background excluded; RGB ID zero/maximum/overflow and renderer replacement mid-request.
   Assert point/normal tolerances in the overall plan, not only a screenshot color comparison.
5. Implement InspectionPresentation, InspectionMeshRenderer and the GUI coordinator from the
   [shared contract](../2026-10-03_00_source-first-cad-overview/inspection-presentation-contract.md). Add
   [inspection-presentation] cases for provider priority/lifetime, stale completion, request release and mask
   intersection. Native fake two-piece provider/effect cases must prove identical color/pick visibility, masks,
   renderer restoration and generation/serial invalidation. No 04/07 headers or actual consumer implementation.
6. Verify the application still renders identical unselected scenes and restored GL state after repeated picks.
   Package-check the two shader resources using existing shader install rules; no new GL dependency is required.

Run [surface-pick-math], [inspection-presentation] and native TestSelection. Exit only after OpenCSG, Manifold/PolySet and convertible CGAL hits
pass on the supported Windows GL driver. Record unsupported capabilities explicitly. If a visibility/sign assertion
fails, fix this pass before implementing consumer UI; do not label the renderer proven from a successful compile.
