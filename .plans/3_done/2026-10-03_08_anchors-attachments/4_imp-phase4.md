# Phase 4: pinned BOSL2 bridge and packaging

Covers AN08/AN10/AN12/AN14. Use the exact revision, source findings and passing planning fixture in
[bosl2-investigation.md](bosl2-investigation.md). It is a bounded adapter, not a replacement attachment engine.

1. Implement libraries/SCADMaxx/bosl2-anchors.scad with smx_bosl2_anchor(id,geometry,selector,label,placement).
   Include the external BOSL2/std.scad, validate supported version/descriptor kinds/selector, call _find_anchor in
   this one adapter and map position/direction/spin to full normal/up using the verified B matrix. No guessed bounds.
2. Transform through explicit placement with the same affine point/normal/tangent rules and validation as C++.
   Return ordinary Anchor fields for typed discovery. Do not invent a new evaluated Value type or inspect arbitrary
   module internals. Keep current argument names only; no deprecated from/to/norot aliases or version fallbacks.
3. Add adapter manifest (pinned commit, version and relevant API source hashes), examples and source-generation
   fixtures. An unsupported installed version reports a clear diagnostic. Keep native core/ordinary Anchor tests
   runnable with no BOSL2 present; do not auto-install or copy the external library into the application package.
4. Register [anchor-bosl2] fixture execution against the pinned library and install/package the SCADMaxx helper using
   the native library resource rules. Confirm packaged include resolution, missing library behavior and source maps.

Rerun bosl2-frame-probe.scad and extend native typed examples for standard cube faces/edge/corner, cylinder end/radial,
sphere direction, named oblique anchors and a shape with explicit reorient placement. Compare pure C++ frames and
actual BOSL2 attachment transforms for the supported basic Mate cases, including negative gap and spin. Native Align
must retain shape/parts and introduce no BOSL2 remove tag; do not map it to inside=true.

Test mirror/nonuniform placement against explicit affine-frame expectations (not an assumption that BOSL2 resizes
children according to our semantics), unsupported 2D/path/VNF descriptors, missing names and wrong version. A supported
geometry descriptor with an explicit override uses the library's returned anchor values; malformed results fail.
The two-child attachable fixture must use an explicit union() group; preserve the corrected planning fixture.
Exit: supported adapter calls, field mapping, version gate and packaged include work. The planning probe alone does
not satisfy this phase; it lacks typed native declarations and the implemented bridge.
