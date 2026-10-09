# Integration performance regression checks

Run this suite after the integrated runtime is deployed and validated, before packaging. Use the same procedure for
full integrations and incremental re-integrations. An authorized integrated build includes these checks; documentation
changes alone do not authorize execution. Do not alter the human-maintained README.

## Scope

`../scripts/Test-RenderPerformance.py` reuses process execution, dependency fingerprinting and numerical geometry/image
comparison from `../../tools/evaluation-benchmark/realworld`. Its existing uv project/lock supplies Python dependencies;
it does not install or rebuild OpenSCAD dependencies. The portable fixtures and screening policy are in `cases.json`.

The quick suite includes simple geometry, a large source library, interpreter recursion, brackets, a perforated panel,
curved geometry, and equivalent plain/semantic part arrays. Extended adds hull and Minkowski. Each case measures:

- `csg`: fresh-process parsing/language evaluation and CSG serialization, with `$preview=true`.
- `preview`: fresh-process PNG preview including CSG preparation, offscreen drawing and PNG encoding.
- `off`: fresh-process full geometry plus indexed OFF export, with `$preview=false` and an explicit backend.

These are process wall times, including startup/shutdown, not pure geometry time. OS caches are uncontrolled; no claim
of cold filesystem cache is made. Native GUI opening, repeated GUI preview, viewport FPS, responsiveness and cancellation
are not covered by this CLI runner. The current HTTP API cannot trigger evaluation; do not substitute the removed temporary GUI probe or
pretend PNG export is GUI first-frame latency. Keep the parent plan in progress until those measurements are implemented.

Native follow-up: `native/GuiPreviewBenchmark.h` now provides a shared validation-only helper for the existing
`--run-all-gui-tests` entry point. The [fixed-feature comparison](../../../runs/hierarchy-freshness-2026-10-07_16-57/report.md)
records its exact test-build adapter, runtimes and execution. It measures initial file open plus Preview in an existing
window, followed by two unchanged Preview requests, retaining completion/return times, CSG outputs and framebuffer
captures. It does not bypass normal capture/freshness checks. It is not enabled in production source; the adapter is
removed after creating separately identified test runtimes. Do not call these first-present, application-startup,
edited-repreview, FPS or responsiveness measurements. General native-run orchestration remains separate from the CLI
runner above; preserve the explicit test-build identity and do not present an instrumented runtime as a release.

## Select explicit build inputs

Create two JSON descriptors in the new run directory: the last accepted delivery as baseline and the exact candidate
runtime. Verify each source revision against its retained build evidence, not the worktree's current HEAD. Example:

```json
{
  "label": "accepted-baseline",
  "executable": "D:/openscad/artifacts/BUILD/DELIVERY/staging/scadmaxx.exe",
  "source_revision": "FULL_40_CHARACTER_GIT_SHA",
  "source_dirty": false,
  "configuration": {
    "compiler": "MSVC",
    "toolset": "RECORDED_TOOLSET",
    "configuration": "Release",
    "architecture": "windows-x64",
    "dependencyProfileSha256": "RECORDED_PROFILE_HASH",
    "composition": "scadmaxx-all-features-SELECTED_INPUT_COUNT-inputs"
  },
  "evidence": ["D:/openscad/runs/BASELINE_RUN/report.md", "D:/openscad/runs/BASELINE_RUN/profile.json"]
}
```

Record different configurations honestly; the comparator marks them incompatible. Feature revision changes are the
subject of the comparison, whereas backend, compiler/profile and measurement changes must not be disguised as identical
conditions. A dirty build also requires `source_snapshot_sha256` for the source actually compiled. Evidence paths must
exist. The runner fingerprints the executable, companion, DLLs, runtime libraries and plugins, plus evidence files.
Do not silently choose a new baseline or advance it after a regression. Baseline acceptance is a separate explicit act.

## Run

From the controls repository, use an empty output directory beneath the new integration run:

```powershell
uv run --project tools/evaluation-benchmark/realworld --locked python experimental/scripts/Test-RenderPerformance.py `
  --baseline ../runs/RUN/baseline.json --candidate ../runs/RUN/candidate.json `
  --output ../runs/RUN/performance
```

Default: Manifold, all three stages, quick corpus, one unmeasured warmup and five measured repetitions per build/case/stage.
Build order alternates within adjacent pairs. `--suite extended` includes hull/Minkowski. `--backend CGAL` is a separate
series. `--ids cube panel` selects focused cases; `--stages csg preview` restricts coverage explicitly. Do not describe a
subset as a complete quick run. Per-sample timeout defaults to 90 seconds; no automatic quality reduction occurs.

Optional private regression case (read-only, source is not copied into the portable corpus):

```powershell
# Append to the same command:
--local-model 'E:/path/to/model.scad' --library-path 'D:/path/to/its/libraries'
```

This case runs CSG and PNG only. Dependencies are fingerprinted for every sample and must remain unchanged. Portable
fixtures use an isolated library search environment and reject unexpected external dependencies. User settings are
isolated. Native build processes are checked before and after each sample; the runner waits up to ten minutes before
stopping rather than timing concurrent compilation. MSBuild's idle reusable nodes are not treated as active compilation.
Process checks are samples, not continuous whole-machine load monitoring: avoid other intensive work while measuring.

## Interpret and retain results

- `metadata.json`: runtime, source/build evidence, fixture/shared-tool hashes, policy, hardware and measurement scope.
- `tooling/`, `fixtures/`, `cases.json`: frozen runner/helper/lock and portable input copies.
- `samples.jsonl`, `samples/`: incremental raw timings, exact commands, logs, outputs and dependency fingerprints.
- `results.json`, `summary.json`, `summary.csv`, `report.md`: correctness comparisons and per-case timing decisions.
- `interruption.json`: incomplete/failed attempt. Never promote its partial samples to acceptance evidence.

Exit 0 means every selected case passed. Exit 2 means review is needed (regression, noise, configuration/input/output
change or incomplete coverage); an execution/preflight failure also returns nonzero and preserves available evidence.
Missing output, diagnostics, invalid solids and timeouts fail. Mesh comparison ignores triangle ordering, checks topology,
bounds/volume and, when necessary, deterministic sampled surface distance. Sampled tolerance is not an equivalence proof.
Image differences require review; identical preview images do not prove identical geometry.

Initial screening limits are both 15% and 0.1 seconds of slowdown, with at least 80% of pairs slower. Relative median
absolute deviation above 15% is inconclusive. Raw ranges remain available. Calibrate per-case limits from stable series
when justified; version any policy change and never loosen limits merely to make a candidate pass. Overall averages
must not hide individual regressions. Keep previous deliveries and failed runs; investigate before packaging a regressed
candidate. No release files or release notes are generated by this suite.

## Runner verification

```powershell
uv run --project tools/evaluation-benchmark/realworld --locked python -m unittest discover `
  -s experimental/performance/tests -v
```

Tests cover known slowdown detection, noise/configuration classification, failed/missing samples, output mismatches and
interrupted reporting. Shared geometric comparator tests live in `tools/evaluation-benchmark/realworld/test_benchmark.py`.
