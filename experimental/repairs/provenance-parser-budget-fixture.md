# Provenance parser-budget fixture ownership

Run `20261006-scadmaxx-all-features` exposed a test-only dependency after merging
provenance `36e43d75020ebe2ff81cb90ce84aca63c482fd8c`. MSVC C2039 in
`src/core/ParserInspection_test.cc:10`: LocalScope has no `assignmentOccurrences`.
Failure log: `logs/20261006T211952815Z-build.log` in that run.

The occurrence list belongs to the later design-persistence feature. This parser
budget fixture creates 3000 uniquely named assignments and needs only the ordinary
core assignment inventory. Repair `b83792596` changes its count assertion to
`accepted->scope->assignments.size()==3000`. All small-budget rejection, large-budget
acceptance, token bounds and parser-context cleanup assertions remain unchanged.
No production behavior or feature dependency changes. Do not import persistence
early, disable the regression, or use the downstream occurrence list for this test.

Check applicability in future runs; use this narrow test repair only if the fixture
still depends on the later feature. Verification is in the provenance repair
checkpoint and the run report. Earlier downstream validation did not prove that the
intermediate provenance-only composition was independently buildable.

The first focused repair passed Configure, Build and Test at `b83792596`:
`runs/20261006-scadmaxx-all-features/logs/20261006T212648678Z-test.json`.
