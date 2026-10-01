# Repair: settings-stream-declarations

- State: reusable; baseline build and tests passed in run `20260930-profile`.
- Failure: MSVC C2678 in Settings.h:367 while compiling InitConfigurator.cc.
- Applies after: baseline; no feature prerequisite.
- Source repository: `D:/openscad/openscad-master`.
- Commit: `c577f934adade4b762fba095abbad79a3b13df30`.
- Retained ref: `refs/experimental-repairs/settings-stream-declarations`.
- Origin: run `20260930-profile`; commit author Roel Vanhout (configured local identity).
- Failure log: `runs/20260930-profile/logs/20260930T231836693Z-build.log`.
- Affected base: `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`, MSVC 19.51.36257.0.
- Cause: LocalAppParameter stream operators are defined in Settings.cc but absent from Settings.h.
  Translation units instantiating SettingsEntryList cannot find the extraction overload.
- Applicability: check the header still lacks these declarations and reproduce the template-instantiation failure.
- Application: `git cherry-pick -x c577f934adade4b762fba095abbad79a3b13df30`.
- Touched file: `src/core/Settings.h`; declares both existing operators before the template.
- Verification: compile InitConfigurator.cc and the complete GUI target, then run baseline tests.
  Passing checkpoint `74168dda7953ebd994e81dab6d22574ed24aef4c`,
  `runs/20260930-profile/logs/20260930T233851201Z-test.json` (unit tests and installed STL/PNG checks).
- Upstream submission: none.
