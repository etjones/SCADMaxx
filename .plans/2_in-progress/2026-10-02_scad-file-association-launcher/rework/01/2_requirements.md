# Consolidated requirements

- Standalone C++17/Qt6 launcher under tools/scadmaxx-launcher, independent of editor builds and runtime versions.
- File types have name, one or more unique normalized extensions, named build sources, explicit builds and exclusions.
  Defaults: OpenSCAD (.scad) and SCADMaxx (.scadmaxx). A type may use either editor; no language compatibility gate.
- Each source has a folder and editable executable basename (defaults openscad.exe / scadmaxx.exe), plus installed
  folder or build collection scope. No global source prerequisite. Add/browse directly while selecting Latest.
- Default selection: fixed executable or latest from one source. Rebuilding a fixed path already follows that build.
- Latest ordering: natural build folder name/date, version (numeric and prerelease-aware), or executable modification
  time. Never creation time. Unknown versions are ineligible for version ordering; show an actionable explanation.
  Deterministic path tie-breaks. Show resolved winner, exact path, and reason; no silent cross-source fallback.
- Collections inspect root, root/bin, immediate child directories and each child/bin. No recursive watchers/scans.
  Skip symlink descendants, source/worktree/dependency/artifact children by default. Explicit roots/installations
  may target those locations; guide folder selection and explain scope. Exclude irrelevant candidates persistently.
- Metadata comes from files, never executing editors: adjacent version.xml and Windows version resources. Cache by
  canonical executable path, size, modification time, plus sidecar fingerprint. Fresh bounded enumeration on open;
  reuse unchanged metadata across launches. Cache is separate from settings; corruption does not block dispatch.
- Global Choose build when opening toggle in manager and tray, saved immediately. Off dispatches default; on shows
  candidates only for the matched file type, default preselected, version/path visible. Selection is one-shot; cancel
  launches nothing. Missing default is explained and chooser permits an explicit alternative.
- Batch files of the same type share discovery and one choice. Unknown/missing documents and self-routing fail.
  Preserve Unicode/spaces and launch editors as separate processes without a command shell.
- Wide manager and normal tray click share one window. Right click provides per-type fixed/latest shortcuts, global
  chooser toggle, rescan, open and quit. Preserve unrelated pending edits when a tray shortcut saves a selection.
- Apply/Revert for type configuration; optional tray and sign-in startup. No default deep scan at boot. User-triggered
  rescan and optional shallow startup refresh. Discovery never changes a fixed default.
- Register per-user Windows handler candidates; guide Default Apps, never write UserChoice. Keep settings and stable
  installation independent of versioned editor/build output. No automated changes to the user's associations/startup.
- Settings are atomically saved and validated; obsolete schema is preserved, not silently rewritten. No compatibility
  shim. Expose explicit backup/start-fresh only to user interaction.
- Keep the purple S icon shared by Explorer/window/tray. XML owns 0.1.0; no automatic bump. Versioned directory/ZIP,
  collision protection and PowerShell release workflow remain. Do not commit.
- Producers should stage builds elsewhere and rename completed folders into the collection. Launcher cannot prove
  that an executable's runtime is complete, and must not claim it can.
