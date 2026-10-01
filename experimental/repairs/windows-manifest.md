# Repair: windows-manifest

- State: reusable; both executables linked, baseline tests and manifest inspection passed.
- Failure: CVT1100 duplicate MANIFEST resource ID 1, followed by LNK1123, in application and unit-test links.
- Applies after: baseline; no feature prerequisite.
- Source repository: `D:/openscad/openscad-master`.
- Commit: `74168dda7953ebd994e81dab6d22574ed24aef4c`.
- Retained ref: `refs/experimental-repairs/windows-manifest`.
- Origin: run `20260930-profile`; configured commit author Roel Vanhout.
- Failure log: `runs/20260930-profile/logs/20260930T233516067Z-build.log`.
- Affected base: `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`, Ninja/MSVC 19.51.
- Cause: Windows RC embeds scripts/winmanifest.xml and the linker generates another manifest with the same ID.
- Applicability: inspect RC input and link flags; only apply while the supplied manifest remains embedded.
- Application: `git cherry-pick -x 74168dda7953ebd994e81dab6d22574ed24aef4c`.
- Touched file: `CMakeLists.txt`; propagate /MANIFEST:NO to MSVC executable consumers of OpenSCADLibInternal.
- Verification: both executables link; inspect embedded manifest and run baseline tests.
- Passing checkpoint: `74168dda7953ebd994e81dab6d22574ed24aef4c`,
  `runs/20260930-profile/logs/20260930T233851201Z-test.json`.
  Windows SDK mt.exe extracted manifest ID 1 successfully; evidence is
  `runs/20260930-profile/baseline-repair-probes/embedded-manifest.xml`, retaining asInvoker and supported OS entries.
- Upstream submission: none.
