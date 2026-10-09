# Shared design objects and persistence: requirements

Status: requirements prepared, 2026-10-03. The user selected `.scad` storage after discussing typed, annotated
objects. [Exploration](1_exploration.md) records the decision; [technical design and phases](3_overall-plan.md) specify
the source/evaluation contract. The selected `@{type: Section}` annotation is not implemented today.

## Source and evaluation

- DO-01: reusable Section/View definitions live in ordinary OpenSCAD source, in the main `.scad` file or an included
  `.scad` file. Source is authoritative for design definitions used to reproduce outputs. No separate design-sidecar
  grammar or hidden editable document model is introduced.
- DO-02: use explicitly annotated declarations with recognized design kinds and ordinary object field expressions.
  A Section or View has a validated schema; an unmarked object with similar keys does not become a design object.
  The initial mechanism types declarations, without requiring user-defined classes or new runtime types on all values.
- DO-03: evaluate fields in their OpenSCAD lexical context so parameters and helper functions can define them.
  A parameter change reevaluates the design record. Evaluated numbers never replace the source expressions merely
  because evaluation, saving, reopening or viewport inspection occurred.
- DO-04: publish design records alongside geometry for the same evaluated source revision. They do not emit CSG
  nodes or alter solid geometry. GUI and headless evaluation must agree; record discovery cannot depend on opening
  a dock. A failed/currently invalid evaluation cannot silently present an older record as current.
- DO-05: report source-located diagnostics for an unknown design kind, invalid field value or duplicate identity.
  Preserve the user's text and identify unusable records to consumers. Route design metadata separately from
  Customizer widget metadata, preserving existing valid annotations and useful unknown-key diagnostics.

## Object identity, schemas and references

- DO-06: use one semantic Section type and one View type across transient, source-backed dirty and saved lifecycle
  states. Deliberate promotion to source keeps identity and existing references. Do not create a separate SavedSection
  or drawing-only Section copy. Changing a label or assignment name must not change an explicit object ID.
- DO-07: a Section provides stable ID, label, target scope, coordinate frame, origin, normal and drawing up direction.
  Validate finite vectors, a nonzero normal and a usable up direction. Consumers use a consistent evaluated frame.
  Clip enablement/helper visibility are personal inspection state, separate from the reproducible definition.
- DO-08: a View provides stable ID, label, target scope, projection and an orientation/framing definition. Support
  deliberate fixed camera views and reproducible direction/up plus fit behavior; semantic-target extensions may
  later express canonical views relative to components. No viewport-pixel coordinate acts as a durable target.
- DO-09: references identify design objects, semantic targets or geometric descriptions with owner/context.
  Resolve them against an identified evaluation revision and expose resolved, changed, missing and unsupported
  outcomes as appropriate. Never silently retarget a missing object to the nearest geometrically similar object.
- DO-10: 14 owns generic reference tokens, result states and a resolver registration contract. Document/world and
  supported geometric references must work without 07/08. Their branches provide semantic/named-feature resolution;
  an unavailable resolver produces an explicit diagnostic. No reverse dependency on those consumers is permitted.
- DO-11: label rename and source movement retain explicit identity. Deletion leaves dependent references visibly
  unresolved; restoring the same identity allows reevaluation to resolve them. Duplicate IDs must not select an
  arbitrary winner. Follow the technical plan's root-wide ID scope, generation and include/local-scope rules.

## Source editing and persistence lifecycle

- DO-12: edits to source-backed definitions use 02's captured document/revision/fingerprint and minimal byte patches.
  One logical edit is one normal undo action. Preserve unrelated text and comments. Reject stale, read-only, closed
  or ambiguous source targets before mutation. An included file must be an explicitly identified open editor.
- DO-13: interactive previews may change a transient working state without rewriting source on every gesture.
  An accepted edit to a source-backed definition commits a source transaction; cancellation preserves its original
  definition. Expression-based fields must retain their parametric relationships: change an explicit editable term
  or use a documented expression-preserving transformation. If the intended change cannot be represented safely,
  explain the limitation and offer source editing instead of substituting a numeric snapshot.
- DO-14: creating/promoting a reusable object adds its declaration to the intended live source buffer and marks it
  dirty. Ordinary Save/Save As performs the disk write with 02's conflict protection. Untitled documents can contain
  declarations; they are not durably saved until source Save As succeeds. Cancel/failure retains editable state.
- DO-15: persisting a consumer must include its unsaved design-object dependency closure, without duplicating IDs
  or leaving dangling references. Preflight missing/unserializable dependencies before editing. New declarations
  belonging in one document use one transaction. Existing declarations in other documents retain their ownership;
  multi-document saves report partial outcomes and never claim atomicity. Do not silently write unopened files.
- DO-16: source-backed records update coherently after typing, GUI edits, undo/redo, reload and Save As. Track current
  source association separately from stable object identity. A new model/tab cannot inherit another model's objects
  simply because an assignment has the same name.

## Personal state and integration boundaries

- DO-17: selection, camera history, temporary visibility and casual agent markup remain personal/workspace state.
  A personal view becomes a reusable source definition only through deliberate promotion. Existing screenshot
  annotation archives retain their distinct purpose; sharing identity machinery does not merge annotation UIs.
- DO-18: reconcile existing `SavedViews` camera persistence with this lifecycle. `.views.json` must not be a second
  authority or fallback for source-defined Views. Retain only distinct personal-inspection behavior and update its
  consumers to the shared model. Do not add a legacy importer/migration or delete existing user sidecar files.
- DO-19: own the generic declaration/kind mechanism, Section/View schemas, reference lifecycle, dependency closure
  and saved-view Inspector contribution. 04 owns clipping; 07/08 add semantic/named-reference kinds; 09 owns drawing
  kinds and layouts. Consumers register with the common mechanism rather than inventing independent storage.
- DO-20: develop on 02/03 plus the selected OEP8 (`pr-6081`) and Customizer (`pr-6642-oep8`) baseline inputs. Deliver
  a complete foundation usable without 04/06/07/08/09, and preserve the existing object and Customizer syntax.

## Acceptance examples

1. Declare a Section with `origin: [0, 0, height / 2]`; change `height` from 40 to 60. Its evaluated origin changes
   from z=20 to z=30, the expression stays intact, and the solid geometry is identical with/without the declaration.
2. Put that definition in an included `.scad` file. Evaluation resolves its parameter context; an explicit GUI edit
   targets that file's live buffer. A stale revision or unopened target cannot cause a hidden disk write.
3. Create a transient Section, reference it from another design record, then promote it. Both references still name
   one ID. Undo/redo restores declaration/lifecycle state coherently. Save/reopen reproduces the same definition.
4. Rename its label and assignment, then move the declaration while preserving its ID. References stay resolved.
   Delete it: consumers report missing. Restore it: they resolve again. Duplicate it: report an identity conflict.
5. Edit a literal field around comments and Unicode text. Only intended bytes change; one undo restores them.
   Attempt an unsupported edit of a derived expression: its parameter relationship and source bytes are preserved.
6. Save a dependent object with an unsaved Section/View. Its closure is persisted without copies. Simulate a conflict
   in an already-owned second source document: report which documents remain unsaved and retain their buffers.
7. Compile invalid metadata or a zero normal; show a source diagnostic and prevent consumers treating it as current
   valid data. Unmarked ordinary objects and existing Customizer annotations retain their previous behavior.
8. Open two models with similarly named variables, change tabs during an edit and save one under a new filename.
   No object crosses document ownership; explicit IDs and source association remain coherent.
9. Use the foundation without hierarchy, anchors or clipping linked. Section/View enumeration, lifecycle, source
   editing and document/world references work; unsupported semantic tokens report their missing resolver.

## Technical contract and implementation verification

The technical plan defines discovery/scope, dispatch, schemas, IDs, references, source edits, closure and SavedViews
integration without requiring 06. Execute its four phases and fixtures against implemented 02/03, including native
undo and headless declaration evaluation. The source-versus-companion storage question is answered.
