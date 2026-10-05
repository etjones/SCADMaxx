# Implementation handoff standard: GPT-6.1 Sol

This is the requested planning quality bar. It does not change the repository's model settings or start an agent.
Use it with [branch composition](3_overall-plan.md), the [readiness audit](planning-readiness.md) and the
[shared verification contract](verification-contract.md), which specifies native test registration and selectors.

## Required contents for each handoff

1. `2_requirements.md`: numbered observable requirements, explicit completion scope and non-goals, failure behavior,
   and concrete acceptance cases. Distinguish requirements from candidate future extensions.
2. `3_overall-plan.md`: existing source symbols inspected, proposed file/module ownership, exact public data types,
   state transitions, algorithms and dependency interfaces. Mark proposed names as new, not existing code.
3. `4_imp-phaseN.md`: a bounded ordered edit sequence, requirements covered, fixtures with expected outcomes,
   runnable checks using the real repository harness, and a clear exit condition. A phase ends with buildable code.
4. Branch prerequisites: exact inputs are recorded at implementation start; dependent branches use a retained
   prerequisite-only base. Never substitute an arbitrary latest integrated branch for the recorded development base.
5. Failure instructions: what to inspect, what may be repaired locally and what invalidates the plan. A failed
   architectural assumption returns to planning; Sol must not silently invent a storage format or reduce scope.

Shared API signatures are defined once by their owner. Downstream phases cite those definitions and include concrete
input/output examples. An unavailable API must not be replaced with a mock in production or guessed from its name.
Ordinary local naming/refactoring choices remain with the implementer; product behavior does not.
Prepared plans select a concrete algorithm; the first applicable implementation phase verifies its risky runtime
invariants before dependent work. Source review is not a substitute for that verification. Follow the phase's stop
condition if its selected algorithm fails; do not turn an implementation phase into an open-ended architecture search.

## Source and build preflight

- Read workspace instructions and the feature's requirements/plan/phases. Inspect the selected checkout, branch,
  dirty files, submodules and local instructions. Preserve unrelated work. Record the inspected and actual source SHAs.
- Use the branch/prerequisite rules in `3_overall-plan.md`. The retained audit checkout is for reference only.
- Re-read owner contracts after prerequisite completion. In particular 02 owns the pre-group external-edit boundary,
  03 owns immutable evaluation inputs/result identity, and 14 owns design declarations and lifecycle undo integration.
- Use the existing Windows MSVC/Qt6/QScintilla profile and shared vcpkg installation. Record actual source/build/run
  paths. No package upgrades, private dependency tree or occupied-worktree reuse to get past a build failure.
- Source CMake changes include headers, moc/resources and install rules as needed. Reconfigure after registration.
  Do not assume tests under geometry are globbed; the present TEST_SOURCES list needs explicit additions there.
- Treat source/control companion changes as separate owned changes with linked revision evidence. Do not alter the
  hand-maintained README, enabled stack, promotion state or remote refs merely to complete a feature.

## Verification commands and evidence

Use the actual recorded build directory and toolchain configuration, not the audit checkout or an invented path.
For a configured source feature tree, the common native sequence is:

```powershell
cmake --build <feature-build> --config Release --target OpenSCADUnitTests
ctest --test-dir <feature-build> -C Release -N
ctest --test-dir <feature-build> -C Release -L <feature-test-tag> --output-on-failure
```

The phase specifies tags and expected named cases. `-N` must list them; zero discovered tests is failure. The current
Catch integration uses test tags as CTest labels. Confirm the generated label spelling before the filtered run.
QApplication-based editor tests need an initialized offscreen Qt application and controlled temporary settings.
Full native GUI tests use the existing `ENABLE_GUI_TESTS` build and `--run-all-gui-tests` harness; do not treat an
offscreen run as proof of real Windows desktop interaction. Use the existing build runbook for Configure/Build/Test
and integration/package checks; do not start a complete composition as an incidental plan-validation step.

Record source SHA, commands, test discovery/counts, exit status and logs. A passing compile is not behavior evidence.
Do not add tests that merely repeat prose or implementation details; use observable invariant/regression cases.

## Completion and stop conditions

Complete a phase only when its code builds, meaningful checks pass and its public contracts match the plan. Preserve
passing evidence and continue to the next phase without needless repeated testing. Record source/base/head, affected
control files, exclusions and limitations in `5_post-implementation-notes.md` at implementation completion.

Return to planning if a required renderer cannot produce the promised hit/cut, a vendor engine cannot build with
the supported runtime, the chosen source grammar conflicts with existing syntax, or an API needs a different owner.
Report the concrete failed assumption and evidence; do not add compatibility shims, silently drop functionality,
rewrite expressions to constants or claim a remaining research problem is implemented.
