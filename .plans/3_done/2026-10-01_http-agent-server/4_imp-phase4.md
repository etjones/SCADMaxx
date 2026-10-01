# Phase 4 — Evaluated model tree and available summaries

Status: implemented and committed as 42aacf037. Depends on phases 2–3. Covers R08, R10–R12, R18, R21.

## Implementation

1. At safe native evaluation/publication boundaries, serialize the instantiated `AbstractNode` hierarchy into bounded
   detached records. Do not reuse native indices as durable public IDs or let transport retain raw `modinst` pointers.
   Verify both SourceFile and node lifetimes until source mapping has been copied.
2. Distinguish `absoluteRootNode` from effective `rootNode` selected by `!`. Record effective roots, children order,
   operation kind, native modifiers and synthetic/group nodes. The public core tree is instantiated geometry, not an
   assertion that normalized renderer CSG retains the same structure. Lowered CSG is not a third required tree API.
3. Add typed property adapters for common primitives, transforms, Boolean operations, colors, extrusions, projection,
   offsets and imports where values are already held. Preserve typed undefined/non-finite/omitted values. Unsupported
   kinds remain traversable with kind/name/location and declared missing properties.
4. Copy available source mapping from module instantiations and Location while valid. Repeated calls/loop expansions
   can legitimately share source spans. Do not invent one-to-one geometry/source identity or runtime expression values
   not retained by OpenSCAD.
5. Associate tree completeness/provenance with attempt and successful result publication. Failed instantiation must
   not replace the old displayed model's tree; an empty successful result has an explicit empty tree. Retain bounded
   older DTOs while their result remains displayed or mark eviction explicitly without changing result identity.
6. Publish observed dependency provenance from real evaluation separately from parse-only discovery. Imports whose
   paths resolve at evaluation may enrich the manifest; missing hashes remain unknown. Hash changes alone do not
   identify successful geometry generation.
7. Add optional parameter/geometry readers only from existing stable typed data. Freeze their supported-field lists
   in the contract. Initial candidates: parameter metadata/current values, renderer/backend/dimension, cached bounds
   and available facet/triangle counts. Never instantiate geometry, perform a full render or compute volume/validity
   merely to answer a query. Record omitted capabilities with reasons rather than allowing them to delay core delivery.
8. Apply process-wide snapshot retention and bounded serialization; cache once per relevant result, not per status read,
   camera frame or node request. Keep ordinary compilation behavior unchanged if inspection reaches its own limits.

## Validation

- Fixtures: repeated module calls, parameter changes, nested transforms/difference, loops, `!`, `%`, `#`, `*`, import,
  2D projection and empty geometry. Check hierarchy, evaluated values and shared source locations.
- Recompile while paginating the previous tree; old references either read their retained DTO or return expired,
  never resolve into new geometry or freed memory. Test close/reopen and server restart too.
- Failed parse/instantiation/render preserves correct previous displayed-result association. Syntax and evaluated
  tree requests identify distinct representations and provenance.
- If summaries ship, verify facet-versus-triangle distinctions, unknown units, stale Customizer settings, empty/2D/
  unsupported backends and absent bounds. Absent metrics must not become zero or trigger extra geometry work.
- Compare normal compile behavior and memory growth with inspection disabled/enabled; budgets cap additional retained
  data even for highly expanded models. Truncation never hides the fact that descendants/properties are missing.

## Exit evidence and handoff

Retain structural/result fixtures, source-mapping examples, concurrency/memory checks and a capability field matrix.
Document unretained mappings/properties explicitly. Phase 5 can rely on consistent displayed-result IDs; phase 6
must exercise actual tree traversal through the public client, not only internal serialization tests.
