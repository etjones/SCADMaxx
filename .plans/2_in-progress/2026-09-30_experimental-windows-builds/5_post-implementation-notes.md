# Implementation notes

Status: tooling implemented and first automated package verified; full Windows desktop acceptance remains open.

- Initialized `D:/openscad` as a separate Git repository on `main` with an allowlist `.gitignore`.
  No control commit or remote created; unrelated annotations planning files remain unstaged.
- Added PowerShell tools for frozen run preparation, configure/build/test/stage/package, structured command logs,
  control snapshots, build-directory ownership, input fingerprints, runtime deployment, and source archives.
- Prepared `experimental/20260930-profile` in its own worktree from upstream
  `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`. Locked #6878 and #6776 in the requested order.
- Selected Ninja/MSVC 14.51.36231, SDK 10.0.26100.0, and vcpkg
  `194964eec5d5601aef90b456d553412f0b2b0ea5`, using a private manifest/install directory for the baseline.
- PowerShell syntax and eleven targeted tool checks passed. Configure, GUI Release build, unit tests, installed
  runtime, staging and fresh ZIP extraction checks passed. The full desktop/clean-machine profile remains unverified.
- Compiled native-DLL and Qt deployment fixtures passed, including missing-DLL rejection, app-local Windows Qt
  plugin loading, controlled-PATH execution, and image rendering. Qt deployment uses the locked Release DLLs and
  plugins with `qt.conf`; the selected Qt profile does not include its optional `windeployqt` executable.
- The first baseline now builds and passes unit tests and installed-bundle rendering. Four separate source repair
  commits address stream declarations, runtime-sized arrays, Cairo linking, and duplicate manifests. Each has
  retained refs and failure/verification evidence in `experimental/REPAIRS.md`.
- PR #6878 is integrated as `1ad60cf12` and passes a full build, unit tests, both STL backends, PDF and PNG export.
  PR #6776 is integrated as `31b143053`; the combined build and all automated runtime checks passed.
- The isolated shortcut widget test passes assignment/key invocation, cross-window action updates, saved-settings
  reload, collision rejection, defaults, and light/dark palette cycles. This is not a Windows desktop theme test.

Deliverables are under `artifacts/20260930-profile/attempt-1/`: Windows ZIP, matching-source ZIP and SHA-256 files.
The source ZIP includes exact submodules, six composition patches, tool/control snapshots, dependency metadata,
logs and focused feature evidence. Final source is `31b1430530c295c4b24662b2d5a4b989bbbabc7d`.

The authoritative execution evidence is in `runs/20260930-profile/`. Remaining checks are Windows desktop theme
switching across the application, full-process shortcut persistence, and clean-machine portability. The plan stays
in progress for those acceptance checks. No external publication or successful-release tag exists. Control files
remain unstaged/uncommitted; source composition and repair commits are retained locally. No recurring job was set up.

## Fix forward: reuse shared vcpkg (2026-10-01)

The user rejected the private manifest/install strategy because it rebuilt dependencies unnecessarily.
New experimental builds now use the existing `D:/openscad/openscad-6991/build/vcpkg_installed` tree, as annotations
already does. The machine/example profiles specify it explicitly; configure disables manifest mode and installation.
The build records its installed status hash, detects changes, and reports missing dependencies without a fallback
install. Source-package reproduction instructions describe shared dependencies instead of a generated manifest.
Separate application build directories and historical first-run evidence remain intact.

The shared tree currently lacks Catch2 and Boost.Nowide; full experimental build/test preflight reports these gaps.
No dependency packages were installed, upgraded or rebuilt, and no new OpenSCAD build was started for this correction.

Verification: PowerShell syntax checks and all 11 existing build-tool checks passed. The new real-toolchain fixture
found Qt6Core in the shared tree despite an unresolvable source manifest, left the package status unchanged,
created no private installed tree and rejected a missing shared tree without creating it. Evidence:
`runs/tool-tests/shared-vcpkg-61cda21be47f4cb7a6bdc88b962bd5b1/` and
`runs/tool-tests/f6419ff1d14346499e4c8beab2e48d1f/`.

## Authorized cleanup and shared dependency rebuild (2026-10-01)

The user subsequently requested removal of the obsolete private build outputs, installation of the two missing
libraries into the shared tree, and a rebuild. Removed the old run's three build directories (28.97 GiB logical
size), retaining source, logs, delivered ZIPs and small dependency/configuration records. Catch2 3.16.0 and
Boost.Nowide 1.92.0 were installed in the shared tree in 43 seconds; all other package records were unchanged.

Rebuild evidence is in `runs/20261001-shared-rebuild/report.md`. It uses the exact prior source composition and
branch with a distinct binary version/run identity, not a newly fetched upstream composition. Configure, compilation,
unit tests, the shortcut/palette probe, installed/staged rendering and fresh-ZIP checks passed with shared dependencies.
The new Windows/source ZIPs and their checksums are in `artifacts/20261001-shared-rebuild/attempt-1/`.

Test preflight exposed unstable dependency metadata key order between PowerShell processes. The helper now returns
ordered fields; a focused cross-process regression check and all 11 existing tool checks passed. After every
dependency value compared equal, the build state fingerprint was migrated without recompiling; evidence is retained.
An extra Unicode CLI filename probe crashes in both the prior and rebuilt binaries, while ASCII controls pass.
This existing source limitation is disclosed in release notes and remains unresolved. Desktop and clean-machine
verification remain pending. No source changes, commits, publication or scheduling occurred during this rebuild.
