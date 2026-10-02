# Test and advance an upstream PR

1. Identify the requested PR/issue and read `../docs/worktrees.md`. Inspect its existing checkout, branch, diff,
   submodule state, instructions, and relevant plan before changing anything. Check the PR's current upstream
   state when starting actual PR work; names and old run records are not current evidence.
2. Reuse the existing checkout when it is the intended work and is not owned by another active process/task.
   Preserve local modifications. Compare overlapping Customizer work before moving changes between checkouts.
   When a new checkout is needed, create a worktree from `openscad-master` following the workspace guide's standard workflow,
   using the selected PR branch or commit as its base.
3. Reproduce the reported behavior and record the base/head revision, toolchain, commands, and observations.
   Keep feature-specific evidence and plans outside the patch sent upstream.
4. Implement a focused change and verify both the intended behavior and relevant regression coverage.
   Use the shared git-workflow skill for scoped commits. Keep environment/build repairs distinct from behavior
   changes when they are independent so maintainers can review them separately.
5. Prepare a reviewable diff and concise PR description or follow-up evidence. Preserve original PR author
   attribution. Do not force-push another person's branch or publish comments/messages without authorization.
6. Report the actual change, validation, remaining blockers, and recommended next step. If creating a PR is
   authorized, attach the resulting PR to the current Codex chat.

Testing a PR does not select it for the experimental build. To include it, the user maintains
`experimental/PR_STACK.md`; do not harvest uncommitted work from a PR checkout into a composition run.
When the user selects our improved version, name its committed repository/ref explicitly as a `pr-variant` using
the [input contract](../experimental/integration-inputs.md). Replacing the source is an explicit selection change;
the upstream PR head remains the default for a `pr` entry. Preserve reusable narrow integration fixes through the
[repair catalog](../experimental/REPAIRS.md) with their original commits and verification evidence.
