# Phase 1: eliminate redundant sin/cos evaluation contexts

Authorized on 2026-10-04 by "Ok try ut" after the concrete experiment proposal.

The standard panel computes 368,640 sin/cos calls per instantiation. FunctionCall::evaluate currently creates
an empty Context before resolving every call. Test a fast path restricted to named calls resolving to the
actual built-in sin/cos functions. Keep normal user-function dispatch, argument evaluation, warnings, scope,
stack guards and exception traces. Do not cache numerical results or approximate arithmetic.

Build baseline and candidate from upstream 9899c745e with the same four needed Windows repairs and shared
dependencies. Freeze each executable and source delta separately. No other feature input, commit or promotion.
Evidence: D:/openscad/runs/20261004-evaluation-math-fastpath. Source checkout remains the existing feature worktree.

1. Build an unoptimized Release baseline and preserve its runtime.
2. Add the bounded dispatch change, then build a matching candidate.
3. Compare fresh and repeated parameter evaluation timings, unchanged CSG/geometry and diagnostic output.
4. Use isolated profiling instrumentation to count Context construction and time SourceFile::instantiate.
5. Retain the candidate only for a repeatable end-to-end improvement with passing language/geometry checks.

Focused regression fixtures cover nested calls, lexical/dynamic variables, named arguments, overridden names,
function-valued shadows, closures, recursive callers, argument side effects and assertion traces. Run the full
unit suite and relevant existing echo tests. Full Hull/Minkowski support remains enabled in all model checks.

The plan directory was untracked, so it was moved intact with native Move-Item into 2_in-progress; git mv cannot
move untracked files without staging them. No unrelated planning lane or dependency ordering changed.

## Outcome

Complete; retain the narrow shortcut. It removes 368,640 of 1,106,671 contexts per standard panel instantiation.
Median language time is 857.800 -> 763.455 ms (-11.00%). Uninstrumented six-update OFF batches improve
9.145 -> 8.454 seconds for local changes and 9.197 -> 8.559 seconds for global changes (three paired rounds).
Fresh-process export is inconclusive; there is no demonstrated bracket benefit or measured GUI-latency result.

Both binaries pass 119 unit cases (75,145 assertions). All 306 paired indexed meshes validate and match;
paired CSG output is identical. The expanded 29-fixture language comparison has identical outputs/exit codes.
Upstream CTest has 32 passes and three existing recursion stack overflows reproduced in the baseline. These
are recorded failures, not passing cases. All three new regression fixtures pass.

Profiling instrumentation is removed from source and retained only in the run's composite measurement patch
and separate profiling runtimes. Final Expression.cc exactly matches the tested uninstrumented candidate.
No commits, promotion, selected-stack change or installed-app replacement occurred.
