# CLI phase implementation and verification

Status: CLI phase implemented and verified on 2026-10-07; native GUI phase remains in progress.
Later that day, the fixed-feature build was compared with upstream using the shared native Preview helper;
see [the follow-up run](../../../../runs/hierarchy-freshness-2026-10-07_16-57/report.md).
It adds initial open-plus-Preview and unchanged re-preview measurements, but not edited re-preview,
first-present, FPS, responsiveness or cancellation coverage. The fixed build remains substantially slower
than upstream. The original CLI-only delivery record below is retained as historical evidence.

## Delivered

- `experimental/scripts/Test-RenderPerformance.py`: paired baseline/candidate measurement, explicit build identity, frozen inputs/tooling, isolated settings, dependency checks, correctness checks, timeout/diagnostic handling and regression classification.
- `experimental/performance/`: versioned portable fixtures, policy manifest, runner tests and [canonical usage guide](../../../experimental/performance/USAGE.md).
- Full integration and re-integration workflows now require these checks before packaging. Results belong under the integration run, outside release ZIPs. Baselines are never automatically advanced.

The implementation reuses `tools/evaluation-benchmark/realworld` execution, runtime/dependency identity and geometric/image comparison, and its existing uv environment/lock. The old plan's checkout-local runner path was stale; the maintained shared tools are in the controls repository. No OpenSCAD dependency was installed or rebuilt.

## Evidence

See [the complete run report](../../../../runs/performance-regressions-2026-10-07_16-23/report.md), which links descriptors, raw samples, exact commands, frozen tooling and both per-case reports.

The last packaged SCADMaxx (`510ca310543a57fec417c4e87de98e4a980d0c68`) was compared with the later validated integration runtime (`1dae1d07fdfd5094d48e7292cbbdaf24d490bc3b`). All 32 comparisons passed: 320 measured samples plus 64 warmups. The private module_plus model improved from 8.804 to 6.651 seconds for CSG and 9.356 to 7.117 seconds for PNG preview. This is a comparison between SCADMaxx builds, not upstream OpenSCAD.

Ten runner unit tests and fourteen shared harness/comparator tests passed. Tests exercise intentional slowdowns, failed/empty outputs, missing samples, incompatible/noisy series, interrupted reporting, geometry comparison and subprocess failures/timeouts. Run commands are in the usage guide. The shared test log is retained in the run directory; runner unit-test output was observed directly in the task tool output.

A preliminary attempt was stopped to replace slow tasklist process discovery with Win32 Toolhelp enumeration. Partial evidence is preserved and excluded from acceptance. Complete runs used the corrected runner, with no concurrent compilation detected before/after samples.

## Local handoff and remaining scope

Controls HEAD at implementation was `b41793db864b553e829e3c9d5c9de3d0abc0d847`; the suite and documentation remain uncommitted alongside preserved unrelated work. No source branch, stack pin, artifact or baseline was changed. No build, merge, commit or push was performed. The existing later unbuilt source fixes are not represented by these runtime results.

Native GUI initial/repeated preview, first visible frame, viewport frame times, responsiveness and cancellation are still uncovered. The existing HTTP interface cannot trigger evaluation. Add supported lifecycle measurement in the owning source feature rather than resurrecting temporary GUI probes; then extend this runner while retaining separately labelled CLI stages. Coordinate cancellation coverage with [background evaluation](../2026-10-07_background-model-evaluation/1_exploration.md). Keep this plan in progress until the native measurement scope is verified.

Initial screening thresholds are provisional and documented. Preserve accepted baseline history and inspect per-case results; never use an overall speedup to hide a regression. Repeat the suite against a newly built runtime when the unbuilt fixes are integrated.
