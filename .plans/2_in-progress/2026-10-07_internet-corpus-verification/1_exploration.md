# Internet model corpus and separate verification

Requested 2026-10-07: approximately 4,000 additional internet models, older stable OpenSCAD STL outputs and
timings, then opt-in comparison with a future experimental build. Keep this outside regular acceptance testing.
User subsequently broadened acquisition beyond GitHub to any online source, and explicitly requested retaining
the full collection rather than culling it to 4,000. Keep every downloaded source, including duplicates/helpers;
the uncapped deduplicated manifest and later rendering classifications do not delete retained files.

Earlier chat: Build OpenSCAD performance benchmark, 01a106e7-d564-7603-a58b-e7f67eeff64b.
Preserve D:/openscad/artifacts/realworld-scad-corpus-20261004 (1,000 files, 234 repositories) and existing runs.
Reuse tools/evaluation-benchmark/realworld/{corpus,benchmark,geometry,report}.py and USAGE.md.
Its original baseline is an experimental feature-base runtime, not an established stable-release baseline.

## Separate work items

0. Investigate original corpus yield: reconcile all 1,000 candidates with the reported 321 eligible STL comparisons.
   Distinguish successfully exported STLs from valid meshes and outputs eligible for paired timing comparisons;
   the 321 count must not be assumed to mean only 321 files rendered. Use retained manifests, raw logs, execution
   outcomes and comparison records to produce exhaustive counts and representative examples. Classify helper/library
   entry points, 2D/empty outputs, missing includes/assets/fonts, syntax or version incompatibility, warnings,
   timeouts, invalid meshes, unstable output and comparison/harness exclusions. Identify acquisition, dependency
   resolution and harness defects separately from genuine model defects. Recommend targeted recovery and better
   discovery filters without silently repairing sources, lowering model detail or excluding slow valid models.
   Preserve the original frozen corpus and runs; any authorized reruns belong in a separate dated investigation.
   Use findings to guide expansion and stable-baseline configuration before freezing the new benchmark population.
1. Expand corpus: 4,000 additional normalized-source-unique candidates, excluding the old manifest. Pin commits,
   assets, license records and hashes; retain diversity caps and acquisition failures. Report candidates separately
   from successful 3D solids. A goal of 4,000 usable solids requires surplus acquisition and screening.
   Updated scope: 4,000 is no longer a cutoff. Search model sites, datasets, independent collections and other
   source hosts. Use --all for the manifest; preserve raw files even when duplicates or original-corpus matches.
2. Capture stable baseline: select the exact older stable executable, pin runtime and dependencies, render unchanged
   inputs to binary STL with wall times and diagnostics. Keep failures, empty results and timeouts. Check supported
   CLI flags before using the current harness. Cache geometry summaries outside the timed operation.
3. Improve fast comparison: cached canonical triangle hashes and baseline summaries; bounds/topology rejection
   before costly bidirectional surface sampling. Bound memory and comparison time. Preserve winding checks;
   never align, scale or repair meshes. Distinguish exact surface, sampled agreement, difference, invalid meshes
   and inconclusive/resource-limit outcomes. Sampling cannot prove equivalence.
4. Opt-in future verification: explicit candidate executable, frozen corpus and baseline; resumable runs and
   correctness/performance reports. Exclude failed/inconclusive cases from speed ratios. Repeat suspicious cases
   and check baseline repeatability for random models. Historical timings support screening; adjacent repeated
   baseline/candidate pairs support performance conclusions. No regular acceptance or release-gate integration.

Expansion precedes baseline capture; capture and comparator work precede future verification. These are workspace
tooling tasks, not changes to the OpenSCAD product. Create downstream feature plans after this split is accepted.
All downloaded source and generated evidence remain in sibling artifacts/runs, outside source checkouts.

## Acquisition setup and blocker

corpus.py now supports --query, --pages and --exclude-manifest. Acquisition command:
D:/openscad/runs/20261007-corpus-expansion/acquire.ps1. Destination:
D:/openscad/artifacts/realworld-scad-corpus-20261007-additional.
First discovery request returned HTTP 403: rate limit exceeded. No additional models were downloaded.
Retry when the public quota recovers. Downloader edits are untested; no build, render run or acceptance test ran.

Collection resumed on 2026-10-07 after the user's explicit request. Discovery now succeeds. Acquisition is strictly
sequential; search requests are spaced ten seconds apart, archives two seconds apart. Rate-limit responses honor
Retry-After/reset headers and retry with backoff. Query/page caches and completed source records support resuming.
The honest SCADMaxx User-Agent is retained. No downloader pool or extra agent is used.
Discovery returned 1,810 filtered repositories across 21 cached search pages. The acquisition command processes
up to 1,600 sequentially; the first seven snapshots were retained successfully. Final unique candidate count is
pending selection, which excludes the original manifest. The collection is active, not frozen or render-validated.

Use the current model for acquisition and incremental tooling, escalating only a concrete blocker or difficult
geometry review. Reuse the existing dependencies and harness. Model switches remain user controlled.
No extra agents, recurring jobs, commits, publication or automatic build integration were requested.
