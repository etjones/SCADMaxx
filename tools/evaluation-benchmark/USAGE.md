# Evaluation benchmarks

For the frozen 1,000-file online corpus, multi-build timings, quantitative geometry comparison and HTML/CSV/PNG
reports, see [the real-world harness](realworld/USAGE.md). The synthetic edit fixtures below remain a separate suite.

See the [feature exploration](../../.plans/2_in-progress/2026-10-04_edit-evaluation-performance/1_exploration.md).
Fixtures are in `D:/openscad/wt-openscad-edit-evaluation-performance/tests/data/scad/benchmarks/edit-evaluation/`.
Open either SCAD file directly. `quality=1` is standard; 0 is smoke and 2 is stress. No external SCAD library.

## Fresh processes

PowerShell 7.2+, a console executable, and a NEW output directory:

```powershell
./Invoke-EvaluationBenchmark.ps1 `
  -Executable D:/openscad/artifacts/20261003-scadmaxx-executable-name/attempt-2/extracted-check/scadmaxx.com `
  -SourceDirectory D:/openscad/wt-openscad-edit-evaluation-performance `
  -OutputDirectory D:/openscad/runs/my-evaluation-run
```

Defaults: five workloads, baseline/local/global inputs, CSG and indexed OFF, three repetitions, standard quality,
45-second timeout. Select with `-Workload panel`, `-Scenario baseline`, or `-Quality 0 -Repetitions 1`.
`-Stage preview` exports F5 PNGs for visual checks; its timing includes drawing.

The catalog defines core, hull-only, Minkowski-only and full brackets. CSG output is checked for the expected
operators. Flags change geometry: compare each variant with its own baseline, not full/core as a claimed speedup.

## Persistent geometry caches

```powershell
./Invoke-EvaluationBenchmark.ps1 `
  -Executable D:/openscad/artifacts/20261003-scadmaxx-executable-name/attempt-2/extracted-check/scadmaxx.com `
  -SourceDirectory D:/openscad/wt-openscad-edit-evaluation-performance `
  -OutputDirectory D:/openscad/runs/my-evaluation-sequence `
  -AnimationSequence -Scenario local,global -Stage off -Repetitions 1
```

Six frames per process: base, A, repeat A, B, repeat B, restore base. B is 1.25 times A's change from the initial
value. Baseline scenario repeats the base. CLI animation parses the AST once and instantiates per frame,
retaining geometry caches. This is parameter reevaluation, NOT GUI edit/reparse latency.

In sequence mode, `seconds` and summary.csv cover the whole six-frame batch. `frameSummaries` in results.json
retain geometry-phase timings and cache statistics. That timer excludes SCAD execution. Do not divide batch
time by six and label it measured local-edit latency.

## Evidence

The runner records binary hashes/version/build manifest, source HEAD/status, model hashes, hardware, exact
arguments, output hashes/sizes, logs, results.json and summary.csv. Errors, warnings, missing/empty outputs and
timeouts fail the run. It does not automatically reduce quality. Output stays under `D:/openscad/runs`.

The initial executable is a validated integrated SCADMaxx build, not the feature branch. Build matching binaries
before claiming an engine improvement. CSG/mesh timings include serialization, and OS caches may be warm. The
initial build enables Manifold Minkowski; CGAL Minkowski is a separate configuration.

Indexed OFF is the reference for topology checks. `-Stage stl` remains available as a separate binary STL
round-trip test. The initial Minkowski fixtures expose a retained STL re-import failure: Manifold reports a
valid result and indexed OFF is closed, but positional merging of binary STL vertices produces a non-watertight
mesh. Do not mark that test passed, repair it silently, or combine its result with the indexed reference.
OFF also has finite text coordinate precision; preserving its indices is not a proof of exact geometry.

`verify_meshes.py` checks geometry using trimesh and NumPy, including no-change/restored animation frames and
local/global edits. Run it in the isolated uv environment documented in the run report; it is not part of the
application’s dependency tree. It accepts one or more run directories and an explicit output JSON path.
