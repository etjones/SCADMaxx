# Source-first CAD: feature overview and implementation order

Status: planning synthesis. Created 2026-10-03; implementation progress is tracked in the readiness audit.

Reviewed for separate feature branches and SCADMaxx integration on 2026-10-03. The
[branch composition design](3_overall-plan.md) specifies branch names, prerequisites, shared-code ownership, merge
boundaries and build/package checks. This overview retains the discussion-derived product scope.

The [readiness audit](planning-readiness.md) assesses each feature for a GPT-6.1 Sol implementation handoff.
The [handoff standard](implementation-handoff.md) defines the required specificity. Features 01/02/03/04/05/06/07/08/11/12/14/15
now have requirements, technical designs and bounded implementation phases. 12's five choices are accepted; its six
phases include guarded candidate evaluation, exact source edits and the required generic 03 foundation follow-up.
Prepared plans do not mean native implementation has been completed.

## Sources and coverage

The user requested new planning features from five ChatGPT discussions, reading the newest synthesis first and
incorporating decisions and relevant background from the other four. These are the source chats, newest first:

| Key | Chat | Material retrieved |
| --- | --- | --- |
| A | [Viewport assisted authoring](https://chatgpt.com/c/6ac0f636-a860-83eb-b7d8-43681926b661) | All three exchanges, including the final synthesis. |
| B | [Adding Vim Mode to QCentella](https://chatgpt.com/c/6ac0f41f-a174-83ed-b3c7-39504935c94e) | The single exchange; QCentella was interpreted as QScintilla. |
| C | [OpenSCAD Technical Drawings](https://chatgpt.com/c/6ac0e938-fc20-83ed-8e9a-932e279e3c8b) | All ten exchanges, including the opening drawing, hierarchy and persistence discussion. |
| D | [Live Cross Section Ideas](https://chatgpt.com/c/6ac0e4d0-2070-83ed-b6a1-ba267f03a2a3) | All seven exchanges, seven final workflows and the original clipping-dock HTML mockup. |
| E | [Search OpenSCAD Skills](https://chatgpt.com/c/6ac0de66-2888-83eb-87fa-fe94b573d38f) | Five user turns and four replies, starting with the initial search request. |

The initial app reader exposed only the last five exchanges of C/D, reporting no older page; browser retries also
failed. After the user opened both chats and scrolled to their beginnings, their cached conversation and older-message
responses were recovered from the local app's Chromium cache on 2026-10-03. The older responses report no previous
page and connect to the recent windows, resolving the earlier coverage gap. Only user messages and visible assistant
replies were used as discussion evidence. The original widget is preserved with
[the clipping plan](../../3_done/2026-10-03_04_live-clipping-sections/assets/clipping-dock-mockup.original.html).

Later user corrections take precedence over earlier assistant proposals. Explicit requests are recorded as decisions;
useful assistant elaborations remain proposed design. External repositories, PR status, library capabilities and
licensing mentioned in the chats are research leads, not freshly verified facts.

## Product boundaries

SCADMaxx remains a source-first CAD environment. Text and geometry provide complementary interfaces to the program.
UI operations that change the model become minimal edits to the authoritative live source buffer.

| State | Owner | Examples |
| --- | --- | --- |
| Model geometry/semantics | OpenSCAD source in the live editor buffer | Parameters, transforms, components, assemblies and holes. |
| Reusable design objects | Typed, annotated declarations in OpenSCAD source, through 14 | Named sections/views, semantic references, deliverable annotations. |
| Personal inspection | SCADMaxx workspace/session state | Selection, temporary visibility, camera history and unsaved clipping. |
| Documentation | Drawing declarations in OpenSCAD source using shared design objects | Sheets, views, dimensions, notes and title blocks. |

The AST interprets source; it does not replace the buffer. Preserve comments, whitespace, expressions and ordering
outside intentional edits. Source changes join ordinary undo/dirty/save behavior. Normal file watching and save
conflict protection handle external editors; a VS Code broker or collaborative-document protocol is not required.
Clipping gestures do not change model geometry. Sections used by drawings must nevertheless have reproducible,
editable definitions that travel with the design. The user rejected separate stable/ephemeral versions of one
concept: one Section object moves between unsaved and persisted states. The user subsequently selected `.scad`
storage using typed, annotated objects; definitions can live in the main file or an included file and use parameters.
Drawing dimensions describe geometry; they do not implicitly become parametric modeling constraints.

## Feature split

Each item is a separate planning feature, with later planning steps added as specified in the readiness audit.
Infrastructure has explicit ownership.
Numbers identify features, not mandatory execution positions. Feature 14 was added from the recovered earlier
discussion. Feature 15 extracts shared geometry work after reviewing branch boundaries. Both are foundations.

| No. | Feature | Responsibility |
| --- | --- | --- |
| 01 | [Agent skill enrichment](../../3_done/2026-10-03_01_agent-skill-workflows/1_exploration.md) | Task reasoning, reconstruction and evidence workflows. |
| 02 | [Source editing foundation](../../3_done/2026-10-03_02_source-editing-foundation/1_exploration.md) | Live buffer, minimal patch transactions, save conflicts. |
| 03 | [Selection and Model Inspector](../../3_done/2026-10-03_03_selection-model-inspector/1_exploration.md) | Geometric picking, basic inspection UI and viewport tool routing. |
| 04 | [Live clipping and sections](../../3_done/2026-10-03_04_live-clipping-sections/1_exploration.md) | Render-side clipping and persistent inspection planes. |
| 05 | [Vim editor mode](../../3_done/2026-10-03_05_vim-editor-mode/1_exploration.md) | Optional editor interaction over the same buffer. |
| 06 | [Source/geometry provenance](../../3_done/2026-10-03_06_source-geometry-provenance/1_exploration.md) | Syntax spans, instances and trustworthy correspondence. |
| 07 | [Semantic model hierarchy](../2026-10-03_07_semantic-model-hierarchy/1_exploration.md) | Typed hierarchy, identities, semantic tree and Customizer binding. |
| 08 | [Anchors and attachments](../2026-10-03_08_anchors-attachments/1_exploration.md) | Geometric/named anchors and reusable placement frames. |
| 09 | [Technical drawings](../2026-10-03_09_technical-drawings/1_exploration.md) | Postponed by user; retain views, sections, dimensions, sheets and output research. |
| 10 | [Interactive source editing](../2026-10-03_10_interactive-source-editing/1_exploration.md) | Postponed by user; additional workflow and editing semantics remain unresolved. |
| 11 | [Component providers/adapters](../2026-10-03_11_component-provider-adapters/1_exploration.md) | Catalogs, parameters, placement metadata and source fragments. |
| 12 | [Contextual insertion](../2026-10-03_12_contextual-insertion/1_exploration.md) | Shift-A, configure/preview/place/commit new source. |
| 13 | [Agent geometry tools](../2026-10-03_13_agent-geometry-analysis/1_exploration.md) | Postponed by user; establish a concrete API/numerical need before adding capabilities. |
| 14 | [Shared design objects and persistence](../../3_done/2026-10-03_14_design-object-persistence/1_exploration.md) | Section/view lifecycle, editable declarations, stable references and dependency persistence. |
| 15 | [Shared geometry services](../../3_done/2026-10-03_15_geometry-services/1_exploration.md) | Numerical measurements and section contours used by drawings and agent tools. |

A presents five user-facing feature families and also describes a Model Inspector. This split retains the inspector
and separately owned foundations. E adds two tracks omitted from A's diagram: skill instructions and actual tools.
C's recovered opening discussion supplies the shared design-object lifecycle in 14, detailed typed hierarchy and
Customizer behavior in 07, and repeatable drawing rules in 09.
The branch review assigns each shared API to one owner. It keeps semantic integrations in their dependent branches,
removes unnecessary dependencies and separates the control-owned skill from fourteen native source branches.

## Implementation order and first priority

Updated after the user's request to prioritize features 01-06. The directory numbers are stable feature IDs, not
execution positions. In particular, 04 needs 14, and 06 needs 02/03. The complete requested first group therefore
contains seven features: 01, 02, 03, 05, 06, 14 and 04. Keeping saved clipping in that group requires 14's shared
source-declaration/evaluation contract; this does not justify a private temporary section store or dropping persistence.

| Execution position | Feature ID and result | New-feature prerequisites |
| --- | --- | --- |
| 1 | 01 Agent skill workflows | None; control repository. |
| 2 | 02 Source editing foundation | None. |
| 3 | 03 Geometric selection / Inspector | None. |
| 4 | 05 Vim editor mode | 02; pre-group edit notification for coherent undo. |
| 5 | 06 Source / geometry provenance | 02, 03. |
| 6 | 14 Shared design objects / persistence | 02, 03. |
| 7 | 04 Live clipping and saved sections | 03, 14. |
| 8 | 07 Semantic hierarchy | 03, 06, 14. |
| 9 | 08 Anchors / attachments | 03, 07, 14. |
| 10 | 15 Shared geometry services | None; may be implemented earlier. |
| 11 | 11 Component providers | None; may be implemented earlier. |
| 12 | 12 Contextual insertion | 02, 03, 06, 08, 11. |
| Postponed | 13 Agent geometry analysis | Proposed 08, 14, 15; recheck scope and actual need if resumed. |
| Postponed | 09 Technical drawings | 08, 14, 15, when the user resumes it. |
| Postponed | 10 Interactive source editing | 02, 03, 06, 08, if resumed with an agreed additional workflow. |

This is one valid priority-respecting sequential order, not an extra set of dependencies. 01/02/03 can develop
independently; 05 follows 02, and 06/14 can follow independently after 02/03. 15 and 11 remain independent
work that may move earlier. Later consumer branches can also proceed independently once their actual prerequisites
are available. No new dependency is introduced merely by adjacency in this table.

After 08's decisions, the user postponed 09, reviewed and postponed 10, and selected 11 for the next discussion.
This changes priority, not dependency edges. Retain 09/10 explorations for later; neither blocks 11, 12 or 13.
On 2026-10-04 the user also postponed 13 after questioning its concrete purpose and overlap with native services and
agent instructions. Preserve its unaccepted ideas; no active feature waits for it. All fifteen items are now reviewed.

Planning readiness is separate: implementation packages exist for the entire requested first group, 07, 08, 11, 12 and 15.
Their early phases perform the specified runtime proofs; renderer, native input, parser and undo checks have not run
during planning. The [readiness audit](planning-readiness.md) records remaining implementation obligations and later
planning work. No implementation or lane move starts here.

11 ships catalogs and supports user/project catalogs, with exact matching to separately installed library revisions.
It bundles no third-party libraries. Its initial recipes are source-probed and it has no new-feature prerequisites.
12 is planning-complete for its bounded insertion scope; its real palette/preview/source transaction remains separate
from 11's registry/fragments. Its native implementation waits for verified prerequisites, including the generic
[03 draft/input follow-up](insertion-foundation-contract.md) and 11 insertion-role metadata. There is no further
unreviewed planning item: 14 is already planned and 15 locally implemented; 09/10/13 remain postponed.

[The dependency graph](../../feature_dependencies.dot) records hard or near-hard sequencing, omitting redundant
transitive edges and the independent skill track. The branch design gives the complete direct dependency table
and existing selected prerequisites. Drawings consume the Section definition from 14, not the clipping dock from 04.
Basic numerical functionality belongs to 15; postponed 13 would require a concrete additional API/numerical need.

## Integration and readiness

- Reuse completed annotations, navigation and the guarded HTTP API as baseline context rather than new feature plans.
- Extend the existing product skill; its completed predecessor stays in `3_done`.
- Existing launcher, build, UI and skill changes predate this task and are outside these planning edits.
- Work stays in the control repository. No source implementation or build-stack change is part of this request.
- Reusable design objects use typed, annotated `.scad` declarations. The first Section/View schemas, evaluation
  interfaces and clipping/picking coverage are specified; later semantic/drawing schemas and provider distribution
  remain planning work. Specified APIs are not already implemented.
- Source changes are integrated as reviewed feature-only deltas, with explicit bases for stacked branches; no branch
  imports the moving final composition as its development base. Build selection remains manually controlled.
