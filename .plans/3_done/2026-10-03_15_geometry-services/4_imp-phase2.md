# Phase 2: numerical measurements and sections

Covers GS01-GS09. Build on phase 1; do not call the general repairing conversion helper.

1. Implement measureSolid using copied/transformed strict Manifold geometry and finite area/volume validation.
2. Implement section using the specified right-handed frame, composed transform, Slice and sanitized Polygon2d.
   Publish contours/holes/frame/area together only after successful validation and a final cancellation check.
3. Add every numerical fixture in [requirements](2_requirements.md), including the through-hole and two disjoint
   boxes supplied as one evaluated Manifold solid, not an unresolved GeometryList.
4. For normals +Z/up +Y, require frame X/Y = world X/Y and transform round trips. Rotate geometry and frame together
   and compare local contours/area; reflect/scale geometry and verify valid nonnegative volume and expected dimensions.
5. Test minimum/maximum-Z coincident planes, flipped normal, tangent/no intersection and multiple disconnected cuts.
   Assert hole classification and net area; checking only vertex counts misses a filled-hole regression.
6. Repeat identical operations and compare deterministic contours within stated tolerances. Test scale variants
   1e-3 and 1e3 with dimensionally scaled expected values; report actual tolerance, including Clipper quantization.
7. Verify cancellation/limits/invalid topology never return plausible zero measurements as a successful fallback.

Verification: rebuild OpenSCADUnitTests, confirm named cases are discovered, run the geometry-analysis label.
Exit: all required numerical fixtures pass; inputs remain unchanged; boundary and accuracy limitations are documented.
If a fixture contradicts the proposed backend contract, resolve the contract here before consumer branches start.
