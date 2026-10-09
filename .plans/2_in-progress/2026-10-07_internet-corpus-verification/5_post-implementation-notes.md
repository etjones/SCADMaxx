# Collection checkpoint, 2026-10-07

Acquisition checkpoint complete; overall work remains in progress. User expanded discovery beyond GitHub and
removed the 4,000 cutoff. Retain all downloaded sources. No commits, pushes, build or acceptance-test integration.

- Corpus: D:/openscad/artifacts/realworld-scad-corpus-20261007-additional.
- Run report: D:/openscad/runs/20261007-corpus-expansion/results.md.
- Raw retained SCAD entries: 24,585; uncapped additional unique candidate manifest: 21,764.
- Source mix: 14,097 GitHub, 7,641 Thingiverse via pinned dataset, 25 CodeCAD, one independent CalcResult source.
- Every candidate file hash matches; IDs/source hashes unique; zero normalized overlap with original corpus.
- Sequential acquisition and rate-limit backoff replace the previous download pool. Importers preserve original
  SCAD text and attribution; pyarrow is added and pinned for public Parquet ingestion. Importer fence/path failures
  and Windows case collisions are recorded without overwriting source. Entire Parquet remains retained.
- Search notes record other sites investigated and blocked/sign-in-only downloads. No bypasses or bot disguise.
- Initial yield reconciliation: 610 original nonempty successful STL exports; 382 clean exports minus 59
  inconclusive meshes and two differences explains 321 accepted pairs. Diagnostic counts are overlapping.

Remaining: full original-yield root-cause investigation, dependency recovery, exact older stable runtime selection
and compatible flags, baseline renders/timings, comparator improvements, and separate opt-in future verification.
Acquisition data integrity was checked; downloader/importer automated tests and OpenSCAD rendering were not run.
The corpus includes helpers/tests and unverified models. Preserve this checkpoint when beginning rendering work.
