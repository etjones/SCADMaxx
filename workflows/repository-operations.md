# Separate repository maintenance, integration and publication

Decision clarified on 2026-10-09: maintain branches and build integrations as separate operations.
Branch maintenance is not an automatic first phase of every build. Dropbox storage and GitHub
publication are separate operations too. Route requests by this table; do not infer additional work.

| Request | Operation | Does not automatically authorize |
| --- | --- | --- |
| Update upstream/master and maintained feature branches | Fetch upstream, advance straight local `master`, merge updates through the maintained feature dependency graph, and record revisions/conflicts | Building, pushing to Dropbox, publishing to GitHub |
| Make a new integrated build | Freeze the selected recorded inputs, integrate changes, validate and package | Refreshing upstream master, maintaining feature bases, pushing or publishing |
| Push to the local bare repository | Push the explicitly requested repository/branches/refs to Dropbox and verify them | Updating upstream, building or publishing to GitHub |
| Publish to GitHub | Push the explicitly approved source/control branches and tags to their GitHub destinations | Updating upstream, building or pushing to Dropbox |

A request explicitly combining operations, such as "update everything and build", authorizes maintenance
followed by integration/build as two recorded operations. It still does not authorize either kind of push.
Fetching a declared ref to obtain a selected input is different from adopting a newer upstream baseline
or merging that baseline into feature owners. Preserve explicit revision pins and readiness rules.

## Maintain upstream and feature branches

1. Inspect branch/worktree status and the dependency manifest. Preserve dirty work and inventory local-only
   commits. Use the shared `openscad-master` repository; never use an integration as a feature's base.
2. Fetch upstream OpenSCAD and freeze the chosen upstream SHA. Fast-forward straight local `master` only
   when its checkout is suitable and its history permits it. Do not resolve divergence by resetting or
   adding feature/integration code to `master`; preserve the checkpoint and report the issue.
3. Merge the baseline into independent maintained feature owners. Update dependent owners in dependency
   order through normal forward merges, so upstream changes and prerequisite fixes flow together.
   Follow [feature ancestry](../docs/feature-ancestry.md); never cherry-pick, squash-copy or merge the
   combined integration back into `master` or a feature owner. Do not update unrelated experiments.
4. Resolve conflicts within existing feature behavior; stop for an actual behavior choice. Record exact
   owner heads and prerequisite pins in `DEPENDENCIES.json`, `SOURCES.json` and the selected stack where
   applicable. Keep acceptance, validation and remote promotion distinct. Source merges alone do not
   make a revision validated or promoted. Run tests/builds only when separately authorized.
5. Leave results local unless a push is explicitly requested. Retain evidence for a later build to identify
   intended committed inputs and any remaining readiness or promotion blockers.

Maintaining selected upstream PR variants also respects their declared dependencies and pinned revisions;
fetching a new author head does not silently replace a selected revision. Maintenance does not create
an integration or release ZIP.

## Integrate and build

Follow [the build entry point](update-and-build-scadmaxx.md). For routine builds, use
[re-integration](reintegrate-scadmaxx.md): retain the previous upstream SHA unless a different recorded
baseline is explicitly selected, and merge only changed selected inputs and their required closure.
A full new composition changes how the stack is assembled; it does not by itself request upstream
maintenance. Use the chosen recorded baseline and freeze all source identities before merging.

If consumer dependency pins are incompatible, report required owner maintenance as a prerequisite;
do not silently expand a build into an upstream-update operation. A request to integrate a named feature
fix includes its necessary forward dependency merges, as documented in the re-integration workflow.
The declared bare/GitHub source and local-only input authorization rules remain in force: a build does
not make newer working-clone commits available in the bare repository automatically.

Tooling limitation: `New-ExperimentalRun.ps1` currently fetches upstream master when preparing a full
composition and has no locked-baseline parameter. Do not use it to refresh the baseline for a build-only
request. Re-integration retains its existing baseline; for a full composition with a fixed baseline,
prepare the recorded composition using normal Git operations and the existing build tools. An explicitly
requested fresh-upstream composition can use the helper. This documentation does not change the script.

## Store locally and publish

There are two histories, described in [Git layout](../docs/git-layout.md): controls in `scadmaxx`, and
application source in `openscad-master` with linked worktrees. The source clone's `origin` is Dropbox,
`upstream` is official OpenSCAD, and `publish` is the user's GitHub OpenSCAD fork. The controls repository
has its own Dropbox `origin`. Remote names identify destinations, not extra branch ancestry.

Commit locally first. An explicit push copies requested commits/refs to the named destination; Dropbox
and GitHub do not synchronize automatically. Neither a local commit nor a completed build proves that
either remote contains it. Verify each requested destination separately.

The intended public layout keeps SCADMaxx's recipes/documentation in the user's SCADMaxx GitHub repository,
and straight master, approved feature branches and integrated source revisions in the OpenSCAD fork.
Publishing controls alone does not publish application source. Publishing an integrated source branch
also publishes its reachable feature history, even without separate feature branch refs.

Before enabling public rebuilding, configure the controls' GitHub destination, define approved source
branches/tags, retain exact delivery revisions, provide public source mappings and usable dependency/build
instructions, and verify required submodule revisions are accessible. Keep local Dropbox mappings available
for local runs; identify the public selection separately rather than silently changing local authority.
Use explicit refspecs, not an all-ref mirror of private experiments, recovery refs and temporary checks.
This documented layout is not permission to configure remotes or push. Publication and ZIP upload remain
explicitly requested actions; this rule installs no synchronization or publication automation.
