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

## Follow-up: hot cache hits and semantic snapshots

Owner investigation: `runs/20261007-owner-evaluation-performance/report.md` (workspace relative).
Inspector commit `335a5762c` removes repeated Windows absolute-path conversion from cache hits;
relative lookups remain current-directory dependent and have a regression test. Hierarchy commit
`c437c0473` checks validity without publishing/copying syntax and reuses the immutable finalized
syntax snapshot. Both fixes preserve source safety and diagnostics. Merge their owner ancestry
normally; do not replay patches in consumers.

Matched owner CSG-export medians improved from 5.682 to 4.811 s for the lookup change and from
8.243 to 7.087 s for the snapshot change, independently. All outputs match. These timings include
diagnostic instrumentation and are not native GUI timings. Declaration-scope validation was
measured at only 32–43 ms and left unchanged. About 49,000 parser provenance records still cost
roughly half a second for the imported libraries; basic renderer-based measurement picking does
not need that metadata. Full remaining cost is not attributed.

Combined integration `1dae1d07fdfd5094d48e7292cbbdaf24d490bc3b` passes 501 unit cases and
deployed-runtime smoke checks. Run: `runs/scadmaxx-all-features-2026-10-07_12-22`.
Uninstrumented three-repeat CSG median falls from 8.197 to 5.757 s (29.8% less elapsed time),
with byte-identical output. Separate PNG previews take 6.43–6.54 s versus 3.82–3.96 s in the
normal build, with visually matching images. The remaining roughly 1.7x preview gap is not
fully attributed. Native GUI first-frame/FPS checks were not rerun. This investigation
rebuilt and verified integration but did not replace the existing packaged ZIP.

The [further GUI/CLI investigation](gui-freshness-performance.md) isolates repeated GUI freshness
validation (45 passes), distinguishes shutdown cleanup from preview latency, compares the local
MSVC baseline, and records a separate Customizer dependency-order failure. These follow-ups are
measured but not yet implemented as production fixes.
