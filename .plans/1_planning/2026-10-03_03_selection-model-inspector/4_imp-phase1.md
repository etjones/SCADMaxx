# Phase 1: immutable inputs and evaluated-result ownership

Covers SI04 and the source-consistency part of SI01/SI09. Follow [the technical contract](3_overall-plan.md).

1. Record a clean feature checkout's selected prerequisite SHAs and base. Inspect AnnotationController's existing
   beginEvaluation/finishEvaluation/rendererChanged and MainWindow compile paths before moving result ownership.
2. Add core EvaluationInputs and GUI EvaluationBinding. Capture editor overrides before compilation; wire root,
   include and use readers to one immutable request. Use binary bytes and preserve the lexer buffer/location stacks.
   Add request-local SourceFileCache ownership, with clear destruction after no AST/context consumer retains it.
3. Extend the existing evaluation/result record with consumed inputs and viewport generation. Connect root/dependency
   source changes, reload, renderer change and close to invalidation; keep stale displayed geometry labeled.
   Publish the owned EvaluatedScene handle; each worker gets its own Tree cache. Test scene retention across tab
   close/recompile and rejection of a late worker result without accessing destroyed AST/context backing.
4. Add `src/core/EvaluationInputs_test.cc` [evaluation-inputs] and `src/guitests/TestSelection.{h,cc}` initial cases:
   - dirty open include overrides disk; dirty use-library function changes result; disk file read once per request;
   - conflicting open buffers for one canonical path fail; identical overrides share one entry;
   - CRLF/UTF-8 bytes retained; root and nested-include path resolution match native behavior;
   - failed compile or dependency edit prevents a current binding; another tab's result never binds to this editor.
5. Register sources/tests in actual CMake lists and TestSelection in the GUI runner. Add a narrow
   `OPENSCAD_SELECTION_TESTS_ONLY` selector following the existing navigation-test selector, without replacing it.

Run unit [evaluation-inputs], TestSelection input/binding cases, existing annotation result/HTTP inspection cases
and module-cache tests using [verification commands](../2026-10-03_00_source-first-cad-overview/verification-contract.md).
Exit: current immutable input/result binding works without later features; existing syntax-inspection limits and
result IDs remain coherent. Do not continue if include/use still silently read a different revision than the binding.
