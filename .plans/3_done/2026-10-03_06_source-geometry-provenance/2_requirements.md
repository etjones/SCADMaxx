# Source and geometry provenance requirements

Behavior, parser/evaluator propagation and ambiguity policies are specified in [the technical design](3_overall-plan.md).
Its phases verify the source-reviewed algorithm; this expands the obligations in [the exploration](1_exploration.md).

- PV01: Locate relevant syntax nodes, arguments and expressions in the authoritative current text with document/file
  identity, source revision/fingerprint and exact spans. Use the UTF-8 byte contract of 02 at its edit boundary.
- PV02: Establish lexer/parser line/column and end-boundary semantics explicitly. Convert to/from editor positions
  without splitting UTF-8 codepoints or confusing Qt UTF-16 positions, LF/CRLF or multibyte comments/identifiers.
- PV03: Distinguish module definition, call site and evaluated instance path, including repeated calls and loops.
  A selected rendered instance must not implicitly mean "edit every instance of this definition".
- PV04: Associate geometry and world/local transforms with available source/evaluation provenance. Boolean-created
  surfaces may have multiple or unknown contributors; expose ambiguity rather than guessing a unique editable source.
- PV05: Source offsets are locations, not durable semantic IDs. Reparse/re-resolve after edits; preserve identity only
  when matching evidence supports it. Do not claim topology naming or stability across arbitrary source changes.
- PV06: Reject stale mappings after source/result/document changes and parse failures. Navigation can show useful
  known source context, but mutation consumers require a fresh, unambiguous target and 02 transaction preconditions.
- PV07: Add source navigation through 03's contribution interface, without making 03 depend on this implementation.
  Do not introduce Part/Component declarations, attachment policy or persistent reference recovery in this branch.
- PV08: Preserve original expressions, comments and formatting. A evaluated value does not authorize replacing an
  expression with a literal. Provide precise original spans/text; consumers choose their explicitly supported edits.
- PV09: Maintain ordinary OpenSCAD and selected OEP8/Customizer parser behavior. A full parser/CST rewrite is not a
  prerequisite; if a lossless representation is needed, justify it with a concrete unsupported operation/fixture.

## Acceptance fixtures

| Fixture | Required evidence |
| --- | --- |
| Literal beside width/2, comments and multibyte text | Exact original UTF-8 spans; expression remains an expression. |
| LF and CRLF variants | Range slicing yields identical intended token/expression, with correct end boundary. |
| Nested transformed module and two invocations | Definition/call/instance are distinct; transforms match visible hits. |
| Loop-generated repeated objects | Distinct current evaluation paths; no false persistent-ID guarantee. |
| include/use with an open dirty dependency | Explicit file/live-revision source identity; no stale disk substitution. |
| Boolean-created surface or merged contributors | Documented ambiguous/unavailable mapping; unsafe edit unavailable. |
| Edit before target / delete target / parse failure | Re-resolve or invalidate; no offset-based retargeting. |
| Tab switch/re-evaluation | Reject previous hit/result mapping; navigation cannot select the wrong document. |

## Required implementation proof

The technical plan records the inspected Location/lexer conventions, precise range corrections, invocation-path
algorithm and honest final-geometry ambiguity policy. Execute the representative fixtures above before accepting
those APIs for consumer edits. This plan does not claim the current checkout already implements source rewriting.
