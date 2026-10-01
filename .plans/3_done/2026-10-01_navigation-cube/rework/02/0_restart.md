# Fix forward: unchanged reload polling cancels camera snaps

Trigger: stationary quick clicks still stop short, while holding the button can succeed. Cycle 01 fixed a real
small-jitter input defect but did not explain or resolve the user's remaining failure.
Starting source: `0ff82ec81d46e06c1e15047233c3b2e488d4cc92`. No rollback; requirements and camera architecture remain valid.

Diagnosis: automatic reload polls named files every 200 ms through `MainWindow::compile(true)`.
The unconditional cancellation at entry interrupted navigation even when no source/dependency changed.
Earlier navigation tests explicitly disabled automatic reload and missed this ordinary operating condition.
Window-routed stationary clicks with 1 ms and 250 ms holds both pass without reload; the unchanged-poll regression
fails before the correction (`runs/navigation-cube/phase6/reload-cancel-before/test-results.xml`).

Correction: cancel in `compileDone` only when evaluation actually occurs. Explicit preview still cancels in
`prepareCompile`; script-driven camera evaluation still cancels before `instantiateRoot`.
Regression covers unchanged immediate and periodic reload checks across a 350 ms animation, exact endpoint,
and cancellation on explicit preview. Retain quick/held window-routed clicks and the earlier jitter tests.

Status: complete, source commit `0947b9e3a840209153d0ad791df27f38ec86858c`, verified on private origin.
All 15 native cases pass at 100%; the separately staged runtime also passes at simulated 150% with system-only PATH.
Evidence: `runs/navigation-cube/phase6/reload-cancel-fixed` and `reload-fixed-staged150`.
Runnable build: `D:/openscad/artifacts/openscad-navigation-cube-reload-fix-win64/openscad.exe`.
The prior executables remain preserved. Existing running instances must be replaced by launching this build.
