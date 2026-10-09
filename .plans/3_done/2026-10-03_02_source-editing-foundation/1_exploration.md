# Authoritative source buffer and transactional editing

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Planning review: [requirements](2_requirements.md), [design and phases](3_overall-plan.md) are prepared for the bounded
foundation. See the [readiness audit](../../1_planning/2026-10-03_00_source-first-cad-overview/planning-readiness.md) for source evidence.

Original exploration status: planning. Sources: chats A/C in the [overview](../../1_planning/2026-10-03_00_source-first-cad-overview/1_exploration.md).

## Settled architecture

The QScintilla live text buffer is authoritative. Typing, Vim commands and graphical model changes edit the same
buffer. The AST provides meaning and locations; evaluation produces geometry.

`UI action -> intended source transformation -> minimal patches -> reparse -> evaluate -> display`

Do not maintain a hidden editable model and serialize it back to OpenSCAD. Preserve comments, whitespace, blank lines,
expression spelling and ordering outside the intentional change. The user's whitespace objection explicitly rules
out reconstructing the source file from an ordinary AST.

## Proposed edit contract

- Insert/replace/delete exact ranges in a known document revision.
- Group a logical graphical operation into one normal undo transaction; support coherent redo.
- Mark the ordinary buffer dirty; committing a graphical action does not silently save it.
- Associate source mappings/evaluation with revisions; re-resolve or reject stale edits rather than using old offsets.
- Preserve untouched text exactly; infer local indentation, braces, line endings and spacing for generated code.
- Use normal document change events for refresh. Incremental parsing/evaluation is a performance direction, not a
  requirement to replace the parser before transactions can work.
- Preserve source through parse failures and distinguish last-valid displayed geometry from current invalid text.

The minimum is precise AST spans plus the original buffer. A lossless token/trivia or CST layer may help structural
transformations, but the later discussion removes it as a blanket prerequisite. Span production and instance mapping
belong to [06](../2026-10-03_06_source-geometry-provenance/1_exploration.md).

## External-editor decision

The user clarified that ordinary save and file-change detection suffice. Graphical edits modify SCADMaxx's unsaved
buffer; an explicit save updates disk. External editors handle reload or dirty-buffer warnings normally. SCADMaxx
needs symmetrical protection when an external editor saves first.

Track the loaded/saved disk version. If disk changes while the buffer is dirty, never overwrite automatically.
Provide review/reload/explicit-overwrite choices. A content hash is a proposed mechanism, not a fixed implementation.
A VS Code-specific broker, OT or CRDT is not required; those earlier proposals were superseded.

## Boundaries, order and evidence

This subsystem owns text-document transactions, not the semantics of clipping or drawings. Its revision, patch,
undo and file-conflict contracts can also serve editable design declarations through
[14](../2026-10-03_14_design-object-persistence/1_exploration.md), now selected to live in main or included `.scad`
source. File commands stay in the document layer, including Vim Ex integration. Start early; provenance,
design-object persistence, interactive edits and insertion consume this contract. Vim also uses the pre-group
external-edit notification to keep its insertion undo group separate from these operations.

Validate literal edits in unusually formatted/commented source, atomic multi-patch undo/redo, unsaved typing before
graphical edits, Unicode/line-ending offsets, stale revisions, external writes before save, and unaffected documents.
Determine included-file edit ownership explicitly before enabling it. No source checkout is selected here.

## Branch boundary

Proposed source branch: `feature/source-editing-foundation`. Own the reusable text transaction/document hooks and
their EditorInterface/Scintilla integration. Preserve existing annotation undo and guarded HTTP revision behavior;
record those selected prerequisites. Compile without provenance, design objects, Vim or graphical editing consumers.
Do not add their semantic types to this API. A range/revision transaction is sufficient to verify the foundation.
Vim now depends on this foundation's pre-group edit notification; 02 remains buildable without Vim code.
See [branch integration and handoff rules](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).
