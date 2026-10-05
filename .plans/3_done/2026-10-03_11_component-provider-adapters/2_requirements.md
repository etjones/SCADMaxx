# Component providers: requirements

All three product decisions accepted on 2026-10-04 local time: bounded initial catalog, declarative user/project
providers, shipped catalogs with separately supplied libraries. The user explicitly requires version matching.

- PR01: provide eight initial entries: cube, sphere, cylinder, plain-hole mask, BOSL2 metric threaded-hole mask,
  BOLTS ISO4017 screw, ISO4032 nut and ISO7089 washer. Sizes M3/M4/M5/M6/M8 for the four library entries. These are
  supported catalog families, not complete library coverage. BOLTS hardware uses its library's simplified threads.
- PR02: expose stable provider/item IDs, names/categories, input types/defaults/limits, units, geometry purpose,
  import requirements and insertion frames. Numerical source lengths are millimetres; no implicit model-unit conversion.
  Carry geometry/component insertion role separately from operation. The three BOLTS entries are Components; the
  other entries are geometry. Reject subtractive Component recipes. This follows 12's accepted destination decision.
- PR03: generate readable ordinary SCAD calls, required imports and any scoped helper definitions from validated
  values. Return fragments; never edit source, save files, place geometry, render previews or implement an Add menu.
- PR04: keep additive/subtractive purpose independent of placement direction. In particular a screw's shaft can
  point into a surface although the screw is additive hardware. 12 owns the actual boolean operation and placement.
- PR05: support user/project catalogs without recompilation. A declarative file describes module calls or existing
  SCAD wrappers; it cannot install executable Python/native application plugins. Unknown schema fields are errors.
- PR06: ship catalogs, schema, examples and matching metadata only. Do not bundle, install, update or download BOSL2,
  BOLTS or other third-party SCAD library code. Research/test copies remain external to shipped application assets.
- PR07: distinguish catalog schema version, provider release version and supported library revision. Match installed
  files against an explicit tested profile; do not infer compatibility from a greater version number or Git HEAD alone.
- PR08: report expected and detected library identity, resolved directory and an actionable mismatch reason. Missing,
  modified, unsupported, shadowed or ambiguous dependencies disable affected entries while independent entries work.
- PR09: use normalized content hashes of every file in the recorded dependency closure to identify supported
  revisions. Line-ending changes alone do not invalidate a match. Files edited without changing a version label do.
  A label such as BOLTS's development is not a unique library version. Preserve both raw label and verified release.
- PR10: match the files the evaluator will actually load, including document-relative shadowing, search-path order,
  nested imports and live included buffers. A match to another installation elsewhere does not enable the item.
- PR11: changes to catalog, source context or library bytes invalidate the binding used by a preview. 12 must recheck
  before source commit. Editing or updating an external library never silently changes the adapter for an active draft.
- PR12: generated source remains usable without the catalog when its SCAD library dependencies are present. Record
  provider/catalog/library identity in a concise source comment; do not claim that this freezes external library files.
- PR13: isolate BOLTS imports in generated helper-module scope; do not change user globals or vendor files to obtain
  millimetre geometry. Keep BOSL2 imports at file scope because its nested use declarations require that placement.
- PR14: deterministic discovery and duplicate-ID diagnostics; no implicit overriding by whichever catalog loads last.
  New profiles for an item have the same exposed parameter contract and must have disjoint matching fingerprints.
- PR15: deliver native registry/query/generation APIs, a headless diagnostic CLI, portable install rules and meaningful
  schema, version, resolution and generated-geometry checks. Work independently of features 09/10 and of 12's UI.

## Concrete acceptance

| Input or situation | Required result |
| --- | --- |
| Empty external library directories | Four built-ins available; four library entries explain missing dependencies. |
| BOSL2 2.0.766 matching recorded closure | Threaded-hole recipe selected; modified screws.scad with same label rejected. |
| BOLTS official 0.4.1 asset | Identified as 0.4.1 by fingerprint despite its internal development label. |
| Older/newer unlisted revision | Unsupported; no nearest-version selection or automatic update. |
| Two installed copies, first one incompatible | Report the effective incompatible copy; do not select a later one invisibly. |
| Valid project catalog with a SCAD wrapper | Entry appears without a C++ change and emits an ordinary wrapper call. |
| Unknown item/input, NaN, bad enum, duplicate JSON key or provider ID | Precise diagnostic; no generated fragment. |
| BOLTS_MODE=bom and BOLTS_DEFAULT_UNIT=in in calling scope | Scoped helper still yields the tested mm hardware. |
| Threaded-hole mask subtracted from 20 x 20 x 10 block | Actual cavity, unchanged block bounds; source reproduces geometry. |
| Extracted SCADMaxx package with no external libraries | Catalogs discoverable; no BOLTS/BOSL2 source accidentally bundled. |

Deferred: NopSCADlib, exhaustive catalogs, automatic module introspection, library installation/update management,
native/Python plugins, GUI palette/placement, and inverse editing of existing objects. 09 and 10 remain postponed.
