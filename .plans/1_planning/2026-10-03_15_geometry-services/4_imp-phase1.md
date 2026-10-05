# Phase 1: contract, frames and strict inputs

Covers GS01-GS03, GS05-GS06, GS08-GS10. Follow the exact DTOs and ownership in [the design](3_overall-plan.md).

1. Create the public header and implementation. Add production CMake registration and explicitly append the new test
   source to TEST_SOURCES. Use Catch tag `geometry-analysis`; verify discovery before any filtered run.
2. Implement input validation, limits, cancellation checkpoints, frame creation and strict backend preparation as
   internal helpers. Add bounds; expose unimplemented solid/section operations only in the next phase, without
   claiming availability to consumers. Keep each commit/build internally consistent.
3. Build indexed fixtures directly in tests using existing Geometry types: closed cube, cube missing one face,
   duplicate/disconnected-index triangle soup, invalid indices, unused remote vertex, empty geometry and 2D polygon.
4. Verify bounds ignore unused vertices and reflect actual transformed vertices, not a transformed AABB. Use a
   rotated non-box mesh whose transformed AABB would be larger. Verify input vertices/matrix remain unchanged.
5. Test finite/zero/parallel normal/up, mirrored and nonuniform transforms, invalid/nonfinite inputs, explicit limits
   and cancellation before work. Verify unknown PolySet manifold flag does not reject a valid indexed cube.
6. Test the strict helper rejects invalid topology without modifying/repairing input. Record backend status in a
   diagnostic. Verify unresolved GeometryList is rejected rather than concatenated.

Verification: the handoff standard's OpenSCADUnitTests build, CTest discovery and `-L geometry-analysis` commands.
Exit: contract compiles, meaningful frame/input/bounds tests pass and no production UI/server dependency exists.
