# Integration performance regression suite

Status: in progress. CLI phase implemented and verified; native GUI measurement remains pending.
The retained exploration below describes the original scope; current delivery/coverage is in
[post-implementation notes](5_post-implementation-notes.md).

## User intent and location

Keep track of evaluation/rendering performance across integrated SCADMaxx builds using representative sample models.
Catch regressions such as the Inspector/captured-source overhead before delivering the next integration.

The maintained suite belongs in the SCADMaxx control repository's existing integration tooling:

- `experimental/performance/`: versioned fixture manifest, self-contained sample geometries and benchmark documentation.
- `experimental/scripts/`: runner and baseline-comparison entry point, following existing validation script conventions.
- `D:/openscad/runs/<run-id>/performance/`: raw samples, per-process logs, machine/build metadata and comparison report.

Those locations are proposed implementation paths, not already-created benchmark tools. Results remain outside source
checkouts and release ZIPs. Native timing hooks and correctness regressions needed by the runner belong in their owning
OpenSCAD branches. Do not create a second integration directory or copy benchmark infrastructure into every worktree.

## Reuse and gaps

Existing investigation scripts under `runs/20261007-remaining-performance` provide useful evidence and runner patterns.
`Measure-Owner.ps1` measures separate-process CSG export. `Measure-Gui.ps1` depends on temporary source instrumentation
that has been removed: it is not a supported GUI test runner and must not be adopted unchanged. Exit status alone did
not distinguish successful preview from an early compilation failure during that investigation.

The independent edit-evaluation experiment contains bracket-array and ventilated-panel fixtures. Inspect its current
files and provenance before reusing them; old documentation mentions a runner path that no longer exists in that
checkout. Keep fixture inputs/versioning independent of experimental evaluator changes.

`experimental/scripts/Test-LanguageExamples.py` already demonstrates invoking an explicit deployed runtime, retaining
logs, enforcing timeouts and checking resulting geometry. Reuse applicable infrastructure instead of creating another
unrelated environment/dependency setup. This performance suite also needs baseline comparison and actual GUI coverage.

## Measurement matrix

| Measurement | Purpose and boundary |
|---|---|
| Fresh-process CSG export | Language/dependency evaluation plus startup/output/shutdown; not a full F5 preview |
| GUI initial preview | Model opening through successful first visible model, recording window-ready time separately |
| GUI repeated preview | Unchanged F5 and controlled source/Customizer changes in one process; includes cache behavior |
| Final geometry render | Fixed-backend F6 completion; CLI mesh export is a separately labelled supporting measure |
| Viewport interaction | Repeatable camera motion/frame times after completion, separate from model computation |

Distinguish phase timings from end-to-end wall time. Retain startup and shutdown costs separately where instrumentation
permits. Do not label a fresh process as cold filesystem cache, or an offscreen export as GUI responsiveness/FPS.
After the background-evaluation feature exists, add UI responsiveness during evaluation and cancellation latency.

## Initial fixture set

- A cube/simple CSG model: startup/publication overhead and accidental fixed bookkeeping costs.
- A library-heavy model with little geometry: parsing/dependency/source-index overhead.
- An interpreter-heavy loop/function case with modest output geometry.
- Repeated parts/bracket array and a perforated or ventilated panel: realistic constructive geometry.
- Boolean-heavy and higher-resolution curved geometry; bounded hull/Minkowski cases in the longer suite.
- A representative model with semantic parts/assemblies, alongside an unannotated counterpart, to detect feature overhead.
- The user's `module_plus.scad` as an explicitly configured local regression case, with dependency fingerprints.

Keep the portable corpus self-contained or use deliberately pinned library inputs; do not silently depend on ambient
`OPENSCADPATH`, a private Dropbox path or whatever library revision happens to be installed. Do not publish/copy the
private model or its dependencies into the corpus without authorization. Missing optional local fixtures are explicit
skips and cannot silently replace required portable coverage.

## Reliable comparisons

- Require explicit candidate and baseline runtimes and record executable hashes, source SHA, dirty-state identity,
  integration input manifest, fixture/dependency hashes, backend, feature flags, parameters and measurement version.
- Compare against the last explicitly accepted baseline, not automatically the newest build. Preserve baseline history;
  a failed/slower candidate never becomes the reference automatically. An upstream build is a separate comparison.
- Record OS, CPU/GPU, graphics driver, compiler/build configuration and relevant runtime/environment settings. Changed
  backends, toolchains or fixture inputs require an explicit comparison classification rather than a misleading pass.
- Use isolated settings and the real deployed runtime. Run serially without builds or other benchmark workers competing
  for resources. Warm up intentionally where appropriate and retain repeated raw samples, median and spread.
- Prefer paired/alternating baseline and candidate samples on the same machine. Keep fresh-process and in-process
  cache-warm measurements separate. Use a quick corpus for ordinary integration and a longer explicitly requested run.
- Establish per-case regression limits after collecting stable baselines. Require both a relative slowdown and a
  meaningful absolute increase; classify noisy/inconclusive data explicitly rather than calling it a pass.
- Keep per-case results visible: improvements in easy models must not hide a severe slowdown in one representative case.
- Treat crashes, timeouts, missing output and unexpected diagnostics as failures, never exceptionally fast samples.
  Check successful evaluation and output correctness. Byte hashes can identify identical deterministic CSG, but mesh
  validation needs appropriate canonical/tolerant checks; triangle ordering alone must not masquerade as wrong geometry.

## Integration and acceptance

Implement the reproducible CLI subset first, then supported GUI measurement through existing capabilities or maintained
native hooks. A CLI-only result must explicitly report that GUI initial-preview/repreview coverage is missing.
Measure GUI completion/first frame rather than relying on sleeps or process exit. Reuse the HTTP interface where it
exposes the necessary lifecycle events; add generic observability in its owner if needed, not temporary bypass modes.

Once implemented and validated, add this suite to both full integration and re-integration validation after compilation
and before final packaging. Follow the existing build/test authorization policy. Preserve the previous delivery when
regressions or inconclusive results require investigation; record raw evidence and likely changed inputs for follow-up.
Do not silently change baseline limits to make a build pass.

Acceptance: an intentionally slower candidate is detected, a failed evaluation cannot pass as fast, equivalent results
are checked, incompatible comparisons are identified, and a subsequent agent can reproduce a report from recorded inputs.

Establish the suite/baseline before validating
[background model evaluation](../2026-10-07_background-model-evaluation/1_exploration.md).
This is validation sequencing, not an OpenSCAD Git ancestry dependency. The suite remains useful independently of that
feature and of the evaluator-speedup experiment. At exploration time, no benchmark had been run and no build workflow
had been changed. Subsequent implementation and execution are recorded in the post-implementation notes above.
