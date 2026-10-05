# Source/geometry provenance: technical design

Status: implementation design prepared from source inspection on 2026-10-03; fixtures below are future checks.
Branch `feature/source-geometry-provenance`; prerequisites 02/03 plus selected OEP8/Customizer and their closure.
Use [requirements](2_requirements.md), [selection's contracts](../2026-10-03_03_selection-model-inspector/3_overall-plan.md)
and [source transactions](../2026-10-03_02_source-editing-foundation/3_overall-plan.md).

## Inspected path and file ownership

Audit source `4c325716b94e444637a80df3966197ce110b2b75`: `lexer.l` advances columns by yyleng (UTF-8 bytes),
initializes line/column at 1, and uses an exclusive end. CR consumes one byte; LF advances the line. The old
text-mode include reader may translate CRLF; 03 replaces it with captured binary input. String/comment states need
explicit token-start handling because LOCATION_ADD_LINES resets first coordinates within a multiline token.
`Location` currently holds file/line/column, not editor revisions or durable IDs.

`ModuleInstantiation::evaluate` invokes the resolved module; `UserModule::instantiate` has both definition context
and call-site arguments. `LocalScope::instantiateModules` walks child calls, including repeated evaluation. CSGTreeEvaluator
creates leaves with node indices/transforms; normalization and geometry caches must not invent persistent IDs.
Final merged geometry lacks a reliable face-to-original-source relation. ParserInspection/syntaxOrder belong to the
existing bounded HTTP inspection facility, not the source of native evaluated-instance identity.

New core files: `src/core/provenance/SourceProvenance.{h,cc}`, `ProvenanceCollector.{h,cc}` and tests.
New GUI files: `src/gui/selection/ProvenanceContribution.{h,cc}`. Change lexer/parser/AST expression locations,
ModuleInstantiation/UserModule/LocalScope/evaluation session hooks, CSGTreeEvaluator/CSG leaf records as needed,
MainWindow result installation and CMake registration. 03 owns EvaluationInputs and geometric selection; no competing
source loader, selection store or result counter is added. No semantic Part/Component type is added here.

## Public immutable records

Namespace `SourceProvenance`, core types contain standard-library values, never editor/AST raw pointers:

```cpp
struct Span { std::string fileKey, fingerprint; uint64_t begin, end; }; // UTF-8 [begin,end)
struct SyntaxKey { std::string fileKey; uint64_t ordinal; }; // scoped to one parse/input set
struct Argument {
  std::optional<std::string> name; uint32_t position;
  Span whole, expression; std::string originalExpression;
};
struct Site { SyntaxKey syntax; Span whole; std::string callable; std::vector<Argument> arguments; };
struct InstanceSegment { SyntaxKey call; uint64_t invocation; };
struct Instance {
  uint64_t id; std::optional<uint64_t> parent;
  std::vector<InstanceSegment> path;
  Site call; std::optional<Site> definition;
  std::vector<size_t> emittedNodeIndices;
};
enum class Confidence { Unique, Multiple, Unavailable, Stale };
struct Mapping {
  Confidence confidence; std::vector<uint64_t> candidateInstances;
  std::optional<Transform3d> localToWorld;
  std::string reason;
};
class Result {
public:
  Mapping forNode(size_t nodeIndex) const;
  const Instance* instance(uint64_t id) const;
  const Site* syntax(SyntaxKey) const;
};
```

Result belongs to exactly one 03 binding and retains its immutable EvaluationInputs. GUI wrapper
`ProvenanceService::resolve(const Selection::Hit&)` first validates its Stamp and consumed inputs. It returns a
Mapping plus the immutable Result handle; consumers cannot reinterpret an old id against a new result.
`editableSpan(Span, EditorInterface&)` returns a 02-compatible captured target only if path/document ownership,
UTF-8 bytes/fingerprint/current revision and expected range all agree. Unique provenance alone does not authorize
an arbitrary expression transformation. Read-only/unopened libraries remain navigable but not silently editable.

## Precise syntax ranges

For each captured SourceInput build lineStarts=[0, every byte immediately after LF]. Convert one-based locations by
begin=lineStarts[firstLine-1]+firstColumn-1 and end=lineStarts[lastLine-1]+lastColumn-1. Reject missing/invalid paths,
out-of-bounds lines/columns and UTF-8 continuation boundaries. Do not use QString character offsets or normalize EOLs.
Whole statements include their terminating semicolon; argument expression spans exclude names, '=' and separators.

Patch lexer token bookkeeping: maintain current cursor and separate tokenStart. Before each match record its start;
advance through raw bytes, with LF resetting column to 1. At opening quote/include/use save a composite-token start,
restore that start when returning the complete token, and retain the exclusive current end. Ignored comments and
whitespace do not become part of the next token. Push/pop the complete cursor state around includes and inspection.
Do not change the language grammar or numeric/Unicode identifier behavior to simplify offsets.

At parser reductions record full call, argument name, argument expression, assignment and definition spans using
the appropriate component locations, not AST pretty-printed length. Keep ordinal SyntaxKeys in an evaluation-owned
table, assigning every parsed occurrence a distinct key. Reassignments retain both syntactic occurrences in this
table while native evaluation continues to use its existing effective-assignment semantics.

Representative byte fixture: `//é\r\nx=width/2;\r\n` has expression `width/2` at [8,15), assignment at [6,16).
Repeat with a multiline string, comment directly adjacent to a token, escaped quote, BOM, non-BMP text, OEP8 object,
attribute block and nested includes. Compare exact byte slices with expected source, not only reported line numbers.

## Evaluation and geometry propagation

Attach an optional collector to EvaluationSession. ModuleInstantiation::evaluate opens an RAII invocation frame
before dispatch and closes it on success/exception. Allocate a monotonically increasing result-local invocation ID;
the path appends (call SyntaxKey, ordinal for this call within the parent invocation). Record UserModule's actual
resolved definition separately. Repeated loop/module calls get distinct invocations even when syntax is shared.
Do not copy every local variable into provenance or add persistent IDs based on loop indices.

At return, associate newly emitted root/group nodes with the invocation and retain descendants' more-specific
ownership. Track node creation explicitly; a null/empty result still closes its frame. Traversal's TransformNode
stack gives the final local-to-world transform for each CSG leaf, including mirror and nonuniform scale. A singular
transform may retain source navigation but has no invertible local edit frame.

Keep the provenance side table separate from cached Geometry. Geometry cache hits may reuse the same mesh for two
instances; attach each current invocation/transform at its node/CSG leaf, never mutate the cached mesh with an owner.
CSG normalization may duplicate one leaf into products; its logical node/instance mapping must remain the same.
Source-owned `render()`/hull/Minkowski/import results map to their producing call or known ancestor candidates,
without claiming triangle-level inner-operation provenance.

03's preview ObjectKey.nodeIndex identifies the emitting leaf. For direct primitives return the unique invocation;
for subtraction show the contributing cutter call and containing boolean path as distinct source contexts. This
means 'source of this boundary', not 'whole final manufactured part'. No source edit is enabled for a final merged
face by geometric proximity. For final mesh/root tokens collect candidate source ancestors; one known producing
call may be navigable, but a merged/multi-source face is Multiple or Unavailable. Record a reason, never choose first.

Reevaluation creates a new complete table and invalidates old editable mappings. No heuristic offset migration is
required in this feature. Refresh Inspector after a new pick or explicit source selection; a stale hit cannot gain
editability by merely matching an old node index. Persistent semantic matching is owned by 07/14.

## UI and consumers

Register one `source-provenance` InspectorContribution through 03. Show call site, definition and current invocation
path separately, with Open call / Open definition navigation. Multiple candidates are listed for explicit navigation;
no candidate receives implied edit priority. Navigate by canonical file and captured span, then validate current
content; if changed, ask for reevaluation through ordinary UI feedback without moving the caret to guessed offsets.

10/12 consume Argument.expression/originalExpression and the guarded editableSpan result. They still own operation
selection and expression rewrites. 07 consumes current instance paths/node ownership for its own semantic identities.
14 does not depend on this service: its bounded design-declaration source edits use its own whole-declaration parser
locations and lossless field scanner, without needing general geometry provenance.

## Phases and evidence

[Phase 1](4_imp-phase1.md) establishes exact ranges, [phase 2](4_imp-phase2.md) collects current invocation/geometry
ownership, [phase 3](4_imp-phase3.md) adds UI and guarded consumer queries. Use the shared verification contract.
No topology naming or generic inverse-expression editing is promised; missing information is an explicit result.
