# Upstream speedup composition and corpus comparison

User requested preservation of our existing optimization and integration of the seven PRs listed in #4654,
followed by another real-world benchmark. Work in the existing performance checkout, preserving local changes.

Run: D:/openscad/runs/20261004-evaluation-upstream-speedups.
Baseline source: 9899c745e47dbf0f48b3ca23562eea31e66f9b82 plus frozen phase-3 input and Windows repairs.
The original patch, source snapshot and measured impact are preserved under original/.
Exact PR heads and author attribution are frozen in upstream/selected-inputs.json.

Integrate #4643, #4648, #4652, #4642, #4653, #4651 and #4650. Record already-upstream implementations instead
of reverting newer code to old patches. Preserve language behavior and geometry correctness when resolving
overlaps. The separate unfinished fast-linalg2 experiment is excluded from the seven-entry composition.

Build with the same Release toolchain and dependencies; run native and language differential checks before
the 1,000-file corpus and repeated follow-ups. Compare against the original baseline and retain phase 3 for
incremental comparisons. Keep source changes local and uncommitted; no selected-stack or distribution change.

## Completed result

The requested experiment is complete. Ports of #4648, #4653, #4651 and #4650 are in the existing working tree;
#4642/#4652 are already merged ancestors and #4643's mechanisms are represented by newer mesh/export code.
Current double-precision ASCII STL behavior, language diagnostics and heap accounting are preserved.

The original engine patch is frozen separately (36 additions/seven removals/five files), with its previous
real-world impact. Complete combined patch SHA256: 06716fa6f704c208da8fe3361d4dd934b863cc71584dceccf5243ac240511daf.
Candidate executable SHA256: 2809e523cdf6460a962c34fbb1a2121d9ff23ee264ed5269880220318333f443.
All 58 recorded source files match the staged build after benchmarking; submodule revisions are unchanged.

All 123 native cases pass (78,874 assertions). All 129 language comparisons match phase 3, including five
unchanged known failures. The corpus comparison records 8,000 executions and 3,210 output checks, with complete
unique coverage and no candidate-only execution regression. Known unstable/invalid geometry stays flagged.

Survey aggregate reductions: CSG 5.92%, preview 2.78%, STL 1.25%; median models improve only 0.11-0.22%.
Repeated evaluator-heavy examples improve 15-27%, while picture-to-SCAD CSG slows 3.9% in all five pairs.
Direct phase-3 comparison on the independent sample gives +1.12% CSG, -0.14% preview, -1.74% STL and +0.62% OFF;
small differences are inconclusive on this shared host. The direct jigsaw run has substantial paired variation.

Full results, tables, graphs and limitations:
D:/openscad/runs/20261004-realworld-upstream-speedups/results.md.
Replay: D:/openscad/runs/20261004-evaluation-upstream-speedups/Replay-Benchmarks.ps1.
Source/build handoff: D:/openscad/runs/20261004-evaluation-upstream-speedups/report.md and final-manifest.json.
No commits, pushes, promotion, selected-stack change or distributed release. Broader feature remains in progress;
GUI open/edit/first-frame instrumentation and quiet-host incremental attribution remain future work.
