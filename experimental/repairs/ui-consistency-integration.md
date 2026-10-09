# Coordinated UI integration, 2026-10-10

Maintain reusable edits on `codex/ui-visual-polish` and `feature/shortcut-presets`, not in the integration.
PR #6878 keeps its stack identity but now selects the maintained preset variant. Merge it normally
into UI polish, Vim, cross sections and insertion. UI depends on both #6776 and #6878.

Integration conflicts with #6878 were limited to independent include additions and the resource list.
Keep both includes; preserve UI's removal of old bitmap Preferences artwork and map the shortcut
category to `stock/keyboard.svg`. Do not restore the legacy PNG for that category.

`Dock::setTitleBarVisibility(true)` must restore its shared `SurfaceWidgets::DockTitle`, not nullptr:
nullptr restores the native Qt title and silently erases the approved palette hierarchy after startup.
Owner repair `08b0f6e42` includes a regression using the actual Dock class. The generic installer also
covers feature QDockWidgets created after setupUi, guarded against early deletion. Hidden titles remain
empty widgets. Do not remove the existing dock reorder/visibility behavior.

Typography checks now expect framed Advanced/Dialogs groups. Preferences page organization places
optional Inspector and Vim settings into groups at runtime, avoiding reverse feature dependencies.
The scheme list scales with font metrics, rather than a fixed pixel limit.

Run Qt autogen as a separate build invocation before the main build, including full integration.
The control Build-Windows.ps1 now follows Build-FeatureApplication.ps1 here. Changes to Dock.h or
generated MainWindow UI cause legitimate recompilation of indirect consumers; preserve that rebuild.

For standalone Windows deployment, configure `CMAKE_INSTALL_SYSTEM_RUNTIME_DESTINATION=.` so MSVC
DLLs sit beside scadmaxx.exe. Copying them out of bin while retaining identical DLLs in bin causes
CMake runtime-dependency scanning to report conflicting paths. Do not weaken dependency checks.

Keep concurrent dirty control/skill research outside a release: stage/package from a clean checkout
of the committed controls, with frozen stack/source manifests. This run used a detached controls
composition. Source/build/package evidence: `D:/openscad/runs/scadmaxx-all-features-2026-10-09_22-34`.
The initial 29c325d package is superseded by the forward-merged title repair eeccd2a7.
One timeout-harness cleanup race passed all 19 tests on retry. The quick performance run was interrupted
by an unrelated MSVC linker; that is incomplete timing evidence, not a performance pass.
