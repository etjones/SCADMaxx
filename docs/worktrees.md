# Checkout inventory

Observed locally on 2026-09-30. Recheck Git status and worktree ownership before every use; this is not live state.
Remotes updated on 2026-10-01: `openscad-master` uses local `origin = E:/Dropbox/bare_repos/scadmaxx.git`,
`upstream = https://github.com/openscad/openscad.git` (push disabled), and explicit
`publish = https://github.com/roel-v/openscad.git`. All source branches push locally by default.
The workspace root has its own origin at `E:/Dropbox/bare_repos/scadmaxx-workspace.git`.

All nine source checkouts below were updated to include upstream master
`612e684c2cbbcdcb9a7a8307973f33fd910f9c17` on 2026-09-30. Existing local edits were restored, submodule revisions
were synchronized, and nothing was pushed. See the [update report](../runs/20260930-worktree-update/report.md)
for resulting commits, conflict resolutions, recovery refs, and verification limits.

| Directory | Observed role / branch | Existing changes |
| --- | --- | --- |
| `openscad-master` | Main checkout, `master`, updated HEAD `612e684c2cbbcdcb9a7a8307973f33fd910f9c17` | Clean; matched upstream master at final verification |
| `wt-openscad-fix-windows-unicode` | `fix/windows-unicode-filenames`, base `31b1430530c295c4b24662b2d5a4b989bbbabc7d` | Focused Unicode CLI filename repair based on the existing experimental composition; shared vcpkg; evidence in `runs/20261001-unicode-filename-fix/` |
| `wt-openscad-ui-visual-polish` | `codex/ui-visual-polish`, HEAD `67101788f`, base `464e25dad0c01af5488375c15aa6734190531eb5` | Foundation including #6776 and Windows repairs, then four icon-system phase commits; source/submodules clean; private-origin head verified; results in `.plans/2_in-progress/2026-10-01_ui-icon-system/5_post-implementation-notes.md`; Customizer/dialog features remain planning; all UI parts stay sequential in this branch |
| `wt-openscad-navigation-cube` | `feature/navigation-cube`, head `c54886b822ed39ff91369c335472788f106e2c50` | Six phases committed; private origin verified; runnable local dev build. [Evidence](../.plans/3_done/2026-10-01_navigation-cube/5_post-implementation-notes.md). Preserve checkout and build. |
| `wt-openscad-experimental-20260930-profile` | `experimental/20260930-profile`, HEAD `31b1430530c295c4b24662b2d5a4b989bbbabc7d` | Four baseline repair commits, then #6878 and #6776; shared-dependency rebuild/package passed; current evidence and limits in `runs/20261001-shared-rebuild/` |
| `wt-openscad-annotations` | `feature/annotations`, created from upstream master `612e684c2cbbcdcb9a7a8307973f33fd910f9c17` on 2026-09-30 | Dedicated annotations checkout; push remote `origin`; not pushed |
| `wt-openscad-pr-6642-dynamic-parameter-changes` | `codex/pr6642` | Modified ParameterObject.cc and surface_node_test.cc |
| `wt-openscad-pr-6776-dynamic-dark-mode-switching` | `codex/pr-6776-dynamic-dark-mode-switching` | Modified GroupWidget.cc/.h |
| `wt-openscad-pr-6871-msvc-build-and-compilation-fixes` | `codex/pr6871-msvc` | Modified core/utility files and dirty Clipper2 submodule; several build directories |
| `wt-openscad-pr-6871-msvc-build-baseline` | Detached updated baseline at `7887eb609dc03b8b4dca69cc86a264d30ac7673d` | Dirty Clipper2 submodule retained; original baseline has a recovery ref |
| `wt-openscad-pr-6999-customizer-header-text-contrast` | `codex/fix-customizer-header-contrast` | Modified GroupWidget.cc/.h |
| `wt-openscad-issue-5425-path-after-2024-10-28` | `codex/issue-5425-canonical-path` | Untracked reproduction script and SCAD fixtures |
| `openscad-6991` | Separate checkout with upstream as `origin`, user fork as `fork` | Modified GroupWidget.cc/.h; existing local plan |

The existing Customizer investigation is at
`openscad-6991/.plans/2_in-progress/2026-09-02_customizer-theme-behavior/1_exploration.md`.
Read it when advancing the Customizer work. Preserve its local-only planning scope and distinguish its historical
repository references from current state. Do not merge its changes with the similar worktree without comparison.

The `OpenSCAD-*` directories and `PythonSCAD` contain installed/extracted applications, not registered worktrees of
`openscad-master`. Dependency and application directories are not available scratch space.

For new worktrees, follow the [standard clone and worktree workflow](../README.md#standard-clone-and-worktree-workflow).
Use `openscad-master` as the shared repository and create the separate checkout alongside it under `D:/openscad`.
Inspect existing worktrees first and reuse only an available, suitable checkout. Record the actual path here.
Preserve existing independent clones and worktrees; do not rename or migrate them merely to match this convention.

- Navigation/annotations verification: `wt-openscad-navigation-annotations-check`, branch
  `codex/navigation-annotations-check`, merge `d16b00019` (navigation `c54886b82`, annotations `d670fad09`).
  Native annotation tests pass. Separate verification checkout, not a selected distribution. Preserve it.
