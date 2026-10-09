# Readiness audit for GPT-6.1 Sol implementation

State refreshed 2026-10-03 20:45 UTC (22:45 Amsterdam) from implementation chats, durable handoffs and 07 decisions. The implementer is
GPT-6.1 Sol; the second implementation chat uses Extra high reasoning. Model capability is not a substitute for an
executable specification or verification. This audit covers all fifteen features; this update starts no implementation
and moves no planning lanes. Status is a snapshot, not a live progress feed.

Feature 08 planning updated at 21:34 UTC (23:34 Amsterdam): all six decisions accepted, source contract/technical
design/six phases prepared and pinned BOSL2 mapping probes passed. This scoped update also specifies the required
14/07 generic extension hooks; it does not refresh the other chats' implementation statuses below.

Subsequent scheduling decisions: the user postponed 09, reviewed 10's scope, then postponed 10 and selected 11.
Existing research remains available; active consumers require neither 09 nor 10. Implementation-chat statuses are
unchanged here.

Feature 11 planning update (2026-10-04 Amsterdam): all three decisions accepted, with explicit library-version
matching. Requirements, provider contract, tested fingerprint/import profiles, technical plan and five phases are
prepared. The final library probes passed 25 cases; the native registry/matcher remains unimplemented.

Feature 12 update, 2026-10-04 Amsterdam: all five choices accepted. Source/preview contracts, technical design and six
implementation phases are prepared. Two plain-source geometry probes passed; native insertion remains unimplemented.
03's completed handoff was read during this review, superseding its earlier active status below. The separately
specified [03 draft/input follow-up](insertion-foundation-contract.md) remains required before 12; 11's role metadata
is also refined. Other implementation-chat progress was not refreshed.

Implementation handoff, 2026-10-04: the user requested a separate chat for prepared features 07/08/11/12. Created and
pinned **SCADMaxx assisted editing third batch implementation**, chat `01a10406-f3ab-76f0-9eac-9c1daebe6175`, in the
openscad project with GPT-6.1 Sol / Extra high. It is primed with the complete plans and owner contracts and instructed
to wait for the user before implementing. This planning chat retains 13 and postponed 09/10. No lane move or source
implementation is triggered by the handoff. A read-only snapshot of the second implementation chat now shows 05 Vim
active (18 engine conformance checks reported passing; native focus/shortcut checks underway); later queue completion
was not inferred.

## Additional feature captured 2026-10-04

[16 Viewport keyboard commands and focus switching](../2026-10-04_16_viewport-keyboard-commands/1_exploration.md)
is a separate exploration requested after the original fifteen-feature review. It records the shortcut inventory,
proposed focus/command model, Vim interaction, and the unresolved boundary between keyboard-triggered tools and
completely mouse-free operation. It is not requirements-ready or implementation-ready and is not added to batch 3.
Foundation work can proceed against existing support; complete 08/12 command coverage follows their implementations.
The original fifteen-feature statuses below remain historical snapshots, not a fresh implementation audit.

## How readiness is assessed

Feature 13 postponed by the user on 2026-10-04 after reviewing the need and the native/agent boundary. Existing
cross-sections use the in-memory model; numerical services remain in 15 and agent workflows in 01. No concrete new
consumer/workflow justified the broad proposed feature. Preserve research and unaccepted choices; resume only on
request with a specific missing capability. No active implementation depends on 13 and no implementation chat was
messaged. All fifteen items have now been reviewed: twelve have prepared packages; 09/10/13 are postponed.

- Requirements-ready: behavior, boundaries and failure expectations are sufficiently settled to write requirements.
- Design-ready: product decisions are settled and the relevant implementation route is supported by source evidence.
- Handoff-ready: requirements, concrete design and bounded implementation phases exist, with named files/interfaces,
  fixtures, expected results, verification commands and stop conditions. It still requires the normal branch/base check.
- Locally implemented: the bounded feature and its specified local checks have a completion record. This does not
  imply committed source, promotion, inclusion in the enabled stack or delivery in an integrated application.

An unimplemented prerequisite is a scheduling dependency. An undefined prerequisite API is a planning gap. They must
not both be hidden behind "integrate with feature X". A prepared handoff specifies the selected renderer/library
algorithm and an early, bounded verification phase. It does not claim that source review proves runtime behavior.
If that phase falsifies the design, stop with evidence and return to planning before building dependent UI.

## Per-feature assessment

The IDs below are identifiers, not implementation order. The user wants 01-06 first; their prerequisite closure adds
14 before 04. Follow [the execution order](1_exploration.md#implementation-order-and-first-priority).
01/02/03/04/05/06/07/08/11/12/14/15 have complete planning packages. 01/02/03/15 have local completion handoffs.
03 has an additional planned generic follow-up required by 12. Later progress of 05/06/14/04 was not checked here.
07 is planning-complete and waits for verified
03/06/14. A Ready entry in the requirements column alone does not establish implementation readiness.

| ID | Feature | Requirements | Current implementation / planning state | Next obligation / constraint |
| --- | --- | --- | --- | --- |
| 01 | [Agent skill workflows](../../3_done/2026-10-03_01_agent-skill-workflows/5_post-implementation-notes.md) | Ready | Bounded local implementation and portable verification complete | Source uncommitted. Real application Stage/Package acceptance remains for the next requested composition. |
| 02 | [Source editing foundation](../../3_done/2026-10-03_02_source-editing-foundation/5_post-implementation-notes.md) | Ready | Bounded local implementation and final patch/hash handoff complete | Consume the recorded uncommitted delta before 05/06/14; synchronous pre-group edit API is verified. |
| 03 | [Selection / Inspector](../../3_done/2026-10-03_03_selection-model-inspector/5_post-implementation-notes.md) | Ready | Original bounded implementation and shared presentation complete locally | Preserve frozen feature patch; implement the separate generic draft-display/sealed-input/focus follow-up before 12. It is not needed to start 04/07. |
| 04 | [Live clipping](../../3_done/2026-10-03_04_live-clipping-sections/3_overall-plan.md) | Ready | Planned; four phases; implementation not started | Wait for implemented 03/14. Verify prepared inspection meshes and eight GPU planes; no caps in this delivery. |
| 05 | [Vim mode](../../3_done/2026-10-03_05_vim-editor-mode/3_overall-plan.md) | Ready; user choices settled | Planned; command matrix and four phases; implementation not started | Wait for verified 02 handoff. Port the pinned engine without GTK/GLib; prove commands/undo before Qt UI completion. |
| 06 | [Source / geometry provenance](../../3_done/2026-10-03_06_source-geometry-provenance/3_overall-plan.md) | Ready | Planned; three phases; implementation not started | Wait for implemented 02/03. Verify UTF-8 spans and instance mapping; no invented final-face identities. |
| 07 | [Semantic hierarchy](../2026-10-03_07_semantic-model-hierarchy/3_overall-plan.md) | Ready; all seven choices accepted | Handoff prepared: source-reviewed technical design and six implementation phases | Wait for verified 03/06/14, including 03's shared presentation refinement. No 04 dependency; minimal-base and later 04 composition tests are specified. |
| 08 | [Anchors / attachments](../2026-10-03_08_anchors-attachments/3_overall-plan.md) | Ready; all six decisions accepted | Handoff prepared: source contract, numerical/evaluation design, six phases and executed pinned BOSL2 mapping probe | Wait for verified 03/07/14 and their closure, including scoped declaration/lifecycle and pre-publication placement hooks. Native implementation/bridge/runtime tests remain outstanding. |
| 09 | [Technical drawings](../2026-10-03_09_technical-drawings/1_exploration.md) | Partial | Postponed by user | Preserve exploration; resume projection, dimensions, layout and output decisions when requested. |
| 10 | [Interactive source editing](../2026-10-03_10_interactive-source-editing/1_exploration.md) | Scope unresolved | Postponed by user; six proposals unaccepted | Retain exploration. Establish a concrete additional workflow beyond 07/08/12 only when resumed. |
| 11 | [Component providers](../2026-10-03_11_component-provider-adapters/3_overall-plan.md) | Ready; all three choices accepted | Handoff prepared: provider/version contract, exact tested library profiles and five phases | Independent of new-feature implementations. Ship catalogs without libraries; implement and verify the real schema/matcher/generator, discovery and packaging. |
| 12 | [Contextual insertion](../2026-10-03_12_contextual-insertion/3_overall-plan.md) | Ready; all five choices accepted | Handoff prepared: source/preview contracts, source audit, examples and six phases | Wait for verified 02/03/06/08/11 closure, including 03's generic follow-up and 11 role metadata. First prove isolated deterministic candidate evaluation, then source/UI/Commit. |
| 13 | [Agent geometry analysis](../2026-10-03_13_agent-geometry-analysis/1_exploration.md) | Scope unaccepted | Postponed by user | Establish a concrete missing capability/consumer before resuming; reuse existing in-memory services and keep agent guidance in 01. |
| 14 | [Design objects / persistence](../../3_done/2026-10-03_14_design-object-persistence/3_overall-plan.md) | Ready; source storage selected | Planned; four phases; implementation not started | Wait for implemented 02/03. Verify typed declarations, the generic host hooks refined for 07, parametric fields, lossless edits and source/lifecycle undo. |
| 15 | [Geometry services](../../3_done/2026-10-03_15_geometry-services/5_post-implementation-notes.md) | Bounded shared core | Bounded local implementation complete; numerical, backend-disabled, build and regression checks recorded | Changes remain uncommitted and unintegrated; consume its recorded API and verified delta, not the unchanged base SHA alone. |

For planned features, prepared handoffs are source-reviewed designs, not claims that future code was compiled or
tested. The shared [implementation handoff standard](implementation-handoff.md) applies to every phase. No numeric
readiness percentage is used: the remaining decision or proof matters more than a misleading average.

## Recorded implementation-chat snapshot and later evidence

Chat observations below are the historical 20:45 UTC snapshot, not current live progress. The later 03 completion
record was read on 2026-10-04 and supersedes references to active 03 work. This review did not message either chat.

- **SCADMaxx assisted editing first batch implementation**, local chat `01a1030f-f743-71c0-9f96-8984e832798b`,
  owns 01/02/15 and has completed all three local implementation handoffs. Each feature has a separate branch
  and worktree. Preserve these occupied checkouts; the second chat must not duplicate their implementations.
- **SCADMaxx assisted editing second batch implementation**, local chat `01a10345-5d81-7093-87fc-3c03d3e07534`,
  is pinned and configured for GPT-6.1 Sol / Extra high. It is actively implementing 03; initial native binding cases
  passed and it is checking conflicting open buffers and native regressions. Its queue is
  **03 -> 05 -> 06 -> 14 -> 04**, each in its own branch/worktree. 07 is not automatically added to that queue.

01's completion record reports 23 artifact/provenance/lifecycle checks and the reviewed portable smoke suite passing.
Its source is in `wt-scadmaxx-agent-skill-workflows`; actual integrated application Stage/Package acceptance is deferred.
15's completion record reports 12 numerical cases, five no-Manifold cases, eight projection/export regressions and
the supported Release application/console build passing, in `wt-openscad-geometry-services`. Its verified technical
replan is recorded in [status.md](../../3_done/2026-10-03_15_geometry-services/status.md).

02's [completion handoff](../../3_done/2026-10-03_02_source-editing-foundation/5_post-implementation-notes.md) is now present,
including synchronous edit-boundary verification, separable patches and exact source hashes under
`runs/20261003-source-editing-foundation`. Its occupied checkout is `wt-openscad-source-editing-foundation`.
The first chat's completed response confirms seven unit cases, the native suite and native application build passed.

This refresh read the handoff records and current chat status; it did not rerun their builds or tests. The implementations
are local and uncommitted. Neither batch has been promoted, enabled in the selected stack or delivered together in a
new integrated release. Before consuming a prerequisite, recheck its current completion record and exact tested inputs.

## Source findings behind the plans

Inspection baseline: integrated source `4c325716b94e444637a80df3966197ce110b2b75`, plus the current control files.
Recheck actual feature bases during implementation; this retained composition is evidence, not a branch base.
The findings below describe that audit baseline. The table and handoffs above record subsequent implementation work;
baseline descriptions of missing behavior must not be mistaken for current status of 01/02/15's isolated branches.

1. `EditorInterface` already has `sourceRevision` and `sourceFingerprint`; document IDs used by HTTP are the editor's
   annotation session IDs. `ScintillaEditor` updates revisions on text changes and integrates annotation container
   undo. 02 must extend these mechanisms, not add competing counters. `setPlainText()` clears annotation history.
2. `TabManager::saveDocument()` coordinates source, `SavedViews` and annotation saving. `saveSource()` uses QSaveFile;
   `MainWindow::fileChangedOnDisk()` currently compares timestamp/size. 02 needs content-aware conflict checks while
   preserving the existing sidecar transaction behavior and explicit partial-save diagnostics.
3. `SavedViews` already stores named camera poses in `<source>.views.json`, with file fingerprints and a lock. 14
   must reconcile that personal-view behavior with reusable Views now selected to live in `.scad` source. The sidecar
   cannot remain a second authority for design Views. Existing screenshot archives serve a separate purpose.
   No unrequested compatibility importer or migration is authorized; existing user files must not be deleted.
4. `MouseSelector` yields an object/node integer. `QGLView::findObject()` calls the renderer's measurement picking;
   `PolySetRenderer::findModelObject()` selects nearby vertices/edges, and the default renderer returns no result.
   Neither is a complete surface point/normal/instance service. 03 specifies ID/depth plus world-normal passes.
   04 specifies a prepared mesh from the already evaluated preview tree: discarding fragments after OpenCSG's
   existing visibility pass alone would not reveal previously hidden surfaces. Native renderer checks are phase gates.
5. `Location` in `src/core/AST.h` stores line/column ranges, while Scintilla is configured for UTF-8. 06 must establish
   lexer byte/column/end-boundary semantics with Unicode/CRLF fixtures; assuming Qt UTF-16 offsets would be unsafe.
6. Manifold already supplies Slice, SurfaceArea and Volume. Its documented slice convention includes bottom faces
   and excludes top faces. Existing general conversion can repair invalid meshes; 15 must avoid silently measuring
   repaired geometry. It uses a strict analysis conversion and documents the slice convention.
7. CMake's TEST_SOURCES glob includes utils/core/io, not geometry. A new geometry test file requires explicit wiring;
   merely adding `src/geometry/..._test.cc` would leave an apparently tested feature untested.
8. The skill builder currently writes generated references into the authored control skill. The control snapshot
   does not include that skill tree. 01 must package a frozen staging copy and include skill inputs in the snapshot
   before its companion can be tied reliably to an integrated release.
9. Native include/library loading does not capture dirty included editors consistently. 03 now owns immutable native
   EvaluationInputs and the shared result binding. 06 and 14 consume these exact bytes rather than reading files again.
10. An external text-change notification occurs too late to split an already opened undo group. 02 adds a synchronous
    validated pre-edit boundary before beginUndoAction; 05 consumes it to close Vim insertion groups. This adds 02 -> 05.
11. UserModule already supplies native parameter/body evaluation and ModuleInstantiation supplies the resolved lexical
    context. 07 extends annotations to those hosts and observes existing binding instead of creating geometry-valued
    objects or reevaluating argument expressions. Its semantic mesh partition retains Parts before final merging.
12. 04's merged clip mesh would otherwise lose 07's per-Part visibility and ownership. The
    [shared inspection contract](inspection-presentation-contract.md) is now specified in 03, with independent fake
    provider/effect tests in 04/07 and a real combined test. Its implementation remains an owner prerequisite.
13. 08 collects parameterized reference objects during native scope evaluation, then resolves live placement before
    preview/render/export publication. Its [14/07 extension contract](semantic-extension-contract.md) defines generic
    scoped dispatch, consumer lifecycle and semantic placement passes with fake-consumer owner tests. The pinned
    BOSL2 2.0.766 probe passed six frame comparisons and two position assertions; it does not validate future native code.

Key source locations: `src/gui/Editor.h`, `ScintillaEditor.cc`, `TabManager.cc`, `MainWindow.cc`, `SavedViews.cc`,
`QGLView.cc`, `MouseSelector.cc`, `src/glview/PolySetRenderer.cc`, `src/core/AST.h`, `src/geometry/manifold/`,
`src/guitests/`, `CMakeLists.txt`, and control `experimental/scripts/{Common,Build-Windows,Build-ScadmaxxSkill}.ps1`.
Each prepared overall plan names its exact existing symbols and proposed new files.

## External research checked during this audit

The [Geany vimode README](https://github.com/geany/geany-plugins/blob/master/vimode/README) confirms a Scintilla-based
engine with GTK event glue and a GPLv2-or-later license. It also documents missing named registers/visual-block mode
and differences from Vim search behavior. This supports reuse investigation, not a claim of a proven Qt/Windows port.
The subsequent [Vim port investigation](../../3_done/2026-10-03_05_vim-editor-mode/port-investigation.md) retrieved the public
interfaces, state, command runner, motion, text-object, edit and undo sources at a pinned revision through GitHub's API.
It found GTK/GLib dependencies, global state and Visual-selection differences requiring adaptation. The technical plan
now specifies selected source files, replacements, per-editor state and the bounded command contract. The user selected
a patched engine with no GTK/GLib dependency; that port has not yet been compiled or verified.

The old [BOLTS repository](https://github.com/boltsparts/BOLTS_archive) directs developers to
[boltsparts/boltsparts](https://github.com/boltsparts/boltsparts). Pin the correct source and validate its actual
OpenSCAD distribution before freezing provider calls. BOLTS remains the user's intended standards library; the name
must not be silently replaced by BOSL2 or NopSCADlib.

The [referenced CAD skill](https://github.com/andreahaku/openscad_claude_skill) separates source/mesh modification and
reconstruction. 01 can author its own task guidance from the already-recorded user discussion without copying that
repository's scripts, fixed scoring policies or unrelated agent instructions.

## Implementation availability and next planning sequence

The original first-priority group was 01-06 plus prerequisite 14. 01/02/03 have local completion records;
the recorded implementation sequence is **03 -> 05 -> 06 -> 14 -> 04**. Later queue progress is unchecked here.
This is a convenient schedule,
not extra dependency edges:

- 03's original handoff includes the shared presentation refinement. A separate draft/input follow-up is now specified
  for 12 only; retain its separate source ownership and verification.
- 05 can start when 02's completed verification/handoff is available; it does not depend on 03.
- 06 and 14 can each start after implemented 02/03; neither requires the other.
- 04 can start after implemented 03/14. It does not wait for 06, hierarchy, anchors, drawings or geometry services.
- 15 already has a local implementation handoff for future 09/13 consumers. It is not a task to repeat in batch two.
- 07 can start after verified 03/06/14 and their closure; 04 and 07 can be developed independently on those bases.
  Its six phases cover grammar/library identity, evaluation/partition, targets/export, tree/display, scoped Customizer
  edits and native composition/handoff. There are no remaining product questions for its accepted initial scope.

08 can follow verified 07/03/14 once their generic extension hooks are available. 11 can be implemented independently
on its recorded native base; its catalog/version choices and five phases are prepared. The third implementation chat
is primed for 11 first, then 07 -> 08 -> 12 as verified prerequisites permit, including 03's separate insertion follow-up.
It waits for an explicit implementation start. 12's insertion contracts and phases are prepared. No further unreviewed
feature remains: 14 is already planned and 15 has a local implementation handoff. 09, 10 and 13 are postponed until
the user explicitly resumes them. Do not delegate their unresolved scope choices to an implementation model.

At implementation start, re-read the prepared owner contracts, record actual prerequisite SHAs and run each phase's
verification gates. See [verification commands and evidence](verification-contract.md). These twelve packages are
planning-complete for their stated scope. The eight not-yet-complete implementations still need their native/runtime proofs.
Existing local implementations remain subject to their recorded handoff and later integration/delivery conditions.
