# Insertion source and placement contract

This is the concrete authoring specification for 12's accepted scope. Existing expressions and declarations are
preserved; inserted parameters are explicit typed values from 11. No inverse editing of an existing expression.

## Target selection and scope

1. Validate 03's hit against the successful root inputs/configuration and resolve 06 provenance. Final aggregate
   geometry without ownership cannot establish a target. Offer explicit source ancestor selection only from that
   retained provenance chain, displaying its span/preview; no name-based or nearest-object guess.
2. A semantic Part hit selects the Part definition's finished geometry. Resolve its declaration in an explicitly
   editable document; show every current instance of that definition. If there are multiple instances, require
   Edit shared definition. Treat zero/unknown invocation coverage as unsupported. Other unopened consumers of the
   same file cannot be enumerated: label the edit as a reusable definition change, not "only these instances".
3. A Component-role item targets the containing Assembly body, or file scope for a root Component. If that Assembly
   definition is repeated, insertion changes every Assembly instance: show and require that shared scope as well.
   Never insert a Component in a Part or inside the selected Part's Component call/transform block.
4. In ordinary SCAD, a geometry item targets an explicitly selected complete source statement at a unique call site.
   A statement evaluated repeatedly is not single-instance editable. Reject loops/conditionals with shared source
   effects unless the user chooses an eligible enclosing unique statement as the whole target.
5. Hardware on ordinary SCAD is emitted as a new root Component with a fixed document-frame transform. Do not wrap the
   existing model in a semantic Assembly. Named live attachment requires a real 08 owner/reference, not invented IDs.
6. Only the root document or an explicitly selected already-open user-owned included document can be edited. "Open
   source" is a separate navigation action, then restart target selection with fresh capture. Vendor/library sources
   remain unavailable as destinations. Imports/helpers/references must be legal in that same document and effective
   from the displayed root. If satisfying the insertion requires a second document edit, explain and disable Commit.

Candidate evaluation uses the displayed root with the target file's bytes replaced, not an isolated included file
with lost arguments. Exactly one target source document changes; the root can remain unchanged.

## Eligible geometry regions

PartBody: after native assignments, annotations and helper definitions, accept a single contiguous run of direct
geometry statements separated only by whitespace/comments. Statements may themselves contain arbitrary valid native
geometry expressions/control/booleans. All preceding declarations stay in the Part's original lexical scope.
An interleaved declaration between geometry statements is unsupported for automatic whole-Part rewriting; show the
source and ask the user through UI to group the intended geometry explicitly before retrying. Do not move declarations.
An empty Part is not a surface-pick target.

OrdinaryStatement: use its full 06 statement span, including attributes/modifiers when present. Initially reject
root/background/disabled modifiers on the chosen target, semantic descendants, a subtractive operand chosen as solid,
and transforms/scopes whose source frame or effective positive role is ambiguous. Offer a proven enclosing positive
CSG subtree where available. Unsupported does not prevent normal source navigation/editing.

The scanner extends a geometry region through its same-line trailing comment, then supplies a newline before any
closing wrapper. Preserve original bytes of that region verbatim, including indentation, line endings and comments.
Do not reprint/reindent existing code. Preserve UTF-8/BOM; generated lines use the destination's dominant EOL (LF tie).
Adjacent insertions at the same byte offset are combined into one patch before 02 validation.

## Geometry edits

Let ORIGINAL be the original contiguous geometry bytes and ITEM the new provider geometry under its placement.
Subtract:
difference() {
    union() {
ORIGINAL
    }
ITEM
}
Add:
union() {
ORIGINAL
ITEM
}

The inner union for subtraction ensures a multi-statement Part is cut as a whole. Existing differences remain inside
ORIGINAL unchanged; do not append a cutter by guessing the operands of an existing difference or BOSL2 diff/tag tree.
Ordinary native difference around a valid positive subtree is the supported subtraction route. Automatic editing of
BOSL2 tagged subtraction internals is outside this initial algorithm. No cross-Part booleans are generated.

Create two boundary insertions (before/after the original region) where possible; keep ORIGINAL's bytes untouched.
The import/helper prefix and wrapper edits must be nonoverlapping in the original document coordinate space.
Coalesce collisions deterministically; verify expected slices before deriving candidate bytes. Parse the candidate
natively before preview. Compile errors never cause a partially applied source change.

Provider holes have the catalog's nominal depth and geometry, including the documented BOSL2 extension. Do not add
an unrequested clearance/tolerance or "through all" operation. A blind depth is explicit; moving/flipping follows the
same contact-frame rules as other entries.

## Includes and names

Emit 11's file imports in declared order at a file-scope prefix after BOM and initial license/comment trivia, before
executable statements. Reuse an existing include only if it is unconditional in that effective file scope, the native
resolution matches the required file and its ordering precedes the generated use. A use is not an include substitute.
If ordered required imports already exist inconsistently, or adding another would duplicate ambiguous effects,
report ImportConflict with locations; do not move existing imports. Imports expanded from another file count only
when native scope/order evidence establishes the same binding. Unknown cases fail explicitly.

Never hoist a helper-scoped import. BOLTS remains included inside its provider helper. No global BOLTS_MODE/unit/$slop
changes. BOSL2 remains at file scope, std.scad before screws.scad. Candidate native provenance must resolve generated
calls to 11's expected defining files, even if an identically named user module exists.

Keep imports at their proven native prefix, but place generated helper definitions after existing native Customizer
fields. Collect these fields through CommentParser and ParameterObject using captured source bytes; preserve their
declarations, comments and applied values. A geometry wrapper that would precede a later original Customizer field
is unsupported (CustomizerScope); show a reason instead of moving that declaration or dropping its value.

Allocate smx_insert_<purpose>_<n> using the smallest positive unused suffix. Check all effective file-scope identifiers,
including imported definitions/assignments and generated reservations; no case folding. New semantic definition IDs,
sibling Component keys, owner Anchor IDs and Attachment IDs have their respective 07/08 uniqueness namespaces.
Use ASCII generated IDs, escaping every user label/string through the native source serializer. IDs are literal
source, never evaluation-order keys. Reuse existing generated helpers only with exact structural/evidence equivalence;
initial implementation always emits fresh helpers, which is simpler and deterministic. Avoid duplicate file imports.

Generate one provenance comment with provider ID, provider release, catalog SHA-256, profile ID and library aggregate
digest. Comments document provenance; they do not enforce a future library version when the saved SCAD is evaluated.

## Generated Component source

For a Component-role fragment, emit a new file-scope annotated Part definition containing the provider helper call(s)
and one Anchor named contact. Generate an ordinary Component call in the target Assembly body or file scope.
The first version uses the validated literal provider configuration in that definition; it does not invent a
bidirectional catalog-backed parameter editor after Commit. The provider helper's own parameters remain ordinary
editable source. Existing Part parameter expressions are never modified.

Example spelling (full BOLTS source belongs to its helper, not the wrapper):
@{type: Part, id: "insert-screw-1", label: "ISO4017 screw"}
module smx_insert_part_1() {
    @{type: Anchor}
    smx_contact_1 = {id: "contact", position: [0,0,0], normal: [0,0,1], up: [0,1,0]};
    smx_insert_screw_1(size="M4", length=20);
}
@{type: Component, id: "screw-1"}
smx_insert_part_1();

The complete helper is file-scope:
module smx_insert_screw_1(size,length) {
    include <BOLTS/BOLTS.scad>
    ISO4017(key=size,l=length);
}

Append new Assembly children/references at its direct body scope, before the closing brace; no nested semantic
definitions. All existing child statements remain byte-identical. Shared Assembly bodies use relative endpoint paths,
so each Assembly instance gets its own new child and attachment. Do not bake a selected Assembly's absolute path into
a shared declaration. Root additions use absolute paths where needed.

## Frames, offsets and Flip

Use column vectors. 08 constructs rigid frames from point/normal/up and solves Mate/Align. Capture camera-up once
using 08's tangent projection/canonical-axis degeneracy rule. Provider contact is Fc; target is Ft.
Offsets are in Ft's unspun X/Y/Z axes, spin is right-handed about Ft +Z. Flip toggles Mate (default) and Align; keep
position/offset unchanged. Do not additionally reverse an item because its operation is subtractive.

For fixed Part geometry or an ordinary statement, first inverse-capture the hit into the exact destination's local
frame with 08's affine point/normal/up rules, then solve placement there. New dimensions are destination-local model
units and inherit its later transforms. For shared Parts, the captured numeric local transform is identical across
instances, even when their parameters differ; do not derive a new parametric expression from their current values.
Singular/ill-conditioned required frames are Unsupported. Serialize finite matrix values with round-trip precision.

Emit translate + rotate only when the computed rotation is identity or an exact canonical principal-axis rotation.
Use multmatrix for general orientation; its 4x4 rows are explicit and readable, with a fixed-local-placement comment.
Never round a general frame to a nearby axis. Tolerances used to detect numerical identity must also bound the emitted
point/normal error to 08's test limits.

Fixed Component on a semantic owner: author a fixed owner-local target Anchor and a live Attachment to that fixed
reference in the Assembly/file scope. This follows owner movement but not changing surface geometry. Commit explicitly
authors those required declarations in the same transaction; clicking/moving alone never persists them.
Named Component: reference the chosen existing anchor and emit an Attachment; no duplicate fixed target anchor.
Ordinary geometry with no semantic owner: emit a numeric document-frame Component transform, marked fixed.
Do not pretend that it tracks an anonymous transform expression after later source edits.

Named example in an Assembly containing plate and the generated screw:
@{type: Attachment}
smx_attachment_1 = {
    id: "insert-screw-1", child: {component: "screw-1", anchor: "contact"},
    target: {component: "plate", anchor: "mount"},
    mode: "mate", offset: [0,0,0], spin: 0
};

08 validates the complete candidate attachment graph after new Components/references are collected. Existing cycles,
missing references or duplicate drivers cannot produce a Ready preview. Source offsets/spin are new literals;
existing anchors' parametric expressions remain intact.

## Required source fixtures

Keep the executable plain before/after examples in fixtures/. Add implementation golden cases for:
multiple direct Part statements; existing nested difference; Unicode/BOM/CRLF and adjacent line comments;
declarations interleaved with geometry (reject); library or closed included file (reject);
shared Part and shared Assembly (explicit scope, every instance changed); repeated ordinary loop call (reject);
root/disabled/background target (reject); symbol and semantic-ID collisions; BOSL2 import order;
helper-local BOLTS imports; named attachment; fixed owner-local capture; mirrored/nonuniform parent; singular parent.
Golden checks compare untouched byte ranges and actual native candidate geometry, not only rendered strings.
