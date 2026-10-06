# Repair: insertion exact-byte fixtures on Windows

- Source repair: `29cb12ee6` in the shared local source repository; no push.
- Applies after contextual insertion `9db25842df0c3d7aad6a26bd6d96a7da86d189fe` when
  `tests/data/insertion/*.scad` lacks an explicit LF checkout rule.
- Failure: final 22-entry unit run at `af68f88238cca4149bf82a23e2e87da025465c81`,
  run `20261004-scadmaxx-all-features`, `20261005T003603142Z-test-unit.xml`.
  One failure in `source_golden_files_match_the_complete_candidate_bytes`: the literal
  `// @PROVENANCE@\n` marker was absent. Git reported `i/lf w/crlf` for all three fixtures.
- Cause: Windows autocrlf changes exact fixture bytes on checkout. The feature was previously
  tested with uncommitted LF files, before Git checkout conversion.
- Repair: scoped `tests/data/insertion/.gitattributes` with `*.scad text eol=lf`.
  Keep production authoring code and exact-byte assertions unchanged. Do not normalize both
  comparison sides in the test, which would hide source-byte regressions.
- Replay: cherry-pick the repair, then refresh these three clean fixture files to LF if they
  were checked out before the attribute existed. Preserve any actual local edits. In the
  isolated run, CRLF-to-LF conversion plus `git add` refreshed index metadata with no staged
  fixture content delta. Verify `git diff --cached --exit-code` and a clean source status.
- Focused verification: 54 assertions, zero failures/errors/skips in
  `feature-checks/insertion-golden-lf.xml`. Full checkpoint rerun is recorded in the run ledger.
- This was focused repair attempt 1. No production behavior or selected feature was removed.

Reproduced with promoted insertion `9ba04f92b` during the forward-merge run
`20261006-scadmaxx-all-features`. Failure: `20261006T220429552Z-test-unit.xml`.
Repair `1521fb795` adds the same scoped attribute as a separate integration repair
commit (no cherry-pick), then refreshes the three clean fixtures to LF. The only
staged content delta is `.gitattributes`. First focused attempt passed all 687869
assertions with zero failures/errors/skips and deployed smoke checks:
`logs/20261006T221251937Z-test.json`. The frozen owner head remains unchanged.
