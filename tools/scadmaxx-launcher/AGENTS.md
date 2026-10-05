# SCADMaxx Launcher

- During launcher development, stop or kill and restart this tool as needed to rebuild or replace its executable.
  The user has authorized this without asking again. Identify the process by its executable path and limit the action
  to SCADMaxx Launcher; this permission does not cover OpenSCAD editors or other applications.
- Prefer updating the existing launcher installation instead of creating another deployment solely because it is running.
- Treat `version.xml` as the only authored launcher version. Change it only when the user explicitly requests a
  version increase; never bump it automatically for builds, commits, fixes, packaging, or output-name collisions.
- Read `BUILDING.md` before changing version/build/package behavior or making a launcher release. Use its script
  so application version, release directory and ZIP filename stay consistent. Keep release outputs outside source.
- Read `USAGE.md` for current file-type/source/Latest/chooser behavior; the original README predates this redesign.
