# Design objects in OpenSCAD source: technical design

Status: implementation specification prepared, 2026-10-03; new annotations/APIs are not implemented yet.
Branch `feature/design-object-persistence`; direct prerequisites 02/03, selected `pr-6081` and `pr-6642-oep8`.
Read [requirements](2_requirements.md), [phases 1-4](4_imp-phase1.md) and the shared verification contract.
No dependency on 06/07/08/09/04. Source evidence: `4c325716b94e444637a80df3966197ce110b2b75`.

## Evidence and owned files

`parser.y` already attaches an ObjectExpression as `NativeAttributes` to Assignment. The ordinary OEP8 `Object`
class is distinct from that fixed-member attribute expression. `ScopeContext::init` evaluates effective assignments
in their lexical context; EvaluationSession is the natural owner of an optional design collector. SourceFile::instantiate
retains the evaluated FileContext. Customizer ParameterObject::fromAssignment currently sends every NativeAttributes
block to widget parsing, which would reject the new type metadata. The new dispatch must occur before that path.

New core files under `src/core/design/`: `DesignKinds`, `DesignObjects`, `DesignCollector`, `DesignReferences`,
`DesignSourceMap` (.h/.cc and tests). GUI files under `src/gui/design/`: `DesignDocument`, `DesignEdits`,
`SavedViewContribution` (.h/.cc). Change Assignment/ScopeContext/EvaluationSession, Customizer dispatch,
MainWindow installation, SavedViews/TabManager, editor undo integration and actual CMake lists.
03 owns EvaluationInputs/result guards and Inspector routing. 02 owns source transactions/save conflicts.

## Annotation and discovery contract

Freeze the working spelling as `@{type: Section}` and `@{type: View}`. The type field must be a bare Lookup expression
naming a registered kind, recognized as metadata syntax; do not evaluate it as a variable or let a variable named
Section redefine the kind. Unknown names/non-symbol type values produce a source diagnostic. Do not introduce type
keywords into ordinary object expressions. Design metadata contains only `type`; mixing Customizer widget keys into
the same block is an error. Existing blocks without type keep their current Customizer behavior and diagnostics.

Section/View declarations are file-scope assignments in the root file or its includes. An include participates in
its existing lexical scope. `use` imports functions/modules, not design records; helpers imported with use can still
construct ordinary objects. A Section/View annotation inside a module/function/local scope is diagnosed, not silently
exported or multiplied. Future registered semantic kinds may declare different scope rules in their own branch.
The RHS may be an ordinary object expression, a helper-function result or an object-comprehension result. These
values remain ordinary OpenSCAD objects; the annotation creates a discoverable application record for the declaration.

After ScopeContext finishes effective assignments, the collector reads each marked assignment's value from that
same context, validates its kind/schema and records source ownership. Do not evaluate an RHS twice or materialize
unused module scopes. Detect multiple design declarations of the same assignment name before effective-assignment
deduplication: reject rather than silently attaching an old annotation to an overriding value. Ordinary unannotated
OpenSCAD reassignment behavior stays unchanged. CLI and GUI use the same collector during native evaluation.

Collector output installs with 03's successful result binding; failed compilation leaves last-good records stale.
Per-record validation errors retain diagnostics and prevent affected consumers from treating records as usable. They
do not alter CSG geometry. Enumerating records must work without a GUI dock or any downstream feature linked.

## Stable identity and core schemas

IDs are nonempty, case-sensitive strings unique across all design kinds in one evaluated root document. They are
not assignment names, display labels, filenames or evaluation node indices. For Section/View require an explicit
string-valued `id` member in the declaration's resulting object; an object returned by a helper may supply that
string value, but IDs must remain stable by author intent. UI-generated IDs are UUID strings created once. Duplicate
IDs invalidate both records and their references; there is no first/last winner. Separate model roots have separate
registries, even when they include the same library. Save As retains the live root's object identities.

All vector numbers must be finite; dimensions/distances use the model's native units. Unknown schema members produce
a diagnostic instead of being silently dropped on GUI save. Core schemas:

| Kind/member | Rule / default |
| --- | --- |
| Both: id, label | id required; label defaults to assignment name; neither label nor name is identity. |
| Both: target | ReferenceToken; default `{domain: "document"}` means this evaluated root. |
| Both: frame | ReferenceToken; default `{domain: "world"}` is identity frame. Other domains require a resolver. |
| Section: origin, normal, up | Required origin[3], normal[3]; up defaults [0,0,1], or [0,1,0] if parallel to normal. Explicit parallel up is invalid. |
| Section: adjust | Optional object: translation[3]=[0,0,0], rotation quaternion xyzw=[0,0,0,1], offset=0. GUI-editable adjustment terms. |
| View: projection | `"orthographic"` default, or `"perspective"`. |
| View: direction, up | Unit viewing direction toward target and up; required for fit views, validated as nonparallel. |
| View: margin | Nonnegative fit margin, default 0.05 of target bounds extent. |
| View: camera | Optional fixed Camera pose with rotation[3], translation[3], distance>0, fov in (0,180). Mutually exclusive with direction/up/margin. Projection still explicit. |

Normalize normal n, project/normalize up u perpendicular to n, derive r=u cross n, giving right-handed (r,u,n).
Normalize a finite nonzero adjustment quaternion q. In the resolved frame, n'=q*n, u'=q*u,
origin'=origin+translation+offset*n'. Transform point/frame to world using the resolved rigid frame; reject non-rigid
reference frames here rather than guessing scale semantics. A normal flip is a 180-degree quaternion rotation around
u', keeping drawing up stable. Store the canonical definition and evaluated world frame separately.

Fit Views derive target bounds through a resolver, orient Camera to direction/up and call the existing Camera fit
behavior with expanded bounds. World/document targets work in this foundation; semantic target bounds come from 07.
Fixed views preserve existing Camera conventions, avoiding an unnecessary second camera representation. Invalid or
empty target bounds report unavailable rather than replacing a requested view with the current camera.

Example (new semantics, becomes executable in phase 1):

```scad
height = 40;
@{type: Section}
middle_section = {
  id: "section-middle", label: "Middle section",
  origin: [0,0,height/2], normal: [0,0,1], up: [0,1,0],
  adjust: {translation: [0,0,0], rotation: [0,0,0,1], offset: 0},
};
@{type: View}
front_view = {
  id: "view-front", label: "Front", projection: "orthographic",
  direction: [0,1,0], up: [0,0,1], margin: 0.05,
};
cube([20,20,height]);
```

## Kind registration, references and records

Namespace `Design`; registration is in-process C++ startup code, not dynamic plugins or user-defined classes.

```cpp
struct ReferenceToken { std::string domain, id; Value data; };
enum class ResolutionState { Resolved, Changed, Missing, Unsupported, Invalid };
struct Resolution {
  ResolutionState state; std::optional<Transform3d> frame;
  std::optional<BoundingBox> bounds; std::string diagnostic;
};
struct Payload { virtual ~Payload() = default; };
enum class DeclarationHost { Assignment, ModuleDefinition, ModuleCall };
struct DeclarationKey {
  std::string fileKey, fingerprint, hostName;
  DeclarationHost host;
  size_t beginByte, endByte; // half-open whole declaration in captured UTF-8
};
enum class DeclarationScope { File, Local };
struct DeclarationContext { DeclarationKey source; DeclarationScope scope; };
struct Diagnostic { std::string code, message; std::optional<DeclarationKey> source; };
struct DecodeResult {
  std::shared_ptr<const Payload> payload; // null on failure
  std::vector<ReferenceToken> dependencies;
  std::map<std::string, Value> canonicalFields;
  std::vector<Diagnostic> diagnostics;
};
struct Record {
  std::string id, kind, label; Value definition;
  std::shared_ptr<const Payload> evaluated;
  std::vector<ReferenceToken> dependencies;
  std::optional<DeclarationKey> source;
};
struct KindHandler {
  std::string name;
  std::set<DeclarationHost> hosts;
  std::set<DeclarationScope> scopes;
  std::function<DecodeResult(const Value&, const DeclarationContext&)> decode;
};
struct ResolveContext {
  std::string resultId, evaluatedInputsFingerprint, configurationFingerprint;
  BoundingBox documentBounds;
  const std::map<std::string, std::shared_ptr<const Record>>& records;
  std::vector<std::string> visitedIds;
};
using Resolver = std::function<Resolution(const ReferenceToken&, ResolveContext&)>;
bool registerKind(KindHandler); // duplicate name fails
bool registerResolver(std::string domain, Resolver); // duplicate domain fails
Resolution resolve(const ReferenceToken&, ResolveContext&);
```

DecodeResult carries either a typed Payload, extracted dependency tokens and canonical field values, or structured
source diagnostics. Registry handlers explicitly state permitted declaration scopes. Concrete Section/View payloads
and their query helpers live here. Downstream handlers own their payloads and field validation without adding those
consumer headers to the foundation. Resolvers receive immutable records, the current evaluation binding and a
visited-ID stack; no callback may edit source or recursively resolve a cycle indefinitely.
Nested resolution goes through resolve(), which owns cycle-stack push/pop. GUI code constructs this core context
from 03's current binding; core code does not include Selection or GUI headers. Existing Value is move-only: clone
the evaluated definition once with Value::clone(), then move values into records; publish shared immutable Records.
Never copy an evaluator-owned reference into a record that outlives its context. Section/View permit only File scope.

Built-in domains: `world` (identity frame), `document` (root bounds/frame), `design` (ID lookup), `geometric` (captured
world point/normal plus an evaluated-input/configuration fingerprint). Geometric references resolve only for the
same fingerprint; after geometry inputs change they return Changed until deliberately rebound. They are weaker
than named features, never nearest-surface guesses. Missing IDs return Missing; an absent semantic/anchor resolver
returns Unsupported. Design self/cycles return Invalid. 07/08 register semantic/named-feature domains later.

## Source editing without flattening expressions

DesignSourceMap starts from a marked assignment's whole parser Location and captured input. Convert one-based byte
line/columns against that input's line-start table and verify the complete annotation/assignment parse. Within this
bounded span a lossless scanner records field value ranges, delimiters and trivia: honor comments, escaped/multiline
strings and nested [],{},(). Do not discover unrelated source statements or infer geometry provenance.

GUI field editing is supported for direct object literals with unique fixed identifier/string keys, including the
nested adjust object. Computed keys, each/comprehensions, duplicate fields or a helper-call RHS remain valid evaluated
definitions but report Source-only editing. Do not rewrite a helper expression into an object snapshot.

Minimal patch rules: replace only a literal label or the selected numeric literal adjustment value; insert absent
adjust/members before the matching closing brace using local indentation/EOL/trailing-comma style. A nonliteral
adjustment term is read-only to its numerical control; provide source navigation instead of inverse solving.
Keep origin/normal/up expressions unchanged. Drag offset modifies adjust.offset; a picked origin modifies literal
adjust.translation relative to the currently evaluated base origin; rotation edits adjust.rotation relative to the
base frame. Thus height/2 remains parametric after a graphical adjustment. Reject changes if captured inputs or
selected record/source mappings went stale during the interaction.

`DesignEdits::prepare(recordId, FieldChange, Stamp)` returns 02's EditRequest or a precise error. No save occurs.
`FieldChange` is Label, Translation(Vector3d), Rotation(Quaternion), Offset(double), DeleteDeclaration or InsertRecord.
Delete removes only annotation+assignment, retaining surrounding comments; refuse if the scanner cannot establish
ownership of that annotation. Multiple changes to the same object are one validated 02 transaction. Declaration
generation serializes only a transient object's explicit definition with deterministic escaping/precision.

## Lifecycle and undo

DesignDocument belongs to the root editor; it owns transient records, current immutable evaluated records and personal
inspection state keyed by ID. APIs: createTransient(kind,definition), beginEdit(id,Stamp), updateDraft(token,changes),
cancelDraft(token), commitDraft(token), promote(ids,destinationEditor), remove(id), records(Stamp). A draft keeps its
same ID and never becomes a second SavedSection. Only one draft per ID; document/result changes cancel stale drafts.
For source-backed objects commitDraft writes source; for transient objects it updates the transient definition.

Promotion stages the source declaration and marks its editor dirty. Source persistence is complete only after
ordinary Save/Save As succeeds. Reevaluate after committed source changes; during errors keep a diagnostic state,
not a live authoritative copy silently diverging from source. Manual deletion leaves references Missing.

Promotion/delete must undo both source and transient lifecycle. Add a generic `EditorUndoRegistry` under gui/source
in this branch: an opaque container token maps to a participant with undo/redo callbacks and editor lifetime. Refactor
the existing annotation token dispatch through that registry, preserving its behavior and removing the old separate
dispatch path. Extend SourceEditing::EditRequest with an optional participant registration; append its Scintilla
container action within the same undo group as validated text edits. No participant executes before validation.
The Design participant stores before/after transient membership and backing association, never another full source
buffer. On undo/redo restore that lifecycle then refresh records from source; retained drafts preserve identity for
references. Clear participants when native history is cleared/editor closes; no token collision with annotations.
02 remains independently buildable; this extension and annotation-consumer update belong to 14's feature delta.

## Dependency closure and existing personal views

Before promotion, DFS required design-ID dependencies using handlers' extracted tokens. Detect unknown IDs, missing
handlers and cycles before mutation. Topologically serialize unsourced records into the explicitly chosen open
destination `.scad` editor, checking ID/variable collisions; one destination means one transaction. Already sourced
dependencies keep their source file and expressions. Do not add include directives implicitly. If their file is not
in the current root's include closure, fail preflight with an actionable missing-include diagnostic.

For explicit disk saving, list the involved dirty editors and call ordinary save sequentially; stop on cancel/failure
and retain per-document outcomes. Source edits may already be dirty even if a later file fails saving. Never claim
cross-document atomicity or write an unopened file. Future drawings use this same closure API.

Refactor SavedViews' camera entries to shared View definitions with a personal backing descriptor. Its existing
`.views.json` path retains only explicit personal inspection views; source-defined Views are enumerated from design
records and never duplicated there. Existing personal views remain personal until Promote to source is selected;
promotion keeps the ID, makes source authoritative and removes the active personal entry on successful source
transaction. Undo restores personal membership. Sidecar saving follows ordinary existing coordination. Do not import,
migrate, delete or rewrite old user files automatically, or introduce a legacy fallback for source-defined views.
Register SavedViewContribution with 03 for source/personal/transient origin, Apply, Promote, Rename and Delete.

## Phases

The [scoped declaration/lifecycle extension contract](../2026-10-03_00_source-first-cad-overview/semantic-extension-contract.md)
was specified during 08 planning. Add Consumer destination callbacks with bounded native scope context in phase 1,
and generic consumer lifecycle adapters in phase 3. Test them with fake kinds without semantic/anchor imports.
Keep Section/View document registry and source schemas unchanged. Record these verified hooks before 08 freezes its
base; a completed owner may supply a focused follow-up instead. Concrete local reference ownership belongs to 08.

The generic host enum, hostName/source key and KindHandler host validation above are a 2026-10-03 refinement from
07 planning and belong in this owner's phase 1. Section/View accept Assignment only. A test-only registered kind
can validate other host contexts without adding module/call grammar or semantic evaluation to 14; those remain in 07.
Assignment edit/create/promote APIs must reject non-Assignment hosts with Unsupported before inspecting RHS fields.
07 consumes these verified hooks and registers its own kinds; it must not rename shared fields or copy generic
registry infrastructure in its feature delta. No compatibility alias for the earlier proposed assignmentName is needed.

1. Kind dispatch, schemas, evaluation and source examples.
2. References and dependency closure.
3. Lossless field patches, drafts and joint source/lifecycle undo.
4. SavedViews integration, headless/native regression, packaging and handoff.

Each phase has concrete fixtures and stop conditions. The storage choice is closed; schema/runtime verification
belongs to these implementation phases and is not claimed complete by this document.
