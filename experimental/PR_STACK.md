# SCADMaxx integration stack

This is the manually maintained agent input for experimental builds. Select PRs, local features, or improved PR
branches and their order here. Keep this filename as the stable entry point.
Agents must not enable, remove, reorder, or silently substitute entries based on available local worktrees.
Use the [input contract](integration-inputs.md) to interpret sources, revisions, delta bases, and dependencies.
Named repositories/refs for local features and PR variants belong in [SOURCES.json](SOURCES.json). Defining a source
there does not select it; only an enabled row does.

## Build policy

- Upstream: `https://github.com/openscad/openscad.git`, branch `master`.
- Local source origin: `E:/Dropbox/bare_repos/scadmaxx.git`.
- Optional future feature publication: `https://github.com/roel-v/openscad.git` (remote `publish`).
- Keep all SCADMaxx compositions and workspace controls local; publish a feature only by explicit user choice.
- Initial target: Windows x64 GUI, Release configuration, portable ZIP.
- Fetch current upstream master once at run start and lock its exact SHA for the entire run.
- Resolve every enabled source and delta base before integration and lock their exact SHAs for that run.
- Apply enabled rows in their written order; commit each integration, then build and commit any required repairs.
- Never carry a previous run's entire composition forward as the new baseline.
- Keep successful ZIPs in `artifacts/<run-id>/`. External publication destination is not configured.
- Schedule: on demand. No recurring job is configured.

## Enabled stack (ordered)

| Order | ID | Kind | Source | Revision | Delta base | Depends on | Reason for inclusion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | pr-6878 | pr | https://github.com/openscad/openscad/pull/6878 | latest | auto-merge-base | none declared | Customize keyboard shortcuts through the GUI |
| 2 | pr-6776 | pr | https://github.com/openscad/openscad/pull/6776 | latest | auto-merge-base | none declared | Correct switching to and from dark mode while OpenSCAD is running |
| 3 | navigation-cube | feature | navigation-cube-local | latest | auto-merge-base | none declared | Native viewport navigation cube |
| 4 | ui-visual-polish | feature | ui-visual-polish-local | latest | auto-merge-base | none declared | Improved OpenSCAD UI from our UI work branch |
| 5 | annotations | feature | annotations-local | latest | auto-merge-base | none declared | Native Blender-style annotation tool |
| 6 | http-agent-server | feature | http-agent-server-local | latest | 85829fa71870c4aa6945d3cd4abbc932faeab392 | navigation-cube, annotations | HTTP endpoint / agent server for OpenSCAD automation |

Selected by the user on 2026-09-30. Both PRs were open and unmerged when checked against GitHub on that date.
PR #6878 is the updated version of the older Shortcuts GUI PR #3338. Resolve fresh heads and validate dependencies
at run start; this selection does not pin today's commits or include uncommitted local fixes.

The three local features were selected by the user on 2026-10-01. They are required members of the intended
SCADMaxx build, but are currently **pending committed feature revisions**: navigation is at its starting commit;
UI work is staged but uncommitted; annotations have uncommitted files and a dirty submodule. Their source definitions
set `ready: false`, so run preparation stops before fetching or creating a build. Do not silently omit them or
integrate their unchanged starting commits as if the features were present. Their development tasks must commit
usable feature revisions, push them to the local origin, then set `ready: true` after reviewing change boundaries
and dependencies. Build runs must not commit another task's unfinished work.

The UI branch currently incorporates PR #6776 as its foundation. Before marking it ready, identify the committed
foundation and declare/review the UI-only delta after the separately selected dark-mode PR. Do not integrate the
same PR twice or silently switch the selected upstream PR to a local variant.

## HTTP agent-server feature handoff

- Dedicated `codex/http-agent-server` head `498c4774d26e7235fbc4cbb9b34f56afb39ca645` is committed and verified in the declared private origin.
  See [completed implementation and evidence](../.plans/3_done/2026-10-01_http-agent-server/5_post-implementation-notes.md).
- Apply its explicit HTTP-only delta after the selected navigation and annotations entries. The base is the
  retained dependency-only composition, an ancestor of the source head; compare newer selected prerequisite revisions
  with the exact reviewed inputs in the handoff. Do not replay the complete branch as an independent feature.
- HTTP readiness does not change other selected features' readiness or start an experimental build.

## Required Windows repairs

The user explicitly selected the Unicode filename fix for the enhanced build on 2026-10-01. Include
[windows-unicode-codepage](repairs/windows-unicode-codepage.md), including its regression test and test-wiring
follow-up, whenever the locked upstream baseline still needs it. Follow the repair record for exact commits and
attribution; this selects the focused fix, not the entirety of upstream PR #6726 or #6357.

On every Windows run, record whether the fix is applied or already present upstream. Require the seven-case
Unicode filename regression to pass through both `openscad.exe` and `openscad.com` in the extracted ZIP.
Do not deliver a build that silently omits this behavior. Keep repair commits separate from feature integrations.

## Focused behavior checks

- `pr-6878`: assign a custom shortcut, verify it invokes the intended action, check persistence across restart and
  consistency across windows, exercise collision handling, and restore defaults.
- `pr-6776`: switch Windows between light and dark modes while OpenSCAD remains open. Check editor, Customizer,
  docks, menus, and newly opened windows for readable colors; repeat in both directions.
- Combined: open the shortcut preferences while switching themes and check readability and shortcut operation.
  These are required run checks, not claims of validation already performed.
- `navigation-cube`: verify orientation, view selection and viewport interaction against its feature acceptance checks.
- `ui-visual-polish`: verify the approved UI changes, readability and interactions in light and dark modes.
- `annotations`: verify creation/editing, persistence and export against the annotations feature acceptance checks.

## Candidates from existing local work

These labels come from local checkout names, not a fresh check of GitHub state or PR contents.

| PR | Local topic | Selection |
| --- | --- | --- |
| https://github.com/openscad/openscad/pull/6642 | Dynamic parameter changes | Not selected |
| https://github.com/openscad/openscad/pull/6776 | Dynamic dark-mode switching | Enabled above |
| https://github.com/openscad/openscad/pull/6871 | MSVC build and compilation fixes | Not selected |
| https://github.com/openscad/openscad/pull/6999 | Customizer header text contrast | Not selected |

The local features above are selected without requiring upstream PRs. To use our improved version of an existing PR,
replace its row's source with an explicit `pr-variant` source; never infer this from an occupied worktree.

## Maintenance

For each enabled entry, supply a reason and any ordering dependencies. Use `latest` to resolve the declared source
ref at the start of each new run, or a full SHA to pin it. Record resolved SHAs even when the input says latest.
Remove or replace obsolete entries manually. A PR already included in upstream must be reported as already present
with evidence; do not manufacture an empty integration commit or silently rewrite this list.

Reusable build repairs are tracked in [REPAIRS.md](REPAIRS.md), separately from feature selection. Adding a repair
candidate does not enable another feature or select a different PR source.
