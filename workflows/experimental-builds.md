# Experimental Windows build workflow

Use this workflow only when a build run is requested. First follow
[the fresh-chat update/build runbook](update-and-build-scadmaxx.md) for control and source synchronization.
Read `../experimental/PR_STACK.md` as the authoritative input.
Use the shared git-workflow skill for commits. Use the [executable tools](../experimental/scripts/README.md) for
preparation and build steps. Integration review and repairs remain agent-operated; record actual commands and
results. Tool availability alone does not imply that the full Windows distribution profile is verified.

Read the [input and integration contract](../experimental/integration-inputs.md),
[repair catalog](../experimental/REPAIRS.md), [Windows profile](../experimental/profiles/windows-x64.md), and
[versioning and release rules](../experimental/versioning-and-releases.md) before running the steps below.
"Entry" includes upstream PRs, explicitly selected PR variants, and our own committed features.

## Prepare and lock

1. Inspect existing worktrees, processes, remotes, branch status, and submodules. Preserve user work.
   Check selected feature readiness in `SOURCES.json` first. If any selected source is marked `ready: false`,
   stop preparation and report its pending reason; do not omit it or commit another task's unfinished work.
2. Create `runs/<run-id>/` and copy `experimental/templates/run-report.md` as its report. Save an exact copy of
   `experimental/PR_STACK.md` there. Snapshot consumed control files, profile/scripts, and repair records with hashes
   and their control-repository identity. Resolve the enabled order and dependencies; reject ambiguous or duplicate rows.
   With no enabled rows, report that selection is needed unless the user requested a baseline-only build.
3. Verify the upstream remote URL, fetch `master`, and record its SHA. Resolve `pr` entries from upstream PR head
   refs (`refs/pull/<number>/head`), not GitHub's synthetic merge refs. Resolve `feature` and `pr-variant` entries
   from their explicitly declared repository/ref. Record source identity, PR URL where applicable, base branch,
   head SHA, source commits, and status. Lock each delta base according to the input contract; preserve the intended
   source diff. Validate pinned revisions and available submodule commits. Do not rely on stale local names or
   implicitly include dirty worktree contents. Compare a PR variant with its original PR and record the differences.
4. Freeze those inputs for this run, retaining fetched refs under a run-specific namespace so later fetches or
   force-pushes do not change the recorded source. Check merged/closed PRs and overlapping/dependent changes,
   including selected variants and partially integrated upstream changes. Document any reviewed residual patch.
   If an entry cannot be applied as selected, record the reason and stop rather than silently omitting it.
   An entry proven to be contained in the locked upstream base is recorded as already present and needs no replay.
5. Create an isolated worktree from the shared `openscad-master` clone, following the workspace guide's standard workflow,
   with a `scadmaxx-YYYYMMDD` branch and `wt-scadmaxx-YYYYMMDD` directory at the locked upstream master SHA.
   Follow the [creation-date and collision naming rule](../docs/git-layout.md#integration-branch-and-worktree-names).
   Record the
   worktree path and branch. Do not reset, clean, rebase, or repurpose existing PR-development worktrees.
6. Record the Windows toolchain and dependency revisions: Visual Studio/MSVC, Windows SDK, CMake, generator,
   architecture, Qt, QScintilla, vcpkg toolchain revision/triplet, shared installed path/status hash, submodules,
   feature flags, and environment setup. Follow the Windows profile's shared dependency policy: use the existing
   installation with manifest mode/install disabled; report missing packages instead of rebuilding dependencies.
   Read the locked checkout's build instructions and inspect relevant existing build evidence before selecting
   a profile. Use the Windows profile's executable-tooling contract and cache rules. Store exact configure, build,
   test, install/deploy, and packaging commands in the run directory. Until the first profile is verified, treat
   establishing it as explicit run work; never infer packaging readiness from an old successful executable build.

## Baseline, then one entry at a time

Build the unmodified upstream baseline first in its own build directory and preserve its result. If it needs a
source repair to build on Windows, make a dedicated baseline-repair commit and record the failure and verification.
If the baseline is known to require a selected build-support PR, keep the failed baseline evidence, apply that PR
first according to the maintained order, and require a passing build before applying unrelated feature PRs.
Do not silently reorder the stack to get past a failure.

For each enabled entry:

1. Save the current integration HEAD, entry ID, source head, delta base, and reviewed patch identity in the report.
2. Apply the reviewed delta using the input contract and create one squash integration commit, for example
   `Integrate openscad PR #6642: dynamic parameter changes`. Include the PR URL, source head, and original source
   commit identities/author attribution in the commit body or referenced run record. Use `Integrate feature <id>`
   for a local feature and identify the selected variant for an improved PR. This gives each run a linear,
   reviewable composition history without claiming the changes were authored by the integration agent.
3. If application conflicts, record affected files and the resolution. Conflict resolution needed to create a
   valid integration belongs in that integration commit; document it explicitly. Preserve a source diff for review.
   Do not hide unrelated repairs in it. If the intended resolution is unclear, stop for the user's answer.
4. Configure/build using the recorded Windows GUI Release profile. Capture command lines, exit codes, and logs.
5. Diagnose failures against the last checkpoint and evaluate applicable cataloged repairs. Record whether each
   considered repair is needed, already present, obsolete, or not applicable. Apply needed repairs individually,
   preserving attribution and recording adaptations. Make new narrowly scoped source fixes in separate commits, such as
   `Repair Windows build after PR #6642: ...`. Describe the cause and failed command, then verify with a new build.
   Record dependency/environment repairs separately when they do not change source; do not create empty commits.
6. Run relevant tests, a focused check of this entry's behavior, and checks of earlier behaviors affected by shared
   files or conflict resolution. Record the resulting passing checkpoint SHA before
   continuing. If blocked, preserve the branch and evidence and mark the run failed or blocked.

Do not disable tests or remove selected functionality merely to turn the build green. Catalog reusable repairs
with retained source commits and failure/verification evidence. On a later fresh run, re-evaluate whether each is
still needed and apply it as its own repair commit; never copy an old run's complete source tree.

The intended history is: locked upstream master, optional baseline repair, PR A integration, PR A repairs,
feature B integration, feature B repairs, and so on. A repair-free entry has only its integration commit.

## Package and verify

After the complete stack passes, prepare the experimental version identity and any separate packaging-metadata
commit required by the release rules. Build/package from the final committed source with clean recorded submodules.
Use a fresh final build/staging directory, or a verified cache configuration that cannot mix incompatible inputs.
Verify both command-line rendering of a small SCAD fixture and GUI startup/preview/render on Windows.
Exercise the selected behaviors, including the focused checks in the selection list; record actual outcomes and
any limits to verification.

Stage a portable application under `artifacts/<run-id>/staging/`, using the checkout's packaging support where
applicable. Include required runtime libraries, Qt plugins, resources, fonts, examples, licenses/notices, and other
redistribution requirements from OpenSCAD and its dependencies. A successful executable build alone is insufficient.
Do not claim portability if testing depends on developer-only PATH entries or installed build tools.

Create `OpenSCAD-experimental-<run-id>-windows-x64.zip` from the contents of the staging directory.
Put `openscad.exe`, DLLs and resource folders directly at the ZIP root, without a `staging/` or other wrapper folder.
After extraction, launch `openscad.exe` directly in the extraction directory. Extract into a separate test directory and repeat the
smoke checks with a controlled runtime PATH. Prefer a clean Windows test environment for a distribution release.
Record the exact environment and limitations if only the development machine was available.
Verify the run identifier in the application's About/version information. Do not create or bundle release notes. Include a build-info
file identifying upstream, ordered source heads and delta bases, integration/repair commits, final source SHA,
control snapshot, and toolchain. Follow the release rules to create the retained source tag after validation.
Provide corresponding source and build/repair material needed by the distribution's licenses; retain a source
archive or stable accessible source reference that actually matches the binary, including relevant submodules.
Generate SHA-256 checksums for final downloadable artifacts and record sizes and local paths in the run report.

## Distribution and future runs

Local ZIP delivery is the initial destination. External hosting remains unconfigured; a draft GitHub release on
the user's fork is a possible future destination, not a currently selected one. Prepare and validate the concrete
artifacts before requesting any missing publication destination or approval. Follow existing authorization if the
user has already supplied it. Verify uploaded assets and record their URLs before claiming publication.

Do not overwrite earlier run artifacts or rewrite their branch histories. Resume an interrupted run using its
locked inputs and checkpoints; a request for latest upstream starts a new run. A scheduler can invoke this workflow
later when requested. Do not mark the run successful until the final stack, tests, ZIP, and extraction checks pass;
track publication separately from local build success.

Before resuming, verify the branch HEAD, submodules, frozen inputs, profile, and checkpoint evidence still agree.
Do not overwrite intervening edits or resume from a presumed last successful step. Preserve all delivered runs,
matching source, and evidence until an explicit retention policy exists.

Retain completed source work in local `origin` (`E:/Dropbox/bare_repos/openscad.git`): explicitly push the run's
integration branch, repair/run refs, and any verified release tag. Ordinary branch pushes do not include custom
refs. Workspace control commits belong in the separate workspace origin. GitHub publication is a separate user
decision; use the [local Git layout](../docs/git-layout.md).
