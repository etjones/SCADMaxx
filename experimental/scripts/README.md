# Windows experimental build tools

Run with PowerShell 7.2 or newer. These scripts never push, publish, tag a release, or modify the enabled selection.
The first real Windows run passed automated build, staging and extracted-ZIP checks; see the profile and run report
for the remaining Windows desktop and clean-machine verification limits.

## Prepare a fresh run

```powershell
pwsh -NoProfile -File experimental/scripts/New-ExperimentalRun.ps1
```

This reads the enabled table, locks master/source/base commits, retains refs and patches, and creates an isolated
worktree. It does not apply patches blindly. Resume an existing run from its `inputs.json`; do not prepare it again.
Preparation failures retain their inputs and logs. Check the actual refs/worktree before manually resuming.
Use `-ValidateOnly` to inspect the selection and source definitions without fetching or creating a run/worktree.

Selected unfinished features use `ready: false` plus `pendingReason` in `SOURCES.json`. Validation reports them;
actual preparation stops before fetching or creating a run. Only mark them ready after their development task
commits and pushes usable revisions to the declared source and their change boundaries/dependencies are reviewed.

For a `feature` or `pr-variant`, the Source column names a definition in `experimental/SOURCES.json`.
An explicitly requested alternate file can be passed with `-SourceDefinitions <json-file>`.
For example (not selected by this example):

```json
{
  "local-annotations": {
    "repository": "E:/Dropbox/bare_repos/scadmaxx.git",
    "ref": "refs/heads/feature/annotations"
  }
}
```

Variants also require `prUrl`. The named definition must agree with the source declared in the selection list.
Dependency and partially-upstream changes still require the agent review described in the input contract.

## Configure, build, test, stage, package

Create a machine profile from `../profiles/windows-x64.example.json`. Save local tool paths in a `*.local.json`
file, which control Git ignores. Set exact installed MSVC/SDK versions, the vcpkg toolchain commit and
`vcpkgInstalled` to the existing shared package tree. On this machine that is
`D:/openscad/openscad-6991/build/vcpkg_installed`, using the toolchain in `D:/vcpkg`.
Manifest mode and automatic installation are disabled; missing dependencies are reported without installing or
rebuilding them. Catch2 and Boost.Nowide were added to the shared tree at the user's request on 2026-10-01;
the full-test profile checks that both are present.
Each build attempt
copies this profile and the consumed controls into its evidence, so local configuration is not lost.

```powershell
$buildArgs = @{
    Source = 'D:/openscad/wt-openscad-experimental-<run-id>'
    Build = 'D:/openscad/runs/<run-id>/baseline-build'
    Run = 'D:/openscad/runs/<run-id>'
    BuildProfile = 'D:/openscad/experimental/profiles/this-machine.local.json'
    Jobs = 4
}
./experimental/scripts/Build-Windows.ps1 @buildArgs -Step Configure
./experimental/scripts/Build-Windows.ps1 @buildArgs -Step Build
./experimental/scripts/Build-Windows.ps1 @buildArgs -Step Test
```

Keep the baseline result. Review/apply the first locked patch, commit its integration, and repeat Configure/Build/
Test using a separate `integration-build` directory. Continue one entry at a time, recording repair commits and
focused behavior checks. Reconfigure for every new source commit. Incompatible profile/dependency changes require
a new application build directory; both directories still use the same shared dependencies. No script removes or
cleans an old one. Old private-dependency runs and artifacts remain historical evidence.

Before staging, write `integrations.json` as an array of records with `id`, `sourceHead`, `outcome` (`integrated` or
`already-present`), `commit` (passing checkpoint), and `verificationLog` (a passing `logs/*-test.json` record for that
exact commit, relative to the run). Record conflicts,
repairs, attribution, and behavior evidence in the run report. Every selected entry needs evidence, even if already
upstream. Write `release-notes.md` with features and known limitations. Then:

```powershell
$buildArgs.Build = 'D:/openscad/runs/<run-id>/integration-build'
$staging = 'D:/openscad/artifacts/<run-id>/attempt-1/staging'
./experimental/scripts/Build-Windows.ps1 @buildArgs -Step Stage -Staging $staging
./experimental/scripts/Build-Windows.ps1 @buildArgs -Step Package -Staging $staging
```

Stage installs upstream resources, copies the locked Release DLL set and Qt plugins with an app-local `qt.conf`,
checks runtime dependencies, and copies license notices. It does not require Qt's optional `windeployqt` tool.
The runtime bundle deliberately includes the installed Release libraries, including indirect plugin dependencies.
Package verifies staging has not changed, creates/checks the ZIP, and exports matching source including submodules.
Both perform CLI geometry/PNG checks with a controlled PATH and reject error diagnostics even with exit code zero.
The Test step requires the Catch2 unit test binary, supplies the locked Qt plugins, and installs a separate test
bundle so rendering exercises the actual shaders and resources.
These automated checks do not claim GUI interactions, selected feature behavior, or clean-machine portability.
Complete those checks in the run report before marking the profile/release verified or creating its success tag.

For a failed staging attempt, use a new staging path; for a failed Package attempt, preserve its outputs and use a
new attempt directory. Final verification evidence and profile/dependency metadata must accompany source delivery.

## Tool checks

```powershell
pwsh -NoProfile -File experimental/scripts/Test-BuildTools.ps1
pwsh -NoProfile -File experimental/scripts/Test-SharedVcpkg.ps1 -BuildProfile experimental/profiles/this-machine.local.json
pwsh -NoProfile -File experimental/scripts/Test-RuntimeDeployment.ps1 -BuildProfile experimental/profiles/this-machine.local.json
pwsh -NoProfile -File experimental/scripts/Test-QtDeployment.ps1 -BuildProfile experimental/profiles/this-machine.local.json -DependencyPrefix <shared-installed-tree>/x64-windows
pwsh -NoProfile -File experimental/scripts/Test-ShortcutFeature.ps1 -BuildProfile experimental/profiles/this-machine.local.json -Source <checkout> -DependencyPrefix <shared-installed-tree>/x64-windows
```

Checks path containment, output capture, nonzero native exit codes, hashes, changed staging content, invalid run IDs,
preservation of existing runs, and refusal to stage real changes while refreshing Clipper's generated-header metadata.
The shared-vcpkg check configures a small fixture with the real toolchain, confirms shared library discovery even
with an unresolvable source manifest, checks stable dependency fingerprints across fresh PowerShell processes,
and checks missing-tree rejection without installing or compiling packages.
The runtime check compiles a small fixture, verifies DLL copying and execution,
and requires a missing DLL to be reported as an error. This is separate from OpenSCAD distribution verification.
The Qt fixture checks the same runtime-copy helper used by Stage: it must load the Windows platform plugin from
its staged folder and render an image with a controlled PATH. It does not display or interact with a user window.
The shortcut probe compiles the selected checkout's widget, redirects only its configuration path into a temporary
directory, and tests key assignment/invocation, existing-window consistency, persisted settings reload, collision
rejection, and defaults. It uses Qt's offscreen platform; Windows desktop interaction still needs separate evidence.
