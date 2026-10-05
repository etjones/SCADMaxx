# Launcher and SCADMaxx packaging requirements

Agreed with the user on 2026-10-02. These are requirements, not a claim that packaging is implemented or tested.
Finish the launcher implementation first; then perform the packaging test in this SCADMaxx workspace.
This records the follow-up only: do not start a packaging run, installation, publication or background monitor now.

## Distribution and installation

- Build the launcher as part of the integrated release workflow, but produce an independently installable package.
- Offer the launcher installer as a separate download. The same installer may also accompany a SCADMaxx download;
  the choice of download presentation remains open. Both forms must install the same independent launcher.
- Install into a stable launcher-owned directory, separate from every versioned OpenSCAD/SCADMaxx installation.
  Proposed per-user location: `%LOCALAPPDATA%/Programs/SCADMaxx Launcher`.
- Keep Windows file associations and optional sign-in startup pointed at this stable launcher executable.
  Retain the explicit Windows Default Apps selection flow; do not overwrite UserChoice.
- Give the launcher its own update/uninstall lifecycle. Removing or replacing an editor build must not delete the
  launcher, its runtime, settings or registration. Removing a selected editor must yield a useful missing-target
  state and allow choosing another installed build.
- Keep settings separate from versioned binaries. Launcher upgrades must preserve saved mappings and discovery roots.
- Launch editors as separate processes. The launcher must work with independently installed OpenSCAD and SCADMaxx
  versions without loading their DLLs or depending on their Qt version.
- This independent installation supersedes the initial proposal to register a launcher living beside one editor
  and borrowing that editor's runtime DLLs. An installer bundled with a release does not change installation ownership.

## Executable identities

- Produce the SCADMaxx editor as `scadmaxx.exe` through build output configuration, rather than renaming a packaged
  executable afterwards. Retain `scadmaxx-launcher.exe` for the separate launcher.
- Audit the Windows console launcher, subprocess paths, tests, install rules and packaging references when changing
  the editor output name. Verify both GUI and command-line invocation; decide the matching console-wrapper name
  during that implementation. Existing OpenSCAD installations retain their original executable names.
- Do not imply the rename is already in the current delivered ZIP or change upstream-facing builds globally.

## Small, self-contained runtime

- Use dynamic Qt6 linking with a private, matching runtime shipped with the launcher. This is C++/Qt, not PyQt.
  Static Qt and a separate static dependency build are not the selected approach.
- Reuse the existing shared build dependencies; do not install or rebuild a private Qt/vcpkg tree.
- Deploy the launcher's actual DLL dependency closure, including transitive dependencies and the required compiler
  runtime. Do not copy the complete shared vcpkg bin directory or OpenSCAD's runtime directory.
- Include the Windows platform plugin and any style plugin actually used. Account explicitly for dynamically loaded
  plugins, since an executable import scan alone cannot prove which plugins are needed.
- Exclude Qt Test, test executables, the offscreen testing plugin and unused image/network/other plugins from delivery.
  Keep test-only dependencies in the validation environment. Validate the delivery using the native Windows platform.
- Exclude OpenSCAD geometry/rendering libraries and unrelated resources unless the launcher's own dependency analysis
  proves they are needed. Retain unavoidable dependencies of the shared Qt build; do not remove DLLs merely because
  the launcher does not directly call their APIs.
- Keep plugin lookup local to the launcher package, with appropriate `qt.conf` configuration.
- Record the delivered file inventory, dependency reasons, Qt/toolchain versions, hashes, compressed package size and
  installed size. Assess size from measured output rather than promising a single executable or an arbitrary limit.

## Licensing material

Use the agreed dynamic-Qt open-source approach and satisfy the applicable LGPLv3 and third-party requirements:
ship required notices/license texts, retain corresponding Qt source and modifications through a compliant source
delivery mechanism, and allow replacement with a modified compatible Qt build. Include notices for the components
actually shipped rather than every package in the shared installation; account for embedded third-party components
as well as separate DLLs. Dynamic linking alone is not a complete compliance check.

Choose and record the launcher's own license before public distribution; this discussion did not assign one.
Installer technology, hosting destination and public publication are also not selected by this requirements record.

References checked during the decision:
- [Qt licensing obligations](https://www.qt.io/development/open-source-lgpl-obligations)
- [Qt Windows deployment](https://doc.qt.io/qt-6/windows-deployment.html)

## Deferred packaging test

After implementation is finished, test the concrete launcher package here and retain evidence under `runs/` and
`artifacts/`, outside source changes:

1. Build and run the launcher tests using the shared dependencies; create a fresh deployment directory.
2. Audit its DLL/plugin inventory and license material; measure compressed and installed size.
3. Test the deployed application with a controlled PATH and no developer Qt/plugin paths. Prefer a clean Windows
   environment as well; distinguish that from a development-machine PATH-isolation check.
4. Exercise native GUI, tray behavior, discovery, saved mappings and file dispatch, including spaced/Unicode paths.
   Test different editor builds with different runtime installations.
5. Install in the stable location and verify the association/startup paths. Use an isolated test account/environment
   for default-app changes so the user's normal associations and settings are preserved.
6. Remove or replace a disposable selected editor build. Confirm the launcher remains usable, reports the missing
   target and dispatches successfully after selecting another build.
7. Test launcher upgrade and uninstall separately: preserve settings on upgrade, remove only launcher-owned files
   and registration on uninstall, and leave editor installations intact.
8. Confirm the editor's `scadmaxx.exe` output name and console invocation work in the integrated release. If the
   launcher installer is included with that download, verify it still installs independently.

Record failures and reproducible fixes; do not mark packaging complete from compilation or an offscreen smoke test
alone. Retain the existing flat editor ZIP and no-release-notes policy.
