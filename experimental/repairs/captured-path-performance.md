# Captured evaluation path performance

Observed with `module_plus.scad` and BOSL2 in the 2026-10-07 integrated build.
Before-fix source `80194e4c5467e4d0060610beedd4694dd66ec58d` did not finish a CLI preview
within 314 seconds; ordinary OpenSCAD finished in approximately 3.4 seconds.

## Cause and ownership

Captured evaluation bookkeeping repeatedly canonicalized library/source paths using filesystem
operations, including Windows file handles. Function/module resolution calls library lookup very
frequently. Provenance resolves source spans during parsing and evaluation. Semantic discovery
also requested identities for ordinary unannotated library declarations.

- Inspector owner `2a006b937`: cache library lookup path identities within SourceFileCache.
- Provenance owner `e2471c774`: cache path identities within a captured SyntaxTable; sealed copies
  retain the map without mutating it on reads.
- Hierarchy owner `fcad5e53f`: reuse provenance identities and defer identity/shadowing work until
  semantic metadata actually requires it. Nested metadata validation remains active.

Caches are evaluation-local. New evaluations resolve identities again; no global stale-file cache
or disabled provenance safety checks were introduced. Absolute lexical keys distinguish working
directories without incorrectly normalizing symlink/parent traversal combinations.

These are maintained feature changes, not patches to cherry-pick into integrations. Normal forward
merges carried Inspector into provenance/persistence, persistence into Cross sections/hierarchy,
provenance into hierarchy, then hierarchy into anchors and anchors into insertion. Current full heads
and prerequisite pins are in DEPENDENCIES.json. All merges were automatic without behavior conflicts.

## Verification and limits

Run: `runs/scadmaxx-all-features-2026-10-07_11-06` (workspace relative).
Integrated head: `510ca310543a57fec417c4e87de98e4a980d0c68`.
Incremental build reused the original integration build directory and unchanged shared vcpkg.
499 unit cases and 46 language/bounds checks passed, including cache lifetime and captured-byte
regressions. CLI preview repeats: fixed integration 7.363/7.736 seconds, normal 3.427/3.463 seconds.
Both report the same 42 CSG elements and geometry-cache size; preview images visually match.

The remaining approximately 2.2x difference is not isolated; these builds also differ in compiler,
dependencies and upstream revision. Measurements are CLI process wall time, not native GUI timings.
The old timed-out run included a brief debugger attachment. Do not present it as an exact speedup ratio.
Commits remain local; no promotion is implied by integrated validation.
