# Navigation cube — implementation evidence

Status: all six source phases committed; local delivery verified. See final handoff and coverage below.

Latest correction: [arrow scaling](rework/03/0_restart.md), commit `8fbde4053f6d721e6fd745690bb26a7fde054d70`.
Latest application: `D:/openscad/artifacts/openscad-navigation-cube-arrow-scaling-win64/openscad.exe`.
It retains the dockable tuning panel and both prior click corrections.

Latest UI refinement: **Window > Navigation tuning** is now a standard dock, initially floating and hidden.
It participates in the Window menu, dock keyboard navigation and saved window layout. Experimental values remain
session-only. Commit `6e8e2f37fc7f988b228a9c907556bfaf591a0fc6` (menu move first committed as `cea9a66ae`).
Latest application: `D:/openscad/artifacts/openscad-navigation-cube-dockable-tuning-win64/openscad.exe`.
Native tests cover menu ownership, docking/floating, close/reopen and Copy settings; all 15 cases pass in
`runs/navigation-cube/phase6/dockable-tuning`. The normal Reorder windows setting governs dock title-bar handles.

Latest correction: [unchanged reload polling](rework/02/0_restart.md), source `0947b9e3a840209153d0ad791df27f38ec86858c`.
Latest runnable build: `D:/openscad/artifacts/openscad-navigation-cube-reload-fix-win64/openscad.exe`.
Cycle 01 alone did not resolve the user's report; the earlier test matrix disabled automatic reload and missed
its unconditional cancellation every 200 ms. The new regression runs transitions through unchanged reload polls.

Follow-up: [click-jitter correction](rework/01/0_restart.md), source `0ff82ec81d46e06c1e15047233c3b2e488d4cc92`.
Latest runnable build: `D:/openscad/artifacts/openscad-navigation-cube-click-fix-win64/openscad.exe`.
The original phase evidence and provisional defaults below are retained as history; the drag threshold now uses
the platform default (10 logical pixels on this Windows profile).

## Final handoff (2026-10-01)

Runnable standalone application:
`D:/openscad/artifacts/openscad-navigation-cube-20261001-win64/openscad.exe`.
Use **View > Navigation tuning…**, then **Copy settings** to report a complete experiment.
The adjacent `README-navigation.txt` explains controls and companion-file ownership.
This is a local development delivery, without the annotation implementation or a public release.

Source head: `c54886b822ed39ff91369c335472788f106e2c50`, branch `feature/navigation-cube`.
Verified private origin ref has that exact SHA: `E:/Dropbox/bare_repos/scadmaxx.git`.
The workspace's feature-completion handoff now requires this private retention; no GitHub push or PR was made.
The intended feature delta starts after baseline repairs at `67884e65f4565c1215a88ecdcd0a2daa122e53d7`.
Those five prerequisite Windows repairs remain separate commits, based on `464e25dad0c01af5488375c15aa6734190531eb5`.
Submodule revisions match the source gitlinks; dependency package-status hash and submodule identities are recorded
in `runs/navigation-cube/phase6/dependencies.txt` and `submodules.txt`. No shared packages were installed or changed.

| Phase | Source commit | Result |
| --- | --- | --- |
| 1 | `3a60e69bb` | Camera operations and native probes |
| 2 | `ea9427744` | Cube targets, orbit and interruptible transitions |
| 3 | `c27b926c8` | Popup, preferences and dev tuning |
| 4 | `a22a2c516` | Document camera views and save/recovery integration |
| 5 | `50acb34f5` | Typed statistics and clean image capture |
| 6 | `c54886b82` | Native integration validation and final corrections |

## Final verification and evidence

All evidence paths below are relative to `D:/openscad/runs/navigation-cube/phase6/`.
Build scripts, dated logs, exact source/dependency identities and runtime deployment log remain there.

- `unit-tests.xml`: 123 Catch2 cases pass (the JUnit aggregate also includes generated assertions/sections).
- `production-final/test-results.xml`: 15 native cases pass with tuning excluded from the build.
- `dev-final`, `final125`, `final200`, `final-dark`: 15 native cases pass in each configuration.
  Earlier `complete150` covers simulated 150%; `staged150` covers that scale again.
- `restart-write.xml` and `restart/test-results.xml`: separate processes verify normal preference persistence
  and reset of experimental overrides.
- `staged-final/test-results.xml`: the packaged application passes 15 native cases with system-only PATH and its own
  Qt plugins. `staged-smoke.stl` and `staged-smoke.png` verify CLI geometry/image export from that package.
- `staged-executable-sha256.txt` and adjacent application `build-info.json` identify the delivered executable.
- `dev-final/copied-settings.txt`: actual clipboard description, including values, units, baselines, overrides,
  resolved widget geometry and display scale. `tuning-window.png` shows the live controls.
- Native popup, saved-list, large-font, small-window, all-target, dark-viewport and clean-capture images were inspected.
  The popup has no title bar/close button. Arrow/triangle contrast now follows the viewport background.
- `combined/final-phase6`: real annotation workflow verification using isolated composition `d16b00019`, which merges
  final navigation with annotation revision `d670fad09`. Draft locks block navigation; permitted movement invalidates
  redo; accepted annotation capture equals one direct composition of the intended stroke. The annotation code is
  deliberately absent from the standalone feature branch. Composition adapters are retained in that separate branch.

Final corrections include preserving list-item identity across inline editing, retaining blank/cancelled names,
keeping QActionGroup projection bookkeeping intact, reflecting shared-action availability, and explicitly labeling
2D and failed evaluation statistics. The actual animation dump caller is exercised and its PNG pixels compared
with the clean framebuffer, alongside clipboard, PNG save and AI capture.

Switching the same CMake build directory from tuning OFF back to ON left a stale AUTOMOC aggregation once.
Rerunning `cmake -E cmake_autogen <build>/CMakeFiles/OpenSCADLibInternal_autogen.dir/AutogenInfo.json Release`
regenerated it; the rebuilt dev and staged tests passed. This was build-cache recovery, not a dependency change.
The separate fresh combined build similarly needed a retry after a missing generated parser header.

## Requirement coverage

| Requirements | Status and evidence |
| --- | --- |
| R01, R27, R28 | Pass on Windows Qt6: independent source, separate repairs, shared dependencies, staged launch/CLI tests; platform limits below |
| R02, R03, R05 | Pass: pure geometry tests and native all-26-target checks/contact sheet, anchoring/resize, four simulated DPI scales |
| R04, R09 | Pass: camera adapter, script/external mutation observation, distinct display/final notifications, no per-frame compile loop |
| R06, R07, R08 | Pass: roll/orbit steps, free-orbit toggle, drag/release, exact endpoints, retarget/cancel and capture interruption |
| R10, R11, R21 | Pass: popup resizing/focus/dismissal, projection radios, shared camera/display actions and state synchronization |
| R12, R13 | Pass: inline default/blank/cancel/focus-loss edits, stable IDs, full-camera round trip and recall |
| R14, R24 | Pass: active versus displayed owner, empty/failed results, source reload, document/window lifetime and close Cancel/Discard |
| R15, R16 | Pass: transaction/lifecycle tests for Save/All/As/Copy, metadata-only save, conflicts, corrupt/oversized data and backup recovery |
| R17 | Pass: isolated process restart and shared normal settings; saved views remain document-owned |
| R18, R19 | Pass: live tuning, complete copied description, reset/session-only overrides, production exclusion |
| R20 | Pass: preview/final counts, 2D/empty/stale/failed/unavailable labels and measured frame interval semantics |
| R22 | Pass: actual clipboard, PNG, animation-dump and AI pixels; state restoration and single annotation composition |
| R23 | Pass in separately identified annotation composition; standalone permission-policy tests also pass |
| R25 | Partial platform matrix: native keyboard/focus/resize, light controls, dark viewport, large font and simulated DPI pass; limits below |
| R26 | Pass for measured native fixtures: bounded samples, cached mesh summaries and no continuous idle repaint loop; no universal FPS claim |

## Provisional defaults and limitations

Scale 0.75; cube right/top offsets 10/26 logical pixels; triangle right/top 8/5. Base widget 140×184 scales to 105×138.
Idle opacity 0.45, hover 1.0, enter delay 0 ms, leave delay 180 ms, fade-in/out 120/250 ms.
Camera duration 200 ms, InOutCubic easing; roll 90°, arrows 15°; free orbit enabled, drag threshold 4 logical pixels.
Popup initial size 300×480, resizable and remembered. Information initially off; triangles/FPS selected, interval off.
These remain deliberately adjustable for the user's visual calibration.

Physical mixed-monitor movement, Windows dark native controls, translated new labels, other operating systems,
Qt5 and a separate HEADLESS build are unverified. Dark tests change the viewport scheme, not the OS theme.
The CMake GUI/headless guards were inspected; runtime compatibility outside this Windows Qt6 profile is not claimed.
Native inline-editor tests log a Qt commitData warning during editor teardown, while all edited-name and close-state
assertions pass. Retain it as a follow-up diagnostic if a user can reproduce an editing symptom.
CGAL Nef triangle counts intentionally report unavailable; preview counts are submitted geometry, not Boolean output.
The isolated composition is not the entire experimental PR stack; later integration still needs its own locked run.

## Source and build

Dedicated checkout: `D:/openscad/wt-openscad-navigation-cube`, `feature/navigation-cube`.
Starting HEAD: `464e25dad0c01af5488375c15aa6734190531eb5`; clean before Serena's local project metadata.
Matching initialized submodules were checked. No running application uses this checkout.
All feature phases will be committed individually at the user's request. No remote publication is requested.

Four recorded MSVC repairs were still applicable by source inspection and applied with attribution:

- `2dd7192f4`: stream declarations, original `c577f934`.
- `aa03f8d98`: Windows argument vectors, original `e1a79825`.
- `7dde81712`: Cairo imported target, original `b5ef9f6c`.
- `b6cc333bb`: duplicate manifest fix, original `74168dda`.

Configure succeeded with shared dependencies, MSVC 19.51, Qt 6.11.1, Catch2 and GUI tests enabled.
Baseline build passed; all 119 baseline unit cases passed. Evidence/scripts: `D:/openscad/runs/navigation-cube/phase1/`.
Application build: `D:/openscad/wt-openscad-navigation-cube/build-navigation-cube`.
The experimental composition builder requires a locked PR stack; this standalone feature uses the same profile
through its isolated recorded build script instead. No packages were installed or changed.
The shared gettext executable needed its existing directory added to PATH. GUI tests additionally required a
portable sleep repair (`67884e65f4565c1215a88ecdcd0a2daa122e53d7`), independently committed before feature work.

## Phase 1 integration findings

The renderer applies native Rx * Ry * Rz, then looks along +Y with +Z up. Front is -Y; left is -X;
top is +Z. The adapter uses native Euler values externally and matrices internally, excluding execution flags.
`cameraChanged` feeds Animate and can evaluate source; a distinct display notification is required for interpolation.
Paint-time observation catches direct script/menu/field mutations without triggering evaluation.

TabManager's current save overload always writes source and rebinds filepath. Save As must retain that behavior;
metadata-only ordinary Save needs a separate intent. Source refresh reads only text, so library loading must attach
to initial document ownership rather than refresh. The viewport's rendered editor differs from the active tab.
MainWindow currently assigns renderedEditor before evaluation and again after render; ownership must follow actual
retained results, including empty success, rather than blindly mirroring every assignment.

## Verification

The feature build and all 121 unit cases passed. Native camera-operation, metadata-lifetime and composition probes
passed at 100% and simulated 150% scaling, plus a dark viewport scheme. Screenshots were inspected. Evidence directories:
`phase1/native-3`, `phase1/native-scale150`, `phase1/native-dark`, with JUnit reports and PNGs.
The first composition probe failed because the hidden Windows launcher suppressed initial window exposure;
the harness now explicitly exposes its test window. This was a test setup correction, not an offscreen substitute.
Native test results use explicit JUnit files because the Windows GUI executable does not retain QTest console output.
The native probes establish composition and the metadata lifetime approach; full saved-view transactions, failure/empty
ownership scenarios, physical mixed-monitor DPI, OS dark controls and final visual calibration are tested in their
later phases. The dark probe changes the model viewport scheme, not the Windows desktop theme. No performance claim
or combined annotation-runtime pass is inferred from these probes.

## Phase 2

Implemented a shared 26-facet chamfered cube geometry for painting/hit testing, face-plane labels, axis letters,
single-click directional/roll actions, keyboard access and virtual-trackball drag. Only front-facing polygons hit.
Quaternion transitions use generation cancellation, exact endpoints and one final operation notification;
pan/FOV interpolate linearly, positive distance geometrically, projection switches once at the start.
Settings are session values until phase 3 adds baselines/overrides and their UI. The triangle is intentionally only
an entry-point placeholder at this checkpoint; the actual popup is phase 3.

Build and 123 unit cases pass. Native tests pass for all 26 target poses, preserved camera fields, four-roll cycle,
enabled/disabled orbit, release outside, unchanged widget placement, exact transition endpoints, retargeting,
cancellation and external camera mutation. Geometry tests verify planar facets, hidden-face culling, center hits,
and true isometric axis lengths. Evidence: `runs/navigation-cube/phase2/complete`, `native-final`, `scale150`, `dark`.
The 26-target contact sheet and native screenshots were inspected. Final default-size/font/opacity calibration,
expanded accessibility and physical mixed-monitor checks remain in phase 6, as planned.

## Phase 3

Implemented popup, persistent normal settings, session-only overrides and dev-only tuning. Clipboard includes all
effective values, units, baselines, overrides, resolved geometry and DPR. Native tests and 123 unit cases pass.
Production configuration omits tuning sources/menu. Corrected saved-list size hints keep buttons visible.
Final process-restart and broader visual calibration remain phase 6. Evidence: runs/navigation-cube/phase3.


## Phase 4

Per-document model.scad.views.json stores UUID, name, full camera pose and document provenance, version 1.
Bounds: 4 MiB, 1000 entries, 256 UTF-16 name units. Add/Remove/Rename remain memory-only until document Save.
Normal metadata-only Save avoids SCAD rewrite; Copy preserves original dirty state. Source refresh preserves views.
Companion locks and SHA-256 fingerprints reject competing writes; recovery uses a new Save As destination.
Existing backup source files receive matching view snapshots and can be reopened without touching the original.
Build/native transaction and lifecycle tests pass; screenshot inspected. Evidence: runs/navigation-cube/phase4/complete.


## Phase 5

Implemented cached typed preview/final triangle data, bounded viewport cadence sampling and single-shot idle expiry.
Preview counts each CSG leaf instance once across all products/highlights/backgrounds. Counts follow VBOBuilder's
triangle/quad/center-fan tessellation. PolySet final rendering is supported; CGAL Nef reports unavailable.
Capture cancels camera transitions, renders without guides, excludes widget overlays, preserves edges and restores
state via scope guard. Optional annotation composition runs once; ModelOnly bypasses it. Existing PNG, clipboard,
animation and AI routes all call this shared boundary. Native pixel comparisons, idle check and exception restore
pass; clean/full-window images inspected. 123 unit cases pass. Evidence: runs/navigation-cube/phase5/complete.
