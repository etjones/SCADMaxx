# Redesign implementation and verification

Implemented 2026-10-03; uncommitted, awaiting user review. Version remains 0.1.0.

## Delivered

- File-type-owned extensions/sources/explicit builds/exclusions, fixed/latest defaults and direct source creation.
- Configurable executable basenames including openscad.exe and scadmaxx.exe; defaults .scad and .scadmaxx.
- Shallow collection/install scans, name/date/version/modified ordering, deterministic ties, non-executing metadata
  reads and persistent best-effort cache. No directory watchers or deep startup traversal.
- Global chooser toggle in manager/tray; per-type candidates/defaults; one-shot choices and cancel; batch resolution
  once per type and no dispatch until all chooser decisions complete. Unicode arguments passed without a shell.
- Wide manager, staged Apply/Revert, immediate tray changes preserving unrelated draft types, source editor/review,
  Windows registration/startup and single-manager activation retained. Draft scans do not leak into saved tray menus.
- Schema 2 with strict validation and atomic persistence. Unsupported files preserved; user-only backup/start-fresh
  action. No migration added. USAGE.md describes current behavior; original hand-maintained README left untouched.
- Version.xml/PowerShell release work retained, shared Explorer/window/tray icon built. Added required Qt ICO plugin
  to tests/deployment. No installer implementation, public distribution, registration changes, startup changes or commit.

## Evidence

- CMake/MSVC Release build using the existing shared vcpkg Qt dependencies passed.
- CTest: launcher-version, launcher-core and launcher-ui all pass (3/3).
- Nine core behavior cases cover normalization/schema corruption, bounded scan/filter scope, natural/date ordering,
  semantic versions/prereleases, no fallback for unknown versions, modified-time/path ties, persistent cache reuse
  and invalidation, new/deleted candidates, source isolation/exclusions, fixed rebuilds, self/missing targets and
  real Unicode subprocess arguments. XML reader tests retain read-only/version validation coverage.
- UI smoke covers Apply/Revert, unrelated pending edits during tray selection, global toggle persistence, chooser
  default/one-shot/cancel, multi-extension editing, source creation/executable filter, latest ordering/tray selection,
  shared icon availability and actual two-document dispatch to the test receiver (including Unicode/spaces).
- Packaged native Windows light/dark UI checks pass with a System32-only PATH and no developer Qt plugin variables.
  Screenshots reviewed; corrected native configuration-dialog clipping and dropdown arrows.
- Windows ExtractIconEx reports one embedded icon group. Package and updated deployment executable hashes match.
- No automated tests registered file associations, changed sign-in startup, or wrote normal user settings.

Paths:
- Build and logs: D:/openscad/runs/scadmaxx-launcher/build
- Native and offscreen captures: D:/openscad/runs/scadmaxx-launcher/redesign-*.png (editor/chooser captures appended)
- Pre-redesign source snapshot: D:/openscad/runs/scadmaxx-launcher/rework-01-before
- Final directory: D:/openscad/artifacts/launcher-redesign-final-20261003/attempt-2/scadmaxx-launcher-0.1.0
- ZIP: same parent, scadmaxx-launcher-0.1.0.zip
- Existing deployment updated and opened: D:/openscad/artifacts/scadmaxx-launcher-refined/scadmaxx-launcher.exe
- Deploy log: D:/openscad/runs/scadmaxx-launcher/redesign-install.log

## Limits and next review

Metadata caching uses size/time fingerprints, not executable hashing. A producer preserving both size and modification
stamp can evade invalidation; completed builds should be staged and renamed into place. A readable executable does
not establish runtime completeness. Native tests used this development machine with isolated search paths, not a clean
machine or installer. Full runtime minimization/license/installer acceptance remains the separate PACKAGING.md scope.
Current package retains the previous deployment helper's broader license inventory and offscreen plugin.

The user can fix forward (bounded corrections), replan (change implementation strategy), restart (revisit requirements),
or supersede (replace the feature objective). Keep prior plan/attempt evidence; do not roll back unrelated work.

## Windows association registration fix (2026-10-03)

User reported the setup button's extension claims did not surface the launcher in Windows Settings.
Read-only inspection showed capabilities/ProgIDs existed but executable Applications identity was absent.
The button now writes Applications/FriendlyAppName, SupportedTypes, explicit open command, icon and App Paths,
plus ProgID Application identity and capability icon. It synchronizes and verifies its writes before publishing,
notifies the shell with SHCNF_FLUSH, checks Settings-launch success and shows per-extension setup/ready status.
The EXE now includes FileDescription/ProductName/version resources generated from version.xml.

Regression coverage exercises the SAME writer under a unique, temporary private registry branch; verifies both
.scad and .scadmaxx, correct quoted commands, repeat registration, and preservation of existing extension defaults
and UserChoice. All three CTest suites pass. The refined deployment was updated and reopened; executable metadata
was read back successfully. No actual file associations were manually patched or registered by the agent.
The user's next button press performs the real registration. Settings UI visibility after that press still needs
confirmation on the desktop; the isolated registry test does not establish that Windows Settings refreshed its cache.
Version remains 0.1.0; nothing committed.

## Desktop registration visibility diagnosis (2026-10-03)

The user's screenshots disproved the earlier registration-visibility claim: SCADMaxx Launcher was absent
from the modern .scadmaxx chooser. Process Monitor showed desktop Explorer receiving NAME NOT FOUND
for HKCU/Software/Classes/.scadmaxx, while probes launched directly from the tool context found the
launcher. The trace also showed tool PowerShell registry operations in a private WC/Silo registry view.
A read-only probe launched through the existing Explorer window's Document.Application.ShellExecute
reproduced the missing launcher; directly invoking a newly created Shell.Application did not.
Same user SID and GetPackageFullName returning APPMODEL_ERROR_NO_PACKAGE were insufficient checks.

Stopped only the refined launcher and reopened it via that existing Explorer window. Confirmed the
new launcher is parented by desktop Explorer (69716), process 56076. No real registry associations were
manually changed, no new build was needed, and nothing was committed. BUILDING.md now records the
interactive launch/verification requirement. The user must press the setup button in this new instance;
visible chooser acceptance remains pending. This supersedes the earlier assumption that the user's
button press in a tool-launched instance necessarily registered handlers in the desktop registry view.
