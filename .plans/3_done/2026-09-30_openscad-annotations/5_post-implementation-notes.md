# Implementation and verification

## Result

All six phases are complete. Native drawing/review, companion persistence, editor lifecycle/undo, opt-in agent access
and the bundled Python client are implemented in wt-openscad-annotations on feature/annotations.
The full Windows x64 Release application builds and passes the focused tests and runtime checks below.
Source changes are uncommitted; no push, PR, publication or experimental PR-stack change was made by this task.

Initial delivery (see the palette correction below for the latest build):

- Application: D:/openscad/artifacts/openscad-annotations-20260930-win64-final/openscad.exe.
- ZIP: D:/openscad/artifacts/openscad-annotations-20260930-win64.zip (57,081,657 bytes).
- SHA-256: adjacent .zip.sha256.txt file.
- Guide: wt-openscad-annotations/contrib/openscad-agent-annotations/README.md, also bundled.
- Open **Window > Annotations**, preview/render a document, then select **Annotate issue**.
- Agent skill/client are bundled under openscad-agent-annotations; no global skill installation was made.

## Build inputs and reproduction

- Baseline: 612e684c2cbbcdcb9a7a8307973f33fd910f9c17 plus this uncommitted implementation.
- Visual Studio 17 2022 x64, MSVC 19.44.35228, SDK 10.0.26100.0, CMake 4.3.2.
- Qt 6.11.1, QScintilla 2.14.1, libzip 1.11.4, CGAL 6.2, built-in Manifold 3.5.3/OpenCSG 1.8.2.
- Explicitly reused classic vcpkg binaries: D:/openscad/openscad-6991/build/vcpkg_installed/x64-windows.
- Toolchain: D:/vcpkg/scripts/buildsystems/vcpkg.cmake; manifest installation disabled.
- Flex/Bison: E:/Dropbox/bin/win_flex_bison-2.5.25/; existing Boost.Nowide include shim in
  D:/openscad/openscad-6991/build-deps/boost-nowide/include.
- Build: D:/openscad/runs/annotations-implementation/Build-Annotations.ps1; add -Configure to configure first.
  All machine-local arguments are recorded there. CMAKE_BUILD_TYPE=Release is explicit even with the multi-config
  generator, so generic library discovery chooses Release dependencies. CL='/MP6 /DQSCINTILLA_DLL'.
- Runtime staging: Stage-LocalBuild.ps1 in the same evidence folder. Existing destinations are preserved.
  Qt plugins and dependencies use the selected tree and vcpkg's app-local deployment tool.
  The workspace Deploy-Runtime.cmake verifies the resulting staged dependency closure.
- Runtime CRT DLLs use the installed VS 18 redistributable (14.51.36231), matching newer Qt dependencies.
  Resources, MCAD, license notices, client and guide are included. Static libraries/debug symbols are excluded.

This local development delivery is independent of the experimental build profile and selected PRs.
It does not establish that a fresh vcpkg installation or clean Windows VM was verified.

## Baseline repairs

The baseline exposed missing LocalAppParameter stream declarations (Settings.h), POSIX sleep in a GUI test,
Windows variable-length argv arrays, unresolved Cairo library lookup and duplicate application manifests.
Repairs are in Settings.h, TestModuleCache.cc, main_wrapper.cc and CMakeLists.txt. Cairo AUTO remains optional;
MSVC uses the pkg-config imported target for complete paths when available. Windows resources are private to the
executable; generated manifests are disabled because the resource file already embeds one.

The initial serial build was interrupted to enable parallel compilation, not because of a compiler failure.
Failure/repair logs are retained. Clipper2's generated version header has only line-ending/stat dirtiness after
CMake; its Git content diff is empty. No submodule revision was changed.

## Verification

Evidence paths below are relative to D:/openscad/runs/annotations-implementation/.

| Check | Result and evidence |
| --- | --- |
| Full Release application | Exit 0, final-build.log; includes native Qt tests |
| Storage/drawing QtTest | 10 passed, zero failed, store-tests.txt, including setup/cleanup |
| HTTP protocol QtTest | 4 passed, zero failed, transport-tests.txt, including setup/cleanup |
| Native integration | 5 passed, zero failed, final/native-tests.txt: three scenarios plus setup/cleanup |
| Display scaling | Native scenarios pass at 125%, 150%, 200% in dpi125/, dpi150/, dpi200/ |
| Standalone runtime | Native tests and bundled Python client pass without developer PATH/Qt plugin paths, standalone/ |
| CLI smoke | STL and PNG export exit 0; smoke.stl, smoke.png and smoke-*-stderr.log; PNG visually inspected |
| ZIP/runtime | ZIP CRC check, fresh extraction, matching executable hash and extracted STL export pass |
| Skill/client | Skill validator passes; discovery/help and live client POST capture/checksum verification exercised |
| Source review | git diff --check passes; source reviewed; tracked diff retained in implementation-tracked.patch |

Hidden Windows test windows do not receive normal compositor swaps. The harness drives real GL rendering with
grabFramebuffer(); production capture waits for a queued post-paint frame acknowledgment. No fake image/frame-ready
event is used. Accepted and fresh PNGs were inspected: strokes occur once in evidence, never in fresh capture;
palette widgets are excluded. The dock thumbnail is fitted.

Final integration also verifies F6 rendered capture and result attribution after an empty preview. Scaling runs
precede that final test extension; they cover drawing, camera, persistence and agent/reload behavior.
Final tests use isolated INI preferences and backup directories. Early lifecycle test development used normal
application preferences; their original values were not recorded or guessed afterward.

## Requirements trace

All requirements are implemented. Automated evidence is distinguished from code inspection; not every interaction
or environmental failure has been simulated.

| Requirements | Evidence |
| --- | --- |
| R01 | Native preview annotation and F6 capture; controller binds displayed result |
| R02 | Twelve-color/movable palette inspected; shared painter tests and PNG inspection |
| R03–R04 | Tiny click, exiting rectangle, undo/redo/navigation tests; native camera lock, Escape/right cancel |
| R05 | Native Unicode Add, Back, Cancel and empty annotation dialog tests |
| R06 | Real GL capture/shared compositor, image inspection and DPR runs |
| R07 | Resize cancellation tested; source/result/session/camera checks and close teardown reviewed |
| R08–R09 | Dock/search/order/edit/confirmation reviewed; fitted thumbnail inspected; selection neutrality tested |
| R10 | HTTP camera set/restore preserves PNG and active document; shares native setCamera path |
| R11 | Native Save/As/Copy and matching backup tests; Save All and close dirty-state integration reviewed |
| R12 | Annotation-only Save preserves source timestamp; live unsaved evidence reads verified |
| R13 | Corrupt/unsupported archive, unexpected entry, compressed expansion and conflicting writer tests |
| R14 | Store failed-write/copy tests; source-before-companion partial-failure reporting reviewed |
| R15–R16 | Timed root reload retains dirty evidence, clears history; mixed undo and read-only mode tested |
| R17 | Cross-tab dock undo/redo; owner Save/As/Copy routing and independent Customizer state reviewed |
| R18 | Hash/generation, parse failure, F6 and empty preview tested; renderer ownership map reviewed |
| R19 | Opt-in start/stop/session tests; per-window routing and discovery reviewed |
| R20–R21 | Live list/read/capture/view/restore; source/execute rejection and allowed-route review |
| R22 | External root/include/use edits trigger automatic reload; new root hash/result generation verified |
| R23 | Host/Origin/server/target, retry idempotency, malformed/oversized body tests; budgets/TTL reviewed |
| R24 | Worker reads while GUI thread blocked during drawing; busy target protocol test |
| R25 | Skill validation and real bundled Python capture in standalone runtime test |
| R26 | Full build, focused tests, scaling, standalone/CLI/extracted runtime checks |

## Limits and follow-up context

- Catch2 3 is absent from the reused dependency tree; the upstream Catch2 suite was not built/run.
  The full upstream GUI regression suite was not run; native annotation tests were selected explicitly.
- Physical mixed-monitor transitions, other GPUs, clean Windows VM, Linux and macOS remain unverified.
- Full dependency/source snapshots are outside annotation scope; metadata reports unknown dependency provenance.
  Include/use verification requires a new successful generation, not merely a root hash match.
- Source and companion saves are separately atomic; cross-file power-loss transactions are not promised.
- Exhaustive filesystem failures, maximum sustained request load and every modal UI path are not automated.
  Implemented guards, budgets and mutation paths were inspected.
- First staging hit duplicate dependency paths in CMake's scanner. Final staging first deploys with vcpkg, then
  verifies the staged tree alone. The incomplete first attempt is retained as evidence.
- New UI strings are present; new translation catalogs were not authored.

Optional rework routes: fix forward (bounded correction), replan (different implementation), restart (revisit
requirements), or supersede (replace objective). Commits/PRs and selecting annotations for the experimental stack
are separate follow-up actions.

## Bounded correction: fixed palette

The user reported viewport streaking when dragging the palette and requested a fixed palette plus an arrow cursor.
Removed the palette drag implementation and its hint. The palette stays at its initial viewport position, explicitly
uses ArrowCursor (inherited by its children), and prevents background mouse events from propagating into drawing.
Updated R02, the OpenSCAD exploration recommendation and usage guide; Blender's original behavior remains historical
reference context. This bounded fix retains the rest of the completed feature and does not require replanning.

Release rebuild passes (palette-fixed-build.log). Existing native integration suite passes: 5 passed, zero failed,
including setup/cleanup (palette-fixed/native-tests.txt). Runtime dependency closure also passes. The removed drag
handlers, fixed placement and explicit cursor/inheritance were inspected; no new mirror-of-implementation test added.

Latest application: D:/openscad/artifacts/openscad-annotations-palette-fixed-win64/openscad.exe.
Latest ZIP: D:/openscad/artifacts/openscad-annotations-palette-fixed-win64.zip, with adjacent SHA-256 file.
The previous delivery remains available; this update does not stop a running application or alter open documents.
