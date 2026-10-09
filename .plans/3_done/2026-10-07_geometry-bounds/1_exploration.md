# Geometry bounds language feature

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

## Purpose and current state

Let SCAD source query evaluated geometry and use its axis-aligned bounds to place or size other geometry.
This is the focused language feature requested on 2026-10-07 after reviewing OpenSCAD PR #4478.
Implementation was authorized on 2026-10-07 and is locally written, awaiting build and validation.
No build or tests were authorized by the implementation request. See `5_post-implementation-notes.md`.

- Owner: `feature/geometry-bounds`.
- Worktree: `D:/openscad/wt-openscad-geometry-bounds`, created through `openscad-master`.
- Direct prerequisite/base: OEP8 #6081, `07b22af25704af0db39959773751fb5c6e4debbe`.
- Stack/source: `geometry-bounds` / `geometry-bounds-local`, selected but `ready: false`.
- Branch contains uncommitted implementation; no feature commits, validation or promotion yet.

## Proposed public behavior

Introduce geometry values and `geometry_bounds(shape)`, returning an ordinary OEP8 object with
`min`, `max`, `size` and `center`. `size = max - min`; `center = (min + max) / 2`.
Center is the bounding-box midpoint, not a centroid or center of mass.

Implemented syntax, not yet build-verified:

```scad
shape = {{ translate([10, 0, 0]) cube([40, 30, 20]); }};
bounds = geometry_bounds(shape);
echo(bounds.min, bounds.max, bounds.size, bounds.center);
translate([bounds.max.x + 5, 0, 0]) cube(5);
```

Bounds include transforms inside the captured shape and describe evaluated Boolean results, not the
union of preview operands. Coordinate axes are those of the captured geometry; later placement of
an output instance must not retroactively alter the value. Proposed 2D convention: three-element
vectors with Z zero. Empty geometry should return `undef` with an actionable diagnostic, not infinite
or misleading zero bounds. Reject non-geometry arguments and mixed-dimension failures cleanly.

Geometry capture must preserve lexical values safely, support passing shapes through functions, and
avoid inadvertently emitting the captured shape. The first version does not add geometry-value output:
call the same ordinary module separately to display it. Do not import #4478's competing output syntax forms.

## Boundaries and implementation approach

Reference: https://github.com/openscad/openscad/pull/4478, reviewed prototype head
`f33829c1d80af2b02aa06382584aa63e878fe529`.
Use its geometry-literal/value and evaluation approach as design input, preserving appropriate attribution.
Do not merge the full prototype: OEP8 objects already have their own selected owner.

The main work is parser/expression/Value plumbing and safe geometry evaluation from a function.
The bounding-box arithmetic already exists in core `Geometry::getBoundingBox()`.
Evaluate through the current geometry evaluator and cache, supporting Manifold and CGAL when available.
Do not carry over the prototype's old CGAL-only mesh extraction or allocate point/face arrays for a bounds query.
Account for evaluation failure, recursion, cancellation, cache lifetime and repeated queries.
An exact bounds query can require expensive Boolean evaluation; it must not trigger a GUI re-render loop.

Exclude module references, hybrid literals, mesh-array extraction, oriented bounding boxes, surface area,
volume and center of mass. Existing CLI/HTTP inspection is distinct from this in-language API.
No dependency on consumer UI branches or the all-features build. If shared services become necessary,
put shared changes in their owner and add a normal forward merge and an explicit dependency.

## Implementation and acceptance handoff

1. Add the minimal geometry value/literal plumbing against current OEP8 syntax.
2. Add `geometry_bounds()` and documented error/empty/2D semantics using evaluated geometry.
3. Document syntax and examples; prepare focused cases for primitives, transforms, Boolean cuts,
   empty results, 2D, invalid arguments, lexical capture, repeated queries and backend differences.
4. Run builds/tests only after explicit authorization. Include an example where subtraction changes
   an extreme bound, so preview-union approximations cannot accidentally pass.
5. Record implementation evidence and exact local head. Replace the provisional manifest checkpoint;
   populate `featureMarker` with the first feature implementation commit, not the OEP8 base.
6. Commit when requested; promote to the Dropbox bare source repository only with explicit push authorization.
   Update validated/promoted heads and readiness before an integrated build includes this feature.

Maintain prerequisites by normal forward merges, never cherry-picks. Keep plans in the controls repository.
