# Layout migration — 2026-10-02

The user authorized moving workspace controls and consistently naming both local bare repositories.
No source changes, build, dependency installation or GitHub publication are part of this migration.

## Current layout and push destinations

| Checkout | Role | Default push destination |
| --- | --- | --- |
| `D:/openscad/scadmaxx` | Build recipes, tools, prompts, docs and plans | `E:/Dropbox/bare_repos/scadmaxx.git` |
| `D:/openscad/openscad-master` | Shared source repository and upstream master checkout | `E:/Dropbox/bare_repos/openscad.git` |
| `D:/openscad/wt-*` registered source worktrees | Feature, PR and integration branches of the shared source repository | `E:/Dropbox/bare_repos/openscad.git` |

`D:/openscad` is now a plain container with an agent-instruction router. Existing applications, dependencies,
`runs`, `artifacts`, `.vscode`, and the independent `openscad-6991` clone stay in place.
`openscad-6991` retains its separate GitHub remotes; its current branch tracks the user's fork.

## Old-to-new mapping

| Old location or ref | New location or ref |
| --- | --- |
| Control checkout at `D:/openscad` | `D:/openscad/scadmaxx` |
| Source bare repository `E:/Dropbox/bare_repos/scadmaxx.git` | `E:/Dropbox/bare_repos/openscad.git` |
| Control bare repository `E:/Dropbox/bare_repos/scadmaxx-workspace.git` | `E:/Dropbox/bare_repos/scadmaxx.git` |
| `wt-openscad-experimental-20260930-profile` | `wt-scadmaxx-20260930` |
| `experimental/20260930-profile` branch | `scadmaxx-20260930` |
| `wt-openscad-experimental-20261001-scadmaxx-all-features` | `wt-scadmaxx-20261001` |
| `experimental/20261001-scadmaxx-all-features` branch | `scadmaxx-20261001` |
| Operational root `README.md` | `scadmaxx/docs/workspace.md` |

Creation dates were verified from worktree reflogs in local time. Renamed branches retain their original HEADs.
The new branch names are also retained in the private source origin; old remote names remain as recovery refs.
The old internal Git administrative worktree IDs may remain under `openscad-master/.git/worktrees`; these IDs
are not checkout directories and need not match their current names. Submodule working-directory links are repaired.

## Resuming historical work

- Preserve frozen run inputs, logs, patches, source archives, and control snapshots. Their old names are historical.
- Resolve old checkout paths and repository identities through this table. In particular, historical
  `E:/Dropbox/bare_repos/scadmaxx.git` source references now mean `openscad.git`, not the new control origin.
- The migrated integration runs have a `layout-migration.json` overlay containing current source path, branch,
  repository URL and the hash of their original `inputs.json`. Build tools verify and read this overlay without
  modifying frozen inputs. Pass current source paths and fresh build directories to the tools.
- Existing CMake build trees retain absolute old paths. Preserve them as evidence and configure a fresh build
  directory within the same run before rebuilding. Do not reuse or text-rewrite their caches and generated projects.
- Old plan notes are retained unchanged. Control paths now gain `/scadmaxx`; relative links from moved plans to
  `runs` or `artifacts` need one extra parent level. Use the unchanged absolute evidence roots when reading them.
- The product README is now `scadmaxx/README.md` and is hand-maintained. Operational updates belong in
  `docs/workspace.md`, the workflows and the source registry, not automatic README regeneration.

Migration evidence, pre-move states and verification are retained in `D:/openscad/runs/20261002-layout-migration`.
