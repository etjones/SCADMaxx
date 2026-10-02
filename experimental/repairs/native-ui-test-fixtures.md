# Repair: native fixtures with UI layout changes

- State: reusable; first repair passed both native suites and standard tests.
- Applies after: UI visual polish, navigation and annotations/HTTP.
- Source commit: `bcf48145d9ebc7ffdcde0414ddde38ceb62f0b6a`.
- Failures at `6486d7660`: F6 capture rejected as `Viewport resized`, animation-frame comparison
  found different dimensions after a compile-banner relayout, and Save Copy automation timed out
  controlling a Windows-native picker. See run `20261001-scadmaxx-all-features`,
  `native-annotations-20261002T111921395` and `native-navigation-20261002T112016810`.
- Repair: wait for a bounded quiet period in viewport geometry before F6 capture; pin and restore
  viewport constraints within the exact-pixel comparison fixture; select Qt file dialogs only in
  an explicit GUI-test invocation with `ENABLE_GUI_TESTS`. Ordinary production dialogs and capture
  invalidation safeguards remain unchanged.
- Replay: inspect whether the same fixture assumptions remain, then cherry-pick the commit with `-x`.
  Build with native tests enabled and run both suites with isolated `OPENSCAD_TEST_SETTINGS_DIR`.
  Use the run's `feature-tests.ps1` and `native-feature-tests.ps1` as concrete command references.
- Attempt limit: this is attempt 1 for these failures. Preserve its evidence and stop if they persist
  after two focused repair attempts; do not disable assertions or bypass capture rejection.
- Passing evidence in the same run: `native-annotations-20261002T112433070` (13/13, 23 live client
  commands), `native-navigation-20261002T112454036` (15/15), and
  `logs/20261002T092400948Z-test.json`. No native tests were skipped.
- Retained ref: `refs/experimental-repairs/native-ui-test-fixtures` in the private source origin.
