# SCADMaxx Launcher

Standalone Windows C++17 / Qt6 Widgets utility. Select an executable per extension; defaults are `.scad` and
provisional `.scadmax`. It does not require an OpenSCAD source checkout or change editor binaries.

Agreed distribution requirements and the deferred packaging test are in [PACKAGING.md](PACKAGING.md).
Finish implementation before running that test; the current deployment helper is not yet evidence that all
installer, runtime-minimization and independent-lifecycle requirements have been met.

Agreed distribution requirements and the deferred packaging test are in [PACKAGING.md](PACKAGING.md).
Finish implementation before running that test; the current deployment helper is not yet evidence that all
installer, runtime-minimization and independent-lifecycle requirements have been met.

## Use

Run `scadmaxx-launcher.exe` and open **Manage builds**:

- **Add installed build** selects one extracted build directory, inspecting that folder and its `bin` child.
- **Add builds collection** remembers a folder and scans it and its immediate children only.
- **Add executable** selects an editor directly.

Collection scans skip artifacts, runs, source checkouts/worktrees, build outputs, and dependency folders. The picker
starts at the last collection, or `D:/openscad` when available. Explicit installed-build/executable selection can
include a particular build from an otherwise excluded directory.

Discovery recognizes `openscad.exe`, `scadmaxx.exe`, and `scadmax.exe`, reads version metadata without launching
candidates, and deduplicates paths. A checklist shows name, version and full path before importing. New candidates
start unchecked. Save selection includes checked builds and remembers unchecked paths as excluded. Cancel changes
nothing. Use Included builds to curate an existing list and Excluded builds to restore previously excluded paths.
Builds used by saved or pending mappings cannot be excluded until those mappings change.

Rescan uses the remembered collections. Optional startup scans only announce new candidates through Review new builds;
they never import or change mappings automatically. Missing included binaries remain visible. Select a build per
extension and Apply to save the mappings. Existing settings remain compatible; old collection roots now scan shallowly.

Click **Open Windows Default Apps** after saving the extensions. This registers this executable as a per-user
candidate handler and opens Windows Settings; select SCADMaxx Launcher for each extension there. The action does
not overwrite Windows UserChoice or select a default for you. Status is refreshed on returning to the manager.

Install/copy the entire deployed launcher directory to a stable location before setup. If you move it later,
repeat Windows setup and toggle sign-in startup off/on to refresh those paths. Each build can live elsewhere.

Left-click the tray icon opens the same wider manager. Right-click exposes build submenus with current mappings
checked; selecting a build saves immediately. A tray selection replaces any pending edit for that extension while
preserving other pending edits. Missing executables are disabled. Closing hides the manager when the tray is active;
otherwise it exits. Quit stops the manager/tray but file opening continues to work. Start at sign-in is opt-in.

`--open <file> [file ...]` dispatches through the saved map then exits. Paths are forwarded as individual Unicode
arguments, without a shell. Missing files/targets or failed starts produce an error with an Open manager action.
`--tray` starts quietly if the tray is available. Repeated launches activate the existing manager.

Settings are atomically saved under the user's local application data directory, `SCADMaxx/Launcher/settings.json`.
A per-user manager lock prevents concurrent configuration writers. Invalid settings are preserved and reported.
Deleting a mapping does not choose a replacement Windows default. Select another app in Windows first if necessary.
Before removing the application, disable sign-in startup and reassign its extensions in Windows Default Apps.

## Build

Use existing Qt6 Core, Gui, Widgets, Network, Concurrent and Test packages, CMake 3.24+, and MSVC x64.
Do not install or rebuild shared dependencies. Example from a Visual Studio developer shell:

```powershell
cmake -S . -B <build-dir> -G Ninja -DCMAKE_BUILD_TYPE=Release `
  -DCMAKE_TOOLCHAIN_FILE=D:/vcpkg/scripts/buildsystems/vcpkg.cmake `
  -DVCPKG_INSTALLED_DIR=D:/openscad/openscad-6991/build/vcpkg_installed `
  -DVCPKG_TARGET_TRIPLET=x64-windows -DVCPKG_MANIFEST_MODE=OFF -DVCPKG_MANIFEST_INSTALL=OFF
cmake --build <build-dir>
ctest --test-dir <build-dir> --output-on-failure
cmake --install <build-dir> --prefix <stable-install-dir>
```

The install step deploys Qt runtime libraries/plugins. `--smoke-test` runs an isolated offscreen-capable UI check;
it does not register associations, change startup, or read/write normal settings. Set `SCADMAXX_LAUNCHER_CAPTURE`
to save that smoke window as a PNG. Tests cover mapping persistence/corruption, discovery and deduplication,
missing/self targets, write failures, and a real child process receiving a spaced Unicode filename.

Windows references:
- https://learn.microsoft.com/windows/apps/develop/launch/launch-default-apps-settings
- https://learn.microsoft.com/windows/apps/develop/windows-integration/default-apps-platform
