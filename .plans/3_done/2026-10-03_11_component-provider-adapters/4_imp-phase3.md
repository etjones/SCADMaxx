# Phase 3: real library catalogs and geometry

Requirements: PR01-04, PR07-13. Prerequisites: phases 1-2. External libraries are test inputs, not application resources.

1. Create bosl2.json/bolts.json using the exact provider-contract matrix and fingerprint profiles. Record upstream
   sources and notices for authored/derived metadata. Copy no vendor SCAD modules or dimension tables into the product.
2. BOSL2: generate file-scope std/screws imports and explicit named hole arguments, including $slop=0. The local
   origin is the bottom of the positive-Z mask; normal +Z lets 08 Mate point it into the picked surface.
3. BOLTS: emit a symbolically named helper for each hardware entry, with BOLTS.scad included inside its module body.
   Helper arguments are explicit. Do not hoist/deduplicate these local imports or add global BOLTS settings overrides.
4. Generate complete standalone SCAD from public APIs, not hand-written equivalent source. Supply fixture libraries
   through explicit paths. Compare native -d dependencies with the 35/41-file profiles and their recorded import edges.
   Test imported-symbol identity and return required defining-file metadata to the consumer.
5. Run first-release sizes M3/M4/M5/M6/M8 and parameter limits. Add a primitive block minus the hole masks to prove
   subtraction in the test harness; boolean source mutation remains 12's responsibility.

## Meaningful checks

- providers-source and providers-external: all emitted files parse/render with --hardwarnings; also scan BOLTS Error/
  Warning echoes. Record dimensions, not only exit codes. Use --summary all; the audit's bounding-box-only JSON was null.
- M4 ISO4017 length20 bounds X +/-3.5, Y +/-4.0414518843, Z -2.8..20. Nut Z 0..3.2; washer radius4.5 and Z 0..0.8.
  Compare bounding values with 1e-6 mm tolerance, using the same pinned $fn=48 fixture.
- M4 BOSL2 depth12 mask bounds Z 0..12.01, diameter about4.118436784. Block-minus-mask bounds remain20x20x10;
  verify a real hole with section/interior-triangle or signed-volume analysis in the test helper, not a screenshot.
- Repeat hardware with calling BOLTS_MODE=bom/BOLTS_DEFAULT_UNIT=in; geometry remains the expected mm hardware.
  Repeat BOSL2 with ambient $slop=2; explicit argument keeps the same tested mask.
- Editing a matched library file disables its item before emit. ISO4762 is absent, not a silent alias for ISO4017.

Exit: native generators produce tested source and geometry from both externally installed pinned profiles.
An unsupported vendor call returns to planning; do not patch/download a replacement vendor library inside this feature.
