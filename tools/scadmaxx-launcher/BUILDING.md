# Building and versioning SCADMaxx Launcher

## Version contract

`version.xml` is the single authored version source. Its initial `0.1.0` preserves the version previously in CMake.
Only an explicit user request authorizes changing the version. Do not increment it for a build, bug fix, commit,
release command, or filename collision. There is no automatic counter and no dependency on RIKS BuildNumber or
ReleaseBuilder.

The file has one `version/current` element, containing `major_version`, `minor_version`, `patchlevel` and
`identifier`. Numeric fields are nonnegative integers without leading zeroes. The identifier is empty for a final
version, or `dev`, `alphaN`, `betaN`, `rcN` for N >= 1. For example, identifier `rc1` produces `0.1.0-rc1`.
`Get-Version.ps1` validates XML with the platform XML parser and only reads it; malformed input fails the build.

CMake reads that script at configure time and reconfigures when XML changes. It generates the application version
header, sets the Qt application version (also available through `--version`), and installs `version.xml` beside the
executable. Do not edit generated headers or add another hard-coded product version.

## Configure and build

Use CMake 3.24+, C++17, Qt6 and PowerShell. Windows PowerShell 5.1 or PowerShell 7 works on Windows; PowerShell 7
provides the same scripts on other operating systems. No ReleaseBuilder executable or Python runtime is needed.
The launcher remains primarily a Windows tool; script portability does not imply verified application support on
other platforms.

From this directory in a Visual Studio x64 developer shell, using this machine's shared dependencies:

```powershell
cmake -S . -B D:/openscad/runs/scadmaxx-launcher/build -G Ninja -DCMAKE_BUILD_TYPE=Release `
  -DCMAKE_TOOLCHAIN_FILE=D:/vcpkg/scripts/buildsystems/vcpkg.cmake `
  -DVCPKG_INSTALLED_DIR=D:/openscad/openscad-6991/build/vcpkg_installed `
  -DVCPKG_TARGET_TRIPLET=x64-windows -DVCPKG_MANIFEST_MODE=OFF -DVCPKG_MANIFEST_INSTALL=OFF
cmake --build D:/openscad/runs/scadmaxx-launcher/build
ctest --test-dir D:/openscad/runs/scadmaxx-launcher/build --output-on-failure
```

Reuse the shared dependencies; do not install or rebuild a private Qt/vcpkg tree. Other machines supply their own
Qt/toolchain paths. `./Get-Version.ps1` prints the current label without configuring or building anything.

## Versioned release artifacts

After configuring, run from the same developer shell:

```powershell
./Build-Release.ps1 -BuildDirectory D:/openscad/runs/scadmaxx-launcher/build `
  -OutputDirectory D:/openscad/artifacts/launcher-releases
```

The script reconfigures, builds, runs CTest, installs the runtime into a fresh versioned directory, and creates a
flat ZIP from that directory. Every native command must succeed. For `0.1.0` the outputs are:

```text
launcher-releases/scadmaxx-launcher-0.1.0/
launcher-releases/scadmaxx-launcher-0.1.0.zip
```

Existing directory or ZIP names are rejected without overwrite. For another build of the same version, select a
new output parent (for example a run-specific directory). A failed staging/archive operation can leave partial
outputs for inspection; retry in a fresh parent. The script never deletes prior artifacts or changes version.xml.
It does not publish, install into the user's registered launcher location, or change associations/startup settings.

Versioned artifact directories are distribution outputs, not the stable installed launcher path. Keep associations
pointing to the independent installation described in `PACKAGING.md`. This ZIP workflow does not complete the
installer, license audit, runtime minimization or clean-machine acceptance work listed there; perform those checks
before public distribution. The release script may be verified locally without performing that full installer test.

## Interactive deployment and association checks

Start the installed launcher from the normal desktop (Explorer) before testing Windows association setup.
A launcher started directly by the Codex tool process on this machine inherited a private registry view:
its registration readback and SHAssocEnumHandlers probe succeeded, while desktop Explorer could not see
those entries. Running under the same user SID, or reporting no package identity, did not rule this out.
Do not treat those checks from the build environment as proof of desktop registration.

After replacing the executable, stop only the launcher at the deployment path, then open it through an
existing Explorer window's Document.Application.ShellExecute (or let the user double-click it).
Creating a new Shell.Application object and calling its ShellExecute directly did not establish the
correct desktop context in the observed case. Confirm the new launcher's parent is desktop Explorer.
Leave association writes to the application's setup button; never repair the real registry by hand.
Verify the launcher actually appears in the desktop chooser after setup. Keep isolated registry tests
for the writer contract, but report their limited scope separately from desktop acceptance.
