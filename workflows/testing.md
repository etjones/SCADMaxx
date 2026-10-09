# Choose and run SCADMaxx tests

Read this file before selecting validation, running tests, or interpreting an existing test report.
The runner is `experimental/scripts/Test-Profiles.py`; its catalog is `experimental/testing/catalog.json`.
Keep runner and catalog changes in controls. Source test changes belong to their owning feature branches.

## Authorization and desktop boundary

- Preserve AGENTS.md's explicit-user-request requirement for builds and tests. An editing request alone does not
  authorize execution. A requested integrated build includes its documented correctness/performance checks.
- When testing is authorized, choose the smallest applicable profile below and complete its checks. Do not ask again
  for tests already authorized. Report omitted coverage as not run, never passed.
- Default to background profiles. Never launch native GUI tests, a windowed probe, desktop screenshots, input simulation
  or native GUI performance merely because the user asked for deep tests or an integrated build.
- Run desktop tests only when the user explicitly requests GUI/desktop testing or explicitly authorizes using the desktop.
  Pass `--allow-desktop` only with that authorization. Prefer a dedicated Windows VM/session; minimizing windows is not
  isolation. Stop and end the turn if desktop authorization must be requested.
- Do not classify a new test as background-safe merely because its parent process is hidden. Audit its child commands
  and Qt platform requirements. Unknown CTest commands stay excluded and visible until classified in the catalog.
- Performance and corpus timing require a quiet machine. Do not run simultaneous builds, tests or other benchmarks.
  Do not terminate the user's unrelated jobs to make the machine quiet. Background resource throttling is not a substitute
  for controlled timing; retain identical thread/memory limits across compared builds.

## When to use each profile

| Change or requested work | Profile and follow-up |
| --- | --- |
| Normal source edit, when tests are requested | `everyday`; add focused owner-specific tests for changed behavior |
| Parser/evaluator/geometry/backend/export changes; substantial integration changes | `everyday`, then `deep-background` |
| GUI behavior, navigation, keyboard, layout, DPI or theme changes | Background checks first; authorized `desktop` feature suites, then full GUI when cross-feature interaction changes |
| Native visual typography, icons, dialogs or Customizer checks | Explicitly authorized `desktop-visual`; hidden Catch cases do not run in the ordinary unit suite |
| Integration delivery or performance-sensitive change | `perf-quick` against last accepted SCADMaxx; `perf-extended` for hull/Minkowski or suspicious regressions |
| Internet-model compatibility or corpus investigation | Explicit `realworld` verification against the pinned older stable OpenSCAD; outside normal acceptance |
| Installed/extracted distribution | `distribution` on the extracted runtime with clean PATH; package/skill-specific checks separately |
| Profile runner, comparator or build-tool changes | `tools`; deployment probes only when their compilation is separately authorized |
| Documentation-only change | No build/test by default; language example execution only when requested |

Do not run everything after every edit. Broaden after failures, substantial shared changes or unresolved evidence.
Promote corpus regressions into small self-contained source fixtures; do not make the downloaded corpus an acceptance gate.
Do not advance performance or compatibility baselines automatically.

## Selected feature coverage

Read `experimental/testing/feature-coverage.json` before claiming integrated feature coverage. It reconciles the selected
native inputs and control companion with source tests, hidden tests and separate runners. The detailed retained audit is
linked from that index. Source presence/registration is not execution evidence.

After changing the selected stack or accepting new owner revisions, refresh the audit with `Audit-FeatureTests.py` using
the intended integration source and its CTest metadata plan. Supply `--catalog-index experimental/testing/feature-coverage.json`
to retain the refreshed catalog index. Audit tracked selected revisions and owner working-tree test changes separately.
Keep explicit records for missing owner cases, unmerged features, absent compiled registrations and separate input needs.
Do not repair a coverage mismatch by merging or substituting source revisions without the integration workflow.
The profile plan records whether the index matches the current selection, observed source and recorded build revision.
An outdated index cannot establish complete downstream coverage even when an individual test profile passes.
An enabled branch with no added test paths still needs a coverage assessment: related existing unit/language/GUI tests
are not proof of all feature behavior. Preserve manual desktop gaps (including native OS theme switching) explicitly.

Ordinary unit execution excludes `[providers-external]` and `[insertion-providers]`. Deep-background runs those in the
`provider-external` suite only with `--provider-libraries PATH.json`. Supply `bosl2` and `bolts` objects containing `root`
and a `files` mapping of relative path to SHA-256 for every retained file. The runner verifies the complete inventories
and passes explicit library roots; absent inputs are NOT_RUN, rather than silently skipped unit coverage.
Do not download or upgrade libraries during a test run. Nested icon/typography restart tests are driven by their ordinary
parent tests. Their hidden tags are not standalone visual coverage.

For authorized desktop tests, pass matching `--source` to activate `tests/annotations/LiveHttpWorkflow.py` in the annotation
suite. Its Python interpreter and evidence directory are supplied explicitly. The future background-evaluation/MainWindow/
module-cache selectors require matching source that declares them; absent selectors are NOT_RUN and never trigger the
full suite as a substitute. Native background-evaluation tests remain desktop tests despite the feature's name.

## Commands and inputs

Use the existing uv project and its Python environment. Provision it only when needed; do not reinstall build dependencies.
Example interpreter: `tools/evaluation-benchmark/realworld/.venv/Scripts/python.exe`.

```powershell
# Lists catalog and profiles; does not execute tests.
& $testPython experimental/scripts/Test-Profiles.py --list

# Prints commands and selected CTest metadata; does not execute tests.
& $testPython experimental/scripts/Test-Profiles.py --profile everyday --discover `
  --source $source --build $build --runtime $runtime --ctest $ctest

# Execute only when authorized, using a new output directory under D:/openscad/runs.
& $testPython experimental/scripts/Test-Profiles.py --profile everyday --run `
  --source $source --build $build --runtime $runtime --ctest $ctest --output $newEvidence

# Explicit desktop authorization is required. Each selected feature starts in a fresh process.
& $testPython experimental/scripts/Test-Profiles.py --profile desktop --run --allow-desktop `
  --gui-suite navigation --gui-suite selection --build $guiBuild --runtime $guiRuntime --output $newEvidence

# Baseline/candidate are JSON build descriptors from the existing performance workflow.
& $testPython experimental/scripts/Test-Profiles.py --profile perf-quick --run --quiet-machine `
  --baseline $baselineDescriptor --candidate $candidateDescriptor --backend Manifold --output $newEvidence

# A corpus run retains failed models and produces a geometry/timing report, not an acceptance verdict.
& $testPython experimental/scripts/Test-Profiles.py --profile realworld --run --quiet-machine `
  --corpus $corpusRoot --baseline-executable $stableExecutable --candidate-executable $candidateExecutable `
  --backend CGAL --output $newEvidence
```

Supply `--annotation-build` and `--customizer-build` for their already-built standalone CMake test projects when running
deep-background. The runner never builds them. Their absence produces NOT_RUN and an incomplete profile result.
Use `--gui-suite all` (the default) for the sixteen-class full GUI sequence. Individual selectors cover thirteen
feature groups including Vim persistence; TabManager/MainWindow/ModuleCache/ExportImage currently require the full sequence.
Do not claim fresh-process isolation between classes in that sequence.
For diagnosis, `--gui-function NAME` selects functions in one named desktop suite; repeat it to preserve their
execution order. Supply matching source with function-filter support. The runner clears inherited test filters,
so use this explicit option instead of setting `OPENSCAD_GUI_TEST_FUNCTIONS` outside the runner. Filtered evidence
covers only those functions, not the full suite.

Repeat `--corpus` for the original and additional frozen collections; each receives its own samples and comparison report.
Pass `--build-argument=candidate=--enable=FEATURE` repeatedly for the actual experimental feature switches under verification.
Use switches supported by the particular build. Do not infer enabled features from compilation flags. The retained raw
commands and per-build argument metadata identify the comparison. Do not change parameters or quality to improve timings.

The default budget is one suite process at a time, two logical CPUs and 4 GiB aggregate committed memory per process tree,
with offscreen Qt and below-normal priority for background suites. Windows job objects enforce affinity/memory limits
and kill descendants after timeout/interruption. Increase budgets explicitly for large models and record the limits.
Timing profiles use normal priority, the same explicit CPU/memory budget for both builds, and the existing paired runner.
The cross-profile lock prevents overlap among cooperating profile runs; it cannot certify that the whole machine is quiet.
If a crashed runner leaves the lock, inspect its PID and evidence before removing the stale lock. Never remove a live lock.

## Evidence and limits

Retain plan.json, identity.json, results.json, summary.json, report.md and per-command logs/JUnit files. Record source/build/runtime
identities separately. A source HEAD is not evidence of the binary revision; a recorded build/source mismatch is rejected.
The Build-Windows Test step uses everyday and records its profile evidence before updating testedSha. That flag still
does not claim deep, desktop, performance or corpus coverage.

CTest selection is the deduplicated Good + Default union excluding the Bugs category. Use exact catalog-listed critical
names for everyday. Keep unknown commands out of background; review missing/unclassified coverage before accepting deep.
Known bug-category exclusions are classification evidence, not a claim that those tests were executed and failed.
Timeouts and changing inputs are inconclusive. Missing binaries, absent standalone builds and unexecuted commands are not run.
Corpus completion is VERIFICATION_RECORDED: read its per-model outcomes and geometry report before drawing conclusions.

CLI PNG output does not measure GUI first-present latency. Offscreen checks do not establish real platform input, layout,
DPI, theme or graphics-driver correctness. Native performance instrumentation remains in the existing performance plan.
Distribution profile verifies CLI exports and language examples, not clean-machine portability or visible GUI startup.
Use the package workflow's clean-path deployment/ZIP checks and separately authorized desktop checks for those claims.
