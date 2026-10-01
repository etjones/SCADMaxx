# Windows x64 GUI Release profile

Status: shared-dependency configure/build/test/stage/package and fresh-ZIP extraction checks passed on 2026-10-01.
Latest evidence: `runs/20261001-unicode-filename-fix/` (prior shared rebuild: `runs/20261001-shared-rebuild/`;
first private-tree run: `runs/20260930-profile/`). The non-ASCII filename crash is fixed by the per-process UTF-8
manifest repair on Windows 10 1903+. Before/after regressions and both launchers in the extracted ZIP are verified.
The local test ZIP contains the complete selected stack; Windows desktop
theme switching, full-process shortcut persistence and clean-machine portability still need verification.
This is not yet promoted to a fully verified distribution profile. See the [tool usage](../scripts/README.md).

## Shared dependency policy

Use the existing shared vcpkg packages for all new builds. On this machine the toolchain is in `D:/vcpkg`,
and the installed packages are in `D:/openscad/openscad-6991/build/vcpkg_installed`, also used by annotations.
Set `vcpkgInstalled` explicitly in the machine profile. Separate application build directories all use this same
dependency tree. Configure with `VCPKG_MANIFEST_MODE=OFF` and `VCPKG_MANIFEST_INSTALL=OFF`.
Do not generate private manifests/install trees, install or upgrade shared packages automatically, or fall back
to rebuilding dependencies. Report missing dependencies instead. Record the actual installed package status hash;
the vcpkg checkout commit identifies the toolchain, not necessarily the revision that built the shared binaries.

On 2026-10-01 the user explicitly requested adding the missing Catch2 and Boost.Nowide packages to the shared tree.
Catch2 3.16.0 and Boost.Nowide 1.92.0 were installed; all other package records remained unchanged. Catch2 runs the
C++ unit tests, while Nowide converts Windows Unicode command-line arguments to UTF-8. Evidence and the rebuild
are recorded in `runs/20261001-shared-rebuild/`. Future missing packages still require reporting rather than an
automatic install. Annotations' earlier build used a Nowide include shim and did not run Catch2.

## Historical first-run recipe

The first run locks the following versions. Machine paths belong in the ignored `this-machine.local.json` file;
do not silently upgrade these pins while resuming a run. That run used private dependency trees; its evidence and
ZIPs are retained as historical results. New runs follow the shared dependency policy above.

| Component | Recorded version |
| --- | --- |
| Visual Studio / MSVC toolset | VS 18 Community / 14.51.36231 (compiler 19.51.36257.0) |
| Windows SDK | 10.0.26100.0 |
| CMake / generator | 4.3.2 / Visual Studio's bundled Ninja |
| vcpkg commit | `194964eec5d5601aef90b456d553412f0b2b0ea5` |
| Triplet / Qt / QScintilla | x64-windows / 6.11.1 / 2.14.1 |
| CGAL / Manifold | 6.2.0 / submodule 3.5.3 |
| Test host | Windows 10.0.26200 x64; development machine |

Resolved packages, compiler/tool hashes, submodules, CMake options, and exact paths are retained in each run's
metadata. Four baseline source repairs were required for the first run; see the [repair catalog](../REPAIRS.md).

## Required configuration

- Use CMake, MSVC, the Windows SDK, Qt 6, QScintilla, and vcpkg with the `x64-windows` triplet.
- Build the GUI (`HEADLESS=OFF`, `USE_QT6=ON`) in Release. Select and record the generator and toolset explicitly.
- Reuse the explicit shared installed tree under the policy above, with manifest mode and installation disabled.
  Record the toolchain checkout, triplet, installed package set and status hash without changing shared packages.
- Record all CMake feature switches, dependency versions, submodule SHAs, compiler/SDK versions, and environment
  setup. A machine-specific tool path is configuration, not a portable default.
- Inspect the locked source's build options and packaging support before implementing commands. The existing
  `scripts/win-msvc-build.bat` default headless path is not the requested GUI distribution recipe.

## Executable tooling

`Build-Windows.ps1` accepts explicit source, build, run, profile, and staging paths and uses upstream CMake/install
targets. `New-ExperimentalRun.ps1` locks selections and prepares the isolated checkout. The build steps are:

| Operation | Required result |
| --- | --- |
| Configure | Validate toolchain and existing shared dependencies, record inputs and CMake cache; fail on missing dependencies or mismatch. |
| Build | Build the selected configuration; log command, source SHA, output, and exit code. |
| Test | Run relevant automated tests and CLI fixtures; record GUI checks separately with actual evidence. |
| Stage | Install/deploy executable, Qt plugins, runtime libraries, resources, and notices into isolated staging. |
| Package | Write build info and release notes, create ZIP/checksums, extract separately, and run runtime smoke checks. |

Fail on native-command failures; do not report success because the surrounding PowerShell process continued.
Support resuming a step without refetching locked inputs or overwriting an earlier delivered artifact. Logs must
avoid credentials and record only environment values relevant to reproducing the build.

## Cache rules

Keep the unmodified baseline build separate from integration builds. Incremental integration builds may reuse
their own directory while the profile is compatible. Reconfigure when source build configuration changes.

Record a compatibility fingerprint covering compiler/toolset, SDK, CMake/generator, architecture, configuration,
vcpkg toolchain revision/triplet, shared installed path/status hash, submodule revisions, and feature switches. Changes require
a fresh directory unless the tooling explicitly verifies compatibility. Never copy CMake caches from another
worktree; they contain source/build paths. A fresh application build directory still uses the same shared vcpkg
installation. Reusing only a download/binary cache does not satisfy the shared dependency policy.

## Promotion to verified

Only mark a concrete profile revision verified after configure, GUI Release build, tests, deployment, and ZIP
extraction checks pass. Test startup, preview, render, required resources, and selected behaviors with a controlled
runtime PATH. Record the test machine and any lack of a clean-machine test. Check the experimental identifier in
the running application as well as the package; use the [release rules](../versioning-and-releases.md).

A run may establish the first profile, but must label intermediate steps unverified. Do not distribute a build as
verified while packaging or runtime checks remain incomplete.
