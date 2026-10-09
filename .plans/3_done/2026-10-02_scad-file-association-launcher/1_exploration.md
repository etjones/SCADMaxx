# SCAD file association launcher

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Original exploration status: implemented in C++ / Qt6; see 5_post-implementation-notes.md for verification and desktop acceptance.

## Intent and ownership

Provide a small Windows desktop utility for choosing which executable opens each registered file extension.
Start with `.scad` and provisional `.scadmax`, allowing additional extensions. Support multiple OpenSCAD master
builds and future SCADMaxx builds, an optional system tray presence, and optional launch at user sign-in.

Product: **SCADMaxx Launcher**, a separately runnable companion maintained with SCADMaxx. Keep its installed
path independent of dated editor builds. The user confirmed the owning
SCADMaxx repository and tools/scadmaxx-launcher location. This plan is now owned here; the chat has not been moved.

## Proposed interaction

- Normal launch or left-click on the tray icon opens the wider main window: one extension per row, selected build,
  executable path, and Windows association status. There is one manager, not two alternative dialogs.
- Changing a selection stages a mapping; Apply saves all valid changes. Revert discards unsaved changes.
- Add extension normalizes the leading dot and case, rejects duplicates and malformed values, and starts unassigned.
- Build library: add an executable manually or discover candidates within user-selected folders; keep multiple builds.
  Show friendly name, family, version when available, path, and availability. Include configurable search folders,
  Rescan, and optional scanning at startup in the first version. Discovery never changes a selected build automatically.
- Right-click tray menu: extension submenus with build shortcuts and a check beside the current saved build;
  selecting an available build immediately saves that extension's mapping and closes the menu. No Apply button here.
  Also provide Open manager, Rescan builds, and Quit. Disable unavailable build shortcuts.
- Both surfaces share saved mappings. A tray change updates the manager's corresponding selection immediately while
  preserving pending edits to other extensions; notify when it replaces a pending edit to that same extension.
- Settings: independent tray and sign-in switches. Closing the window hides it only when tray mode is enabled.
- Startup defaults off pending user choice. Quitting the tray does not disable file opening through the launcher.
- Setup: register the launcher as an available handler and guide the user to Windows Default Apps. Show setup needed
  separately from mapping validity. Recheck after the user returns; never imply opening Settings completes setup.
- Missing selected executable: show its exact path and a choose-replacement action. Never silently choose another build,
  especially for `.scadmax`, whose language extensions may not be accepted by ordinary OpenSCAD.

## Architecture proposal

Windows associates each extension with a stable launcher. The launcher reads a per-user extension-to-executable map,
dispatches the supplied file to that executable, and exits without requiring the tray process. The manager and tray
edit the same configuration atomically. Separate the association registration, dispatch, and UI concerns.

Use the GUI executable for opening documents, not the console launcher used by repository export tools. Preserve paths
with spaces and Unicode through argument-safe process creation; do not construct a shell command. Reject self-routing
and missing/non-executable targets. Keep selected paths pinned until the user explicitly changes them.

Register file types through supported per-user Windows mechanisms. Do not write protected UserChoice hashes, silently
take over existing associations, or reclaim defaults changed elsewhere. Removing a managed extension must explain how
to select another handler if Windows still points at the launcher. Uninstall should guide reassignment and remove only
registrations owned by this product. Prior Windows defaults cannot be promised as an automatic rollback.

Microsoft reference, consulted 2026-10-02:
https://learn.microsoft.com/windows/apps/develop/windows-integration/default-apps-platform

## Mockup scope

Interactive conversation mockup shows the wider manager and a simulated tray icon. Normal click opens the manager;
right-click opens a compact menu with extension/build shortcuts. An explicit preview button makes the menu accessible
without a mouse. Main-window Apply/Revert and immediate tray selection update the same mappings. Builds, discovery,
association setup, and settings remain local simulations, not a scan of or changes to this computer.

## First implementation boundary

Deliver Windows-only mapping, manual executable selection, supported association setup, independent dispatch, optional
tray, opt-in sign-in launch, and folder-based build discovery with Rescan and optional startup scanning. Exclude build downloads,
automatic upgrades, parsing or converting SCAD syntax, and per-project overrides from the initial version.

Acceptance scenarios: independently map both defaults; add a third extension; switch one without changing the others;
open a spaced/Unicode filename; open with the tray stopped; cancel staged edits; recover from a deleted build; retain
settings across restart; distinguish Windows setup needed from saved routing; honor externally changed defaults.

## Decisions for review

Confirmed: wider main window on normal open, compact build shortcuts on tray right-click, discovery in the first version.
SCADMaxx ownership and repository are confirmed. `.scadmax` remains provisional and user-editable.
Implementation language/toolkit: C++17 and Qt6 Widgets, selected by the user. This independent proposal changes no
existing ParametricDesigns feature ordering, so the sparse dependency graph remains unchanged.
