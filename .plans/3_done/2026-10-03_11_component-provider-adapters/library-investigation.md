# Provider libraries: source and executable evidence

Reviewed 2026-10-03 UTC / 2026-10-04 Amsterdam. This verifies candidate source calls using an existing executable;
it does not implement the provider registry, its matcher, UI or insertion. No vendor library is bundled with the plans
or proposed application. A downloaded research fixture is isolated under the run directory below.

## Pinned inputs

- BOSL2: existing D:/openscad/runs/20261002-scadmaxx-skill/libraries/BOSL2; 2.0.766,
  e173fa0ae45f9e2082e0d8c0382dae98621b7c20. Reused the exact 08 investigation input without fetching/changing it.
- BOLTS: the [official downloads page](https://boltsparts.github.io/en/downloads.html) still points to the
  [0.4.1 release](https://github.com/boltsparts/BOLTS_archive/releases/tag/v0.4.1), published 2021-09-13.
  The current boltsparts/boltsparts repository has no latest release through GitHub's releases API (404 at audit).
  The development repo and released OpenSCAD asset are different inputs. Use the measured artifact, not assumed main APIs.
- OpenSCAD asset: boltsos_0.4.1.tar.gz, 35,932 bytes. SHA-256
  1b5656d984ef8019ff78ae5bfdf44baea5e2daab73e25c1e992d96dc8ae990b1.
  Extracted solely into D:/openscad/runs/20261003-provider-planning/libraries/BOLTS after reviewing archive entries.
  The asset contains an LGPL 2.1 license; no vendor implementation/dimension table is copied into shipped catalogs.
- BOLTS common/version.scad says development and [2021,9,13], not 0.4.1. Never use that string alone for matching.
- Executable: D:/openscad/artifacts/20261003-scadmaxx-executable-name/attempt-2/extracted-check/scadmaxx.com.
  Console launcher SHA-256 29dbf910f840c565686eed856a1a0cbb6d20181fea1630878ba9da2505b8f5e2.
  It launches the existing 2026.10.03-experimental-20261003-scadmaxx-executable-name application from the
  4c325716b94e444637a80df3966197ce110b2b75 source audit; this is not a newly built provider branch.

[library-fingerprints.json](library-fingerprints.json) records normalized SHA-256 for 35 BOSL2 and 41 BOLTS source
files reported by native -d. [library-import-edges.json](library-import-edges.json) records 37 and 40 include/use edges
from those exact files. Reachability from std.scad/screws.scad and BOLTS.scad equals the respective native file sets.
Extraction ignored comments/strings; every edge's target was checked inside its matched root. Runtime matching uses
these frozen edges after byte verification, not that research extraction script or runtime regex source parsing.

Aggregate identities under the contract's path/NUL/hash/LF encoding:

- BOSL2: af99ecc69d19198e63794f952c491c162f1039dbbad0cc1cd4c1da8035d25f27.
- BOLTS: d08ca4bd8bc2eb2a6c0a94fc93aad0d3f6c522da620a6d31aeab74f1809795e6.

## Calls and findings

[provider-call-probe.scad](provider-call-probe.scad) SHA-256:
1c11f22658ab3b3813ca39078c7a707ece6aa36a8d1fd090e1c242c8e5aa9efc.
Library APIs inspected: screws.scad screw_hole at line848; BOLTS classes/hexscrew2.scad ISO4017 at91,
classes/hexagonnut1.scad ISO4032 at74, and classes/plainwasher1.scad ISO7089 at132.
Their public calls, dimension tables and geometry origins support the chosen matrix.

The [BOSL2 screw-hole documentation](https://github.com/BelfrySCAD/BOSL2/wiki/screws.scad#module-screw_hole) distinguishes
threaded masks from clearance masks. The pinned call explicitly sets thread=true, head=none, atype=shaft,
counterbore=0, bevel=false, tolerance=6H and $slop=0. BOTTOM/UP are emitted as literal vectors. At nominal M4/depth12,
the generated mask extends to 12.01 and has diameter 4.118436784. This is mask geometry, not an inferred final bore size.

BOLTS ISO4017/ISO4032/ISO7089 supply simplified hardware geometry. The ISO4762 alternative in this release accesses
undefined h in base/hex_socket/hex_socket.scad:48; --hardwarnings rejects it. The selected first screw family is ISO4017.
There is no vendor patch and no runtime alias from the unselected family.

Root include and use forms both inherited command-line BOLTS_MODE=bom/BOLTS_DEFAULT_UNIT=in. A let at the call site
did not isolate the module's lexical settings: the command exited 0 while producing a 1 mm placeholder cube.
Including BOLTS.scad inside a generated module helper produced the expected mm hardware despite those same overrides.
BOSL2 cannot use that import scope: std.scad includes color.scad's file-level use declaration, which fails when nested.
Thus BOLTS imports remain helper-local and BOSL2 imports remain file-level. These are explicit recipe differences.

## Executed evidence

Run root: D:/openscad/runs/20261003-provider-planning. Input archive/API metadata and negative experiments remain there.
The initial cases 0-3 rendered cube, sphere, cylinder and actual plain-hole subtraction successfully.
Final verified-results.json records 25 exits 0: cases 4-8 for each of M3/M4/M5/M6/M8. All final logs were scanned for
OpenSCAD warning/error and BOLTS warning/error echoes: none. Every result reports simple geometry.
Numerical checks verified each threaded mask Z 0..12.01 and each screw shaft end Z 20; M4 bounds are in phase 3.
The final runs deliberately supplied BOLTS_MODE=bom, BOLTS_DEFAULT_UNIT=in and $slop=2 to exercise recipe isolation.
Files verified-<case>-<size>.json/.stl/.log contain native summaries, actual meshes and diagnostics.

Representative command, using PowerShell array arguments and restoring OPENSCADPATH after the run:

```powershell
# OPENSCADPATH points to the two recorded parent library directories, separated by semicolon.
& '<recorded-scadmaxx.com>' --backend Manifold --hardwarnings --export-format asciistl `
  --summary all --summary-file '<run>/verified-5-M4.json' `
  -D 'probe_case=5' -D 'probe_size="M4"' -D 'BOLTS_MODE="bom"' -D 'BOLTS_DEFAULT_UNIT="in"' -D '$slop=2' `
  -o '<run>/verified-5-M4.stl' '<plan>/provider-call-probe.scad'
```

Earlier final-* files are the failed attempt to nest BOSL2 imports, not passing evidence. Earlier scoped-* commands
rendered but --summary bounding-box alone wrote null JSON in this binary; verified-* uses --summary all. Retain those
failed/limited attempts as evidence rather than treating exit 0 as a full geometry check.

Remaining native obligations: real JSON loader, schema checks, exact profile matching, unsaved/shadowed dependencies,
generated rather than hand-authored recipe source, project registration, package contents and the actual 12 consumer.
Those are specified in the phases. No native implementation/runtime readiness is claimed by these library probes.
