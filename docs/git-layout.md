# SCADMaxx local Git layout

Current publication status (2026-10-09): controls are mirrored to the private
`roel-v/SCADMaxx` repository; the selected feature branches and current integration are published to
the public `roel-v/openscad` fork. See [the verified publication record](github-publication.md).
The installation and migration descriptions below retain their original local-only decisions.

Product name: **SCADMaxx**. Tagline: **OpenSCAD, with the sliders turned up.**

Decision recorded on 2026-10-01: SCADMaxx experiments, composed builds, and the workspace root/control history
remain private and local. Individual features may be published later by explicit user choice. A usable feature
can be shared as a branch/patch before becoming an upstream PR. Readiness alone does not authorize publication.

Status: installed on 2026-10-01 and renamed on 2026-10-02; see [migration details](layout-migration.md).
The source clone and all worktree contents are preserved. Both origins are private
bare repositories in the user's existing Dropbox repository folder. GitHub is retained only as the explicit
source `publish` remote. No GitHub push was made. Migration evidence is in `runs/20261001-dropbox-git-setup/`.

## Two histories, both with local bare origins

| Bare repository | Working checkout | Contents |
| --- | --- | --- |
| `E:/Dropbox/bare_repos/scadmaxx.git` | `D:/openscad/scadmaxx` | README, agent instructions, PR selection, build scripts, plans and documentation |
| `E:/Dropbox/bare_repos/openscad.git` | Existing `D:/openscad/openscad-master` and its linked worktrees | OpenSCAD history, private feature branches, repairs, composed build branches and tags |

`D:/openscad` is a plain container. Its `scadmaxx` repository holds build recipes, tools, prompts and documentation.
The sibling `openscad-master` contains the shared source repository and its clean upstream checkout.
Keeping these histories separate lets a feature become an upstream-facing patch without taking private workspace
instructions or unrelated experiments along. Neither local bare repository needs a GitHub counterpart.

Keep existing worktrees attached to `openscad-master`; configure that clone to push to the local bare source
repository. The bare repository is the authoritative local remote, while `openscad-master` remains the working
clone that owns the worktrees. All `wt-*` source checkouts, including SCADMaxx integrations, share that repository.
Bare repositories contain Git
history and refs, not checked-out source or build directories.

## Source remotes

| Remote | Destination | Use |
| --- | --- | --- |
| `origin` | `E:/Dropbox/bare_repos/openscad.git` | Store private feature, repair and integration history locally |
| `upstream` | `https://github.com/openscad/openscad.git` | Fetch master and explicitly selected PR heads; no pushes |
| `publish` | `https://github.com/roel-v/openscad.git` | Fetch published features; push only explicitly approved feature branches |

`remote.pushDefault=origin` and `push.default=current` are set. All existing source branches have
`branch.*.pushRemote=origin`; non-master branches fetch/pull their matching local-origin branch. Master still
tracks `upstream/master` for fetching/pulling, while pushing to local origin. Upstream's push URL is disabled.
If changing remotes later, audit per-branch overrides so private branches never default to `publish`.
Use explicit remote/refspec pushes for publication. Never mirror the private repository to GitHub or push all
branches/tags there. Keep `push.followTags` disabled for publication unless specific tags are deliberately selected.
The workspace checkout has only its local origin.

## Build composition

Keep branch maintenance, integration/building, pushing to Dropbox and publishing to GitHub separate.
The canonical [repository operations](../workflows/repository-operations.md) defines their scope and the
intended public two-repository layout. A build alone does not advance straight master or feature bases.

For the full fresh-chat procedure, source synchronization decisions and replay semantics, follow
[Update everything and build a new SCADMaxx](../workflows/update-and-build-scadmaxx.md).

`experimental/PR_STACK.md` remains the manually maintained selection; `experimental/SOURCES.json` maps feature
IDs to repositories and full refs. A feature's source can be the local bare repository or a GitHub branch.

1. Lock the chosen upstream baseline SHA; refresh it only when explicitly requested. Reuse the maintained
   integration for routine builds, or create a fresh local `scadmaxx-YYYYMMDD` branch for a full new composition.
2. Resolve the selected upstream PR heads, local feature heads, and any selected published
   feature heads. Lock all source and accepted dependency SHAs before integrating with normal merges; see
   [maintained feature ancestry](feature-ancestry.md).
3. Apply applicable Windows baseline repairs, then each selected feature/PR as its own integration commit,
   followed by separate build-fix commits and verification. Include the required Unicode filename repair unless
   upstream already supplies the behavior; retain its regression checks.
4. Package from the verified final source, retaining source, provenance and run evidence. Push integration and
   repair refs to the local bare repository only when explicitly requested. Never merge a composed build back into master.

Example of the selected annotations source (the real definition also records readiness):

```json
{
  "annotations-local": {
    "repository": "E:/Dropbox/bare_repos/openscad.git",
    "ref": "refs/heads/feature/annotations"
  }
}
```

Only an explicit user push/promotion request advances selected local feature work in the declared origin.
Commit and build requests do not authorize that step. Lock the already-promoted revision for a build;
if newer local work is required, report the revision awaiting promotion rather than pushing automatically.
Uncommitted working-tree edits are not build inputs and are not stored by a bare remote. Publishing a feature
later can change its declared source to GitHub; do not enable both copies of the same feature.

## Integration branch and worktree names

For new SCADMaxx compositions, name the branch `scadmaxx-YYYYMMDD` and its directory
`D:/openscad/wt-scadmaxx-YYYYMMDD`. Use the date the branch/worktree is created in the workspace's local timezone
(Europe/Amsterdam), not the upstream commit date or the eventual build completion date.
For example, a composition created on 2026-10-01 uses branch `scadmaxx-20261001` and worktree
`wt-scadmaxx-20261001`. Do not add `experimental/`, `openscad`, or descriptive feature suffixes to these names.

If another fresh composition is created on the same date, use the first available matching numeric suffix,
starting at `scadmaxx-YYYYMMDD-2` and `wt-scadmaxx-YYYYMMDD-2`. Check both existing refs and directories;
never overwrite or repurpose an existing composition. Resuming a run retains its original names and creation date.
Record the exact branch, worktree path, and unique run ID together in the run evidence. Run IDs, retained input
refs, artifact names, and release tags keep their existing conventions; they need not match the branch name.

The two existing integration worktrees were migrated with user authorization on 2026-10-02.
Feature and PR worktrees retain `wt-openscad-*` names. Integration branches push to
`E:/Dropbox/bare_repos/openscad.git`. Historical run snapshots retain their original names; use the
[migration mapping](layout-migration.md) when resuming them.

The preparation script implements the creation-date naming rule and checks directory, local-branch and known
origin-branch collisions. A new branch name is separate from the unique evidence/run ID.

## Publishing one feature later

Develop each feature against upstream master or an explicitly declared feature dependency. Before publication,
review every outgoing commit and its ancestry. Pushing one branch also publishes its reachable history; a branch
based on a composed SCADMaxx build can therefore expose other experiments. Prepare a clean feature-only branch
from upstream and transfer only the intended changes when necessary.

After the user chooses publication, push only that branch, for example:

```powershell
git -C D:/openscad/openscad-master push publish refs/heads/feature/annotations:refs/heads/feature/annotations
```

This command is illustrative, not authorized for execution now. A public feature branch can later support an
upstream PR; publication does not require publishing SCADMaxx's combined branch or workspace control repository.

## Retention and routine use

The migration preserved all 166 inventoried source refs with their original object IDs, including the detached
baseline's recovery ref. Seven stash reflog commits also have named recovery refs in the bare repository.
Git's receive operation rejects `refs/stash`, so that ref was fetched and installed locally in the bare repository.
The original stash and worktree files were left intact. Config snapshots and verification are in the migration record.

Feature and control commits remain local by default. Follow the
[push authorization and promotion rule](../workflows/update-and-build-scadmaxx.md#push-authorization-and-promotion):
push only on an explicit user request for the relevant repository/branch or refs. A feature push to the build-input
origin promotes its revision for future integration. Before integrating, check that the declared source ref contains
the intended promoted commit. Build completion does not authorize pushing integration branches, repair/run refs or
release tags. An ordinary branch push does not include custom refs. Never use an all-ref push to GitHub.

Keep the Dropbox bare repositories available offline, and allow syncing to complete before using them on another
machine. Avoid concurrent writes to their synced copies. Automatic Git GC is disabled on the bare repositories;
perform maintenance deliberately when no other machine is writing. Dropbox transfer completion was not verified
by the local Git checks.

Submodule repositories and uncommitted files remain in their existing checkouts and are not copied by a bare
superproject push. Preserve them separately where needed; the source bare repository records submodule commit IDs.

Git references: [bare clones](https://git-scm.com/docs/git-clone),
[worktrees](https://git-scm.com/docs/git-worktree), [explicit pushes](https://git-scm.com/docs/git-push).
