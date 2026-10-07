# SCADMaxx Launcher: file types, sources and opening behavior

This is the current usage guide for the redesigned launcher. The older README describes the initial global-build
library; this guide supersedes that interaction. Build/version policy is in BUILDING.md. Independent installation
and the remaining installer/public-distribution requirements are in PACKAGING.md.

## Configure a file type

The main window shows each file type and its default. Choose Configure to edit:

- Name and file extensions (comma- or space-separated). Defaults are OpenSCAD `.scad` and SCADMaxx `.scadmaxx`.
  Extensions are unique across file types. The file extension does not restrict which editor can open it.
- Search folders owned by this type. Each is identified by its full folder path and has an executable filename and scan scope. For example,
  SCADMaxx releases can look for `scadmaxx.exe` while OpenSCAD nightlies look for `openscad.exe` within the same type.
- Fixed executable, or Latest from folder with a source and ordering mode. Browse directly to an executable,
  or use Choose folder beside Latest to create its source immediately. No global folder setup is required.
- Available builds, showing versions and complete paths. Uncheck a build to exclude it from discovery/latest;
  check it again to restore it. New matching builds in a source participate automatically. Change a fixed
  selection before excluding it. Explicitly selected executables remain available even outside source folders.

Save closes the file-type dialog and stages changes in the main window. Apply writes them; Revert discards them.
Close in the configuration dialog leaves its file type unchanged unless you save it. File types can own multiple extensions, so `.scad` and another
extension can intentionally share the same default and build sources.

## Fixed and Latest

A fixed executable follows rebuilds at that exact path. Use it for a feature branch whose output is overwritten.
Latest follows builds at different paths within ONE selected source, for example new nightly release directories.
It never falls back to a different source or editor family when its selected source has no eligible builds.

Ordering modes:

- Build name / date: recognize valid dates such as 2026.10.03, 2026-10-03 and 20261003 in build names; dated names
  take precedence over undated names. Order dates chronologically, then naturally sort the name. Other names use
  natural ordering (`build-10` after `build-9`). For executables in bin or staging, use the enclosing build directory's name; attempt names include their release folder.
- Version: read adjacent `version.xml` in the documented version/current format, otherwise Windows executable
  version resources. Compare numeric components, then dev < alpha < beta < rc < final; suffix numbers are numeric.
  Builds without a parseable version are ineligible. No eligible versions produces an explanation, not a guess.
- Executable modified time: use last modification time of the executable, never its creation/extraction time.

Ties use canonical executable paths deterministically. The configuration preview shows the resolved winner,
its path, and why it won. The main window shows the most recently previewed result; file opening resolves afresh.

## Discovery and caching

Installed-build scope checks the selected folder, bin, staging and staging/bin. Collection scope applies these
checks to immediate child folders too. Select the release folder above attempt-1, attempt-2, etc. to discover
attempt-N/staging/scadmaxx.exe. Arbitrary deeper folders and extracted-check copies are not scanned.
Discovery does not recurse further, follow descendant symlinks, run editors to query
versions, or watch directories. Common artifact/source/worktree/dependency children are skipped. An explicitly
selected root or installed build is allowed even inside those locations: select a focused folder, not a broad drive.

Every latest/chooser opening enumerates the needed file type's sources. Metadata is cached separately in
build-cache.json using canonical executable path, size and modification time, plus version.xml size/time.
Unchanged entries avoid repeated version-resource reads; added and removed executables are discovered each time.
A broken or unwritable cache is nonfatal. Several files of the same type in one --open invocation share one scan
and one choice. No scan is needed for direct fixed-path opening. Manual Rescan updates manager/tray choices;
optional startup refresh is shallow and disabled by default.

Keep independent feature branches and release/integration collections separate when using Latest. Producers
should assemble complete builds elsewhere and rename completed folders into the selected collection. The launcher
can check an executable exists and is readable; it cannot prove all runtime files finished copying.

## Choose build when opening

This is one global switch in both the manager and the right-click tray menu. It saves immediately.

Off: open each handled file with its file type's configured fixed/latest default.
On: show that file type's available builds with its last successfully launched executable selected.
If it is no longer an eligible candidate, select the configured fixed/latest default instead. With neither
available, require an explicit selection. Successful launches remember the executable separately per file type
in last-used.ini, including launches with the chooser off. Cancel and failed launches do not update history.
The remembered selection does not change the configured default.

For example, add both an OpenSCAD source and a SCADMaxx source to the `.scadmaxx` type. Keep SCADMaxx as its default,
and explicitly choose OpenSCAD in the opening dialog when desired. The launcher does not translate the language.

For a multi-type batch, all chooser decisions complete before any editor launches. Files of one type are passed
together as separate Unicode arguments to the chosen executable, without shell quoting or a command shell.

## Tray, Windows and settings

Normal launch or left-click opens the same wide manager. Right-click offers fixed builds, Latest rules per source,
the global chooser switch, rescan, manager and quit. A tray choice immediately saves that type; unrelated pending
file-type edits remain. A pending edit to the chosen type is replaced and the manager reports this.

Keep in system tray and Start at sign-in are independent options. Closing hides the manager when tray mode is
available; otherwise it exits. File associations still work without a running tray process. Set up Windows associations registers
this stable launcher as a handler candidate and opens Default Apps for your explicit choice. It never sets UserChoice.
Install in a stable launcher-owned directory; do not register an executable in a disposable versioned build directory.

Settings remain under the user's SCADMaxx/Launcher local application data. Schema 2 replaces the old global-library
schema. An unsupported or damaged file is left intact. The manager offers Back up and start fresh; only that explicit
choice copies the original to a uniquely named backup and writes new defaults. There is no automatic migration or
version bump. Dispatch cannot reset settings. Normal manager instances use a per-user lock and activation IPC.
