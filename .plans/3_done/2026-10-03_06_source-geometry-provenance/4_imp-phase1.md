# Phase 1: exact source ranges on captured inputs

Covers PV01/PV02/PV08/PV09. Requires implemented 02/03 APIs; inspect their actual headers against the design first.

1. Implement SourceProvenance immutable Span/SyntaxKey/Site and byte conversion against 03 EvaluationInputs.
2. Patch lexer token-start/end tracking, include stack restoration and parser reductions as specified in the overall
   plan. Add argument-name/expression ranges and syntax occurrence records without changing evaluation semantics.
3. Add `src/core/provenance/SourceProvenance_test.cc` with [source-provenance] cases: literal/expression, the exact
   [8,15) CRLF fixture, multiline strings, comments without surrounding spaces, BOM/Unicode/non-BMP, nested include,
   use-library definition, reassignment occurrences, ordinary objects and fixed-key attributes.
4. Verify syntax inspection and ordinary compilation produce their intended AST behavior, including inspection-only
   disabled nodes. Native parsing must not accidentally inherit the HTTP token/time limits.

Run [source-provenance], existing parser/surface/object/Customizer fixtures and relevant TestAnnotations syntax cases.
Exit: every tested range slices the exact input bytes and no normal parser behavior regresses. Stop before geometry
mapping if a span depends on normalized disk text, a pretty-printed AST or assumed UTF-16 positions.
