# Edit-to-result evaluation performance

## Objective and scope

Reduce the time from a SCAD source/parameter edit to updated usable geometry. Viewport rotation is outside this
feature's performance objective. Preserve correct geometry, language semantics and useful diagnostics.

Requested on 2026-10-04: create an independent feature, branch/worktree and a few complex but bounded benchmark
models; investigate full operation support alongside explicitly excluding Hull and Minkowski. This delivery
established the feature and benchmark corpus. Phase 1 tested a narrow sin/cos dispatch optimization; phase 2
replaces it with lazy entry contexts for all function calls. Phase 3 transfers ordinary function parameter maps
instead of rebuilding them. See 4_imp-phase1.md, 4_imp-phase2.md, 4_imp-phase3.md and the latest handoff.
Broader incremental/GPU evaluation remains research work. No geometry operation was removed.

## Ownership

- Source: `D:/openscad/wt-openscad-edit-evaluation-performance`.
- Branch: `feature/edit-evaluation-performance`.
- Freshly fetched upstream base: `9899c745e47dbf0f48b3ca23562eea31e66f9b82` (2026-10-03).
- Source fixtures: `tests/data/scad/benchmarks/edit-evaluation/`.
- Runner/catalog/usage: `D:/openscad/scadmaxx/tools/evaluation-benchmark/`.
- Evidence: `D:/openscad/runs/20261004-edit-evaluation-performance/`.
- Independent of the source-first CAD queue; no meaningful dependency edge to add to `feature_dependencies.dot`.
- Preserve unrelated changes. No commits, pushes, selected-stack promotion or integrated release are requested.

Fixture validation uses the existing validated SCADMaxx console executable under
`artifacts/20261003-scadmaxx-executable-name/attempt-2/extracted-check/`, built from integrated source
`4c325716b94e444637a80df3966197ce110b2b75`. This is NOT a build of this branch. Run records preserve both identities,
binary/model hashes and the build manifest. Build matching baseline/candidate binaries before comparing engines.

## Candidate costs from source inspection

The common path parses SCAD, executes functions/modules/loops and constructs the shape/operation tree. Preview
generates leaf meshes, evaluates geometry-producing subtrees, and normalizes CSG. Full render evaluates Boolean
geometry, converts representations and serializes exports.

- `MainWindow::instantiateRoot` reconstructs the model tree when compiling.
- `Expression.cc` interprets numerical expressions and list comprehensions.
- Geometry caches already reuse matching subtrees. Investigate language execution before those cache lookups.
- `Tree::getIdString` / `NodeDumper` derive cache identities from textual node representations.
- `GeometryEvaluator::evaluateGeometry` explicitly leaves converted PolySets out of its geometry cache.
- `ManifoldGeometry::binOp` copies/merges provenance and colour collections on successive operations.
- Manifold already has parallelism and lazy CSG evaluation: a binary wrapper loop does not prove eager execution.

Most are candidate costs, not measured hotspots. Phase 1 measured and reduced empty interpreter contexts for
built-in sin/cos calls: 11% lower panel instantiation time and 7-8% lower repeated-update batch wall time. Fresh
export gains were inconclusive. Phase 2 reduces language time another 10.27% and repeated-update batch medians
2.76-4.14% versus phase 1; its broader interpreter change preserves all tested language and geometry behavior.
Phase 3 reduces panel language time another 6.79%, with unchanged context counts; repeated-update batch medians
improve 3.69-8.66% against phase 2, with substantial variation. Brackets show no useful improvement. These are
corpus-specific CLI measurements, not cumulative percentages or GUI edit/reparse timings. Continue measuring individual costs
before committing to architectural changes.

## Full and restricted support tracks

**F: full compatibility.** Preserve all existing operations, including hull(), minkowski(), imports, polyhedra,
text, 2D Boolean operations, offset, projection, extrusion, render(), colours and modifiers. Preserve faceting
settings and `$preview` behavior. Existing invalid-input behavior remains explicit.

Common opportunities include fewer copies/conversions, efficient cache identities, caching proven-pure numerical
expressions, dependency tracking across edits, and independent geometry jobs. Hull/Minkowski remain materialized
geometry nodes, reusable while their inputs are unchanged. Changes inside a node still require recalculation.

**R: exclude exactly hull() and minkowski().** Study an explicitly selected execution mode that rejects active
unsupported nodes before producing partial output. Check the expanded operation graph, including library-produced
and render()-nested operations. Uninstantiated dead branches are permitted. No automatic fallback to full mode
or silently substituted geometry; users may deliberately select full mode. Everything else remains supported
unless a further restriction is explicitly proposed and accepted.

The fixtures' flags establish eligible workloads; no restricted engine or runtime rejection is implemented yet.

| Candidate change | Full track | Effect of excluding Hull/Minkowski |
| --- | --- | --- |
| Incremental interpreter/dependencies | Applicable | Simpler geometry graph; numerical and scoping costs remain |
| Cache keys, metadata copies, conversion caches | Applicable | No fundamental difference; benchmark both tracks |
| CPU jobs and batched construction | Applicable with synchronization | Fewer opaque expensive tasks; still workload dependent |
| Direct Boolean-tree preview evaluation | Hybrid with materialized advanced nodes | More trees can remain combinations of leaf shapes |
| GPU implicit/interval evaluation | Needs advanced materialization or more algorithms | Removes two difficult constructors, but other operations still need faithful handling |
| GPU mesh intersection/classification | Applicable to mesh Boolean portions | Robust triangulation, topology and transfer costs remain |

Analytic SDF-only evaluation usually requires more restrictions or conversion paths than R. Imported meshes,
text, extrusions, projection and deliberately faceted primitives remain obligations. A smooth analytic sphere
does not preserve `$fn=8`. Export still requires constructing a surface. Approximate volume sampling requires
its own accuracy contract; excluding Hull/Minkowski does not authorize approximation or further omissions.

## Benchmark corpus

Two standalone files avoid external-library and download noise. These are mechanical benchmark fixtures, not
manufacturing deliverables. Presets: smoke (0), standard (1), stress (2), with explicit detail controls.

1. `ventilated-panel.scad`: numerical harmonic profiles, repeated extrusions, ribs, bosses and Boolean cuts.
   Standard: 96 apertures with 240 profile points each. Local edit changes one aperture; global edit changes
   every profile. Always R-eligible. Expected connected solid count: one.
2. `bracket-array.scad`: nonconvex pads, multi-cylinder convex hulls and bored links. Standard: 16 brackets,
   eight reusable types. Minkowski combines a nonconvex pad with a sphere. Local edit changes one pad/link/bore;
   global edit changes all pads/links. Flags select core, hull-only, Minkowski-only and full. Expected connected
   solid count: columns times rows (16 at standard).

Full and core brackets are different shapes. Their timing difference measures workload composition, not an
optimizer speedup. Compare each optimized workload with its own baseline, identical inputs/detail and output
contract. Exercise all four bracket combinations. Local edits must actually change geometry in every preset.

## Measurement and correctness protocol

- Capture exact binary/source identities, build settings, model hashes, CPU/OS, arguments, geometry sizes,
  exit status, raw logs, failures and timeout evidence. Use a new run directory; do not overwrite evidence.
- Fresh-process CSG export includes startup, language/tree generation and text serialization. OFF/STL also include
  geometry and mesh serialization. Neither is a pure phase timer. Their difference is not measured Boolean
  time. OS caches may be warm even though OpenSCAD's geometry cache is fresh.
- Three repetitions with rotated workload order give an initial range, not a statistical performance claim.
  Run sequentially and avoid concurrent builds/benchmarks for controlled comparisons.
- Same-process proxy: six CLI animation frames `base,A,A,B,B,base`. The AST is parsed once, the model is
  instantiated per frame, and geometry caches persist. Distinguish unchanged cache hits from changed frames.
  OpenSCAD frame-summary time starts after language execution; batch wall time includes all stages.
- GUI acceptance remains pending: source edit/reparse, parameter edit, no-change rerun and restore. Measure
  first-result availability, not orbit time or idle waiting. Distinguish `$preview` and full-render behavior.
- Instrument parse, instantiate, primitive construction, backend evaluation, cache keys/lookups, conversion,
  CSG normalization and first-result availability, with cache hit/miss/eviction and node counts.
- Fail warnings, missing frames, empty output or timeout. Validate positive volume, closed/wound surfaces,
  expected components/bounds and edited versus repeated geometry. Ignore incidental triangle ordering.
- Restricted engine acceptance must reject active Hull/Minkowski inside libraries and render() while allowing
  supported graphs and dormant unsupported branches. Keep the full engine available by explicit selection.

## Work after profiling

1. Add low-overhead phase timing/cache counters and establish warm GUI measurements.
2. Fix measured copy/key/conversion costs; compare regressions before changing geometry semantics.
3. Prototype incremental evaluation of proven-pure regions. Include lexical/special variables, `$children`,
   imports/includes and tessellation in dependencies. Preserve echo/assertions/warnings/random semantics.
4. Compare full versus restricted strategies on identical eligible geometry. Separate CPU work, GPU work,
   allocation, transfers and synchronization. Keep Manifold as the measured full baseline.

No speedup target is asserted before profiling. Standard fixtures should take seconds; the runner has a
45-second per-process guard. A timeout fails rather than automatically lowering quality.

## Initial correctness finding

The Minkowski variants report `NoError`/simple Manifold geometry but fail binary-STL re-import topology checks.
An indexed OFF export of the same full bracket model preserves a closed, consistently wound 16-component mesh.
Retain the failing STL round-trip evidence as a separate known issue. Indexed OFF is the reference for this
evaluation study; do not repair or discard failing outputs to make an optimization appear correct. Investigate
the exporter/precision/topology boundary before claiming STL compatibility. OFF coordinate serialization is
also finite precision, so passing indexed topology alone does not prove exact geometry or absence of intersections.
