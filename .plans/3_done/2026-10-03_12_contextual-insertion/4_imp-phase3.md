# Phase 3: Components, provider bindings and placement

Requirements: IN02, IN05-08, IN11-15, IN18. Read 3_overall-plan.md and both source/preview contracts first.

1. Consume 11 insertionRole and matched immutable bindings. Component/geometry policy comes from data, not catalog
   names. Add a dependency-free fake Component catalog for native tests, without changing the four shipped built-ins.
2. Implement PlacementDraft through 08 capture/resolve/solve operations. Geometry solves in destination local frame;
   semantic Components author named or fixed-owner anchors/attachments; ordinary Components use a fixed root transform.
3. Generate fresh Part/helper definitions, Component calls, literal contact anchors and Attachment declarations.
   Place definitions at file scope, calls/references at direct Assembly/file scope. Reserve all namespaces separately.
4. Ensure repeated Assembly insertions use relative paths and explicit shared scope. Evaluate every affected instance;
   test differing parameters and that a fixed hole remains local while a named Component follows anchor changes.
5. Preserve scoped BOLTS imports and ordered BOSL2 includes. Validate native generated module provenance and the actual
   dependency closure against the captured profile. Test missing/modified/locally shadowed libraries.

Checks: insertion-placement and insertion-providers; also providers-external with explicitly supplied pinned libraries.
Cases: transformed face; Mate/Align Flip at unchanged origin; X/Y offsets unaffected by spin; sphere bottom frame;
mirrored/nonuniform destination and singular rejection; different widths sharing a Part; repeated Assembly siblings;
IDs colliding with imported definitions and owner anchors; no nested Component inside a Part.
named-component.after.scad puts peg origins [10,10,10] and [65,10,10]; changing fixture-a width to 24 moves only its peg
to [12,10,10]. shared-part.after.scad retains cuts at local x=10 on both Parts, irrespective of width.
M4 BOLTS screw under-head meets the surface and shaft points inward; nut/washer sit outward. Threaded hole produces a
real cut and catalog depth, with pinned native dimensions from 11. Test hostile ambient BOLTS mode/unit and $slop.
Unavailable external libraries can skip ordinary CI's optional suite, but feature handoff needs actual passing runs.

Exit: all initial entries place/generate correctly and source alone recreates relationships. No annotations/placement
depend on hidden UI state. If an owner API cannot support the contract, return to planning rather than bake a named
live attachment into numeric coordinates or alter a shared definition without explicit scope.

Use the overview verification-contract.md with the actual isolated build path: build OpenSCADExe and
OpenSCADUnitTests, run ctest -N, then the named CTest labels. Native cases use the registered GUI harness selector.
No zero-test result counts as passing; retain commands, discovery and logs in the feature run directory.
