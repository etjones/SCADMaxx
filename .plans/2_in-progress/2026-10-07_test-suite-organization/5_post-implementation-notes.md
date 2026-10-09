# Implementation and validation status

Implemented in the controls repository, uncommitted. Existing unrelated changes were preserved.

- Catalog-driven Test-Profiles.py wraps Catch2, CTest, language examples, standalone Qt projects, existing CLI performance,
  corpus execution/reporting, native GUI selectors and control-tool tests.
- Everyday includes both unit binaries, launcher/export smoke and five critical CLI regressions. Build-Windows Test now
  invokes it after deployment; testedSha still represents only that profile. Retain the profile evidence path in the attempt.
- Deep selects Good + Default, deduplicates names, excludes Bugs and rejects unclassified commands. Dependencies/fixtures
  stay in a single CTest invocation; implicit fixture expansion is disabled. Exact regex chunks respect Windows command size.
- Background suites use offscreen Qt, serial execution, below-normal priority, affinity and aggregate commit limits.
  Suspended processes join a Windows kill-on-close job before starting; descendants cannot launch before budget assignment.
  All cooperating profiles use one lock. Timing suites require explicit quiet-machine selection and use normal priority.
- Desktop requires --allow-desktop and a GUI-test-enabled build. Individual selectors start in fresh processes. The full
  GUI sequence still shares a window across classes; source-level isolation/uniform QTest output remains future owner work.
- Missing standalone builds produce NOT_RUN. Reports retain separate coverage rather than silently claiming completeness.
- Repeat --corpus to verify both frozen collections without dropping entries. Per-build arguments identify effective
  experimental feature switches. Each corpus receives its own geometry/timing report; completion is not acceptance.
- AGENTS.md routes agents to workflows/testing.md. Integration/reintegration/PR workflows use the policy. The packaging
  smoke helper explicitly selects offscreen Qt; extracted visible launch is separately authorized. Control snapshots
  include the policy, catalog and profile self-test source.

Validation performed without running tests or building:

- Python AST parsing and catalog JSON parsing succeeded.
- PowerShell parser accepted the edited Build-Windows.ps1 and Common.ps1.
- CTest metadata-only discovery on the retained integration build selected all five everyday critical tests.
- Deep discovery selected 3,155 healthy CLI registrations, excluded the known Bugs category and left exactly two absent
  standalone-build inputs visible (annotation/transport and Customizer widget projects).
- Metadata plans: D:/openscad/runs/20261007-corpus-expansion/test-profile-plan.json and deep-test-profile-plan.json.

Application tests, runner self-tests, Windows resource enforcement and end-to-end execution are not yet exercised:
the workspace requires an explicit test request, and this implementation request did not launch validation processes.
Eight focused orchestration self-tests were added for selection, desktop overrides, dependency grouping and exclusions.
No source checkout edits, build, GUI launch, commit, push or baseline promotion occurred.

The existing render-performance plan owns native timing gaps. The existing internet-corpus plan owns stable-baseline
capture and corpus-wide verification. This feature remains in progress pending authorized execution validation; do not
claim runtime-tested readiness or move it to done based on metadata discovery alone.

## Authorized coverage reconciliation and tooling validation

The user subsequently requested the complete selected-feature inventory and background-only tooling validation.
These replace the earlier unexecuted-tooling limitation; application builds/tests and desktop execution remain unrun.

Audited all 24 enabled native stack rows and the selected control/skill companion using the pinned revisions in
PR_STACK.md/DEPENDENCIES.json, plus separately hashed owner working-tree tests. The durable audit tool is
experimental/scripts/Audit-FeatureTests.py. The control index is experimental/testing/feature-coverage.json; detailed
evidence is D:/openscad/runs/20261007-feature-test-coverage-current/feature-tests.json and report.md.
The earlier reconciled snapshot is retained separately. Concurrent owner/consumer maintenance changed selected pins
during this pass; the final index was refreshed and its selection/dependency hashes match the current controls.
Feature deltas include inherited dependency tests; their path counts must not be summed as distinct test cases.

Coverage wiring additions:

- Hidden icon/typography/dialog/Customizer visual Catch cases have the explicit desktop-visual profile.
  Their hidden restart helpers are driven by existing ordinary parent tests, rather than treated as standalone visuals.
- Provider and insertion tests requiring real BOSL2/BOLTS roots have provider-external coverage in deep-background,
  with complete pinned inventory verification. Ordinary unit execution excludes those tags to prevent silent skips.
- The desktop annotation suite supplies the LiveHttpWorkflow driver and Python interpreter when matching source is given;
  otherwise its missing input is reported. No HTTP native workflow was executed in this tooling pass.
- Transparency script entry points are approved for offscreen deep testing. Source-declared animation/transparency/color
  export checks absent from compiled CTest registration become NOT_RUN and require reconfiguration/build.
- Future background-evaluation/MainWindow/module-cache GUI selectors are cataloged with source capability checks.
  An absent selector never falls through to running the full GUI suite.
- Profile evidence includes the selected-feature index and its source/selection/build matching flags; snapshots retain it.
  Agent policy requires refreshing the audit after selection/owner changes and prohibits claiming complete coverage from
  stale source presence or registration metadata.

Actual outstanding coverage is explicit: ten selected revision pins are not ancestors of this integration, eleven distinct
test paths need newer source or compiled registration, and background-evaluation native tests are absent from this
integration. Some missing cases are inherited owner fixes, not omitted runner registrations.
Do not copy them into integration directly; follow owner/consumer forward maintenance and the selected-build workflow.
PRs 6878, 6776 and 6081 add no test/fixture paths in their audited deltas. Existing shortcut probes, GUI/theme checks and
language examples are separate related coverage, not proof that every behavior in these PRs is tested. Native theme
switching retains its previously documented manual desktop validation gap.

Background-only final tooling profile passed:

- 14 real-world geometry/execution harness tests.
- 10 performance policy/harness tests.
- 16 profile-selection, inventory, authorization and Windows job-object tests, including actual CPU affinity and timeout
  cleanup of a spawned Python descendant. No OpenSCAD executable or GUI window was launched by these tests.
- 19 build-tool checks using disposable local fixture repositories under runs/tool-tests; no application compilation.

Evidence: D:/openscad/runs/20261007-test-profiles-tools-validation-final/report.md and summary.json.
The initial tools run is retained in 20261007-test-profiles-tools-validation. Its build-tool failure exposed stale run-ID
fixtures; Test-BuildTools.ps1 now uses the current build-name/date/minute contract. The corrected check and final full
tooling profile pass. Product run-ID validation was not relaxed.

The final tooling evidence retains the earlier index snapshot and correctly reports it stale against the concurrently
updated selection. The subsequently refreshed index is metadata-only; runner and catalog hashes still match the passing
tooling run. This does not turn the unexecuted feature/application coverage into passing results.

Control implementation and tooling verification are complete for this request. Keep the plan in progress until matching
application profile execution validates the new Build-Windows connection and downstream integrated coverage. Native
instrumentation and full internet-model verification remain owned by their existing plans. No source worktree edit,
application build, application test execution, desktop test, commit of controls, push or baseline promotion occurred.
