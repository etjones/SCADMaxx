# SCADMaxx Launcher implementation and verification

Date: 2026-10-02. Implementation complete; retained in progress for real desktop/default-app acceptance.

## Ownership and delivery

The user selected C++ / Qt6 under the SCADMaxx control repository's `tools` directory.
Source: `D:/openscad/scadmaxx/tools/scadmaxx-launcher`.
Runnable deployment: `D:/openscad/artifacts/scadmaxx-launcher/scadmaxx-launcher.exe`.
Build/evidence: `D:/openscad/runs/scadmaxx-launcher`.
This is a standalone tool; no OpenSCAD source worktree or integration-stack entry is needed.
The control repository's `.gitignore` now admits `tools/`. Its root README was not changed.
No commits, pushes, public releases, or association/startup changes were performed.

## Implemented

- Qt6 Widgets manager with wider layout, extension rows, editable build selections, paths and Windows status.
- Main-window Apply/Revert; add/remove extension; manually add an executable.
- Configurable recursive folder discovery; Rescan; optional startup scan; version-resource inspection without
  executing discovered binaries; case-insensitive path deduplication. Missing binaries remain visible.
- Left-click tray opens manager. Right-click extension submenus check current builds and save immediately.
  A tray change replaces the same extension's pending edit while preserving other pending edits.
- Independent opt-in sign-in startup, tray preference, close-to-tray and Quit.
- Per-user registration as a Windows candidate handler, Default Apps deep link, status refresh on activation.
  Protected UserChoice values are not touched. Registration is performed only by the setup button.
- Independent file dispatch with exact Unicode argument forwarding, missing-build recovery and self-routing guard.
- Atomic JSON saves, malformed-settings preservation, per-user single-manager lock and local activation socket.
- Repeatable CMake build/install; deploy required DLLs, Windows/offscreen plugins, style, MSVC runtimes and notices.

## Verification

Toolchain: MSVC 19.51.36257.0 / VS 18, CMake 4.3.2, Qt 6.11.1, Ninja, Release x64.
Shared vcpkg tree: `D:/openscad/openscad-6991/build/vcpkg_installed`; packages were not installed or upgraded.
Dependency status SHA-256: `2983CAF4494A3428F029553E921A862000477E8E1266A8B74846ACDE80C7C2E1`.

CTest: 2/2 suites passed. Core QtTest: 6 behavior cases plus init/cleanup, 8 passed, no failures.
Evidence: `core-tests.txt` and `build/Testing/Temporary/LastTest.log` in the run directory.
Cases cover extension normalization, persistence/corruption, discovery/deduplication without retargeting,
missing/self executable targets, failed writes, and actual child-process forwarding of a spaced Unicode filename.
UI smoke covers staging, Apply, persisted tray selection/check state, preservation of another pending extension,
Revert, and the compact menu actions. It runs with temporary settings and no Windows integration writes.
The installed executable passed the smoke check with PATH limited to Windows/System32 and Windows, using its
deployed plugins. Offscreen capture `manager.png` was inspected; a deferred-widget redraw artifact was corrected.
Deployment without windeployqt uses CMake dependency discovery; repeat installs accept identical DLL copies and
reject mismatched runtime versions. See `deploy.log` for the final successful installation.

## Remaining desktop acceptance and limits

- Select actual build folders/executables and exercise normal document opening through Windows Default Apps.
- Verify actual tray click behavior, sign-in startup, and second-process activation on the user's desktop.
- Check native light/dark appearance and clean-machine portability; offscreen rendering is not proof of those.
- `.scadmax` remains the provisional second default extension; it is editable in the manager.
- Install/copy the entire deployed directory to a stable location before registering it. Moving the launcher requires
  refreshing handler registration and toggling startup off/on. There is no installer/uninstaller in this version.
- Discovery finds executable names, not language capabilities. Selecting a build remains a user decision.
- Scans run asynchronously; closing during a scan waits for the selected folders to finish.
- Source is intentionally uncommitted: the shared git-workflow skill requires an explicit commit request. Consequently
  no committed/private-origin readiness claim is made and no combined SCADMaxx distribution entry was enabled.

Follow-up options: fix forward for bounded corrections, replan for a changed approach, restart for changed assumptions,
or supersede with a different tool.

## UI refinement — 2026-10-02

User requested a closer match to the approved mockup. Replaced the native table with individual extension rows,
full-width selectors, inline paths/status, subtle separators and per-extension remove actions. Added the branded
header, Segoe UI typography, consistent control spacing, primary Apply styling, and distinct footer. Folder
configuration is accessible behind Build folders instead of occupying the main view. Added system-aware light/dark
colors, themed control palettes, and explicit selector arrows. Native title-bar/window behavior remains intact.

Existing mapping and tray regression suites passed after the layout change. The revised deployed executable passed
its isolated smoke check in both light and dark appearance with a minimal PATH. Inspected both captures:
`D:/openscad/runs/scadmaxx-launcher/manager-refined.png` and `manager-refined-dark.png`.

The original deployed process was running. It was not stopped or overwritten. Updated source is in the same tools
folder; the review deployment is `D:/openscad/artifacts/scadmaxx-launcher-refined/scadmaxx-launcher.exe`.
Quit the old tray instance before opening this review build, because both use the same single-manager lock/settings.
Windows associations/startup have not been changed. Repoint registration/startup only after choosing the final stable
installation location. Changes remain uncommitted.

## Guided build selection — 2026-10-02

Replaced Build folders with Manage builds, offering installed-build, shallow collection, and executable selection.
Collections inspect only their root and immediate children, skipping artifacts/runs, source/worktree and dependency
folders. Explicit installed-build selection checks its root/bin and bypasses collection exclusions. Picker starts at
D:/openscad when present and no collection has been selected.

Every import now uses a name/version/full-path checklist; new candidates begin unchecked. Exclusions persist in an
optional excludedBuilds settings field without breaking existing schema-1 settings. Included/Excluded builds actions
support pruning and restoring entries. Saved and pending mappings protect their selected builds. Cancellation saves
nothing. Startup discovery queues review rather than importing automatically; collection rescans omit excluded paths.
Existing imported builds are preserved until explicitly excluded by the user; extension mappings remain unchanged.

Both CTest suites passed. Added two core cases for shallow/excluded traversal with explicit override, and persisted
curation/restoration/protected mappings. UI smoke exercises checklist default selection, accepted import and cancelled
review. Offscreen Manage builds capture inspected at runs/scadmaxx-launcher/manage-builds.png. Rebuilt and deployed to
the original artifacts/scadmaxx-launcher location, with a successful deployed smoke check. No launcher instance was running at deployment time; no process needed to be stopped or restarted.
