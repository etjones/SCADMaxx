# SCADMaxx Windows executable names

SCADMaxx distributions must build `scadmaxx.exe` and `scadmaxx.com` as CMake outputs. Do not
rename an already-built `openscad.exe`, ship old-name aliases, or change independent upstream builds.

Source commits, in order: `4586db20555997712a68e104520c63723a8d0ad2` and
`9fccf36f3bf31563bf380da7b383757238220845`, then
`4c325716b94e444637a80df3966197ce110b2b75` in the shared `openscad-master` repository. The final
commit is retained under `refs/experimental-repairs/windows-executable-name` in private origin.
Apply all three commits when the locked source lacks them. The second prevents the later installation
block from overwriting the Windows output name; without it Ninja still targets `openscad.exe`.
The third makes `tests/test_cmdline_tool.py` recognize SCADMaxx and supply `-o` export arguments.
Without it, CTest opens the input/output as GUI documents and waits indefinitely. Stop only the
test-owned processes, apply that correction, and rerun the same cases; do not change expected output.
This packaging support is needed
by the SCADMaxx Windows profile, including its baseline checkpoints, independently of selected PRs.

The change adds `OPENSCAD_WINDOWS_OUTPUT_NAME` (upstream default `openscad`). The SCADMaxx
recipe explicitly sets it to `scadmaxx` and includes it in the build fingerprint and package metadata.
The GUI target output, console output and child executable name, Windows file metadata, and
CTest executable path agree. Both outputs reside at the build root; no manual console copy is needed.
This does not rename the internal `OpenSCADExe` CMake target or upstream library/resource names.

Future run procedure:

1. Check for this support and apply all three retained commits, in order, with `cherry-pick -x` if absent.
2. Configure with `-DOPENSCAD_WINDOWS_OUTPUT_NAME=scadmaxx`; use a fresh build directory when
   changing an existing fingerprint. Reuse shared vcpkg and keep manifest installation disabled.
3. Run the standard build/Test/Stage/Package steps. Smoke checks require both new names,
   reject `openscad.exe`/`openscad.com`, and check the console version as well as GUI rendering.
4. Run `tests/test_unicode_filenames.py` against both extracted executables. Preserve older ZIPs.

Initial correction run: `runs/20261003-scadmaxx-executable-name`, linked to
`20261002-scadmaxx-updated` without changing its eight frozen feature inputs. See its report
for actual verification results and remaining limits.

Verification: Configure/Build/Test passed at final source `4c325716b94e444637a80df3966197ce110b2b75`;
78,118 unit assertions, both launcher version checks, Manifold/CGAL STL, PDF and PNG checks passed.
Seven Unicode cases passed through each launcher. All six focused CTest cases passed with the corrected
harness. Runtime dependency and Qt plugin deployment probes passed. See the linked run report for
final archive/extraction results. Shared dependency records are unchanged.

## Newer upstream resource templates

Run `20261004-scadmaxx-all-features` applies the same three repairs to upstream
`81ade7d33a8ed14fc6817a1cf0d44334592bb9fc`. The first cherry-pick conflicts in
`resources/openscad_win32.rc.in` and `resources/openscad_win32-nightly.rc.in` because upstream
now uses `2009-${OPENSCAD_YEAR}` in the copyright field. Keep that upstream year expression
and its numeric version fields; change only InternalName to `@OPENSCAD_WINDOWS_OUTPUT_NAME@`
and OriginalFilename to `@OPENSCAD_WINDOWS_OUTPUT_NAME@.exe`. Do not restore the old hardcoded
2024 copyright year or the previous nonnumeric resource version handling.

The adapted first commit is `910f4023d16fa9c34027ad8e6ade7ce32bec5f53`, followed by
`c57996e956413593cc5e8b32df94be28da390114` and `f1e091abe5606e3e2b447b7733ef749edb2d63f9`.
These commits are retained locally in the shared source repository, not pushed. The repaired
baseline passed build, 75,145 unit assertions and controlled-PATH runtime smoke checks at
`fdeeff10b05da7b30ae42f6860f2b4e816924462`; see that run's
`logs/20261004T221415751Z-test.json`. Final composition/package validation is separate.
