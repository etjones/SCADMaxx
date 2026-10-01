# Navigation cube — overall implementation plan

Status: six implementation phases complete; implements [2_requirements.md](2_requirements.md).
The user requested all six phases in sequence, with a commit after each phase. Product questions are resolved.

## Checkout, evidence and constraints

- Source: `D:/openscad/wt-openscad-navigation-cube`, branch `feature/navigation-cube`.
- Planning-time HEAD: `464e25dad0c01af5488375c15aa6734190531eb5`; clean source tree observed. The branch now tracks
  `origin/feature/navigation-cube`; the exploration's no-push statement describes initial setup, not current remote state.
- Reinspect worktree, submodules and checkout-local instructions before source edits. Do not reset to the recorded SHA,
  update the branch, merge other features or repurpose another checkout as an incidental implementation step.
- Proposed application build: `D:/openscad/wt-openscad-navigation-cube/build-navigation-cube` (check availability first).
  Proposed evidence root: `D:/openscad/runs/navigation-cube/`; each attempt gets a fresh subdirectory. Local staging,
  when needed for a runnable application, belongs in `D:/openscad/artifacts/navigation-cube/<attempt>/`.
- Follow [Windows profile](../../../experimental/profiles/windows-x64.md): toolchain `D:/vcpkg`, installed packages
  `D:/openscad/openscad-6991/build/vcpkg_installed`, `VCPKG_MANIFEST_MODE=OFF`, `VCPKG_MANIFEST_INSTALL=OFF`.
  Record package status hash and compiler/SDK/generator/features. Do not install or rebuild shared dependencies.
- There is no root dependency graph at planning time. These phases form one feature; no new graph or project split is
  needed. Annotation and UI-typography branches are integration context, not prerequisites to standalone implementation.

## Source evidence and integration map

| Existing area | Relevant behavior | Planned change boundary |
| --- | --- | --- |
| `src/glview/Camera.cc/.h` | Native angles, pan, distance, projection, fit/reset and script conversion | Tested adapter and camera value snapshots; preserve public SCAD mapping |
| `src/gui/QGLView.cc/.h` | Camera input, paint, notifications and framebuffer capture | Widget ownership, observation, guarded operations and clean capture |
| `src/gui/MainWindow.cc/.h/.ui` | Direct standard-view mutations, projection/actions, rendered owner | Shared operations/actions; displayed-document association |
| `src/gui/ViewportControl.cc`, `Animate.cc` | Camera consumers and possible reevaluation | Keep final notifications; avoid interpolation-driven compile storms |
| `src/gui/TabManager.cc/.h`, `Editor.h`, editor implementation | Save, Save As/copy/all, reload and dirty/close paths | Separate view-library metadata state, normal save integration |
| `MainWindow::writeBackup` | Source and Customizer backups | Companion backup/recovery integration |
| `src/gui/Preferences.*`, `QSettingsCached.*` | Persistent UI preferences | Navigation visibility/animation, popup size and normal overlay choices |
| `src/RenderStatistic.*`, `src/glview/VBOBuilder.*`, renderer classes | Backend-dependent geometry/counts | Cached typed summaries rather than parsing log output |
| `QGLView::grabFrame/save`, `MainWindow` export/copy/frame dump | Shared GUI cached framebuffer images | One clean-capture policy for all routes |
| `src/gui/ai/ViewportGrabber.cc` | Existing AI image capture calls `grabFrame` | Inherit clean images without a new agent API |
| `CMakeLists.txt`, `src/guitests`, `src/gui/*_test.cc` | Qt GUI harness and Catch2 unit target | Focused native/logic tests registered in existing systems |

`TabManager::save` always writes source today, while dirty predicates only cover source/Customizer. Implementing
metadata-only saves therefore requires explicit save intent, not setting source modified or skipping every clean save.
Save As/copy must still write destination source even when the source buffer is clean. Source-only auto-reload must
not route through companion reload. The existing annotation lifecycle design is evidence to learn from, not code to
copy wholesale or an implicit dependency.

## Proposed components

Names below are proposed new classes/files; inspect local conventions before choosing exact filenames.

1. **Camera pose and navigation controller.** A small value type stores native-compatible orientation, translation,
   distance, FOV and projection. A pure adapter converts to camera basis/rotation matrices and back. A viewport-owned
   controller applies commands, enforces an injectable navigation policy, cancels/retargets transitions and notifies
   observers. Separate visual camera updates from final user-operation notifications consumed by Animate.
2. **Cube geometry and widget.** Generate the 26 facets from a truncated cube with stable identities. Project and
   depth-sort the visible polygons; use the same geometry for painting and hit tests. A fixed Qt child widget paints
   with QPainter using native palette/fonts. Geometry and hit testing are testable without a GL context.
3. **Viewport popup and settings.** A thin-frame `Qt::Popup`-style widget with explicit resizing and keyboard handling,
   shared QActions for existing commands, radio projection controls, metric choices and saved-view list. An independent
   tiny triangle invokes it. Persistent baselines plus session overrides feed both widgets and Copy settings.
4. **Saved-view store and document controller.** Document-owned entries, dirty/save state, format validation, file
   conflict detection and lifecycle operations. The viewport binds to the displayed owner without changing active editor.
5. **Statistics snapshot and text overlay.** Result-generation-keyed count data plus monotonic frame samples. UI updates
   consume cached values; geometry workers/renderers publish typed summaries at result/preparation boundaries.
6. **Clean capture scope.** Freeze the displayed camera/result snapshot, suppress helpers through render flags, perform
   the required framebuffer render/readback, restore state on all exits, and compose applicable annotations separately.

Prefer existing Qt/Eigen/JSON facilities; no Coin3D or extra 3D framework. Keep GUI code out of headless targets. Start
with Qt child composition; if the phase-1 native probe fails, document the failure and choose the narrowest alternative
overlay implementation that still satisfies input, DPI and capture requirements before expanding the UI.

## Camera and event decisions

- Generate target directions from six axis normals, twelve normalized sums of adjacent axes and eight normalized
  signed XYZ vectors. Match front/back/top/bottom labels against the actual OpenSCAD basis, not a reference CAD basis.
  Derive upright basis from projected world Z except poles, which use the existing principal-view up direction.
- Represent interpolation internally as quaternions with shortest-path rotation. Preserve the exact specified final
  native target at completion. Interpolate saved-view pan/FOV continuously and positive distance geometrically; apply
  a changed projection once at transition start. For Center/View All/Reset, calculate their existing final camera on
  a temporary value and transition to it without changing their semantics.
- Free orbit uses a screen-space virtual trackball around the current target, with no automatic pole flip or imposed
  upright reset during a gesture. Use a logical-pixel drag threshold and sensitivity control. Snap targets restore
  standard upright orientation; orbit does not relocate the widget or zoom/pan the camera.
- During a transition, publish display updates for cube/fields and repaint only; finalize one operation notification.
  Do not broaden suppression to ordinary mouse behavior or existing model Animate updates. Guard all programmatic
  updates against signal feedback and observe script-driven camera changes after evaluation.
- On capture, stop a transition at the displayed camera and invalidate its remaining callbacks before readback. Add
  saved view snapshots the displayed value atomically; it need not finish or persist the transition destination.
- Popup dismissal consumes the dismissing pointer press/release. Inline editing owns Enter/Escape; outside dismissal
  commits a valid current name, otherwise retains the previous/generated name. Clicking the triangle closes, never
  closes-and-reopens. Resize grab is an internal interaction, not an outside click.

## Saved-view format and transactions

Use `model.scad.views.json` for the experimental companion. Version 1 stores a schema version and ordered entries with
stable UUID, Unicode name, translation vector, orientation in documented native/public units, positive distance,
bounded FOV and projection enum. Store enough precision for round trips; never persist NaN, infinity, viewport size,
render pointers, locked/viewall/autocenter flags or overlay settings. Use a bounded file/entry/name size and validate
before creating live objects. Freeze the exact schema and limits in phase 4 and test supported/unsupported versions.

Associate a store with document identity, not a filename string alone. Track loaded-file identity/hash separately from
in-memory dirty state. Use atomic file replacement and cooperative locking/check-before-write to reject conflicting
writers; no silent last-writer-wins. Do not create companions for untouched empty libraries. Persist empty state after
deleting the last entry or when an explicitly accepted overwrite must replace an old destination library.

Distinguish save-to-current, save-as and copy intents. Preflight companion conflicts before source writes when possible.
On source success/companion failure, report the actual source path, preserve metadata and dirty state, and retain enough
destination information for retry. Save As rebinding must match what actually committed; Save a Copy never rebinds or
clears original dirty state. Never report whole-document success just because source was saved. Backups capture metadata
without marking it saved. Source reload preserves it; only explicit document discard/reload of companion drops edits.

No undo-stack integration beyond existing text/Customizer behavior is added by this feature. Remove directly deletes
the selected library entry in memory; do not route it into text undo or add a new confirmation/history interface.
The ordinary save/discard lifecycle handles unsaved library changes.

## Settings and developer access

Normal Preferences owns persisted navigation visibility and animation on/off/duration; existing display choices retain
their established keys, and popup size uses a feature-specific key. Each window reads defaults and keeps checked states
in sync through existing preference/action plumbing. Session overrides never write those keys. Clearly separate baseline,
override and effective values so Copy settings is truthful and editing a persisted preference has a visible result.

Compile the tuning window behind a dedicated development option (proposed `ENABLE_NAVIGATION_CUBE_TUNING`) and expose
it through a View-menu entry only in that build. This local iteration enables it; ordinary production builds omit it.
Keep the popup's end-user layout free of tuning controls. Reset clears session overrides; Copy settings emits a stable
plain-text parameter list with units, effective/baseline values and viewport/DPI context. Positions are right/top insets
in logical pixels; report both requested offsets and actual clamped geometry.

## Statistics and capture policy

Preview triangles count tessellated model instances prepared for display, once per instance, excluding navigation,
helpers and repeated renderer passes. Final triangles count the final model's available triangulated representation.
Associate counts with result generation and rendering mode; preserve old-result identity on failed evaluation and
label it stale. Use an unavailable label for unsupported geometry rather than converting facets or forcing F6.

Measure intervals between completed viewport paints while it is actively updating, with rolling averaging; frame time
is the same completed-frame interval in milliseconds, not GPU execution time. Exclude special capture repaint samples,
do not synthesize frames for the overlay, and switch to Idle after an inactivity interval. Throttle text refresh and
stop timers when hidden. Exact averaging/idle/refresh values are dev-tunable calibration choices.

All GUI image routes share a clean model render policy. A child-widget-only exclusion is insufficient because world
axes and guides are drawn in GL. Suppress them for readback without committing preferences or changing ordinary display.
Retain model edge shading and scene background; annotated evidence is composed by its own annotation path exactly once.
In the standalone branch, test an injected annotation compositor/policy contract; real annotation compatibility needs
a later isolated composition using an explicit available annotation revision. Never merge that branch into this source
checkout merely to test. Record unavailable combined evidence as a limitation, not a standalone pass.

## Ordered phases and coverage

| Phase | Deliverable | Depends on | Primary requirements |
| --- | --- | --- | --- |
| [1 — Foundation](4_imp-phase1.md) | Native composition/lifecycle probes, tested camera adapter and operation boundary | Existing base | R01, R04, R09, R14, R27 |
| [2 — Cube and motion](4_imp-phase2.md) | 26-target widget, arrows, free orbit and interruptible transitions | 1 | R02–R08, R24–R26 |
| [3 — Popup and tuning](4_imp-phase3.md) | Resizable popup, shared actions, preferences and clipboard tuning | 2 | R10–R11, R17–R19, R21, R25 |
| [4 — Saved views](4_imp-phase4.md) | List, full camera recall and complete document companion lifecycle | 1–3 | R12–R16, R24 |
| [5 — Statistics and captures](4_imp-phase5.md) | Typed metrics, clean readback and annotation policy hooks | 1–4 | R20–R23, R26 |
| [6 — Integration and calibration](4_imp-phase6.md) | Complete acceptance evidence and runnable local tuning build | 1–5 | R01–R28 |

Each phase keeps the application usable, registers relevant tests and records evidence before moving on. Build repairs
and feature changes remain separate review units. Do not claim disabled placeholders as completed functionality.

## Validation and completion

Use Catch2 for camera math/store/value logic and the existing Qt GUI harness for real widgets and lifecycle. CMake
supports `ENABLE_TESTS`, `ENABLE_GUI_TESTS` and `OpenSCADUnitTests`; verify how new tests are discovered before placing
them. A file in `src/glview` is not automatically covered by the existing unit-test glob. Test actual native rendering
for transparent child widgets, popup events and clean captures; synthetic math or mocks alone cannot prove those.

Keep profiles, companions and backups isolated from the user's working settings. The Windows GUI Release build uses
the shared dependencies and a dedicated compatible build directory. Record exact commands when they are run; this
plan is not evidence of a successful configure/build/test. The fresh source base can require known MSVC repairs;
inspect the workspace repair catalog and keep only demonstrated necessary repairs.

Final evidence includes requirement coverage, unit/native test results, visual DPI/theme matrix, clean image samples,
performance/event observations, source/dependency fingerprints, calibration text copied from the app, and a runnable
local path. Update `5_post-implementation-notes.md` when work is executed. A ZIP, public release, PR, upstream push or
experimental-stack inclusion remains a separate request. If combined annotation/runtime/platform checks cannot be
performed, state the exact limitation and do not mark those checks complete.
