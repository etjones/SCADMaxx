# SCADMaxx local Git layout

Product name: **SCADMaxx**. Tagline: **OpenSCAD, with the sliders turned up.**

Decision recorded on 2026-10-01: SCADMaxx experiments, composed builds, and the workspace root/control history
remain private and local. Individual features may be published later by explicit user choice. A usable feature
can be shared as a branch/patch before becoming an upstream PR. Readiness alone does not authorize publication.

Status: installed on 2026-10-01. The existing source clone and worktrees remain intact. Both origins are private
bare repositories in the user's existing Dropbox repository folder. GitHub is retained only as the explicit
source `publish` remote. No GitHub push was made. Migration evidence is in `runs/20261001-dropbox-git-setup/`.

## Two histories, both with local bare origins

| Bare repository | Working checkout | Contents |
| --- | --- | --- |
| `E:/Dropbox/bare_repos/scadmaxx-workspace.git` | `D:/openscad` | README, agent instructions, PR selection, build scripts, plans and documentation |
| `E:/Dropbox/bare_repos/scadmaxx.git` | Existing `D:/openscad/openscad-master` and its linked worktrees | OpenSCAD history, private feature branches, repairs, composed build branches and tags |

The workspace repository is the project root and build recipe. The source repository holds the application.
Keeping these histories separate lets a feature become an upstream-facing patch without taking private workspace
instructions or unrelated experiments along. Neither local bare repository needs a GitHub counterpart.

Keep existing worktrees attached to `openscad-master`; configure that clone to push to the local bare source
repository. The bare repository is the authoritative local remote, while `openscad-master` remains the working
clone that owns the worktrees. No worktree relocation or conversion is required. Bare repositories contain Git
history and refs, not checked-out source or build directories.

## Source remotes

| Remote | Destination | Use |
| --- | --- | --- |
| `origin` | `E:/Dropbox/bare_repos/scadmaxx.git` | Store private feature, repair and integration history locally |
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

`experimental/PR_STACK.md` remains the manually maintained selection; `experimental/SOURCES.json` maps feature
IDs to repositories and full refs. A feature's source can be the local bare repository or a GitHub branch.

1. Fetch OpenSCAD master and lock its SHA. Create a fresh local `experimental/<run-id>` branch from that commit.
2. Resolve the two selected upstream PR heads (#6878 and #6776), local feature heads, and any selected published
   feature heads. Lock all SHAs and intended delta bases before integrating.
3. Apply applicable Windows baseline repairs, then each selected feature/PR as its own integration commit,
   followed by separate build-fix commits and verification. Include the required Unicode filename repair unless
   upstream already supplies the behavior; retain its regression checks.
4. Package from the verified final source, retaining source, provenance and run evidence. Store integration and
   repair refs in the local bare repository. Never merge an entire previous composed build back into master.

Example of the selected annotations source (the real definition also records readiness):

```json
{
  "annotations-local": {
    "repository": "E:/Dropbox/bare_repos/scadmaxx.git",
    "ref": "refs/heads/feature/annotations"
  }
}
```

Commit and push selected local feature work to the local origin before locking a build that reads from it.
Uncommitted working-tree edits are not build inputs and are not stored by a bare remote. Publishing a feature
later can change its declared source to GitHub; do not enable both copies of the same feature.

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

After a feature commit, `git push origin` in its worktree stores that branch in Dropbox. Before integrating it,
check that the declared source ref contains the intended commit. After a build, explicitly push its integration
branch, repair/run refs and any verified release tag to local origin; an ordinary branch push does not include
custom refs. Never use an all-ref push to GitHub. Workspace control commits use the workspace's own local origin.

Keep the Dropbox bare repositories available offline, and allow syncing to complete before using them on another
machine. Avoid concurrent writes to their synced copies. Automatic Git GC is disabled on the bare repositories;
perform maintenance deliberately when no other machine is writing. Dropbox transfer completion was not verified
by the local Git checks.

Submodule repositories and uncommitted files remain in their existing checkouts and are not copied by a bare
superproject push. Preserve them separately where needed; the source bare repository records submodule commit IDs.

Git references: [bare clones](https://git-scm.com/docs/git-clone),
[worktrees](https://git-scm.com/docs/git-worktree), [explicit pushes](https://git-scm.com/docs/git-push).
