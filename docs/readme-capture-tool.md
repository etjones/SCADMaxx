# Native README captures

For screenshots from an **already shipped executable**, start with
[the release capture recipe](readme-release-captures.md). The harness below requires a separate
test-enabled binary and is not the default path for capturing the shipped release.

The reusable capture harness is retained on source branch `codex/readme-captures`.
Its former checkout `D:/openscad/wt-openscad-readme-captures` was retired on 2026-10-08.
Its starting point is the integrated SCADMaxx
revision `bcf48145d9ebc7ffdcde0414ddde38ceb62f0b6a`. It shares the source repository in
`openscad-master`; its default push destination is the private OpenSCAD origin.
The runner, model and shot recipe belong to this SCADMaxx control repository.

The harness calls real Qt widgets and sends native application events. It uses the actual
annotation drawing tool, comment dialog, navigation popup, connection dialog and Preferences.
Separate top-level popup/dialog pixels are included at their real positions in the application
capture because `QWidget::grab()` alone omits those windows. No mock UI is drawn.

## Run

The capture and baseline checkouts are created on demand. For historical replay, first verify the target
path is absent and the branch is not checked out elsewhere with `git worktree list`, then recreate the
required checkout from the retained branch:

```powershell
git -C D:/openscad/openscad-master worktree add D:/openscad/wt-openscad-readme-captures codex/readme-captures
git -C D:/openscad/wt-openscad-readme-captures submodule update --init --recursive
```

For the matching old-UI baseline, substitute `wt-openscad-readme-baseline` and `codex/readme-baseline`.
The [retirement record](../../runs/20261008-worktree-retirement/report.md) retains ignored files and
submodule working state if exact historical reconstruction is needed. The runner defaults to the former
capture path and reports a missing checkout before initializing build tools. For current-release screenshots,
use the release recipe above; for a new test-enabled harness build, follow the reuse section below.
Creating a checkout does not authorize a build or desktop capture.

From `D:/openscad/scadmaxx`, using the existing local Windows build profile:

```powershell
./experimental/scripts/Capture-Readme.ps1 -Step Configure
./experimental/scripts/Capture-Readme.ps1 -Step Build
./experimental/scripts/Capture-Readme.ps1 -Step Capture
```

Configure and Build are needed initially and after source changes. Subsequent captures reuse
the binary. Dependencies come from the existing shared vcpkg installation; automatic dependency
installation is disabled. Build artifacts stay under `D:/openscad/runs/readme-captures/build`.

Each capture uses a fresh output directory and isolated application settings. It retains the
model, recipe, logs, image dimensions, source revision and executable/input hashes. Override
`-Source`, `-Build`, `-Output`, `-BuildProfile`, `-Model` or `-Recipe` as needed.

Edit `experimental/readme-captures.json` for the annotation comment and normalized stroke
coordinates. The demonstration model is `docs/screenshots/models/mounting-bracket.scad`.
Inspect full-size output against [the screenshot brief](readme-screenshots.md) before manually
selecting images for the README. The runner does not overwrite approved images or edit README.md.

## Reuse for future builds

Keep the harness as a small source delta over the chosen integrated build. Apply that delta to
a dedicated capture branch based on the next integration revision and rebuild there. Do not
merge an old integration wholesale into a new SCADMaxx composition just to obtain this tool.

The entry point is compiled only with `ENABLE_GUI_TESTS=ON` and activated only by
`OPENSCAD_README_OUTPUT` during `--run-all-gui-tests`. Ordinary release builds exclude it.
Captures therefore come from a test-enabled build of the recorded integrated source, not the
byte-identical shipped executable. Preserve that distinction in image provenance.

An old/new UI comparison additionally needs genuine baseline captures with the same model,
camera, dimensions and display scale. Never simulate the old UI by recoloring the new one.

The initial comparison baseline is `codex/readme-baseline` in
`D:/openscad/wt-openscad-readme-baseline`, based on `8bef263eb`: regular OpenSCAD
`03da906b4` with four Windows build repairs and no selected feature/PR integrations.
It has a minimal capture entry point and isolated settings. Use the same runner with
`-Source D:/openscad/wt-openscad-readme-baseline` and
`-Build D:/openscad/runs/readme-captures/baseline-build` for all three steps.

## Initial verification

Both native builds and capture runs completed on 2026-10-02. Inspected outputs are retained in
`D:/openscad/runs/readme-captures/integrated-final` and `baseline-final`; the selected images and their hashes
are recorded in `docs/screenshots/sources.json`. Full application images are 1280 by 820 pixels.
The integrated harness is 216 lines of C++, plus five lines of test/build wiring; the runner is 69 lines.
The baseline helper adds approximately 45 lines, including settings isolation and a portable test sleep.

On this machine, the sandboxed CMake post-build shell could not resolve `dirname`, while the identical
build passed in the normal user environment. Run Build in that environment if this recurs.
Capture also stages the source tree's shaders, color schemes, fonts and localization resources alongside
the executable. It selects the normal light icon theme explicitly for the regular OpenSCAD baseline.

The light/dark pair uses Tomorrow/Tomorrow Night viewport backgrounds selected by the harness; automatic
OS palette switching does not itself select a viewport color scheme. The annotation dock is floated and
hidden while its drawing palette remains visible, giving the model and comment dialog the available space.

The harness changes were subsequently committed: `e5991ad0a` on `codex/readme-captures` and
`f65fe98dd` on `codex/readme-baseline`. Both branches remain after checkout retirement.
