# Customizer group visibility in the integrated Qt harness

The 2026-10-05 composition includes the PR 6642 variant at
`1dad283e17be06380f2ff6b23daca68719d1f70c`, including hiding empty groups and restoring
their disclosure state. The standalone GroupWidget test target is insufficient after
UI polish adds its UIUtils dependency.

Keep the production behavior unchanged. The integration repair `986459145` ports the
selected branch's assertions into `src/gui/Typography_test.cc`, which is already linked
with the integrated Qt dependencies. It checks hidden parents, restoring collapsed and
expanded groups, disabled but visible controls, and repeated hide/restore cycles.
Replay that commit after PR 6642 and UI polish if the test is absent; do not add another
duplicate test. The normal Build-Windows Test step runs it with the unit suite.

Evidence: `runs/20261005-scadmaxx-all-features`, source-editing checkpoint and subsequent
unit checkpoints. This is a test-harness adaptation, not a production behavior repair.
