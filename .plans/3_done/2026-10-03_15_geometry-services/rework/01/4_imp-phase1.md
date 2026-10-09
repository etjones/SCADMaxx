# Correction phase: implement and verify strict CGAL conversion

1. Add the shared converter analysis behavior and classified failure contract specified in this cycle's design.
2. Route the GeometryAnalysis CGAL adapter through it. Keep Render callers' behavior intact.
3. Run the ordinary CGAL box without initialized application resources; require the specified area/volume/section.
4. Add translated float-collapse and failed-topology/triangulation regression inputs where constructible. Require
   typed failure and absent payload; retain input geometry. Verify the valid empty solid's zero measurements.
5. Reconfigure, verify actual geometry-analysis CTest discovery and run the complete numerical suite. Preserve
   earlier failures as evidence. Run relevant existing projection/cut/export regression checks after converter edits.
6. Continue initial phase 3 supported application build, no-Manifold coverage and recorded local handoff. The already
   passing no-Manifold compile/test evidence remains valid only if later changes do not affect that configuration.

Exit: original GS requirements and public contract pass actual tests, strict CGAL needs no application state, and
normal rendering/projection checks pass. Return to design again if this route cannot preserve strict topology;
do not substitute GUI initialization or remove CGAL support. No commit, promotion or final composition is included.
