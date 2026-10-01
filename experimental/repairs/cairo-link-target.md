# Repair: cairo-link-target

- State: reusable; baseline build, tests and Cairo PDF export passed.
- Failure: LINK LNK1181 cannot open cairo.lib despite an installed vcpkg Cairo package.
- Applies after: baseline; independent of selected features.
- Source repository: `D:/openscad/openscad-master`.
- Commit: `b5ef9f6cedaab8bb5087f82bc223dcbe18328c14`.
- Retained ref: `refs/experimental-repairs/cairo-link-target`.
- Origin: run `20260930-profile`; configured commit author Roel Vanhout.
- Failure log: `runs/20260930-profile/logs/20260930T233354928Z-build.log`.
- Affected base: `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`, MSVC 19.51, Cairo 1.18.4 via vcpkg.
- Cause: CAIRO_LIBRARIES contains only cairo; the MSVC CMake branch drops CAIRO_LIBRARY_DIRS.
- Applicability: check both MSVC Cairo detection branches still link bare pkg-config library names.
- Application: `git cherry-pick -x b5ef9f6cedaab8bb5087f82bc223dcbe18328c14`.
- Touched file: `CMakeLists.txt`; request IMPORTED_TARGET and use PkgConfig::CAIRO in both MSVC branches.
- Verification: GUI and unit-test executables must link; run baseline tests and a Cairo PDF export.
- Passing checkpoint: `74168dda7953ebd994e81dab6d22574ed24aef4c`,
  `runs/20260930-profile/logs/20260930T233851201Z-test.json`;
  PDF export evidence in `runs/20260930-profile/baseline-repair-probes/` (22,373-byte PDF, exit zero).
- Upstream submission: none.
