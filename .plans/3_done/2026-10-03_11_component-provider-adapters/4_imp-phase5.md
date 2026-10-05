# Phase 5: consumer contract and feature handoff

Requirements: all PR01-15. Prerequisites: phases 1-4. This does not implement feature 12.

1. Add a fake consumer of the public API that loads, binds, generates, supplies helper names and revalidates a draft.
   Use two independent document contexts with different library resolutions. Verify no shared mutable selection state.
2. Exercise library/catalog replacement during a draft and preserve its original immutable binding for diagnostics.
   The consumer must discard stale output, not quietly regenerate with a different adapter under the old preview.
3. Verify required defining-module metadata catches a model-level name collision when used by the integration fixture;
   12's real provenance/candidate-evaluation check remains a consumer obligation documented in its plan.
4. Run the focused suites, real pinned-library suite and representative existing parser/import/export regressions.
   Rehearse composition with selected native baseline inputs without importing another unfinished consumer branch.
5. Stage/extract the feature build using normal workspace packaging and validate provider commands from the extracted
   executable with an empty external-library environment, then with explicit test-library paths. Keep test copies out.
6. Write 5_post-implementation-notes.md with source base/delta identity, catalog/profile identities, exact tests/counts,
   scope, generated-source samples, package contents and remaining 12 integration work. Follow the local handoff rules.

## Exit evidence

- Native build and discovered providers-schema/match/source/cli cases pass; providers-external executed against the
  recorded 35-file BOSL2 and 41-file BOLTS closures. Missing external fixtures cannot be reported as passing coverage.
- Fake consumer proves capture/isolation/revalidation and symbolic helpers; it is never production code for preview.
- Extracted executable discovers catalogs and no vendor code is bundled. Existing manually installed libraries and
  user catalogs are unchanged. Readable generated SCAD renders independently with its declared libraries.
- Report 12's exact API requirements: captured-input adapters, scoped helper preservation, import/name handling,
  effective module provenance, correct Mate/Flip interpretation, preview verification and pre-commit revalidation.

At implementation completion, report fix-forward/replan/restart/supersede options under plans-workflow. Commit, push,
promotion and stack selection require their separately authorized workflow; this phase does not grant those actions.
Stop for owner/API or recipe failures that invalidate the design; ordinary implementation errors are fixed locally.
