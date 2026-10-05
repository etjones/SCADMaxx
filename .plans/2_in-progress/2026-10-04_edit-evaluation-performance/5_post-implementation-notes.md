# Edit-evaluation performance handoff

## Latest: upstream speedup composition and benchmark complete

The original phase-2/phase-3 engine patch and its impact are preserved under
`D:/openscad/runs/20261004-evaluation-upstream-speedups/original`. Four PRs from #4654 are ported into the existing
performance working tree: #4648 identifier interning/prehashing, #4653 virtual simplification, #4651 cached
duplicate-name analysis and #4650 variable-map reservation. Three other inputs are already represented upstream.
The ports preserve current language behavior, diagnostics, heap accounting and STL precision. The unfinished
fast-linalg2 experiment is excluded. No unrelated feature source is included.

Base/HEAD remains `9899c745e47dbf0f48b3ca23562eea31e66f9b82` on `feature/edit-evaluation-performance`.
Source is uncommitted. Complete patch SHA256: `06716fa6f704c208da8fe3361d4dd934b863cc71584dceccf5243ac240511daf`.
Executable SHA256: `2809e523cdf6460a962c34fbb1a2121d9ff23ee264ed5269880220318333f443`.
The run's 58-file source snapshot and final verification still match the tested binary. All six submodules
remain at the recorded base revisions; runtime dependencies/resources match the comparison builds.

All 123 native cases pass, with 78,874 assertions. All 129 echo/language comparisons match phase 3, including
five known failures. The 1,000-file survey and repeats total 8,000 executions and 3,210 output checks. Coverage,
unique sample keys, runtime hashes and output comparisons are audited. No new deterministic discrepancy was
identified; random cityscape and unstable rackstack outputs, invalid meshes and failed inputs remain flagged.

Survey aggregate time reductions are 5.92% CSG, 2.78% preview and 1.25% STL; typical-model changes are near zero.
Selected heavy examples consistently improve 15-27%, with a retained 3.9% picture-to-SCAD CSG slowdown.
The direct independent 24-model comparison against phase 3 shows only small incremental changes: +1.12% CSG,
-0.14% preview, -1.74% STL and +0.62% OFF. Jigsaw's direct paired results vary substantially. Compilation and
desktop activity limit timing attribution. GUI opening, warm edits and first presentation remain unmeasured.

Read `4_imp-upstream-speedups.md` and
`D:/openscad/runs/20261004-realworld-upstream-speedups/results.md` for the complete outcome and replay links.
No commit, push, promotion, selected-stack change or distribution. This requested experiment is complete;
the broader feature remains in progress. Future work may fix forward, replan, restart, or supersede this attempt;
preserve both original and combined evidence when choosing a different optimization scope.

## Real-world corpus supplement, 2026-10-04

The separate `4_imp-realworld-corpus.md` work is complete for CLI benchmarking. Controls are under
`tools/evaluation-benchmark/realworld`; frozen data are at `D:/openscad/artifacts/realworld-scad-corpus-20261004`.
The 1,000-file selection spans 234 repositories and 219 owners, with an actual maximum of eight files per
repository/directory. All 3,000 baseline CSG/preview/STL operations are recorded; 378 files complete every stage
cleanly. Failed, empty, diagnostic, unresolved-dependency and timed-out cases remain explicitly recorded.

The original pre-optimization baseline versus preserved phase-2 candidate passes all 720 executions in a
24-model, five-stage, three-repetition sample. All indexed OFF meshes and preview images match; 115 stage
comparisons pass and five identical STL cases remain inconclusive due to existing topology defects.
Fourteen focused harness/comparator tests pass. HTML/CSV/JSON/PNG reports and quantitative mesh differences
are retained. Shared-host timings are exploratory. Native GUI open/edit/first-present instrumentation is still
future work, not a measured CLI stage. No engine edits or interference with the separate phase-3 experiment.

Reproducible handoff: `D:/openscad/runs/20261004-realworld-handoff.md`; source/integrity evidence:
`D:/openscad/runs/20261004-realworld-evidence`. All work remains local and uncommitted.

## Earlier: phase 3 experiment complete

Function bodies now take ownership of the existing ordinary-parameter map instead of reinserting its entries.
Special variables retain their merge/override behavior; transferred variables are added to heap accounting in
one batch. Context.cc/.h and ContextFrame.cc/.h add the transfer helper; Expression.cc has one changed call site
on top of phase 2. No argument-vector, geometry or operator-support changes are included.

Evidence: D:/openscad/runs/20261004-evaluation-parameter-transfer/report.md and final-manifest.json. The frozen
phase-2 candidate is the comparison baseline. Twenty-five final source files match the tested uninstrumented
candidate. Patches, binaries, helpers, pinned dependencies and verification outputs provide the local handoff.

Panel language time improves another 6.79% (720.228 to 671.300 ms), with unchanged 392,332 contexts. All five
paired language batches improve. Three alternating uninstrumented pairs improve local/global six-frame OFF
medians 8.66%/3.69%, with substantial variation; every paired panel sequence improves. Fresh panel OFF medians
improve 3.27-9.00%. Brackets show no useful gain: warm medians regress 1.16-5.30%, while their language phase
increases about 34 microseconds. These are corpus-specific results, not cumulative percentages or GUI latency.

All 120 unit cases pass. All 128 echo comparisons match, comprising 123 successful exits and five unchanged
failure cases. Focused CTest passes 36/39; known Windows recursion failures remain. All 306 OFF meshes validate
and match, and all paired CSG bytes match. Hull and Minkowski remain supported; neither is accelerated here.

Read 4_imp-phase3.md and the latest run report for continued work. Profiling edits are removed from source;
the four Windows repairs remain separate. Changes are local, uncommitted and unpromoted. This authorized
experiment is complete; the broader feature stays in progress. Earlier milestones below remain preserved.

## Earlier: phase 2 experiment complete

The general initial-context optimization replaces the narrow sin/cos shortcut in the same branch/worktree and
on the same upstream base. Final engine scope is src/core/Expression.cc (13 added / 6 removed lines against
upstream), with two additional language regression fixtures/expected outputs. Earlier tests/models remain.
The four independent Windows build repairs remain separate. No profiling code, commit or promotion is retained.

Evidence: D:/openscad/runs/20261004-evaluation-general-contexts/report.md and final-manifest.json. The frozen
phase-1 candidate is the comparison baseline. Sixteen final source files are byte-matched to the tested
candidate; source/submodules, build helpers, binaries, commands, patches and measurements are recorded.

Panel language time improves another 10.27% (786.500 to 705.726 ms), with 345,699 fewer contexts per evaluation
(738,031 to 392,332). Three alternating uninstrumented pairs improve median local/global six-frame OFF batches
2.76%/4.14%; every paired panel sequence improves. Fresh panel OFF medians improve 1.04-4.40%. Bracket timings
have no consistent gain; no Hull/Minkowski acceleration is claimed. GUI edit/reparse latency remains unmeasured.

All 119 unit cases pass. The 126-case echo differential is identical; after generating a missing parser-stress
fixture, 121 have successful exits, with four baseline stack-overflow failures and one Unicode filename failure
remaining. The focused CTest set passes 34/37. Every paired CSG output and all 306 validated OFF meshes match.
No geometry approximation or operator restriction was introduced. The final source is uninstrumented.

Read 4_imp-phase2.md and the latest run report for continued work. The broader performance feature stays in
progress; this authorized experiment is complete. Phase-1 evidence below is historical and remains preserved.

## Earlier: phase 1 experiment complete

The narrow built-in sin/cos context shortcut is retained on feature/edit-evaluation-performance. Source base
and worktree are unchanged. The final engine change is 19 lines in src/core/Expression.cc, with three new
language regression fixtures and expected output. Four Windows build repairs remain separate in the evidence.
No temporary profiling code remains in the source. Changes are uncommitted and unpromoted.

Evidence: D:/openscad/runs/20261004-evaluation-math-fastpath/report.md. Frozen baseline/ and candidate/ runtimes
were built from the same base, repairs and dependencies; their build-info.json files distinguish exact source
and executable hashes. Source/tool snapshots and the final manifest provide the complete local handoff.

The panel removes 368,640 contexts per instantiation, reducing measured language time 11.00%. Three alternating
uninstrumented pairs show 7.56% lower local-update batch time and 6.94% lower global-update batch time. Batches
are six CLI animation frames with caches retained, not measured GUI edit/reparse latency. Fresh-process OFF
results are inconclusive, and brackets show no attributable benefit. Full Hull/Minkowski support is retained.

Both binaries pass 119 unit cases (75,145 assertions each); all 306 paired indexed meshes validate and match.
The 29-fixture language differential has no differences. CTest passes 32 of 35 selected fixtures; the three
recursion stack-overflow failures also occur in the baseline and remain explicitly unresolved. New tests pass.
Earlier STL round-trip limitations remain separate. Consult 4_imp-phase1.md before extending the experiment.

The proposed next experiment was to remove redundant initial contexts more generally in the interpreter.
Phase 2 above implements and verifies that extension.

## Earlier benchmark foundation

Status: requested branch/worktree, fixture corpus and benchmark tools are created. The performance engine feature
was still in planning at that milestone; phase 1 above supersedes that implementation status. No restricted backend exists.

Source branch: `feature/edit-evaluation-performance`, worktree `D:/openscad/wt-openscad-edit-evaluation-performance`.
HEAD/delta base: `9899c745e47dbf0f48b3ca23562eea31e66f9b82`. Intended source delta consists only of the two fixtures
under `tests/data/scad/benchmarks/edit-evaluation/`; they are uncommitted. All submodules are initialized at the
base's revisions. No source modifications from other features, commits, promotion or selected-stack edits.

Controls: `tools/evaluation-benchmark/{Invoke-EvaluationBenchmark.ps1,cases.json,verify_meshes.py,USAGE.md}`,
this plan and an appended entry in `docs/worktrees.md`. Existing unrelated control edits are preserved. The
dependency graph has no new edge because this feature is independent of the source-first CAD queue.

See `D:/openscad/runs/20261004-edit-evaluation-performance/report.md` for executable identity, timing tables,
commands/evidence references, failed attempts and correctness limits. Fixture validation uses the existing
integrated SCADMaxx binary at source `4c325716b94e444637a80df3966197ce110b2b75`, not a new build of this branch.

Fresh CSG/binary-STL execution and all operator-presence checks passed (90 cases), as did 60 animation frames
and three visually inspected preview PNGs. Independent STL mesh validation found a real retained failure:
42 Minkowski/full exports lose watertightness/component topology after re-import. No mesh repair is applied.
Indexed OFF is the geometry reference, with STL left as a separate failing round-trip check. All repeated,
restored and changed-volume comparisons in the original STL matrix passed despite that topology issue.

All 105 indexed OFF meshes from the final standard fresh/animation matrices pass independent topology,
positive-volume, component and edit/repeat/restore checks (`reference-mesh-validation.json`).
Smoke and stress checks also pass; the combined final report validates 122 indexed meshes. Standard fresh
exports take about 1.9 seconds for the panel and 1.3 seconds for full brackets; the larger stress panel takes
8.8 seconds. `source-snapshot/manifest.json` retains the exact six submodule revisions and byte-matching
fixture/tool copies with hashes. All intended source additions remain uncommitted and no application was built.

Important lessons: measure language execution separately from geometry; animation's geometry summary excludes
the interpreter, and CSG export includes serialization. Existing cache reuse already makes local bracket changes
much cheaper than initial full construction. Full/core operator variants are different geometry, not evidence
of an optimizer speedup. Hull is not dominant in these small convex-hull operands.

Next implementation step: matching baseline build plus low-overhead phase/cache instrumentation, then warm GUI
source/parameter edits. Preserve full support; evaluate exactly-Hull/Minkowski-excluded mode separately. No
silent extra omissions, fallback, analytic faceting changes or approximate export contracts.

The Windows file-creation helper was already installed/configured but stopped. It was started hidden on its
configured loopback endpoint, scoped to D:/openscad, to create the plan paths after an ACL-related creation
failure. No Codex configuration, ownership or ACL rewrite was performed.
