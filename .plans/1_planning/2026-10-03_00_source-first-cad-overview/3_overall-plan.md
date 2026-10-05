# Branch composition and integrated SCADMaxx delivery

Reviewed 2026-10-03 at the user's request. This refines the feature split for separately developed branches that
compose into one application. These are proposed branch boundaries; no branches or build selection were created.

For each feature's current requirements/design/phase readiness, see the [readiness audit](planning-readiness.md).
Detailed phases follow the [GPT-6.1 Sol handoff standard](implementation-handoff.md); a branch dependency does not
substitute for a concrete interface specification. The composition order below remains unchanged by this audit.

## Findings and resulting split

The product split is useful, but the original dependency graph was insufficient as a branch plan. Some early features
promised later semantic integration inside their own branch, making completion depend on downstream consumers.
It also put provider metadata behind anchors and drawings behind the clipping dock without a code-level need.

Keep the existing feature IDs and make these ownership changes:

- 03 owns geometric selection, a basic Inspector and viewport interaction seams. 07 adds the semantic tree and
  Customizer binding; 06 supplies source navigation; 14 adds saved-view operations. 03 compiles without them.
  Its [shared inspection presentation contract](inspection-presentation-contract.md) also composes 04's clipping
  effect with 07's per-Part meshes/visibility. Verify this owner refinement before freezing either consumer's base;
  do not add an artificial dependency between clipping and semantic hierarchy.
- 14 owns complete generic Section/View lifecycle, persistence and reference-resolution interfaces. Concrete
  semantic-target and named-feature resolvers belong to 07 and 08. 14 never imports their implementations.
- 11 owns catalog metadata and source fragments; 12 owns placement integration, boolean/include edits and insertion UI.
  12's accepted insertion roles are metadata in 11. Its source/preview contracts and six phases are prepared;
  the generic 03 draft-display/sealed-input/focus follow-up is specified in insertion-foundation-contract.md.
  That follow-up belongs to 03 before 12 freezes its base, without adding 12 headers or changing 04/07 dependencies.
  Provider discovery can compile and be exercised without the viewport or source editor transaction implementation.
- Add 15 for shared geometric measurements and section computation. 09 owns drawings; 13 owns agent-facing tools.
  Neither owns a private copy of the other's shared geometry operations.
- 09 consumes Section definitions from 14, not clipping UI from 04. 04 may still be delivered first for user value.
- 01 belongs in the control repository and its companion package. The other fourteen features own source branches.

## Build-system evidence

The authoritative contracts are [integration inputs](../../../experimental/integration-inputs.md),
[the update/build runbook](../../../workflows/update-and-build-scadmaxx.md),
[the selected stack](../../../experimental/PR_STACK.md), and
[the build tools](../../../experimental/scripts/README.md).

The current system starts each composition at freshly locked upstream master, applies selected changes in order,
and records one squash integration commit per entry. It does not merge every feature branch's complete ancestry.
`New-ExperimentalRun.ps1` requires dependencies to be selected earlier and an explicit 40-character delta base for
every dependent entry. `SOURCES.json` names repository/ref and readiness; it does not itself enable an entry.

Source inspection used the retained integrated checkout `wt-scadmaxx-20261002` at
`4c325716b94e444637a80df3966197ce110b2b75`, not a newly fetched baseline. Important existing seams are
`EditorInterface`/`ScintillaEditor`, `MouseSelector`, `MainWindow`/`QGLView`, the parser's source locations,
`AgentAnnotations::Store` and its undo integration, and the guarded agent transport. `MouseSelector::select()`
currently returns an integer, so a complete point/normal/result hit contract still needs implementation.
`ManifoldGeometry` already exposes slice/project operations suitable for investigation by 15.

The enabled stack includes shortcuts, themes, navigation, UI polish, annotations, HTTP, OEP8a and the Customizer
variant. Preserve those behaviors when adding features. This review did not refresh remote revisions or establish
that a particular future combination compiles; actual branch bases must be recorded when development starts.

## Branch and prerequisite map

These names are proposals, not existing refs. Source branches live in the shared `openscad-master` repository;
their worktrees follow `wt-openscad-<slug>`. The table lists direct new-feature API prerequisites. Their transitive
closure and the existing selected entries in the next section form each branch's development base.

| ID | Proposed branch | Direct new-feature prerequisites | Mergeable result |
| --- | --- | --- | --- |
| 01 | `feature/agent-skill-workflows` (control repo) | None | Enriched, verified companion skill ZIP. |
| 02 | `feature/source-editing-foundation` | None | Revision-aware text transactions and document hooks. |
| 03 | `feature/selection-model-inspector` | None | Geometric hits, Inspector shell and interaction routing. |
| 04 | `feature/live-clipping-sections` | 03, 14 | Live clipping dock using shared Section objects. |
| 05 | `feature/vim-editor-mode` | 02 | Optional Vim input with coherent external-edit undo boundaries. |
| 06 | `feature/source-geometry-provenance` | 02, 03 | Current source/instance mapping and Inspector source navigation. |
| 07 | `feature/semantic-model-hierarchy` | 03, 06, 14 | Typed hierarchy, semantic target resolver, tree/Customizer UI. |
| 08 | `feature/anchors-attachments` | 03, 07, 14 | Named references, frames, attachment math and reference resolver. |
| 09 | `feature/technical-drawings` | 08, 14, 15 | Repeatable drawing documents, dimensions and exports. |
| 10 | `feature/interactive-source-editing` | 02, 03, 06, 08 | Existing-object manipulation with source transactions. |
| 11 | `feature/component-provider-adapters` | None | Provider registry, parameter metadata and source fragments. |
| 12 | `feature/contextual-insertion` | 02, 03, 06, 08, 11 | Palette, preview, placement and committed insertion. |
| 13 | `feature/agent-geometry-analysis` | Proposed 08, 14, 15; recheck if resumed | Postponed; concrete need and scope unaccepted. |
| 14 | `feature/design-object-persistence` | 02, 03 | Typed `.scad` design declarations, lifecycle and saved-view integration. |
| 15 | `feature/geometry-services` | None | Numerical geometry/section service and non-GUI fixtures. |

Use the branch slug after `feature/` as the proposed source registry key and stack ID. 01 is a control change,
not an OpenSCAD stack entry. Dependencies in an eventual stack use those IDs, never the numeric plan labels.
The sparse [dependency graph](../../feature_dependencies.dot) omits redundant transitive edges.

### Existing selected prerequisites and shared-file conflicts

- 02 must preserve the annotation undo hooks and HTTP document/source/result revision guards. Develop against
  those selected entries, and record `annotations`/`http-agent-server` plus their dependency closure.
- 03 works with selected `navigation-cube`, `annotations` and `http-agent-server`. It owns picking/tool arbitration
  and shared immutable evaluation inputs/result binding; HTTP syntax-inspection reader integration uses that baseline.
- 05 uses selected `pr-6878` shortcuts, annotation undo and new-feature 02's pre-group edit boundary. Test interleaved
  Vim/programmatic/annotation undo on that prerequisite base; a notification after text modification is insufficient.
- 06, 07 and 14 develop against selected `pr-6081` and `pr-6642-oep8`. Their parser/lexer work must preserve both
  ordinary OEP8 objects and fixed-key Customizer annotations. 14 owns the generic typed design-declaration mechanism;
  07 registers its semantic kinds. This existing baseline does not add a new dependency from 14 to 06 or 07.
- 04/09/10/12 add actions through the selected shortcut system (`pr-6878`); all new docks must remain compatible with
  selected theme/UI changes. UI polish need not become a compile prerequisite unless its APIs are actually used.
- 13 extends selected `http-agent-server` and its capability description, targeting and asynchronous result guards.
  Reuse that service rather than adding an independent server. Any CLI surface invokes the same analysis service.
- 15 can begin on upstream geometry alone. 11 can begin on existing language/library facilities alone; individual
  adapters must declare required library versions rather than assuming BOLTS/BOSL2/NopSCADlib are packaged.

These dependencies must be checked against the actual delta and headers at handoff. Include every prerequisite
whose changes are excluded by a branch's recorded base, even when it is only a transitive dependency in this table.

## How to develop and integrate a dependent branch

1. Record upstream and exact prerequisite revisions. For an independent feature use freshly fetched upstream;
   for a dependent feature create a dedicated prerequisite-only composition in the shared source repository.
   Include only required selected entries and necessary build repairs. Do not use a moving all-feature integration
   branch as the feature's base or merge unrelated features into its history.
2. Retain that prerequisite composition as an ancestor commit `B`, with a manifest of its input SHAs and resolutions.
   Start the feature at `B` and record its eventual head `H`. Its intended delta is `git diff --binary B H`.
   With several prerequisites, `B` is their actual composed commit, not an arbitrary individual prerequisite tip.
3. Keep prerequisite updates out of `B..H`. If they must change, record a new reviewed base and rebuild/review the
   feature-only delta; retain the previous base/head evidence. Do not absorb those updates as feature code or rewrite
   a retained/shared branch without the appropriate maintenance decision.
4. Compile and check the feature on its minimal declared prerequisite base. Also rehearse applying that delta to
   an isolated composition containing the current selected SCADMaxx stack and the intended earlier new features.
   This catches both undeclared dependencies and conflicts with existing functionality.
5. At integrated delivery, follow the runbook: freeze the exact upstream, heads, bases, controls and repairs; present
   those inputs; apply each reviewed delta in order and commit it separately. Earlier squash integrations do not
   carry original branch ancestry, so blindly merging a dependent head can replay its prerequisites.
6. Resolve mechanical overlaps at integration. Fix shared API/behavior defects in the owning feature branch and
   verify consumers, so the next composition can reproduce the correction. Keep unavoidable composition repairs
   explicit in the repair/run evidence; do not leave indispensable product behavior only in an undocumented merge.

Existing retained HTTP prerequisites demonstrate this pattern. It supports separate branches with real dependencies;
it does not promise every feature can compile against bare upstream alone or merge without conflicts.

## API ownership and module boundaries

| Owner | Shared contract | Consumers must not duplicate |
| --- | --- | --- |
| 02 | Document identity/revision, text patch transaction, undo/save/conflict hooks | Private text buffers or disk writers. |
| 03 | Immutable evaluation inputs/result binding, geometric hits, Inspector/tool/overlay routing | Divergent source snapshots, separate picking or competing gesture capture. |
| 06 | Source ranges, result provenance, instance correspondence | Pixel/triangle IDs treated as source identity. |
| 14 | Section/View records, resolvers, source/dependency lifecycle and generic container-undo registry | Drawing-only Section copies or conflicting annotation/design undo tokens. |
| 07 | Typed Part/Component/Assembly tree, target resolver and parameter ownership | A second hierarchy in drawings or Inspector. |
| 08 | Named geometric references, frames, attachment transforms and their resolver | Consumer-specific coordinate/anchor conventions. |
| 15 | Geometry measurements and section results | Copied slicing kernels in 09 and 13. |
| 11 | Provider metadata, parameter schemas, generated source fragments | Per-library branches in the palette. |

Keep new implementation in cohesive feature modules with narrow public headers. Shared application files
(`MainWindow`, `QGLView`, `ScintillaEditor`, parser/lexer, CMake source lists) receive the necessary small wiring edits.
03's contribution seams should remain small, not become a general plugin framework. Each consumer registers its
own UI/tool; foundational code does not include future consumers' headers or use placeholder implementations.
Branch boundaries are not runtime feature switches: dependencies are compiled normally when selected, and every
intermediate composition must build. Do not add speculative compatibility shims for old versions of these APIs.

Each source feature owns its CMake sources/headers, Qt moc/resources, install rules, focused fixtures and capability
documentation. Record any compile switch in the build fingerprint and exercise the delivery setting. Shared build
scripts/profile changes belong in a companion control commit attributed to that feature, not copied into source Git.
Libraries and catalog assets need licenses, declared versions and portable install/resource paths.

## Merge waves and checkpoints

The user's first priority is 01-06. Because 04 requires 14, use the dependency-correct order in
[the overview](1_exploration.md#implementation-order-and-first-priority). These are integration groups, not instructions
to launch parallel agents or create all worktrees now. Requirements being written does not make every branch ready.

1. First-group foundations: 02 and 03, then Vim 05 after 02; 01 progresses in control history independently.
2. First-group follow-through: provenance 06 and persistence 14 after 02/03. Each can develop independently.
3. Complete the requested first group with live clipping 04 after 03/14.
4. Semantic hierarchy 07 after 06/14, then anchors/references 08. Verify semantic Section rebinding and selected-node
   Customizer behavior. 03/14 still do not import their dependent semantic resolvers.
5. Deliver 12 on its declared prerequisites; 09, 10 and 13 are postponed by the user. Independent geometry service 15
   remains available for explicitly resumed 09/13 work;
   independent provider service 11 must precede 12. Either foundation may be delivered earlier without changing the graph.
   Consumers remain independent of one another: drawings need neither 10 nor 12; insertion needs neither 09 nor 10.

At every integration checkpoint build the resulting source and run the new feature's checks plus affected earlier
features. High-risk pairs are 02+05+annotations (undo/input), 03+04+navigation+annotations (picking/overlays),
06+07+Customizer (grammar/source ranges), 07+08+14 (identity/persistence), 09+13+15 (section results),
and 10+12+Vim+HTTP (source/result revisions, cancellation and document targeting).

With 10 postponed, verify 12+Vim+HTTP independently; composition checks involving 10 resume only if that feature does.
13-specific composition checks are likewise deferred; do not implement new analysis endpoints or numerical services
to satisfy a postponed feature. Existing 15 measurements/sections and active feature checks remain unaffected.

The final scenario opens a parametric assembly, edits parameters using text/Customizer, inspects a saved section,
adds a genuinely subtractive provider item, undoes/redoes edits, regenerates a dimensioned drawing and measures the
same evaluated result through HTTP. Save/reopen and an external-file conflict check must retain the correct targets.

The drawing step above is deferred with 09; it is not an acceptance condition for delivering the currently selected
features. Run it when drawings are resumed and implemented.
Validate the declared renderer/backend coverage, theme/shortcut behavior and multiple documents.

## Windows packaging and readiness handoff

Reuse the shared vcpkg tree and current MSVC/Qt6/QScintilla profile. No private dependency installations, automatic
upgrades or development-machine-only Python/plugin paths. New optional backends or Vim/vendor code require explicit
dependency/license/Windows-build assessment before becoming a selected implementation dependency.

Each branch handoff records repository/ref, upstream and prerequisite SHAs, `B`, `H`, feature-only diff, submodule
revisions, test evidence, capability/resource requirements and any companion control commit. Local completion and
promotion remain distinct under the runbook. Keep pending sources out of the enabled stack during planning; when
explicitly selected before readiness they must be marked pending rather than stopping builds by surprise.
This review does not change `PR_STACK.md`, `SOURCES.json`, push any ref, or start a build.

Feature 01 uses the existing `Build-ScadmaxxSkill.ps1` companion path. Current application Stage copies the source
HTTP bundle under `openscad-agent-server`; it does not automatically copy `skills/scadmaxx` from control history.
01 must own the control-side release hook/verification needed to deliver its versioned companion alongside the
application, tied to the final integrated capability set and canonical Customizer documentation. Freeze both control
and source revisions. Do not create a fake source-stack row for a control-only skill change.

Use per-worktree application build directories, existing shared dependencies, the required executable-name/Unicode
repairs, and the standard Stage/Package/extracted-ZIP checks. Verify shaders, catalogs, drawing resources, server
contracts and any new runtime DLLs from the extracted package. Preserve source/control/run provenance and report
unexecuted GUI or clean-machine checks. This planning review establishes ownership and order, not build validation.
