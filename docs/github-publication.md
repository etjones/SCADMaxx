# GitHub publication status

Publication on 2026-10-09 was explicitly authorized by the user.

| History | Dropbox origin | GitHub `publish` destination | Visibility |
| --- | --- | --- | --- |
| SCADMaxx controls | `E:/Dropbox/bare_repos/scadmaxx.git` | https://github.com/roel-v/SCADMaxx | Private |
| OpenSCAD application source | `E:/Dropbox/bare_repos/openscad.git` | https://github.com/roel-v/openscad | Public |

Both working repositories retain Dropbox as their default push destination. GitHub pushes use the
explicit `publish` remote; there is no automatic synchronization. Git Credential Manager authentication
must select the `roel-v` account when multiple saved accounts exist.

The 18 native source branches selected in `experimental/SOURCES.json` and the current integration
`scadmaxx-20261006` were pushed to both source destinations. Every remote revision was checked against
the frozen publication manifest in [github-publication.json](github-publication.json). The integration
checkpoint is `f4f87a8eea11172037c459dd5ae9848b566fd044`; its history includes the selected upstream PR
revisions and integration repairs. Straight master was not updated by this publication.

The controls' `main` branch and selected `feature/agent-skill-workflows` companion are published to the
private controls repository. Publication copies committed history; it does not include uncommitted
worktree changes, build directories or delivery ZIPs. Unrelated experiments, verification/recovery refs
and historical integrations were not published as branch refs.

Local build selection still uses Dropbox paths. GitHub publication does not silently replace their
authority. For a remote rebuild, clone the controls repository with access to the private repository,
and resolve the source refs in the manifest from `https://github.com/roel-v/openscad.git` instead of the
local Dropbox path. The current integrated source branch can also be cloned directly. Follow the
recorded Windows dependency and build instructions; local machine paths require configuration.
Publishing commits does not establish clean-machine build acceptance or complete pending validation.

`SOURCES.json` records the pushed revisions in `promotedHead`. Existing validation/readiness flags remain
unchanged: publication is not a validation pass. Evidence for the publication and original commits is in
`D:/openscad/runs/scadmaxx-publication-2026-10-09`.

The controls repository can be made public later by changing its GitHub visibility. The application
feature history is already public in the OpenSCAD fork. No GitHub releases, workflow runs, builds or tests
were requested as part of publication.

## Coordinated UI update, 2026-10-10

The user explicitly authorized necessary pushes for this implementation/build. UI polish, the maintained
shortcut-preset variant, Vim, cross sections, insertion and integration `scadmaxx-20261006` were pushed
to both source remotes and verified by exact SHA. Current integration is `659f5abf0e8959bc03c62155b436b1b6b44a8aca`.
The source manifest records these updates; temporary standalone build compositions remain local.
Source publication does not publish ZIPs or turn incomplete performance/desktop coverage into passes.
Evidence: `D:/openscad/runs/scadmaxx-all-features-2026-10-09_22-34/publication.json`.
