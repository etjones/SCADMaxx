# Semantic model hierarchy: technical design

Status: implementation in progress, 2026-10-04; see [current checkpoint](status.md). All seven product choices are accepted.
Read [requirements](2_requirements.md) and [accepted examples](source-authoring-proposal.md).
Source branch `feature/semantic-model-hierarchy`; direct prerequisites 03/06/14 plus selected OEP8/Customizer entries
and their closure. No 04/08/09/10/12 implementation dependency. The technical design below remains authoritative.

## Evidence, base and ownership

Read-only audit: `wt-scadmaxx-20261002`, HEAD `4c325716b94e444637a80df3966197ce110b2b75`. This is source evidence,
not the feature's future base. Record a prerequisite-only composed base and exact verified deltas before coding.
03's [inspection presentation contract](../../1_planning/2026-10-03_00_source-first-cad-overview/inspection-presentation-contract.md)
must be implemented in its owner and verified before 04/07 freeze their bases. Undefined/missing owner APIs stop
preflight; do not absorb untracked prerequisite changes into this feature's delta.

Existing seams inspected: parser.y attribute_block applies to assignments; UserModule carries name/parameters/body;
ModuleInstantiation::evaluate resolves an InstantiableModule with defining_context; UserModule::instantiate creates
UserModuleContext and a GroupNode. Parameters::parse binds actual arguments and then evaluates omitted defaults in
defining_context. ScopeContext/FileContext preserve native include/use lookup. GroupNode already retains geometry
without requiring a new primitive type. ParameterWidget's existing applyParameters mutates global Customizer values;
instance edits must use a separate source-backed adapter. MainWindow::actionExport currently exports rootGeom only.

New core `src/core/semantic/`: SemanticKinds, SemanticCollector, SemanticScene, SemanticParameters, SemanticTargets
(.h/.cc and focused tests). New GUI `src/gui/semantic/`: SemanticController, ModelTreeModel, ModelTreeDock,
SemanticParameterPanel, SemanticSourceEdits, SemanticMeshJob, SemanticExportJob, SemanticInspectorContribution.
New `src/guitests/TestSemanticHierarchy.{h,cc}` and fixtures `testdata/scad/semantic/`.
Extend parser.y, UserModule/ModuleInstantiation AST metadata, ScopeContext/Parameters binding observation,
EvaluationSession, MainWindow/ParameterWidget/exports and actual CMake/resources. Consume 14's generic host hooks.
03 owns the generic display/pick/Inspector infrastructure, 06 source spans, 02 edits and 14 reference infrastructure.
07 owns semantic data/enrichment and registers contributions; foundations never import semantic headers.

## Grammar and annotation hosts

Use the accepted syntax verbatim. Extend declaration/call reductions, not expr: there is no module-valued expression.
Attach immutable NativeAttributes plus 06 byte spans to UserModule and ModuleInstantiation. Annotated module calls
must directly name a Part/Assembly module; place transforms outside a braced annotated call as in the example.
Component calls have no supplied child block in this version; reusable geometry lives in the definition's body.
Ordinary helper modules and normal argument expressions remain supported inside definitions.

| Host / kind | Metadata fields and validation |
| --- | --- |
| File-scope module / Part or Assembly | type bare registered symbol; id required nonempty string literal; label optional string literal, default module name. |
| Module call / Component | type bare Component; id expression evaluated once in caller scope to nonempty string; label optional string expression, default definition label. |
| Assignment / Section or View | Unchanged 14 schema: annotation only type; data in RHS object. |

Unknown/duplicate fields and kind/host mismatches are source diagnostics. Existing Customizer blocks without type
retain their assignment-only rules. Recognize type syntactically, never resolve a variable named Part or Component.
Definition IDs are literals so discovery never executes unused module bodies or library assignments to find IDs.
Dynamic loop keys belong on Component calls. Nested/local semantic definitions are diagnosed; ordinary local helper
modules remain legal. Annotated definitions cannot be redeclared/shadowed within the same effective file scope without
a diagnostic; preserve ordinary unannotated redefinition rules. Bare calls to marked templates diagnose missing
Component metadata; do not invent an instance key. Unannotated modules elsewhere retain normal behavior.

Refactor the module-definition parser midrule into one common declaration production so annotation/no-annotation
paths share parameter/body scope handling. Component metadata attaches to single_module_instantiation and keeps
existing !/#/%/* modifiers associated with that call. Source spans include annotation and full host; child argument
spans remain separately available. Pretty printing preserves attributes for debug output, but editing never relies
on a pretty-printed AST. Require no new unresolved parser conflicts versus the selected baseline.

14's owner plan now supplies DeclarationHost {Assignment, ModuleDefinition, ModuleCall}, hosts in KindHandler,
and generic hostName/host in DeclarationKey. Require those verified hooks in the prerequisite base; do not rename
shared fields in this feature. Section/View handlers accept Assignment only. DeclarationContext identifies host
and scope. Semantic kinds declare their own allowed
metadata keys; keep 14's Section/View type-only rule. Register Component as a call host handler but collect its records
in the semantic instance index, not 14's document-global ID map. All decoding/identity validation uses the shared
registry, with semantic payloads owned by 07.
Generic 14 assignment-field editing, transient creation and promotion must reject ModuleDefinition/ModuleCall hosts
as Unsupported. They cannot treat a module body as an object RHS. Semantic definitions are source-authored here;
07's parameter edits below are the only new source-writing UI. Source label/ID edits use ordinary editor behavior.

## Libraries, evaluation and parameter capture

Enumerate file-scope marked definitions from the captured root/include AST and reachable use-library ASTs in 03's
request-local parse cache. Definition identity is the explicit id across that evaluated root, including unused public
definitions. Repeated discovery of the same fileKey/declaration occurrence deduplicates; distinct declarations sharing
an ID invalidate both, including collisions with Section/View IDs. Canonical fileKey is 03's captured-input key,
not a second path canonicalizer. Do not traverse beyond the native captured include/use closure.

Normal native lookup decides which module a call resolves to. Use imports marked module definitions, never that
library's top-level geometry, Components, Sections or Views. Included top-level Components follow normal include
execution. Library metadata does not cause eager FileContext/body execution. Retain the definition's AST and native
scope locator in the owned EvaluatedScene backing; instantiate its default preview/export lazily in a separate job
using that native defining context. A hidden/shadowed definition remains inspectable by its source declaration key,
not by resolving a same-named module in the caller. Do not evaluate library assignments twice in the main evaluation.

At ModuleInstantiation::evaluate, resolve the native callable once and validate Component's target kind. Evaluate its
id/label once in caller context. A session-owned RAII semantic stack establishes nearest Assembly parent and rejects
Component nesting inside a Part. UserModuleContext uses the unchanged Parameters::parse algorithm. Add an optional
binding observer to that path: record actual winning argument ordinal/name, cloned bound Value, default expression
or argument expression span, and whether native duplicate/extra argument diagnostics made binding ambiguous.
Never rerun expressions merely to obtain Inspector values. Ordinary calls have no observer overhead beyond null checks.

Register each entered Component and capture the returned existing GroupNode plus 06 invocation ID. Pop RAII state on
success/exception. `if` branches not executed and `*` disabled calls emit no instances; duplicate siblings in executed
branches fail. Keep deterministic emitted source order for tree presentation; identity never uses that order.
After root-tag handling retain only instances present in the installed evaluated tree. A `!` root inside a Part
that discards its semantic boundary is an unsupported composition diagnostic, not a guessed partial Part.

## Immutable semantic records and identity

Use move construction / Value::clone for move-only Values; immutable shared snapshot ownership outlives workers.
Namespace Semantic; core types contain no Qt:

```cpp
enum class DefinitionKind { Part, Assembly };
enum class Origin { DefinitionDefault, LiteralArgument, ExpressionArgument };
struct ParameterBinding {
  std::string name; Value value; Origin origin;
  std::optional<SourceProvenance::Span> expression;
  std::optional<size_t> argumentOrdinal;
  bool ambiguous;                          // duplicate/extra native binding diagnostics
};
struct Definition {
  std::string id, label, moduleName; DefinitionKind kind;
  SourceProvenance::SyntaxKey syntax; SourceProvenance::Span declaration;
  // owned AST/scope locator in scene backing; declaration parameter/default spans
};
struct Instance {
  std::string path, parentPath, key, definitionId, label;
  uint64_t invocation;                    // 06's result-local Instance::id
  SourceProvenance::SyntaxKey call;
  std::vector<ParameterBinding> parameters;
  std::shared_ptr<const AbstractNode> localRoot;
  Transform3d localToParent, localToWorld;
  std::vector<std::string> children;
};
struct Scene {
  std::string resultId, inputsFingerprint, configurationFingerprint;
  std::map<std::string, Definition> definitions;
  std::map<std::string, Instance> instances;
  std::map<SourceProvenance::SyntaxKey, std::vector<std::string>> callInstances;
  // owned evaluation backing, diagnostics, residual roots and node -> deepest Part mappings
};
```

The root parent path is empty. Escape key segments with JSON Pointer escaping (~ -> ~0, / -> ~1), then join with /.
Store raw keys separately; paths are case-sensitive UTF-8. Definition IDs and paths are different target classes.
Duplicate definition IDs invalidate their global records; duplicate sibling keys invalidate the semantic scene for
targeting/display installation. Keep diagnostics and stale last-good UI; never install a partly overwritten index.
Native source/evaluation errors also invalidate current semantic tools. Labels are not keys; reordered calls preserve
paths. ID/reparent/delete resolves Missing, with source navigation where possible, and never retargets by shape.

Postwalk the evaluated node tree to compose transforms outer-to-inner and map leaves to the deepest Part. Use the
existing transformation conventions; a Component's local frame is its module-call entry, so transforms inside the
Part remain part of its geometry. For nested Assemblies accumulate local-to-parent along traversal rather than
inverting a possibly singular world matrix. Keep affine transforms including reflection/nonuniform scale; consumers
requiring a rigid frame reject those explicitly. Local export can still work when placement is singular; As placed
reports an invalid/degenerate result if the existing backend cannot export it.

## Geometry partition and target preparation

Part localRoot is its already evaluated GroupNode including its finished boolean geometry. Assembly localRoot retains
its internal Component placements. Do not add geometry wrappers that change union/difference evaluation or cache keys.
Across semantic boundaries allow grouping, transforms and colors; explicit boolean/render/hull/minkowski/extrusion/
projection operations enclosing a Component are unsupported and diagnosed. Explicit union of Components is also
outside the contract; an Assembly groups them. Operations inside a Part are ordinary native geometry operations.
An Assembly body may use control flow/helper modules to emit Components but may not emit loose primitives. Unassigned
geometry belongs outside Assemblies, in Other geometry. Diagnose anonymous output in an Assembly at its source.

Build the display partition by walking outside Part boundaries: collect each deepest Part localRoot with its world
transform and visual role; stop at that boundary. Collect maximal semantic-free residual subtrees with their ancestor
transforms as Other geometry. An anonymous subtree may contain its own arbitrary native CSG. Reject an unsupported
operation crossing semantic/residual boundaries before attempting to extract it. Grouping itself introduces no
cross-Part manufacturing boolean. Respect background/highlight roles without making background surfaces pickable.

SemanticMeshJob retains 03 EvaluatedScene, constructs its own Tree/cache and serializes backend work using existing
evaluation lock discipline. Evaluate each Part/residual subtree with GeometryEvaluator, convert through existing
supported geometry-to-PolySet paths and publish InspectionPieces. Do not rerun source or change $preview. Deduplicate
mesh storage only by native geometry cache key plus captured configuration, never definition ID alone. Empty Part
geometry is a valid empty row; unsupported 2D/nonconvertible inputs keep inspection status explicit, while ordinary
2D rendering/export remains available through existing native paths. No new geometry repair/backend or exact volume
service is introduced. Preserve per-Part identity before whole-document export/final CSG can merge it.

## Reference resolver and target API

Publish Part/Assembly definition records into 14's global record map with SemanticDefinitionPayload. Component paths
live in Semantic::Scene, sharing the same successful result. They do not collide with an unrelated Section named
left. Register domain `semantic`, requiring data.role = "definition" or "instance"; id is a definition ID or encoded
full instance path respectively. `data` is an ordinary object; unknown fields/roles are Invalid.

`resolveTarget(token, expectedResult)` returns {Resolved/Missing/Changed/Unsupported/Invalid, retained scene,
target root, localToWorld, parameter bindings, optional bounds, diagnostic}. Resolve definitions through their retained
declaration/default job, never an arbitrary existing instance. Define bounds lazily from prepared local geometry;
until available return Unsupported with Preparing target geometry, request asynchronous preparation, then notify 14
to refresh consumers. No backend computation on the GUI thread from a resolver callback. Cache by result/target/role.
A definition target frame is identity in its own local space, an instance target frame is its actual localToWorld.
Bounds delivered to 14 are in the same world/document space as that frame's transformed target; preserve local bounds
separately in 07. 14 rejects non-rigid frames for Sections rather than silently discarding scale/reflection.

Stale input/configuration returns Changed even when an identical path exists. An updated current result re-resolves
the explicit key; it does not reuse draw/node IDs. Definition-ID collisions and malformed tokens return Invalid.
Section/View dependencies refer to these tokens through 14's resolver; ordinary root Sections continue to work
without 07. Named anchors, face/edge topology and attachment math remain with 08.

## Tree, selection and display

ModelTreeModel is QAbstractItemModel backed by one immutable semantic snapshot. Display actual Components beneath
their Assembly parent and a separate Definitions section with Part/Assembly icons. Definition rows emit no geometry.
Without semantic definitions/instances, show exactly Model; with a semantic model include Other geometry only when
unassigned emitted geometry exists. Empty reusable definitions remain accessible. Diagnostic/stale state is visible.

SemanticController owns selected target, hidden paths and optional solo path per live document. Do not save these in
source or treat them as suppression. On reevaluation retain only existing keys and drop invalid hide/solo targets.
Effective visibility = no hidden ancestor AND within solo subtree (when set); solo does not erase eye states.
Click selects without altering eyes/solo. Clearing solo restores prior visibility. Definitions have no eye toggle.

Publish the provider/masks through 03's shared inspection coordinator; never replace QGLView's renderer privately.
Map each prepared Part drawId to its instance path; Assembly tree selection highlights its descendant visible pieces.
Other geometry has no durable semantic ID. On ordinary renderer hits use 06's exact deepest owner if available;
ambiguous merged output stays unavailable until the prepared display is ready. Never nearest-bound/triangle-guess.
Tree selection of a hidden item remains possible and does not show it automatically. Fit uses selected target bounds;
Inspector reports transforms, definition/source links, parameter provenance and validity.

Provide show/hide, solo, fit, select/highlight, Go to definition/call and Export for applicable rows. Create Section
uses a transient 14 Section targeting the selection; it is available only with valid bounds/frame. Drawing/anchor
actions are registered by later consumers, with no nonfunctional placeholder commands here. Navigation/tool routing
and overlays use 03. Source edits and result changes cancel stale operations across all panels.

## Parameter inspection and edits

Add a scoped panel to the existing Customizer dock: Selected instance, explicit Definition defaults, and All parameters.
All parameters is a grouped, read-only inventory of current instances and definition signatures, with navigation to
their owner panel. Existing global Customizer remains available and unchanged for ordinary models. Semantic controls
do not create preset JSON or pass through ParameterWidget::applyParameters. Reuse existing bool/number/string/vector
widgets through a value/callback adapter; first delivery uses type-derived controls without new parameter annotation
syntax. Show objects/functions/undef/nonfinite/heterogeneous vectors read-only with source navigation.
Supported editable literals are booleans, finite signed numbers, strings and flat finite numeric vectors; nested
expressions, comprehensions and computed vectors remain source-only even when their current Value has a simple type.

Instance controls show effective Value, origin and expression text. Numeric edits are enabled only when:
the source owner is an open writable editor, 06 validates the span against 03 captured inputs, native argument binding
is unambiguous, the call SyntaxKey occurs once across the whole evaluated invocation map (not merely visible rows),
and the existing argument is a supported literal or is absent. Expressions such as width + 10 remain read-only.
Count calls even if hidden or excluded by a root modifier so editing cannot affect a concealed second invocation.
A repeated call site's literal is still shared; navigate to source with Shared call site feedback instead of editing
one instance by silently changing every use. This is an explicit first-delivery capability limit, not a hidden store.

For a unique call's omitted parameter, insert a named argument before its closing parenthesis, adding a comma only
when required by the existing list. For a literal positional/named argument, replace only its expression span.
Reset override removes a named argument and its adjacent delimiter only when comments can be retained exactly;
positional reset or ambiguous trivia is source-only in this delivery. Never rewrite the entire call.
Definition defaults require deliberate Edit definition defaults; display that all default-inheriting uses can change.
Literal defaults can be replaced; an absent default can receive = literal at its parameter span. Expression defaults
remain read-only. Library defaults require opening that library's writable editor and using this explicit action.

SemanticSourceEdits builds 02 EditRequest with exact expected bytes, revision/fingerprint and one undo group. Lexed
token boundaries from 06 determine insert/remove spans; preserve comments, BOM, newline style and untouched bytes.
Serialize supported literal Values with finite, round-tripping numeric precision and normal SCAD string escaping.
Reject on any failed guard before prepareExternalEdit/beginUndoAction; no auto Save, disk patch or compatibility alias.
After commit invalidate old controls, perform ordinary reevaluation and rebind the selected path. Undo restores
source normally; recompute semantic state, never maintain a second parameter authority. The 02 pre-group hook lets
05 close Vim insertion correctly without requiring 05 to build this feature.

## Targeted export

SemanticExportJob accepts an explicit target token, current Stamp, coordinate choice Local (default) / As placed,
existing file format/options and captured evaluation configuration. Display target path/definition, values and
Preview/Render configuration in the export UI. Component export evaluates its frozen localRoot, not the default
module and not the visibility-filtered display mesh. Source is never rerun with a different $preview implicitly.
Assembly-local output retains internal relative placements; As placed transforms the completed target by its captured
localToWorld. Local output is obtained directly, not by inverse-transforming merged world geometry.

Definition export runs a separate native instantiation of that exact definition in its captured lexical/library
environment with an empty argument list. Retain captured global Customizer/configuration inputs, use the definition's
own parameter defaults, and do not copy any selected instance's arguments. Resolve nested Components with the same
rules in that isolated target job. Missing/invalid default parameters report a target error, no arbitrary instance
fallback. This derivative evaluation does not replace the document's current semantic tree or result binding.

Use existing GeometryEvaluator, backend validity/dimensionality checks and exportFileByName/export option dialogs.
Extract shared export-options handling from MainWindow without switching its rootGeom or renderedEditor globals.
Expose only existing compatible formats; no new STEP or BOM exporter. Whole-model exports keep native behavior;
separate semantic meshes do not alter the output format's ordinary aggregate/union policy.
Hide/solo, renderer clipping and other inspection state are absent from the target request. Reject stale targets
before work and before committing output. Write to a temporary sibling, then atomically publish with QSaveFile;
on cancel/failure remove only the job's temporary file and preserve any existing destination. Workers hold scene
ownership and obey the existing backend lock; never operate on MainWindow's mutable Tree.

## Phases and acceptance gates

The [semantic extension contract](../../1_planning/2026-10-03_00_source-first-cad-overview/semantic-extension-contract.md), specified
during 08 planning, adds current-scope access and pre-publication placement passes to this owner. Implement/test the
generic driver in phase 2 with a fake pass, without Anchor/Attachment headers. The concrete graph/math stays in 08.
Record the verified hook revision in the handoff before 08 freezes its base; an already completed 07 would require
a focused owner follow-up. This extends source evaluation, not renderer-only placement or a reverse dependency.

1. [Grammar and declaration/library identity](4_imp-phase1.md): SH01/02/10/11/19/20.
2. [Evaluation, parameter capture and partition](4_imp-phase2.md): SH02-06/10-13/18/19.
3. [Targets, references and export](4_imp-phase3.md): SH03/13/14/17/19.
4. [Model tree and composable display](4_imp-phase4.md): SH05/12/15/16/18/20.
5. [Customizer and guarded source edits](4_imp-phase5.md): SH06-09/12/19.
6. [Native regressions and composition handoff](4_imp-phase6.md): all SH01-SH20.

Each phase must leave a buildable increment and pass its named checks before the next. Use the shared
[verification contract](../../1_planning/2026-10-03_00_source-first-cad-overview/verification-contract.md). Early failures return
to a focused technical correction; do not ask Sol to silently weaken product decisions or invent new source forms.
