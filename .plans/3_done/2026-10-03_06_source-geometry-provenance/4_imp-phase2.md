# Phase 2: invocation paths and honest geometry attribution

Covers PV03/PV04/PV05/PV06. Requires phase 1 and 03's frozen input/result binding.

1. Add the optional EvaluationSession collector and RAII invocation frames around module evaluation. Record actual
   definition/call sites, current parent invocation and emitted node indices; unwind cleanly on errors.
2. Build node/CSG-leaf side tables during CSGTreeEvaluator traversal. Record transforms/polarity and preserve logical
   identity through normalization; do not mutate shared cached meshes. Final result records provide candidate
   ancestors rather than invented per-face ownership.
3. Extend [source-provenance] tests with a module invoked twice, nested transformed modules, for-loop repetition,
   children(), a cache hit in two different instances, mirror/nonuniform/singular transforms and exceptions.
   Assert call/definition separation, distinct invocation IDs, correct path parents and exact world transforms.
4. Difference/hull/render fixtures must report their documented attribution and ambiguous final-face result.
   Edit/insert text before the call and recompile: prior mappings fail Stamp validation even if offsets/node IDs recur.

Exit: deterministic current-evaluation paths and safe ambiguity results; no claim of identity across arbitrary edits.
Run the labeled unit cases and preview/final TestProvenance fixtures described in phase 3 before freezing consumer use.
