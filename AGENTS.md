# OpenSCAD workspace

This repository contains SCADMaxx build recipes, tools, prompts and plans; it is not a source checkout.
Control-relative paths below start at `D:/openscad/scadmaxx`. Source worktrees, runs and artifacts live in
the parent container `D:/openscad`. See `docs/layout-migration.md` when resuming older records.

- Whenever you ask the user a question, stop and end your turn. Resume only after an explicit answer.
  Do not use a timeout, choose a default, or interpret silence as permission.
- `README.md` is hand-maintained by the user. Do not regenerate or update it unless the user explicitly requests an edit.
- Do not add or retain backward-compatibility code, aliases, shims, fallbacks or migrations unless the user explicitly
  authorizes that compatibility. When replacing behavior, remove its obsolete paths and update the affected consumers.
- For README screenshots, follow `docs/readme-screenshots.md`; replacement captures are deferred until the integrated build works.
- Read `docs/workspace.md` for the workspace layout and `docs/worktrees.md` before selecting a checkout.
- Create new OpenSCAD worktrees from the sibling `openscad-master` clone; follow `docs/workspace.md`.
- For annotations, read `workflows/annotations.md` and its linked feature exploration.
- For SCADMaxx update/build requests, including "update everything and build a new SCADMaxx", start with
  `workflows/update-and-build-scadmaxx.md`, then `workflows/experimental-builds.md` and `experimental/PR_STACK.md`.
  Only the enabled entries in that manually maintained list belong in a build.
- Keep commits local unless the user explicitly requests a push for the relevant repository/branch or refs.
  Commit requests, feature completion and update/build requests do not authorize pushes. Promotion into the
  future-build input repository is a separate explicit user decision; see `workflows/update-and-build-scadmaxx.md`.
- At feature completion, record the local handoff described in `workflows/update-and-build-scadmaxx.md`.
- For testing or advancing a PR, read `workflows/pr-development.md`.
- Keep workspace plans, run records, and artifacts outside upstream-facing source changes.
- Inspect branch, worktree status, submodules, and checkout-local instructions before source edits.
  Preserve existing changes and worktrees; never repurpose an occupied checkout for a build run.
- Follow the shared `plans-workflow` skill for `.plans` and `git-workflow` skill for commits.
- A request to arrange this workspace does not start a build, publish artifacts, or schedule recurring runs.
