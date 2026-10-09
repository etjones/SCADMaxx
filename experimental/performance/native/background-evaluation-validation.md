# Background evaluation validation adapter

Built and exercised 2026-10-07. This adapter is for the background-evaluation source branch only.
Recorded runs: `D:/openscad/runs/20261007-background-integration-readiness/real-model-*`.
Schema 2 includes the timer interval which crosses job completion: sampling only current `busy()` state
incorrectly excluded publication stalls. Schema 1's heartbeat summary is not acceptance evidence.
Corrected measurements exposed a roughly 0.47–0.49 second initial publication/first-frame heartbeat gap,
principally Customizer widget creation. Language cancellation and equivalent CSG output passed those runs.

Use the existing performance corpus and baseline `GuiPreviewBenchmark.h` unchanged. For the candidate's
validation-only build, include `BackgroundEvaluationBenchmark.h` and call `runBackgroundEvaluationBenchmark`
from the same GUI-test entry point used for the baseline adapter. Do not commit that entry-point wiring into
production source or add this adapter to a release build.

The ordinary `OPENSCAD_BENCHMARK_MODEL` and `OPENSCAD_BENCHMARK_OUTPUT` inputs still apply. The additional JSON
records snapshot, queue, worker, validation, publication and first on-screen frame observations, plus a 50 ms
GUI heartbeat. Existing `gui.json`, CSG hashes, console and image artifacts remain available for comparison.
Stage timestamps are cumulative elapsed offsets, not individual stage durations. Queue wait includes other jobs;
native-gate wait is included in worker duration. No numbers are acceptance evidence until collected from a build
whose complete source identity is recorded.

Optionally set both `OPENSCAD_BENCHMARK_CANCEL_MODEL` and `OPENSCAD_BENCHMARK_CANCEL_STAGE` for a controlled
cancellation sample. Stage names include `Parsing`, `Loading dependencies`, `Evaluating parameters`,
`Evaluating language`, `Generating CSG`, `Normalizing CSG`, `Rendering geometry`, and `Preparing render geometry`.
Use a fixture whose requested stage lasts long enough to observe. A missed stage or timeout is a failed sample.
The current adapter uses Preview; invoke a Render request in the validation-only harness for F6-specific stages.

Capture process peak memory and repeated-run retention with the process runner. Native GUI tests selected by
`OPENSCAD_BACKGROUND_EVALUATION_TESTS_ONLY` cover queue priority/coalescing, heartbeat during work, cooperative
cancellation/recovery, language cancellation, and rejection of an obsolete queued Preview while retaining the
previous renderer. They are regression checks, not a substitute for the full feature-composition matrix.

Builds, test execution, baseline/candidate runs and packaging require separate user authorization in this workspace.
