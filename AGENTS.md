# OpenSCAD workspace

This directory coordinates OpenSCAD development; it is not an OpenSCAD source checkout.

- Whenever you ask the user a question, stop and end your turn. Resume only after an explicit answer.
  Do not use a timeout, choose a default, or interpret silence as permission.
- Read `README.md` for the workspace layout and `docs/worktrees.md` before selecting a checkout.
- Create new OpenSCAD worktrees from the existing `openscad-master` clone; follow README.md's standard workflow.
- For annotations, read `workflows/annotations.md` and its linked feature exploration.
- For experimental builds, read `workflows/experimental-builds.md` and `experimental/PR_STACK.md`.
  Only the enabled entries in that manually maintained list belong in a build.
- For testing or advancing a PR, read `workflows/pr-development.md`.
- Keep workspace plans, run records, and artifacts outside upstream-facing source changes.
- Inspect branch, worktree status, submodules, and checkout-local instructions before source edits.
  Preserve existing changes and worktrees; never repurpose an occupied checkout for a build run.
- Follow the shared `plans-workflow` skill for `.plans` and `git-workflow` skill for commits.
- A request to arrange this workspace does not start a build, publish artifacts, or schedule recurring runs.
