# Real-world corpus and comparison harness

Authorized on 2026-10-04: find approximately 1,000 varied online SCAD files, freeze the original-engine baseline,
compare future engines, show tables/graphs, and distinguish opening/evaluation/display/STL stages. User added:
geometry must agree within floating-point rounding tolerance; quantify meaningful differences without assuming
that either output is necessarily correct.

Controls: `tools/evaluation-benchmark/realworld`. Corpus: sibling
`artifacts/realworld-scad-corpus-20261004`. Runs: sibling `runs/20261004-realworld-*`.
This work does not modify the in-progress phase-2 evaluator or consume its moving build as a baseline.

- Freeze source commits, assets and licenses; deterministic deduplication and repository/directory/owner caps.
- Retain all execution outcomes, including non-standalone files, warnings, empty geometry, failures and timeouts.
- Sequential, resumable fresh-process runs with exact binary/runtime/input identities and adjacent paired order.
- AST, CSG, preview PNG, STL and indexed OFF scopes are separate overlapping end-to-end measurements.
- Native GUI open/first-present and pure engine phase timers require matched future instrumentation.
- Geometry comparison ignores triangle order, tolerates quantified coordinate rounding, and checks surface
  distance, bounds, volume and topology. No mesh repair or shape alignment. Sampling is explicitly not proof.
- Produce standalone HTML, CSV/JSON and PNG charts; correctness failures exclude performance speedup claims.
- Keep all changes local/uncommitted and preserve unrelated source/control work.

Verification includes known-good reordered/retriangulated/rounded meshes and known-bad displaced/scaled,
missing-component/hole cases, then actual baseline/candidate execution and output comparison on corpus models.
Record run coverage and remaining GUI instrumentation scope in the handoff; do not claim 1,000 clean models
from a static filename count or equate a same failure on both binaries with a passing model.

## Outcome

Complete as the CLI corpus/harness supplement. Corpus: 1,000 files, 234 repositories, 219 owners, maximum eight
per repository/directory. The full three-stage, one-repetition survey records all 3,000 outcomes; 378 files
complete CSG/preview/STL cleanly. Raw helper/dependency/diagnostic/timeout cases remain visible.

The 24-model, five-stage, three-repetition original-baseline/phase-2 comparison has 720 clean executions.
115 model/stage comparisons pass; five identical STL cases are inconclusive due to existing non-watertight
round-trip topology. All indexed OFF meshes and preview images match; no baseline instability or output change.
Fourteen focused tests pass. Shared-host timings are exploratory; native GUI timing remains unimplemented.

Handoff and commands: `D:/openscad/runs/20261004-realworld-handoff.md` and the tool's `USAGE.md`.
Final reports: `D:/openscad/runs/20261004-realworld-{baseline,paired}-report/index.html`.
No engine source changes, commits, promotion or selected-stack change. Preserve concurrent phase-3 work.
