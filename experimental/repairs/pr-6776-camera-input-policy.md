# Unresolved integration policy: PR 6776 camera input ranges

State: behavior decision approved on 2026-10-02; integration build and standard tests passed.
Evidence: run logs/20261002T074635087Z-test.json at 0a1df09ea9d1e278606434ce254671001c468278,
plus shortcut/palette probe runs/tool-tests/shortcuts-aeccef39a7a24d818cfa2b760ffc9349.
Physical Windows theme switching remains unverified; do not claim full desktop acceptance from these checks.
The user explicitly approved adopting the PR camera limits after clarification that spinbox stepping wraps,
while arbitrary typed out-of-range numbers are not normalized by the spinbox. SCAD expressions remain separate.
Use the PR ranges/wrapping and preserve master's font-derived widget sizing. Do not ask this decision again.
Discovered in run `20261001-scadmaxx-all-features` after passing keyboard-shortcut integration.

## Frozen context

- Master: `03da906b4c437e6935ba91d8209cb153d3259a37`.
- PR 6776: `aab4aed030dd61b80c5f850177f2af93e067eb7d`.
- Last passing checkpoint: `8da46458826509d73e2a69a3c681c2b8607d87dc`.
- Private branch: `scadmaxx-20261001` in `E:/Dropbox/bare_repos/openscad.git`.
- Worktree: `D:/openscad/wt-scadmaxx-20261001`.
- Original patch: `runs/20261001-scadmaxx-all-features/pr-6776.patch` (hash/base recorded in inputs.json).
- Application: `git apply --3way --index <absolute-path-to-pr-6776.patch>`.

## Why an agent must stop

In ViewportControl::initGUI, master sets all absolute-camera double spin boxes to [-DBL_MAX,+DBL_MAX].
The PR removes those overrides. Its ViewportControl.ui sets rotations to [0,360] with wrapping, camera distance
minimum to 1, and field of view to [0,180]. Keeping the C++ overrides would silently defeat these PR restrictions;
dropping them changes the accepted inputs from master. The user required stopping before choosing feature behavior.
This was a behavior gate, now settled by the decision above. This is not a compiler failure or an exhausted
repair budget. No focused repair was attempted for this conflict.

## Other conflicts to resolve after the policy is settled

- Animate.cc: retain the current animateParameters widget name; review existing validators before adding PR copies.
- MainWindow.cc/.h: PR replaces transient/delayed progress widgets with a persistent resettable widget.
  Review setupStatusBar, updateStatusBar, showProgress, all progress pointers and cancellation paths together.
  Preserve master's saveWindowState and GeometryWorker migration; do not restore obsolete CGALWorker.
- OpenSCADApp.cc: font-setting conflict overlaps the new upstream stylesheet removal. Preserve native theme updates.
- ViewportControl.cc: retain font-derived control sizing independently of whichever numeric-range policy is chosen.

Do not resolve these files wholesale with ours/theirs. The staged, apparently clean parts also change related APIs.
Checkpoint copies, combined diff, staged diff and unmerged index records are in the run's checkpoint-pr-6776/.
Historical conflict files/index records remain in the checkpoint directory. The conflicts were resolved in
`0a1df09ea` by adopting PR status-bar/progress ownership, retaining master saveWindowState and GeometryWorker,
using QApplication::setFont, adding explicit validator includes, retaining animateParameters's current name,
and preserving font-derived control sizing while removing C++ range overrides. Build and standard tests passed
at `0a1df09ea9d1e278606434ce254671001c468278`, `logs/20261002T074635087Z-test.json` in the frozen run.
The combined shortcut/palette probe also passed; physical OS theme switching remains unverified.

## Replay and validation

Resume this frozen run, do not fetch newer sources. Verify HEAD matches the passing checkpoint and inspect any
intervening edits before resolving. After approval, resolve the complete PR consistently, commit its integration
with source attribution, reconfigure/build/test, and exercise progress/cancel, camera inputs and palette transitions.
Record the chosen policy here, with exact changes and new verified commit, so future agents need not decide again.
Keep the two-focused-attempt limit per failure. No selected feature may be dropped to obtain a passing build.

PR 6878's earlier conflict was comment-only: remove its obsolete 'make sure it looks nice' comment in
restoreWindowState, retaining master's surrounding statements. That resolution passed the full build, unit/runtime
tests and a separate shortcut-widget probe; detailed evidence is in the run report.
