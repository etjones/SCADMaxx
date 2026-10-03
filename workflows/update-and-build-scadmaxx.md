# Update everything and build a new SCADMaxx

This is the entry point for a fresh chat receiving that request, or equivalent wording. No previous chat history
is needed. It requests a new Windows composition from current selected sources, including integration/repair
commits, tests and local ZIP delivery. It does not request pushes to Dropbox origins or GitHub publication,
dependency upgrades, or rebasing all feature worktrees. A documentation-only request does not start a build.

Read `docs/workspace.md`, `docs/git-layout.md`, `docs/worktrees.md`, `experimental/PR_STACK.md`,
`experimental/SOURCES.json`, and `workflows/experimental-builds.md`. Follow the linked integration, repair,
Windows profile and release contracts. Only the enabled selection is authoritative; do not infer features from
worktree names, public branches, open PRs or remembered conversations.

Follow the human-maintained [Luna-first model workflow](../docs/workspace.md#model-workflow-luna-first-astra-to-unblock).
At a genuine blocker, retain the run state and concise handoff in the run report. A user-controlled Astra pass
addresses that blocker, then Luna resumes the same frozen run. Switching models does not change inputs or checks.

## Which repository supplies what

| Input or output | Authority | Update operation |
| --- | --- | --- |
| Workspace instructions and selection | `D:/openscad/scadmaxx`; origin `E:/Dropbox/bare_repos/scadmaxx.git` | Fetch control `origin`; reconcile as described below |
| OpenSCAD baseline | `https://github.com/openscad/openscad.git`, `refs/heads/master` | Fetch once into a new run-specific ref |
| Enabled upstream PR | That row's PR URL, resolved as `refs/pull/<number>/head` | Fetch the actual PR head from OpenSCAD GitHub |
| Private feature | Exact `repository` and `ref` in `SOURCES.json`; currently the Dropbox source bare repo | Fetch the already-promoted source into a run-specific ref; do not push newer local commits |
| Published feature or PR variant | Exact GitHub repository/ref explicitly selected in `SOURCES.json` | Fetch that declared source, regardless of the local branch's tracking configuration |
| Repairs | `experimental/REPAIRS.md` and linked records | Obtain the retained commits, check applicability, apply separately |
| Integration history | Fresh `scadmaxx-YYYYMMDD` branch in `wt-scadmaxx-YYYYMMDD` | Retain locally; push specified refs to the private origin only on explicit user request |
| ZIPs, matching source, logs | `artifacts/<run-id>/` and `runs/<run-id>/` | Retain outside source/control Git; no external publication by default |

The source clone's `origin` is Dropbox, `upstream` is OpenSCAD GitHub, and `publish` is the user's GitHub fork.
The workspace checkout has a different `origin`, containing only workspace controls. Always use an explicit
working directory and repository/ref; do not treat these two origins as interchangeable.

## Push authorization and promotion

Keep intermediate and completed commits local by default. A commit request, accepted feature, readiness check,
or "update everything and build" request does not authorize a push. This applies to source, workspace controls,
integration branches, repair/run refs and tags, including private Dropbox destinations.

Pushing a feature branch to its declared build-input repository promotes that revision for future integrated
builds. Require an explicit user request to push/promote the relevant repository/branch or refs. Authorization
for one promotion does not authorize later commits or other branches. Promotion does not itself enable a new
entry in the manually selected PR stack. Record local completion separately from promoted build readiness.

When explicitly authorized, review the outgoing range, use the named remote and exact refspec, push without
force, and verify the remote object ID. Do not add automatic pushes to hooks, scripts or completion workflows.

## 1. Reconcile the workspace controls

Inspect workspace status, staged changes and ongoing tasks before fetching its local origin. Fetching is safe for
working files. Fast-forward `main` to `origin/main` only when the checkout is clean, not actively edited, and the
update is a fast-forward. Re-read the instructions after an update.

If local controls are ahead or edited and the remote has no unseen commits, preserve and use the current controls,
recording their commit plus exact dirty-file snapshots. Do not sweep concurrent plan changes into a commit.
If origin has unseen changes that conflict with local work, or histories diverge, report the unresolved control
revision and stop before preparing a run. Do not silently use stale controls, discard edits, or force an update.
Git control commits are separate from the source integration/repair commits authorized by a build request.

## 2. Check readiness of promoted feature inputs

Run `New-ExperimentalRun.ps1 -ValidateOnly` to inspect all selected entries without fetching/building. For each
selected local feature, find its source checkout in `docs/worktrees.md` and inspect its branch, committed HEAD,
dirty state, submodule revisions and `SOURCES.json` readiness. The four current local sources are navigation cube,
UI visual polish, annotations, and HTTP agent server. Their exact refs live in the registry, not this runbook.

If a selected feature is `ready: false`, stop preparation and report the reason. Do not change the flag merely to
make a build run, integrate its initial empty branch, omit it, or commit unfinished source changes for another task.

For each ready feature whose declared repository is the Dropbox source origin, fetch that declared branch into
an inspection ref and compare it with the matching local feature branch. Use full SHAs and ancestry checks:

| State | Action |
| --- | --- |
| Local and bare heads match | Lock the declared bare ref in the new run |
| Local branch contains newer committed feature work | Report the unpromoted local head and preserve it. Lock the already-promoted bare revision if it still satisfies the selected build; if the task requires the newer revision, obtain explicit promotion authorization before proceeding |
| Bare branch is ahead | Build from the newer declared bare ref; do not reset or merge into an occupied feature checkout |
| Local branch or checkout is absent | Use the declared ready source if available; a build need not have every development checkout |
| Histories diverge, source ref is missing, or newer commits have unclear readiness | Stop and report the affected feature; no force-push or fallback source |
| Working files/index/submodules are dirty | Preserve and report excluded edits; only eligible committed source can enter the build |

An update/build request reads promoted private feature inputs; it does not promote newer local commits.
If the requested revision is not available in the declared repository, report the exact branch/commit awaiting
promotion. Do not silently substitute the local checkout, change the declared source, or push to make it available.
After an explicitly authorized push, re-read the declared ref before freezing it; never force a conflicting update.

Do not pull upstream master into all feature branches before composing. The integration branch starts from fresh
upstream and resolves compatibility there. Updating a feature's own base is separate feature-maintenance work.
An explicitly pinned `Revision` remains pinned even during an "update everything" request; never replace it with latest.

## 3. Fetch and freeze the selected composition

Choose a new run ID and follow the [integration naming rule](../docs/git-layout.md#integration-branch-and-worktree-names).
Invoke `experimental/scripts/New-ExperimentalRun.ps1` from the control repository. Its defaults locate controls
in `D:/openscad/scadmaxx` and source/run directories in `D:/openscad`. It fetches master and each selected
repository/ref, locks full head/base SHAs, retains refs under `refs/experimental-runs/<run-id>/`, saves binary-capable
patches and original commit identities, and creates the isolated integration worktree. It does not perform the
control reconciliation and promoted-input checks above; the agent must complete and record those first.

Record the source synchronization decisions in the run report. Freeze `PR_STACK.md`, `SOURCES.json`, applicable
repair records, profile, scripts and instructions with hashes. Do not refetch or change selections halfway through
a run. If inputs must change, preserve the failed/abandoned attempt and start a new run ID.

Review dependencies and overlapping changes before integration. In particular, the UI branch currently includes
the dark-mode PR as its foundation. Record an explicit base/dependency or reviewed residual UI-only patch so
#6776 is not applied twice. A selected change already upstream gets evidence and an `already-present` result.

## 4. Integrate, build, test and deliver

Follow `workflows/experimental-builds.md` and `experimental/scripts/README.md`: preserve baseline evidence,
integrate each entry in order, commit its conflict resolutions, make separate repair commits, and verify each
checkpoint. The agent resolves implementation conflicts; the scripts do not automatically merge the stack.
Report genuinely ambiguous behavior conflicts instead of silently dropping functionality.

Use the existing shared vcpkg installation and recorded Windows profile. Do not install/upgrade dependencies or
create a private dependency tree. Apply the required Unicode filename repair when applicable and run its tests.
Every selected feature needs behavior evidence; compilation alone is insufficient.

Package the combined GUI executable with its DLLs/resources, matching source including submodules, build info,
notices and checksums. Do not create or bundle release notes. Test a fresh extraction with a controlled PATH. Record any missing desktop
or clean-machine checks honestly. Current scripts use `OpenSCAD-experimental-<run-id>` artifact identities; the
SCADMaxx product name does not imply that binary/ZIP branding has already been changed.

Retain the integration branch and run/repair refs locally, with run/control snapshots and matching source archives.
Push only the refs explicitly requested by the user, following the authorization rule above. A release tag also
requires its validation before an authorized push. Ordinary branch pushes do not retain custom refs. Keep unrelated
staged edits out of control commits; committing controls does not authorize pushing the workspace origin.

## Feature completion and later GitHub publication

Each feature-development task must leave a reproducible local handoff: source state (committed when requested),
matching submodule revisions, tests/evidence, exact source head and intended delta boundary, and reviewed dependencies.
Feature acceptance and local commits do not require or authorize a push. Report any completed but unpromoted revision.

After the user explicitly requests promotion, verify the push to the declared repository and update build readiness
for that promoted revision. Set `ready: true` only when it is available and validated. For a new source awaiting
promotion, retain `ready: false` with a concrete reason. If an older promoted revision remains usable, keep its
readiness evidence tied to that revision; do not mark newer local work promoted merely because the feature is done.

When the user chooses to maintain a feature publicly, publish only its reviewed feature history and deliberately
update that entry's `repository`/`ref` to the GitHub source. It can instead remain sourced from Dropbox while a
public copy exists. The registry decides; the presence of a GitHub branch never changes the source automatically.
Do not enable both copies or publish the private combined history.

## Replaying an earlier build

"Build a new SCADMaxx" resolves current selected sources. "Rebuild run <id>" uses that run's frozen inputs and
recorded final source; do not run fresh preparation or reinterpret `latest` against today's branches.

Use retained run refs/commits or the matching source archive, exact submodule contents, control snapshots,
toolchain/profile and dependency records. Replay the recorded integrations/repair commits and resolutions, or
build the already-integrated final commit. An archive includes `experimental-build-material/REBUILD.txt` for the
direct CMake path. Keep old outputs; create a new delivery attempt or linked replay run rather than overwrite them.
If dependencies, tools or source objects are missing, report the gap instead of substituting current versions.

This preserves the exact source and recorded build recipe. It does not claim byte-identical ZIPs or binaries:
timestamps and toolchain/environment details can affect bytes. The scripts handle preparation/build/package
steps; agent review, source synchronization, conflicts and feature verification remain explicit workflow steps.
