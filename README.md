# SCADMaxx

*OpenSCAD, with the sliders turned up.*

This is the private, local SCADMaxx development workspace. The source experiments, integration branches and
workspace control history stay local. Publish an individual feature to GitHub only when the user explicitly
chooses to make it public. The two bare origins live in `E:/Dropbox/bare_repos`; see the
[local Git layout](docs/git-layout.md) for the installed repositories and publication workflow.

This workspace supports three kinds of work:

| Work | Instructions | Durable input |
| --- | --- | --- |
| Native OpenSCAD annotations, based on the Blender feature | [Annotations](workflows/annotations.md) | [Implementation and verification](.plans/3_done/2026-09-30_openscad-annotations/5_post-implementation-notes.md) |
| Native viewport navigation cube | Dedicated `wt-openscad-navigation-cube`, branch `feature/navigation-cube`, head `c54886b82` | [Completed implementation and local build](.plans/3_done/2026-10-01_navigation-cube/5_post-implementation-notes.md) |
| UI visual polish (foundation and icons implemented) | Dedicated `wt-openscad-ui-visual-polish`, branch `codex/ui-visual-polish` | [Evidence and remaining Customizer/dialog work](.plans/1_planning/2026-10-01_ui-visual-polish/1_exploration.md) |
| Experimental Windows builds of current upstream master plus selected PRs | [Build workflow](workflows/experimental-builds.md) | [Manually maintained PR stack](experimental/PR_STACK.md) |
| Testing and improving an individual upstream PR or issue | [PR development](workflows/pr-development.md) | The relevant checkout and feature plan |

## Layout

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
- `wt-openscad-*/`: separate working directories for feature, PR, issue, and experimental-build branches.
- Other existing source checkouts, such as `openscad-6991/`: retained in place with their existing work.
- Existing `OpenSCAD-*` and `PythonSCAD` directories: installed/extracted builds; retained in place.
- `vcpkg`, `deptools`, and `test-vcpkg*`: existing dependency tooling and experiments.

Use a UTC run ID such as `20260930T120000Z`; add a suffix if necessary to make it unique.
Use a separate `experimental/<run-id>` source branch for every fresh composition. Annotations should have their
own `feature/annotations` branch, and each PR investigation should retain its own branch and checkout.
The annotations branch is now prepared in `wt-openscad-annotations`, based on freshly fetched upstream master
at `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`. The six implementation phases and full Windows Release build are complete;
changes remain uncommitted in that checkout. The local runnable build and ZIP are under
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
   (`E:/Dropbox/bare_repos/scadmaxx.git`) for local pushes. GitHub is the explicit `publish` remote, used only when
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

Windows builds reuse the existing shared vcpkg packages at
`D:/openscad/openscad-6991/build/vcpkg_installed` with the toolchain in `D:/vcpkg`.
Separate worktrees/application build directories do not require separate dependency installations.
See the [shared dependency policy](experimental/profiles/windows-x64.md): automatic package installation and
private dependency builds are disabled.

Example requests:

- "Develop the OpenSCAD annotations feature using its exploration."
- "Run the Windows experimental build from the enabled entries in experimental/PR_STACK.md."
- "Test and fix PR #6642 in its existing worktree."

The stack selects PR #6878 (customizable keyboard shortcuts), PR #6776 (dynamic dark-mode switching), navigation
cube, UI visual polish and annotations. The three local features are pending usable committed revisions in the
Dropbox source origin; run preparation stops until they are ready. An HTTP endpoint / agent server is planned
without a branch yet. Other existing PR worktrees remain candidates for manual selection; see the selection list.
The [build tools](experimental/scripts/README.md) implement the recorded build steps; the agent still reviews
integrations and diagnoses repairs. The first local run completed automated build, test, staging and extracted-ZIP
checks on 2026-10-01. It includes #6878 and #6776, preceded by four separately committed Windows baseline repairs.

The current delivery fixes Unicode filenames in that composition using the focused UTF-8 manifest change from
upstream PRs #6726/#6357, with a new regression test. It reuses the shared dependency installation, with Catch2 and
Boost.Nowide previously added at the user's request. The obsolete private build directories were removed (28.97 GiB of files);
historical logs and original ZIPs remain available.

- [Windows ZIP](artifacts/20261001-unicode-filename-fix/attempt-1/OpenSCAD-experimental-20261001-unicode-filename-fix-windows-x64.zip)
- [Matching source ZIP](artifacts/20261001-unicode-filename-fix/attempt-1/OpenSCAD-experimental-20261001-unicode-filename-fix-source.zip)
- [Run report and verification limits](runs/20261001-unicode-filename-fix/report.md)

Extract the complete Windows ZIP and run `staging/openscad.exe`. SHA-256 files sit alongside both archives.
Build, 119 unit-test cases, standard rendering checks and fresh-ZIP extraction checks passed. The Unicode filename
crash is fixed on Windows 10 1903+: seven filename cases pass through both launchers, including in the extracted ZIP.
Existing UTF-8 AST, echo and CSG tests also pass. Shared dependencies were unchanged by this repair.
Windows desktop theme switching, full-process shortcut persistence and clean-machine portability remain unverified;
the [experimental-build feature](.plans/2_in-progress/2026-09-30_experimental-windows-builds/1_exploration.md)
retains those acceptance checks. No successful-release tag, external publication or recurring job was created.

The workspace root is a separate Git control repository on `main`, with local origin
`E:/Dropbox/bare_repos/scadmaxx-workspace.git` and an allowlist excluding source checkouts and generated artifacts.
The initial private workspace history was established as part of the 2026-10-01 Dropbox setup. The scope and per-attempt
snapshot procedure are defined in [versioning and release rules](experimental/versioning-and-releases.md).
