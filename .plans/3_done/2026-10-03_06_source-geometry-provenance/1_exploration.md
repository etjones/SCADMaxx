# Source ranges and geometry provenance

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Planning review: [requirements](2_requirements.md), [technical design and three phases](3_overall-plan.md) are prepared.
Byte-range, invocation and ambiguity fixtures are specified for implementation verification. See the
[readiness audit](../../1_planning/2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Original exploration status: planning. Sources: chats A/C in the [overview](../../1_planning/2026-10-03_00_source-first-cad-overview/1_exploration.md).

## Purpose

Connect live source, syntax, evaluation instances and rendered geometry reliably enough to navigate or edit source
from a viewport selection. A triangle number alone is not source provenance. This is shared infrastructure for
Model Inspector, semantic hierarchy, interactive editing and insertion.

## Proposed contract

- Map syntax nodes and relevant arguments/expressions to precise current source spans, with file/document identity
  and source revision. Define byte/character conversions explicitly for QScintilla and Unicode.
- Retain evaluation paths so repeated calls and loop-generated instances can be distinguished from their definitions.
- Carry source provenance through geometry construction where possible; report ambiguity or unavailable provenance.
- Keep node identity separate from offsets. Edits before a node move ranges; offsets cannot be persistent IDs.
- Preserve identity through incremental matching where practical. Explicit semantic identifiers offer stronger
  identity than anonymous syntax, but no stability guarantee should exceed what the implementation can support.
- Record world/local transforms and relevant source invocation/parameters for consumers, without promising that every
  derived coordinate can be inverted into a unique source edit.
- Invalidate or re-resolve mappings when the source, evaluated result or target document changes.

Keep source/instance provenance distinct from persistent references to generated faces or edges. Semantic owners
and named features can have stable identities even when tessellation and boolean topology change. Reference-strength
and broken-reference policies belong to [08](../../1_planning/2026-10-03_08_anchors-attachments/1_exploration.md) and
[14](../2026-10-03_14_design-object-persistence/1_exploration.md); provenance alone does not solve topological naming.

## Source preservation

Use [02](../2026-10-03_02_source-editing-foundation/1_exploration.md) as the authoritative document/edit contract.
Precise spans plus original text are the initial approach. Tokens/trivia or a lossless CST may later help robust
insertions and structural changes; a full parser rewrite is not an accepted prerequisite. Untouched comments,
spacing and expressions must survive whichever representation is chosen.

An expression such as `width / 2` is not interchangeable with its evaluated number. Selection may identify its
location without proving which parameter the user intends to change. Definition edits, invocation edits and
instance-specific wrappers have different consequences and need explicit action policies in consumers.

## Research context

C identifies Johann Felipe Gonzalez's bidirectional CSG research at Carleton/Lille as useful precedent. It describes
direct manipulation changing the internal editor buffer, with a single-file limitation in that prototype.
It distinguishes OpenSCAD PR #5279 (source selection feedback) and #5778 (viewport overlays) from the full research
translate/rotate/scale source-rewriting system. Their current status and exact code need verification before reuse.

- [Research project](https://cil.csit.carleton.ca/bidirectional-programming-csg-cad/)
- [Research paper](https://thomaspietrzak.com/bibliography/gonzalez23.pdf)
- [PR #5279](https://github.com/openscad/openscad/pull/5279)
- [PR #5778](https://github.com/openscad/openscad/pull/5778)

## Order and evidence

Start after the source revision and geometric selection contracts are usable. Own the source-navigation contribution
to [03](../2026-10-03_03_selection-model-inspector/1_exploration.md) in this branch. Establish this before source-backed
semantic identities and committed viewport edits rely on it.

Verify literals and expressions, nested/transformed modules, repeated instances, loops, includes/use, boolean-created
surfaces, parse failures, changed ranges and stale geometry. An unknown mapping must not cause an edit to the wrong
file, definition or instance. Decide supported initial editing scope from evidence, not the research prototype's claims.

## Branch boundary

Proposed source branch: `feature/source-geometry-provenance`, depending on 02/03 and the selected OEP8/Customizer
parser baseline. Own precise syntax ranges, evaluation-instance mapping and source-navigation contribution code.
Keep semantic Part/Component/Assembly declarations in 07. Publish a provenance interface that compiles without
semantic hierarchy, anchors or graphical consumers. Parser/lexer conflicts must preserve ordinary objects and
Customizer annotations, with their regression suites. See
[branch integration and handoff rules](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).
