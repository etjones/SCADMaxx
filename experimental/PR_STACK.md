# SCADMaxx integration stack

This is the manually maintained agent input for experimental builds. Select PRs, local features, or improved PR
branches and their order here. Keep this filename as the stable entry point.
Agents must not enable, remove, reorder, or silently substitute entries based on available local worktrees.
Use the [input contract](integration-inputs.md) to interpret sources, revisions, merge ancestry, and dependencies.
Named repositories/refs for local features and PR variants belong in [SOURCES.json](SOURCES.json). Defining a source
there does not select it; only an enabled row does.

For fresh-chat update/build requests, use [the update-and-build runbook](../workflows/update-and-build-scadmaxx.md).
It defines source synchronization and the handoff required when each feature becomes ready.

## Build policy

- Upstream: `https://github.com/openscad/openscad.git`, branch `master`.
- Local source origin: `E:/Dropbox/bare_repos/openscad.git`.
- Optional future feature publication: `https://github.com/roel-v/openscad.git` (remote `publish`).
- Keep all SCADMaxx compositions and workspace controls local; publish a feature only by explicit user choice.
- Initial target: Windows x64 GUI, Release configuration, portable ZIP.
- Fetch current upstream master once at run start and lock its exact SHA for the entire run.
- Resolve every enabled source and accepted dependency before integration and lock their exact SHAs for that run.
- Merge enabled rows in their written order; commit each integration, then build and commit any required repairs.
- Never carry a previous run's entire composition forward as the new baseline.
- Keep successful ZIPs in `artifacts/<run-id>/`. External publication destination is not configured.
- Schedule: on demand. No recurring job is configured.

## Enabled stack (ordered)

| Order | ID | Kind | Source | Revision | Integration | Depends on | Reason for inclusion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | pr-6878 | pr | https://github.com/openscad/openscad/pull/6878 | latest | merge | none declared | Customize keyboard shortcuts through the GUI |
| 2 | pr-6776 | pr | https://github.com/openscad/openscad/pull/6776 | latest | merge | none declared | Correct switching to and from dark mode while OpenSCAD is running |
| 3 | navigation-cube | feature | navigation-cube-local | 6b42cbf3f95bfe1ad2ff4b845a6dc20f4ed336fe | merge | none declared | Native viewport navigation cube |
| 4 | ui-visual-polish | feature | ui-visual-polish-local | 6096a42d2ee5e8c8530b8b5776c9ca04a1a9afd2 | merge | pr-6776 | Improved OpenSCAD UI from our UI work branch |
| 5 | annotations | feature | annotations-local | d670fad09dba45526487e958b90fd553c6e1ace0 | merge | none declared | Native Blender-style annotation tool |
| 6 | http-agent-server | feature | http-agent-server-local | f2c9de2c94745b834b5a120fdc5c29a5999128c9 | merge | annotations, navigation-cube | HTTP endpoint / agent server for OpenSCAD automation |
| 7 | pr-6081 | pr | https://github.com/openscad/openscad/pull/6081 | latest | merge | none declared | OEP8a object literals and object comprehensions |
| 8 | pr-6642-oep8 | pr-variant | pr-6642-oep8-local | 306c92d39c4cbb7fe82981e179161aa85d44774e | merge | pr-6081 | Native Customizer attributes using fixed OEP8-style key: value entries |
| 9 | source-editing-foundation | feature | source-editing-foundation-local | 0bcafded2a98d98802a8e869e44a658770ebc3b4 | merge | http-agent-server | Guarded source transactions and source lifecycle |
| 10 | selection-model-inspector | feature | selection-model-inspector-local | 6440acdfd1c21f979d3074b2cdd60478d0aa8977 | merge | http-agent-server | Geometric picking and shared inspection presentation |
| 11 | vim-editor-mode | feature | vim-editor-mode-local | f6e316ed43dcaa4726520dbee76980015e681ec7 | merge | source-editing-foundation, pr-6878 | Native Vim editing without GTK or GLib |
| 12 | source-geometry-provenance | feature | source-geometry-provenance-local | 36e43d75020ebe2ff81cb90ce84aca63c482fd8c | merge | source-editing-foundation, selection-model-inspector, pr-6642-oep8 | Source spans and evaluated instance provenance |
| 13 | design-object-persistence | feature | design-object-persistence-local | cdfc439c169ead84b91366bca7096348380c1fd1 | merge | source-editing-foundation, selection-model-inspector, pr-6642-oep8 | Typed design objects stored in SCAD source |
| 14 | live-clipping-sections | feature | live-clipping-sections-local | ce8af12e4b4d4cee14b82f697062f75cf552f0c3 | merge | design-object-persistence, pr-6878 | Live cross section clipping planes and saved cross sections |
| 15 | geometry-services | feature | geometry-services-local | 4e1286c7b362f84e920a21ba65e13042178a6fea | merge | none declared | Strict in-memory measurement and section services |
| 16 | component-provider-adapters | feature | component-provider-adapters-local | 9d0cb2097efcac6856ae5dafb31a642803ec32d7 | merge | none declared | Version-matched component catalogs and source generation |
| 17 | semantic-model-hierarchy | feature | semantic-model-hierarchy-local | aca9bcd54aaa739d6a1d5af4c0e9228618e6ebe0 | merge | source-geometry-provenance, design-object-persistence | Parts Assemblies Components and scoped parameters |
| 18 | anchors-attachments | feature | anchors-attachments-local | bd0a54c5c0eb8ded39cc3e2d8d5ff79230c9b4ab | merge | semantic-model-hierarchy | Typed anchors references and attachment placement |
| 19 | contextual-insertion | feature | contextual-insertion-local | 9ba04f92b79fb15715c79c84af677078dafda53f | merge | anchors-attachments, component-provider-adapters, pr-6878 | Searchable insertion palette isolated preview and guarded Commit |

The selected product features are unchanged. The three historical foundation-followup rows have been retired:
their shared behavior now belongs to the maintained owners listed in [the migration record](../docs/feature-ancestry.md).
Those original commits remain in consumer histories; do not replay their old patches.

Native entries use real merges of the frozen heads. No B..H feature patches or squash integration commits.
[DEPENDENCIES.json](DEPENDENCIES.json) records the reviewed source heads and exact direct prerequisite revisions.
Preparation rejects missing dependencies, different accepted revisions, and known excluded features hidden in ancestry.
Updating a GitHub PR beyond a consumer's accepted prerequisite requires owner-branch maintenance first.

The 2026-10-06 migration and follow-up repairs passed owner/forward-consumer validation
in `runs/20261006-validation-promotion`. The selected revisions were explicitly promoted
to Dropbox and verified; `SOURCES.json` records their exact validated/promoted heads.
Fresh integrated composition checks remain required. A build request alone does not
authorize future pushes. Original runs retain their frozen controls and old contract.

Features 09/10/13 remain postponed; viewport keyboard commands and the evaluation-performance experiment remain
outside this native selection. The skill companion below is a separate control-repository input.

### Selected skill/package companion: feature 01

`agent-skill-workflows-local` in `SOURCES.json` selects feature 01 from the control repository. Its pinned head and
delta base are in the local commit ledger. This is part of the requested delivery, not an OpenSCAD source patch.
Before the next build, incorporate the promoted revision's reviewed control/skill delta
into the build controls, then freeze those controls and run the companion Stage/Package checks with the new binary.
Do not apply it to the native source tree or assume registration alone has updated the currently checked-out scripts.
Its promoted source is ready; application to build controls and integrated packaging acceptance remain build work.

## HTTP agent-server feature handoff

- Dedicated `codex/http-agent-server` head `498c4774d26e7235fbc4cbb9b34f56afb39ca645` is committed and verified in the declared private origin.
  See [completed implementation and evidence](../.plans/3_done/2026-10-01_http-agent-server/5_post-implementation-notes.md).
- Apply its explicit HTTP-only delta after the selected navigation and annotations entries. The base is the
  retained dependency-only composition, an ancestor of the source head; compare newer selected prerequisite revisions
  with the exact reviewed inputs in the handoff. Do not replay the complete branch as an independent feature.
- HTTP readiness does not change other selected features' readiness or start an experimental build.

## OEP8 and Customizer syntax

Selected by the user on 2026-10-02. Use OEP8a #6081; the broader #4478 geometry and module-reference
prototype is not selected. Apply the #6642 variant after OEP8a and preserve both expression classes.
Annotations use `@{ key: expression, ... }` with fixed identifier keys and optional trailing commas;
computed keys, quoted keys, `each`, and comprehensions are not annotation syntax. Ordinary OEP8 objects
retain their own full syntax. Existing reactive `hidden`/`locked` values remain supported.
Follow the source readiness record and
[implementation evidence](../.plans/1_planning/2026-10-02_oep8-customizer-syntax/5_post-implementation-notes.md).

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
- `pr-6081`: exercise literal construction, object(), lookup, computed keys, comprehensions and object merging;
  run object/JSON/text-metrics echo regressions because OEP8 changes object serialization.
- `pr-6642-oep8`: run the native-attribute parser and Customizer tests, including rejected dynamic-key syntax,
  printer round trips, numeric widget configuration and reactive included parameters using special variables.

## Candidates from existing local work

These labels come from local checkout names, not a fresh check of GitHub state or PR contents.

| PR | Local topic | Selection |
| --- | --- | --- |
| https://github.com/openscad/openscad/pull/6642 | Dynamic parameter changes | OEP8 syntax variant enabled above |
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
