# Phase 6: Regression, branch composition and implementation handoff

Requirements: IN01-18. Read 3_overall-plan.md and both source/preview contracts first.

1. Run complete insertion unit/native suites on the feature's prerequisite-only base. Discover every named case;
   report missing tests, skipped external-library tests and actual backend/DPI limitations separately.
2. Run all eight catalog entries through pick/preview/Commit/Undo/Redo. Compare committed native geometry to candidate
   meshes under identical configuration and verify independent Save/reopen with only source and required libraries.
   Include M4 threaded hole and all three BOLTS families; retain pinned library hashes and actual dependency traces.
3. In a separate composition checkout, test 04 clipping/hide/solo suspension and restoration, 05 Vim, annotations,
   measurement, navigation, shortcut customization and HTTP concurrent source edits. 09/10 remain absent.
4. Exercise a portable extracted feature package: internal worker resolves the same executable/build and shader
   resources with spaces/Unicode paths. Shipped catalogs work; no vendor library or preview scratch source leaks into
   the package. Worker crash/closure cannot strand a process or stale viewport lease.
5. Write 5_post-implementation-notes.md with base/head or exact uncommitted patch hashes, owner follow-up revisions,
   commands/test discovery/pass counts, library evidence, fixture geometry, build settings and material limitations.
   Preserve unrelated changes and separate repairs. Do not mark ready from documentation or compilation alone.

Checks: all insertion-* labels, owner refinement labels and native selector per the shared verification contract.
Record OpenSCADExe/OpenSCADUnitTests builds, actual CTest discovery, full native test runner and focused DPI runs.
Where source is uncommitted, freeze feature-only deltas and affected-file hashes; HEAD alone is not source evidence.
No automatic commit, push, promotion, enabled-stack modification or new complete SCADMaxx delivery is authorized by
this plan. Follow the workspace's explicit implementation-completion handoff procedure.

Exit: bounded insertion feature passes its behavioral checks, including real libraries and package worker launch.
Remaining integration/release obligations are explicit. Repeated tests are only needed for new changes/failures,
not to increase a vague confidence score.

Use the overview verification-contract.md with the actual isolated build path: build OpenSCADExe and
OpenSCADUnitTests, run ctest -N, then the named CTest labels. Native cases use the registered GUI harness selector.
No zero-test result counts as passing; retain commands, discovery and logs in the feature run directory.
