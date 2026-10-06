# SCADMaxx workspace guide

For feature dependencies and forward-only maintenance, read [maintained feature ancestry](feature-ancestry.md).
The 2026-10-06 local migration supersedes historical snapshot/delta instructions below.

*OpenSCAD, with the sliders turned up.*

Latest local delivery: [scadmaxx-2026100-windows-x64.zip](../../artifacts/scadmaxx-all-features/20261005T195510539Z/scadmaxx-2026100-windows-x64.zip).
Extract the complete ZIP and launch `scadmaxx.exe`; `scadmaxx.com` provides console invocation.
Both names are CMake outputs, with no `openscad.exe`/`openscad.com` aliases. This delivery includes all
22 native entries frozen for the 2026-10-05 integration run, plus the selected skill companion.
Final source is `dcd732fefa0aef5b12d4e5d0a2097223caf32726`. Unit, native/DPI, rendering,
experimental/Minkowski, extracted Unicode and library/catalog checks passed. Matching source and
skill archives sit beside the Windows ZIP. See the
[run report](../../runs/20261005-scadmaxx-all-features/report.md) for checksums, frozen inputs and limits:
live Windows theme switching and clean-machine portability remain unverified. Feature branches,
integration history and controls are retained in the Dropbox bare repositories under the user's
explicit 2026-10-05 push authorization. No GitHub publication was made.

The control repository is `D:/openscad/scadmaxx`; the container is `D:/openscad`. The source experiments, integration branches and
workspace control history stay local. Publish an individual feature to GitHub only when the user explicitly
chooses to make it public. The two bare origins live in `E:/Dropbox/bare_repos`; see the
[local Git layout](../docs/git-layout.md) for the installed repositories and publication workflow.

This workspace supports three kinds of work:

| Work | Instructions | Durable input |
| --- | --- | --- |
| HTTP endpoint / agent server | Dedicated `wt-openscad-http-agent-server`, branch `codex/http-agent-server` | [Completed implementation and verification](../.plans/3_done/2026-10-01_http-agent-server/5_post-implementation-notes.md) |
| Native OpenSCAD annotations, based on the Blender feature | [Annotations](../workflows/annotations.md) | [Implementation and verification](../.plans/3_done/2026-09-30_openscad-annotations/5_post-implementation-notes.md) |
| Native viewport navigation cube | Dedicated `wt-openscad-navigation-cube`, branch `feature/navigation-cube`, head `c54886b82` | [Completed implementation and local build](../.plans/3_done/2026-10-01_navigation-cube/5_post-implementation-notes.md) |
| UI visual polish (all four features implemented) | Dedicated `wt-openscad-ui-visual-polish`, branch `codex/ui-visual-polish` | [Final audit and verified private handoff](../.plans/3_done/2026-10-01_ui-preferences-dialog-polish/5_post-implementation-notes.md) |
| Experimental Windows builds of current upstream master plus selected PRs | [Build workflow](../workflows/experimental-builds.md) | [Manually maintained PR stack](../experimental/PR_STACK.md) |
| Testing and improving an individual upstream PR or issue | [PR development](../workflows/pr-development.md) | The relevant checkout and feature plan |

## Layout

Control files below live in `D:/openscad/scadmaxx`. Source checkouts, `runs`, `artifacts`, installed applications
and dependency directories live alongside it in `D:/openscad`. See [the Git layout](git-layout.md).

- `AGENTS.md`: short entry point for agents working anywhere under this directory.
- `workflows/`: instructions for the three activities.
- `experimental/PR_STACK.md`: the authoritative, ordered selection of PRs, PR variants, and local features.
- `experimental/integration-inputs.md`: source selection, locked change boundaries, and overlap handling.
- `experimental/REPAIRS.md`: reusable repair catalog, backed by individual records when repairs are discovered.
- `experimental/profiles/windows-x64.md`: Windows profile with a tested build/packaging recipe and explicit GUI limits.
- `experimental/scripts/`: executable run preparation, build, test, deployment, and packaging tools.
- `experimental/versioning-and-releases.md`: control-repository scope, input snapshots, and release identities.
- `experimental/templates/`: build-run and repair evidence templates.
- `.plans/`: feature planning, using planning, in-progress, and done lanes as needed.
- `docs/worktrees.md`: discovered checkouts, their roles, and important existing work.
- `runs/<run-id>/`: evidence from future experimental runs; created when a run starts.
- `artifacts/<run-id>/`: staged Windows distribution, ZIP, and checksums; created during packaging.
- `openscad-master/`: shared OpenSCAD clone and main `master` checkout; create new worktrees from this repository.
- `wt-openscad-*/`: existing feature, PR, issue, and historical integration worktrees.
- `wt-scadmaxx-YYYYMMDD/`: new SCADMaxx integration worktrees; see the naming rule below.
- Other existing source checkouts, such as `openscad-6991/`: retained in place with their existing work.
- Existing `OpenSCAD-*` and `PythonSCAD` directories: installed/extracted builds; retained in place.
- `vcpkg`, `deptools`, and `test-vcpkg*`: existing dependency tooling and experiments.

Use a UTC run ID such as `20260930T120000Z`; add a suffix if necessary to make it unique.
Use a separate `scadmaxx-YYYYMMDD` source branch and `wt-scadmaxx-YYYYMMDD` worktree for every fresh composition,
following the [integration naming rule](../docs/git-layout.md#integration-branch-and-worktree-names).
Annotations should have their
own `feature/annotations` branch, and each PR investigation should retain its own branch and checkout.
The annotations branch is now prepared in `wt-openscad-annotations`, based on freshly fetched upstream master
at `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`. The six implementation phases and full Windows Release build are complete;
six commits end at `d670fad09`, verified in the private origin and marked ready for integration. The build and ZIP are under
`artifacts/openscad-annotations-palette-fixed-win64` and `artifacts/openscad-annotations-palette-fixed-win64.zip`.
See the linked verification notes for test evidence, build commands and limitations.

## Standard clone and worktree workflow

Use the existing `D:/openscad/openscad-master` clone as the shared repository for new OpenSCAD worktrees.
Keep its main checkout on `master` as the baseline, and do feature development, PR testing, and experimental
compositions in separate worktrees alongside it under `D:/openscad`. Each worktree has its own checked-out branch
and working files while sharing the clone's Git history and remotes. A new task normally needs a branch and
worktree, not another clone or GitHub fork.

1. Inspect `git -C D:/openscad/openscad-master worktree list` and the relevant checkout's status. Reuse a suitable
   available worktree when possible; preserve occupied worktrees and local changes.
2. Fetch the required upstream refs through `openscad-master`. For a new feature, use freshly fetched
   `upstream/master`; for an existing PR or resumed task, use its explicitly selected branch or commit.
3. Create the worktree from `openscad-master`, with a dedicated branch and a descriptive `wt-openscad-...` folder.
   Record the actual base SHA. Fetching updates remote-tracking refs; it does not move the main checkout's `master`.
4. Initialize its submodules and verify that the new checkout is clean. Keep the branch local and use `origin`
   (`E:/Dropbox/bare_repos/openscad.git`) only for explicitly user-requested pushes/promotions. Neither a commit
   nor a build request authorizes a push. GitHub is the explicit `publish` remote, used only when
   the user chooses to publish an individual feature. Creating a worktree does not push a branch or create a PR.
5. Record the worktree in `docs/worktrees.md` and link it from the relevant plan.

Example for a new feature (replace `example` with its name; run commands one at a time and stop on failure):

```powershell
git -C D:/openscad/openscad-master fetch upstream master
git -C D:/openscad/openscad-master worktree add --no-track -b feature/example D:/openscad/wt-openscad-example upstream/master
git -C D:/openscad/wt-openscad-example config branch.feature/example.pushRemote origin
git -C D:/openscad/wt-openscad-example submodule update --init --recursive
git -C D:/openscad/wt-openscad-example status --short
```

The annotations worktree follows this arrangement: `wt-openscad-annotations` belongs to the `openscad-master`
repository and checks out `feature/annotations`.

## Starting work

In a fresh chat, **"update everything and build a new SCADMaxx"** means follow the
[update-and-build runbook](../workflows/update-and-build-scadmaxx.md). It defines each source of truth, how ready local
feature commits reach the Dropbox origin, how GitHub PRs/features are fetched, and how inputs are frozen for replay.
Feature completion uses the same runbook's handoff so future builds can find committed, ready revisions.

Windows builds reuse the existing shared vcpkg packages at
`D:/openscad/openscad-6991/build/vcpkg_installed` with the toolchain in `D:/vcpkg`.
Separate worktrees/application build directories do not require separate dependency installations.
See the [shared dependency policy](../experimental/profiles/windows-x64.md): automatic package installation and
private dependency builds are disabled.

### Model workflow: Luna first, Astra to unblock

1. Start with **GPT-6 Luna / Medium thinking**, including for the first combined build. Follow the documented
   workflow and complete all authorized work that can progress. Attempt focused fixes and respect readiness and
   verification checks; do not escalate simply because the run is long or a stronger model is available.
2. When genuinely blocked, preserve the current run and write a concise handoff in its report: run ID, worktree,
   branch and HEAD, last passing checkpoint, failing command and relevant log, fixes already tried, the unresolved
   issue, and the next useful action. Complete independent work where possible, then report the blocker to the user.
3. The user switches to **GPT-6 Astra for a minimal, focused unblocking pass**. Astra should address the recorded
   blocker, verify the fix, and record any repair and the exact resume point. "Minimal" describes the scope of the
   intervention; it does not prescribe a reasoning-effort setting.
4. Switch back to **Luna / Medium** to finish integration, tests and packaging. Repeat this cycle if another blocker
   appears. Resume the same frozen run rather than refetching inputs, restarting successful steps, or rebuilding
   dependencies. Start a new run only when the documented input-change rules require it.

Model switches are user-controlled. This workflow does not automatically spawn extra agents or change models.

Suggested starting request:

> Update everything and build a new SCADMaxx. Follow the documented Luna-first workflow. Do everything you can
> until blocked, then preserve the checkpoint and leave a concise handoff for a focused Astra pass.

### Other example requests

- "Develop the OpenSCAD annotations feature using its exploration."
- "Run the Windows experimental build from the enabled entries in experimental/PR_STACK.md."
- "Test and fix PR #6642 in its existing worktree."

The stack selects PR #6878 (customizable keyboard shortcuts), PR #6776 (dynamic dark-mode switching), navigation
cube, UI visual polish, annotations and the HTTP endpoint / agent server. Current feature readiness, validated
heads and handoffs are recorded in `experimental/SOURCES.json`; run preparation stops for any pending entry.
Other existing PR worktrees remain candidates for manual selection; see the selection list.
The [build tools](../experimental/scripts/README.md) implement the recorded build steps; the agent still reviews
integrations and diagnoses repairs. The first local run completed automated build, test, staging and extracted-ZIP
checks on 2026-10-01. It includes #6878 and #6776, preceded by four separately committed Windows baseline repairs.

The earlier 2026-10-01 delivery fixed Unicode filenames in that composition using the focused UTF-8 manifest change from
upstream PRs #6726/#6357, with a new regression test. It reuses the shared dependency installation, with Catch2 and
Boost.Nowide previously added at the user's request. The obsolete private build directories were removed (28.97 GiB of files);
historical logs and original ZIPs remain available.

- [Windows ZIP](../../artifacts/20261001-scadmaxx-all-features/attempt-5/scadmaxx-2026100-windows-x64.zip)
- [Matching source ZIP](../../artifacts/20261001-scadmaxx-all-features/attempt-5/OpenSCAD-experimental-20261001-scadmaxx-all-features-source.zip)
- [Run report and verification limits](../../runs/20261001-scadmaxx-all-features/report.md)

Extract the complete Windows ZIP and run `openscad.exe` directly in the extraction directory. The ZIP has no
wrapper folder. SHA-256 files sit alongside both archives. This build includes all six selected features;
141 unit-test cases, 13 annotation/HTTP and 15 navigation native checks passed, along with standard rendering
and fresh-ZIP extraction checks. Seven Unicode filename cases pass through both launchers in the extracted ZIP.
Shared dependencies were unchanged. Attempt 5 also enables experimental features and Manifold
Minkowski. Standard unit/render checks, six focused experimental/Minkowski regressions and
Unicode filename checks through both extracted launchers passed. Navigation tuning remains enabled:
open **Window > Navigation tuning** for session-only adjustments. Native navigation/tuning and
annotation/HTTP results above are from preceding validation of the same source revision,
before enabling experimental features and Manifold Minkowski. The ZIP retains its flat layout
and contains no release notes. See the [compile-time feature audit](../experimental/scripts/README.md).
Windows desktop theme switching, full-process shortcut persistence and clean-machine portability remain unverified;
the [experimental-build feature](../.plans/2_in-progress/2026-09-30_experimental-windows-builds/1_exploration.md)
retains those acceptance checks. No successful-release tag, external publication or recurring job was created.

The `scadmaxx` directory is a separate Git control repository on `main`, with local origin
`E:/Dropbox/bare_repos/scadmaxx.git` and an allowlist excluding source checkouts and generated artifacts.
The initial private workspace history was established as part of the 2026-10-01 Dropbox setup. The scope and per-attempt
snapshot procedure are defined in [versioning and release rules](../experimental/versioning-and-releases.md).

The 11 → 07 → 08 → 12 implementation queue is locally complete with verified handoffs for all four features. Feature 07's
[completion notes](../.plans/3_done/2026-10-03_07_semantic-model-hierarchy/5_post-implementation-notes.md) lock its
uncommitted delta, minimal source closure, extracted runtime and real clipping/Vim composition. Feature 08's
[completion notes](../.plans/3_done/2026-10-03_08_anchors-attachments/5_post-implementation-notes.md) retain its source,
native/package/DPI and actual clipping/Vim acceptance. Feature 12's
[completion notes](../.plans/3_done/2026-10-03_12_contextual-insertion/5_post-implementation-notes.md) record its
interactive candidate preview, guarded source Commit and all six accepted phases in `wt-openscad-contextual-insertion`.
Its [run report](../../runs/20261004-contextual-insertion/report.md) links replayable source captures, the extracted
development package, 295 unit cases, 155 native rows and 184 actual clipping/Vim composition rows, plus 150%/200% DPI
and all eight catalog entries through both launchers. These local uncommitted feature results leave the selected
stack and latest delivered distribution unchanged.
