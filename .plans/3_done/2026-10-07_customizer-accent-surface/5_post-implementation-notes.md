# Implementation and local handoff

## Validated and promoted — 2026-10-07

This supersedes the pending validation/promotion state recorded below.
Commit `d52e03649893fffb487976c36e4e0e028176b701` is verified at the private source repository
`E:/Dropbox/bare_repos/openscad.git`, `refs/heads/codex/ui-visual-polish`.
The UI stack pin, source registry and accepted-head record now select this commit.
The current feature has no uncommitted source edits; canonical build-title/icon patches and generated
Clipper2 metadata remain local and excluded from the feature commit. Workspace controls remain local.

Application build and 77,593 ordinary assertions passed. The extended native fixture passed 320 checks
across light/dark and simulated 100%/200% DPI, including distinct hover/press fills and live theme switching.
The first dark capture exposed a fixture timing issue: the initial preview had temporarily disabled the
Customizer. Waiting for the enabled state fixed the fixture; no production change was needed.
High-contrast system switching and physical mixed-monitor DPI remain unverified.
No new integrated delivery was built. Exact commands, logs, captures and remaining limits:
[validation report](D:/openscad/runs/20261007-customizer-accent/report.md).

## Initial implementation record

Implemented on 2026-10-07 in `D:/openscad/wt-openscad-ui-visual-polish`, branch `codex/ui-visual-polish`.
Source baseline: `6096a42d2ee5e8c8530b8b5776c9ca04a1a9afd2`. Changes remain uncommitted in
`src/gui/parameter/GroupWidget.h` and `.cc`; no integration, promotion or build-readiness changes.
Accepted dependency: #6776, `aab4aed030dd61b80c5f850177f2af93e067eb7d`.

`GroupDisclosureButton` initializes a fresh native style option each paint, blends Window/Accent and
sets only its Button role. Press takes precedence over hover. Native complex-control drawing retains
the border, arrow, text and focus. Existing non-checkable disclosure behavior and accessibility remain.
Disabled/high-contrast states use native drawing; contrast-preference changes trigger a repaint.
The implementation uses QPalette::Accent and QAccessibilityHints directly, targeting current Qt 6.11.1;
the latter requires Qt 6.10. Older Qt builds are not supported by this new code; no compatibility path was added.

Drawing guidance and primary Qt links are recorded beside the painter and in `docs/ui-conventions.md`.
Reviewed the source diff and whitespace. No builds or tests run, as required by workspace instructions.
Runtime validation of the source implementation remains pending; the approved prototype is separate evidence.

Submodules matched recorded gitlinks on inspection:

- MCAD: `1ea402208c3127ffb443931e9bb1681c191dacca`
- Clipper2: `c7f820f6a03fa91f189b866d27bf40dfe47abaa6`
- OpenCSG: `9bf122715213dca05e70993dd8672fe3aa36c518`
- manifold: `0edd9d54876f3135e431575214dd6d8a72866fee`
- mimalloc: `30b2d9d89099bee08e9f67a1ffb3e12e7ba45227`
- sanitizers-cmake: `bcb1fc68616e9645ca5acea2992412606373ab04`

Future integration must consume the owner branch with normal ancestry after commit/validation/promotion
are requested. The registry's existing promoted revision and its evidence remain unchanged.
