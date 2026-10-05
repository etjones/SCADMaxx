# Shared design objects, persistence and reference lifecycle

Planning review: the user selected OpenSCAD source storage on 2026-10-03. [Requirements](2_requirements.md) are
prepared, with [technical design and four phases](3_overall-plan.md) defining evaluation, edits and shared APIs. See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Status: planning. Added after recovering C's earlier five exchanges on 2026-10-03. Sources: chats C/D/A in the
[overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md).

## Why this needs its own feature

Saved sections, views, annotations and drawings must reference the same design objects, survive source changes and
reproduce outputs. Storage cannot be independently reinvented by every dock. This shared feature owns document
objects, persistence and reference resolution; the feature-specific UIs and geometry operations remain elsewhere.

The recovered user discussion establishes these constraints:

- Reconsider saved views, annotations and sections once semantic model targets become first-class.
- Sections used for drawings need a reproducible definition; the user specifically proposed expressing them in code.
- Do not duplicate one concept into a stable type and an ephemeral type.
- Moving definitions to a separate text file does not eliminate external-editor unsaved-change conflicts.
- Graphical changes should modify the live text-buffer representation, with normal save/conflict handling.

The user resolved storage after discussing typed, annotated objects: "yes, that was it. So they live in openscad
source." Reusable definitions live in the model's `.scad` source or an included `.scad` file, using existing object
and annotation notation with recognized design kinds. Fields can use ordinary model expressions. This supersedes
earlier assistant proposals for a `.scadproj` sidecar. Personal inspection state remains a separate concern.
No external-editor broker, CRDT or automatic disk rewriting is needed.

## Single object model, multiple lifecycle states

Use one Section type whether unsaved in memory or backed by a saved declaration. Saving attaches persistence to the
same object, not a second `SavedSection` object. Apply the same principle to View and relevant annotation objects.
Runtime manipulation, backing document, dirty state and save are lifecycle properties, not alternate semantic types.

Proposed Section data: stable ID, label, target scope, frame, origin, normal, drawing up direction and optional
semantic references/offsets. Renderer enablement and helper visibility are inspection options. A drawing up direction
is needed even though rotating a mathematical clipping plane about its own normal does not change the clipping.

Proposed View data: stable ID/label, semantic target, projection, direction/up or a canonical front/top/etc. relation,
fit rule/margin, and optional deliberate fixed camera. Prefer "front of component X" and "through axis Y plus offset"
over arbitrary world/pixel coordinates where those semantic relations describe the intended output.

## Reproducible design versus personal inspection

Definitions required to reproduce an output travel with the design: named sections/views, dimensions, drawing layout,
semantic references, deliverable annotations and render presets. Current selection, temporary visibility, camera
history and casual inspection/agent markup can remain workspace/session state. A saved personal inspection view is
not automatically an output definition; promotion must be explicit and keep the same underlying object identity.

Keep annotation purposes distinct: agent markup/feedback, semantic model notes such as a required flat face, and
drawing notes/callouts such as `SECTION A-A` or `4x M6`. Share identity/storage machinery where appropriate without
forcing all purposes into one annotation UI or automatically turning screenshot markup into source.

## Reference resolution and persistence closure

- Store semantic IDs, named anchors/features and geometric reference descriptions instead of screen pixels.
- Bind references against the evaluated source revision; a last-resolved source hash can provide useful diagnostics.
- Rebind by stable identity after evaluation; report resolved/changed/missing states and surface unresolved targets.
- Never silently retarget a deleted component to a geometrically similar one.
- Persist dependencies transitively: saving a drawing that uses an unsaved Section also persists that Section.
  It must not manufacture an independent drawing-only copy or leave a dangling reference.
- Define renaming, deletion, reparenting, source movement and reference recovery behavior explicitly.

## Text editing and storage contract

Reuse document revision, patch, undo, dirty/save and disk-conflict behavior from
[02](../2026-10-03_02_source-editing-foundation/1_exploration.md). Edit the actual `.scad` buffer containing the
declaration, including an explicitly identified open included file. Changing a design object does not silently save.

The [technical design](3_overall-plan.md) freezes schemas, file-scope discovery, field-level serialization, ID creation
and untitled lifecycle within this selected storage model. Preserve lexical text for UI edits to definitions.
Do not implement source-only geometry editing just to save a section, or require every inspection gesture to commit.

## Order and evidence

Build the complete generic object/lifecycle and document-edit contract on source transactions and picking. This
unblocks saved clipping planes without a full semantic assembly system. Expose reference tokens, resolution states
and a small resolver interface. Concrete semantic-target rebinding belongs to the dependent
[07](../2026-10-03_07_semantic-model-hierarchy/1_exploration.md) branch; named-feature resolution belongs to
[08](../2026-10-03_08_anchors-attachments/1_exploration.md). Neither implementation is imported by this foundation.

Consumers are clipping (04), drawings (09), semantic/reference extensions (07/08) and relevant agent features.
This branch also adds saved-view commands through 03's Inspector contribution interface.
Validate same-object save, reopen, undo, externally modified declaration files, dependency closure, parameter-driven
updates, stable label rename, missing targets and preservation of separate inspection/geometry/documentation state.

## Branch boundary

Proposed source branch: `feature/design-object-persistence`, with 02/03 as direct prerequisites and selected
`pr-6081` / `pr-6642-oep8` object/annotation support as existing baseline inputs. Own Section/View
data, generic reference lifecycle, dependency closure, declaration-document integration and saved-view contributions
to 03. All reusable declarations use the shared `.scad` representation; dependent branches register kinds instead
of inventing competing stores. Test document-level/geometric references and explicit unresolved tokens without needing
07/08; their branches add resolution and their own semantic fixtures. This is one completed foundation, not an early
partial branch that later imports its consumers. Existing agent screenshot annotations retain their distinct purpose;
integrate only deliberate shared lifecycle needs, without silently replacing their archive format. See
[branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Existing implementation to reconcile

The source audit found `src/gui/SavedViews.h/.cc`, already saving named camera poses to `<source>.views.json` with
document identity, IDs/labels, camera projection/rotation/translation/distance/FOV, fingerprints and a file lock.
`TabManager::saveDocument` coordinates its source-save callback with annotations. Reusable design Views now belong
in `.scad`; the existing personal camera-view behavior must use the same View lifecycle without becoming a second
authority for reusable definitions. Retain only distinct personal-inspection behavior and update affected consumers.
No compatibility importer or automatic migration is authorized. Do not delete existing user sidecar files.

The technical plan now defines file-scope discovery, parameter evaluation, Section/View examples, stable IDs,
untitled lifecycle, dependency closure, lossless field patches and personal-view promotion. Its implementation
phases must verify these contracts before downstream code uses them; no runtime proof is claimed by this exploration.

## Accepted source representation and specified technical design

The user accepted storage in OpenSCAD source after the typed, annotated-object explanation. Use a small
typed-declaration extension built on existing object and annotation notation. The technical plan selects the spelling
below and its exact scope/schema semantics; implementation must verify the parser, not assume it already executes.

Verified against the integrated source's `doc/customizer-attributes.md` and the control fixture
`experimental/fixtures/oep8-customizer.scad`: ordinary OEP8 objects use `{key: expression}`, and `@{...}` currently
attaches fixed-member metadata to the next assignment. It currently supports Customizer keys, not design-object types.
Unknown Customizer keys are diagnosed. The proposed example below is therefore not currently executable syntax.

```scad
height = 40;

@{type: Section}
middle_section = {
    id: "section-middle",
    label: "Middle section",
    origin: [0, 0, height / 2],
    normal: [0, 0, 1],
    up: [0, 1, 0],
};
```

Proposed meaning: the annotation declares a recognized design kind; the object supplies ordinary evaluated fields.
Section/View are native recognized identifiers, not arbitrary strings such as `kind: "section"`. Each kind has a
known schema and validation. Evaluating a marked declaration produces a typed application design record alongside
geometry; it does not emit a clipping plane into CSG. Unmarked ordinary objects do not become design records merely
because they contain familiar field names. The technical plan freezes this spelling for the first implementation.

This is a language-semantic extension even if the parser can reuse existing grammar. The bounded initial design
uses type identity on discoverable declarations; ordinary objects and helper functions construct their field data.
It does not require a general static type system, user-defined classes, or type identity on arbitrary function values.
The technical plan specifies file-scope declarations in the root/includes; use imports helpers, not design records.
Section/View declarations in local or repeated module scopes receive diagnostics.

Reevaluation uses model expressions, so height/2 stays parametric. Graphical edits must preserve such expressions:
an explicit offset may be changed as an offset; the UI must not silently replace height/2 with a numeric snapshot.
Source expressions remain authoritative, with evaluated fields used by clipping/drawing consumers. A marked named
definition may live in the main source or an included source file under the selected scope/evaluation rules.

The technical design specifies declaration validation, source association, dependency reevaluation and
expression-preserving UI edits. Route design metadata separately from Customizer widget
metadata without weakening unknown-key diagnostics. OEP8/Customizer are existing selected baseline inputs for
this branch. Feature 14 owns the generic mechanism and Section/View kinds; 07/08/09 register their own semantic,
reference and drawing definitions without creating a dependency from this foundation back to those consumers.
