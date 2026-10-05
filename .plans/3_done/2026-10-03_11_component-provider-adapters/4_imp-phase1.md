# Phase 1: catalog schema and deterministic source recipes

Requirements: PR01-05, PR14-15. Read provider-contract.md; no library matching or live editor access yet.

1. Record the branch/base/shared toolchain and checkout instructions. Register new core/providers files/tests in CMake.
2. Implement owned value types, immutable snapshots, Diagnostic with code/path/JSON pointer, and SAX JSON loading.
   Detect duplicate keys while parsing; ordinary nlohmann map conversion would otherwise lose that evidence.
3. Implement schema 1 validation, ID/reference checks, limits, typed values, defaults, enums and checked expression
   evaluation. Include cycles/duplicate helper/parameter definitions and unknown fields in diagnostics.
4. Implement ScadFragmentWriter over typed statements/imports/helpers, numeric round-trip formatting and string
   escaping. Require symbolic helper-name bindings. Return fragments atomically after all validation passes.
5. Add the four dependency-free built-ins with exact dimensions, contact frames and operation flags from the contract.
   Library-backed recipes may parse structurally but remain unavailable until matching exists; no fake production match.
6. Carry insertionRole through items/fragments/CLI. Test geometry default, explicit component, unknown role rejection
   and subtractive-component rejection. Never infer roles from labels or library names.

## Meaningful checks

- Discover/run providers-schema and providers-source. Cube 10/20/30 gives bottom-centre [5,10,0], normal -Z and the
  exact named-argument call. Plain hole has +Z mating normal and subtractive intent; its body is still a positive mask.
- Locale with comma decimals still emits SCAD decimal points. Strings containing quotes, backslashes, Unicode and
  newlines remain one argument; attempted SCAD syntax in a string cannot become statements. Reject NUL/NaN/infinity.
- Duplicate keys, missing references, bad enum, unknown input and default outside bounds all yield diagnostic/no fragment.
- Values just inside/outside numeric bounds; division by zero; nested expressions beyond depth limit. Verify default
  and explicitly provided identical values produce identical fragments and frames.
- Generate valid SCAD for cube/sphere/cylinder using the feature executable; assert expected geometry dimensions.

Build OpenSCADExe/OpenSCADUnitTests and run the named labels per the shared verification contract. Keep fixture source
and output in a run directory, not source assets. No need for GUI/GL tests in this phase.

Exit: catalog-only schema/recipe implementation builds, rejects malformed input and generates tested built-in SCAD.
If recipe semantics require executing arbitrary catalog code, return to planning; do not introduce a scripting engine.
