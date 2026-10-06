# SCADMaxx application icon

Use the shared purple icon for every SCADMaxx build, including feature worktrees and integrated releases.
The source artwork and platform assets are in assets/icons; the canonical binary patch is
experimental/patches/scadmaxx-icon.patch. Do not create separate recolorings per branch.

Before the next authorized build, apply:

```powershell
pwsh -NoProfile -File D:/openscad/scadmaxx/experimental/scripts/Apply-ScadmaxxIcon.ps1 -Source D:/openscad/<source-worktree>
```

This command only applies source assets; it does not configure, compile, run the application or run tests.
It skips an already-applied patch and stops on conflicting assets. Retain unrelated local changes.
For integrated builds, apply after composing the selected stack and before the final source checkpoint,
then record the patch hash and include its changes in a distinct branding commit under build authorization.
Keep this common branding delta separate from upstream-facing feature code. No extra PR-stack feature is needed.

The patch replaces existing resource files, so current Qt, Windows resource, Linux install and macOS icon
references consume the same branding without per-branch code changes. Both standard and snapshot/nightly icons
are purple. It changes application icons, not the launcher S icon or the separate document-file icon.
Existing executable files and pinned shortcut caches do not change until rebuilt/refreshed.

Artwork: recolored from OpenSCAD resources/icons/openscad.png using the built-in image generator.
Palette reference: launcher.ico background #5143BA (RGB 81,67,186), with light/shadow variations.
Prompt: preserve the existing geometry, composition, perspective and shading; recolor the yellow/orange/green
palette to purple based on #5143BA; no text, outline or new objects; transparent background.
The approved master is scadmaxx-master.png. Export-ScadmaxxIcon.ps1 converts it into PNG sizes, multi-size ICO
and PNG-backed ICNS; it does not regenerate artwork. resource-map.json records destination mappings.
Derived artwork retains the upstream icon's licensing context; preserve upstream COPYING and notices.

No application build or tests were run when introducing this patch. Windows/resource integration and macOS/Linux
appearance remain unverified until explicitly requested. Applying or editing assets never authorizes a build/test.
