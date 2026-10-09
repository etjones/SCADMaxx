# Geometry bounds implementation handoff — 2026-10-07

## Readiness review and decisions

The exploration was ready to implement without a user behavior decision. Settled the remaining choices:
three-component bounds for 2D (Z zero), diagnostic plus undef for empty/invalid geometry, and no direct
geometry-value output in this first version. Normal module calls remain the display mechanism.
Capture instantiates module arguments immediately in lexical scope; Boolean evaluation is lazy and cached.

## Local implementation

Worktree: `D:/openscad/wt-openscad-geometry-bounds`, branch `feature/geometry-bounds`.
Base: `07b22af25704af0db39959773751fb5c6e4debbe`. Local feature commit:
`cbf75e737de7f4f36882a23968298bdabdcb699d`; clean owner worktree, no push.

- Parser and Expression: `{{ statements }}` with its own LocalScope and explicit union root.
- Value: opaque geometry alternative with cloning, identity equality and safe string output. Captures retain
  the literal AST and instantiated node tree, without retaining a lexical Context for deferred instantiation.
- `geometry_bounds(shape)`: positional/named argument, OEP8 min/max/size/center, finite-result validation,
  empty diagnostics and cached repeated queries. Requires `object-function`, like its object result API.
- GeometryEvaluator: opt-in strict dimension/transform handling; strict cache namespace cannot consume a
  permissive cached result that dropped invalid operands. Existing rendering callers retain their defaults.
- Source documentation and `examples/SCADMaxx/geometry-bounds.scad`.
- Object echo fixture and expected output: exact subtraction bounds, transforms, multiple children, 2D,
  local assignments/modules, function-returned captures, named argument, nested containers and reuse.
  The existing OBJECT_TEST glob discovers it; reconfigure to include the new file.

This is a focused implementation informed by #4478's proposal, not a port/merge of its mesh-array code.
No shared foundation changes were required. The user subsequently authorized the local commit and integrated validation.

## Integrated validation, 2026-10-07

Merged into the maintained integration as `2c0cda639`; integration-only shared-scope repair `80194e4c5`.
The existing build directory and shared vcpkg packages were reused. Incremental build and parser generation
passed (zero Bison conflicts). Evidence: `D:/openscad/runs/20261007-geometry-bounds-reintegration/report.md`.
All 497 unit cases passed; four object/geometry echo regressions passed. All ten language-guide examples
passed on Manifold and CGAL (46 checks including geometry error cases and rendered bounds).
The standalone owner was not separately built. Cancellation responsiveness, exhaustive malformed capture
recovery and GUI interactions were not newly validated. The detailed checklist below retains those follow-ups.
Keep readiness false until an explicit promotion request: nothing was pushed to Dropbox or GitHub.

## Validation still required

For broader owner-level acceptance beyond the integrated checks above, retain this checklist:

1. Configure/build this owner with the recorded Windows/shared-vcpkg profile; verify Bison reports no conflicts.
2. Run the object/echo suite and new fixture with both available CGAL and Manifold backends, plus lazy-union.
3. Exercise empty capture and complete subtraction, wrong/missing/extra/named arguments, mixed 2D/3D at nested
   operators, non-finite transforms, disabled object-function and repeated evaluation after source changes.
4. Exercise cancellation during expensive query evaluation and existing evaluation recursion limits; exceptions
   propagate through the implementation, but responsiveness has not been demonstrated. There is no new GUI job
   scheduling or asynchronous evaluation path. Imported files follow normal evaluator/cache semantics.
5. Exercise parser error recovery and AST printing of nested captures, followed by normal document evaluation.
6. Check ordinary render behavior and cache reuse, particularly rendering a previously rejected mixed-dimension
   shape and querying a previously permissively rendered shape.

Commit only when requested. After validation and explicit promotion authorization, update local/accepted/validated/
promoted heads, set the first feature commit as `featureMarker`, remove `implementationPending`, and mark ready.
Do not use the prerequisite-only committed HEAD as a completed feature. Keep earlier integration/builds untouched.


## Lifecycle closure — 2026-10-07

Moved to done at the user's request. Existing verification evidence and historical limits are preserved.
The user's acceptance criterion for this PR is successful integration and Windows build; recorded integrated checks satisfy it.
