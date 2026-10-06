# Feature build titles

Before selecting or configuring a feature build, follow [the ancestry preflight](../docs/feature-ancestry.md).
Report missing owner revisions and local/accepted differences. Build/test only when requested.

Apply the shared [SCADMaxx icon patch](scadmaxx-branding.md) as well as the title patch below.

For standalone feature builds, apply the shared patch before configuring/building:

```powershell
pwsh -NoProfile -File D:/openscad/scadmaxx/experimental/scripts/Apply-FeatureBuildTitle.ps1 -Source D:/openscad/wt-openscad-live-clipping-sections
```

Then use that feature's existing configuration/deployment recipe and shared dependencies. Build the application with
`experimental/scripts/Build-FeatureApplication.ps1 -BuildDirectory <existing-feature-build-directory>`.
It completes Qt code generation in a separate build invocation before compiling the application. This prevents
stale indirect consumers of generated UI headers from retaining an old class layout after a branch update.
The startup crash and debugger evidence are recorded in `runs/20261006-sections-startup-crash`.
The title patch script is idempotent;
use -CheckOnly to check applicability without editing. It preserves unrelated changes and stops on conflicts.
If upstream moves these hooks, update and verify the central patch; do not make different per-branch implementations.

The canonical implementation is experimental/patches/feature-build-title.patch.
It changes Qt's application display name to OpenSCAD [<branch>], leaving filename/dirty-marker handling intact.
The actual application name, settings keys, executable name and document-loading behavior are unchanged.
Branch and worktree names are distinct: feature/live-clipping-sections is the branch; the folder is
wt-openscad-live-clipping-sections. Detached checkouts display <worktree-folder> (detached).

Identity is embedded during CMake configuration, never read from Git at application runtime. The checkout's
Git HEAD is a configure dependency, including linked worktrees, so switching branches regenerates the label.
A copied executable retains the identity it was built with. Rebuilding is required to label existing executables.

SCADMAXX_FEATURE_TITLE defaults ON in patched checkouts. Set -DSCADMAXX_FEATURE_TITLE=OFF for an integrated
release or source-archive build if this patch is present there. Do not silently apply feature labels to releases.
Keep this common workspace patch distinct from upstream-facing feature changes. There is no need to merge
other feature branches to use it. Do not change launcher's collection/settings as part of applying the patch.

Validation and the Sections demonstration build are recorded in runs/20261006-feature-build-title
under the workspace container. The patch was checked against all 16 feature-owner worktrees; only the Sections
checkout was changed during initial validation. Apply it to other checkouts when building them.
