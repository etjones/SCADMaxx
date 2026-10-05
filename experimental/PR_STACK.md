# SCADMaxx integration stack

This is the manually maintained agent input for experimental builds. Select PRs, local features, or improved PR
branches and their order here. Keep this filename as the stable entry point.
Agents must not enable, remove, reorder, or silently substitute entries based on available local worktrees.
Use the [input contract](integration-inputs.md) to interpret sources, revisions, delta bases, and dependencies.
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
| 4 | ui-visual-polish | feature | ui-visual-polish-local | latest | be352f27972d570d61c9224a927079fa21055ac0 | pr-6776 | Improved OpenSCAD UI from our UI work branch |
| 5 | annotations | feature | annotations-local | latest | auto-merge-base | none declared | Native Blender-style annotation tool |
| 6 | http-agent-server | feature | http-agent-server-local | latest | 85829fa71870c4aa6945d3cd4abbc932faeab392 | navigation-cube, annotations | HTTP endpoint / agent server for OpenSCAD automation |
| 7 | pr-6081 | pr | https://github.com/openscad/openscad/pull/6081 | latest | auto-merge-base | none declared | OEP8a object literals and object comprehensions |
| 8 | pr-6642-oep8 | pr-variant | pr-6642-oep8-local | latest | 612e684c2cbbcdcb9a7a8307973f33fd910f9c17 | pr-6081 | Native Customizer attributes using fixed OEP8-style key: value entries |
| 9 | source-editing-foundation | feature | source-editing-foundation-local | 3131a23d6ec04f4405952d8804a41dd8296b2dc5 | 179f2d528ef32bfcdde3ad70f3094a1a2472a8c6 | http-agent-server | Guarded source transactions and source lifecycle |
| 10 | selection-model-inspector | feature | selection-model-inspector-local | ced629047eaa725a319f0c5a6a3602330b033c6d | b611584e013b8b4dbee123d62fabe9621b4bc137 | http-agent-server | Geometric picking and shared inspection presentation |
| 11 | vim-editor-mode | feature | vim-editor-mode-local | 1c48233689c4582754784c66fd23ed4273d56981 | 657aeead6534583964bec8797ae99f445404714c | source-editing-foundation, pr-6878 | Native Vim editing without GTK or GLib |
| 12 | source-geometry-provenance | feature | source-geometry-provenance-local | bb68db75a8d0fb259d17f50322306007d3750ebe | 6c8d2634c9de02265166464a1ab89fbb09eab6b8 | source-editing-foundation, selection-model-inspector, pr-6642-oep8 | Source spans and evaluated instance provenance |
| 13 | design-object-persistence | feature | design-object-persistence-local | 015aa3172759c00979830ab178cc3515b4e7fd50 | 0b7edfd57110dead25670bfbb83b743a2abf330a | source-editing-foundation, selection-model-inspector, pr-6642-oep8 | Typed design objects stored in SCAD source |
| 14 | live-clipping-sections | feature | live-clipping-sections-local | 06d073f73720a391f5d806911a3d91a27b1ebd4e | 2878c9234181f6a9cfadbd93af0e00dfc37ec42a | design-object-persistence | Live clipping planes and saved sections |
| 15 | geometry-services | feature | geometry-services-local | 4e1286c7b362f84e920a21ba65e13042178a6fea | e95c9bd5662f20e6df671889a3351c28a6b0f90e | none declared | Strict in-memory measurement and section services |
| 16 | component-provider-adapters | feature | component-provider-adapters-local | 9d0cb2097efcac6856ae5dafb31a642803ec32d7 | 35145c58c2b7c018158ce010ac18f8564a192923 | none declared | Version-matched component catalogs and source generation |
| 17 | semantic-foundation-followups | feature | semantic-model-hierarchy-local | e1d33c876493ed7bbe0dc61c3183280f0347e4d2 | 29c7ce594716b0fb2bb851b685113cd9248496bc | source-geometry-provenance, design-object-persistence | Captured evaluation jobs source navigation edit guards and reference validation |
| 18 | semantic-model-hierarchy | feature | semantic-model-hierarchy-local | 966b68b98fc21308d1fd1d40dbcb8eebeda7cc2f | e1d33c876493ed7bbe0dc61c3183280f0347e4d2 | semantic-foundation-followups | Parts Assemblies Components and scoped parameters |
| 19 | anchor-foundation-followups | feature | anchors-attachments-local | af0948f5d9711dc7f9336f6e08ffce21aba87364 | b223fe6702d13debc53f7c1d8ecec5ae53006131 | semantic-model-hierarchy | Scoped consumer lifecycle placement extension hooks and inspection fixes |
| 20 | anchors-attachments | feature | anchors-attachments-local | 56ceab74239507093067f11d078d73c12ae431c4 | af0948f5d9711dc7f9336f6e08ffce21aba87364 | anchor-foundation-followups | Typed anchors references and attachment placement |
| 21 | insertion-foundation-followups | feature | contextual-insertion-local | 2895ab7f882ca65a4b4fe35fc726ae7f74e1b43b | 5c5d75b133af95f90763853992bf90b62fd308dc | anchors-attachments, component-provider-adapters, pr-6878 | Sealed draft inputs focus groups parser guards ownership checks and Windows unit manifest |
| 22 | contextual-insertion | feature | contextual-insertion-local | b298c802905289b4fb94178d9127c6a8283342b7 | 2895ab7f882ca65a4b4fe35fc726ae7f74e1b43b | insertion-foundation-followups | Searchable insertion palette isolated preview and guarded Commit |

The first two entries were selected by the user on 2026-09-30. Both PRs were open and unmerged when checked against GitHub on that date.
PR #6878 is the updated version of the older Shortcuts GUI PR #3338. Resolve fresh heads and validate dependencies
at run start; this selection does not pin today's commits or include uncommitted local fixes.

The local features were selected by the user on 2026-10-01. Their current readiness and exact validated heads live
in `SOURCES.json` and their linked handoffs. Pending entries stop preparation; do not omit them or integrate their
starting commits as if the features were present. Build readiness applies to validated revisions promoted by an
explicit user push/promotion request; local completion and intermediate commits do not authorize that step.
Follow the [promotion rule](../workflows/update-and-build-scadmaxx.md#push-authorization-and-promotion).
Build runs must not commit another task's unfinished work.

The UI source is verified at `8f5b3ae4707a8718db28722deb2fd723fd9415ab`. Apply only its explicit UI delta after
`be352f27972d570d61c9224a927079fa21055ac0`, which excludes the already-incorporated #6776 and four Windows baseline
repairs. It depends on the selected `pr-6776`; review newer dependency revisions during composition and apply
applicable baseline repairs separately. See the [complete audit and handoff](../.plans/3_done/2026-10-01_ui-preferences-dialog-polish/5_post-implementation-notes.md).
Do not replay the full branch or silently substitute a local variant for the selected upstream PR.

## Source-first feature selection, 2026-10-04

The user selected all twelve completed features and requested local commits. Entries 9-22 select the eleven native
features and three separately bounded foundation-follow-up groups, in dependency order. Revisions are pinned to the
verified local commits. The shared follow-up entries use ancestor revisions on their consumer's branch; they are
separate deltas, not additional copies of the consumer or its whole prerequisite composition.

These new sources are selected and `ready: true`: the user subsequently authorized their pushes to the declared
Dropbox repositories, and all twelve remote feature heads were verified against the pinned local commits.
See [the local commit ledger](source-first-local-commits.md) for feature heads, delta bases, retained prerequisites,
follow-up boundaries and verification. Original feature handoffs describe the same tested source before committing.
Features 09/10/13 remain postponed, 16 remains exploration-only, and the separate evaluation-performance experiment
is not selected by this request.

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
