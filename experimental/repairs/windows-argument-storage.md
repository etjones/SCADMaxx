# Repair: windows-argument-storage

- State: reusable; baseline build and tests passed in run `20260930-profile`.
- Failure: MSVC C2131 at main_wrapper.cc:34 and :35; argc is not a constant expression.
- Applies after: baseline; independent of feature PRs and the settings repair.
- Source repository: `D:/openscad/openscad-master`.
- Commit: `e1a798257aeaabb0f82898e477ef8f5e6fd3558d`.
- Retained ref: `refs/experimental-repairs/windows-argument-storage`.
- Origin: run `20260930-profile`; commit author Roel Vanhout (configured local identity).
- Failure log: `runs/20260930-profile/logs/20260930T232915084Z-build.log`.
- Affected base: `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`, MSVC 19.51.36257.0.
- Applicability: wmain still uses variable-length arrays of char pointers and std::string.
- Application: `git cherry-pick -x e1a798257aeaabb0f82898e477ef8f5e6fd3558d`.
- Touched file: `src/main_wrapper.cc`; use pre-sized vectors and pass argv8.data().
- Semantics: preserves UTF-8 conversion, string storage lifetime, argument order and null terminator.
  Does not change the CRT entry point.
- Verification: compile the wrapper and GUI executable, then run baseline unit and CLI smoke tests.
- Passing checkpoint: `74168dda7953ebd994e81dab6d22574ed24aef4c`,
  `runs/20260930-profile/logs/20260930T233851201Z-test.json`.
- Upstream submission: none.
