# Contextual insertion requirements

All five choices accepted on 2026-10-04. Use [the technical plan](3_overall-plan.md),
[source contract](source-edit-contract.md), [preview contract](preview-contract.md) and six implementation phases.
All six implementation phases are locally accepted; see [implementation and evidence](5_post-implementation-notes.md).

- IN01: Implement pick -> searchable Add palette -> choose item -> configure/position preview -> commit. Integrate
  the Shift-A interaction with the existing configurable action/shortcut system.
- IN02: Populate the palette from 11's registry, including capability/availability and provider-defined parameters.
  Do not hard-code every library into the UI. BOLTS retains its distinct intended role as the standards library.
- IN03: Capture document/source/result identity, intended source target, selected instance and available semantic/frame
  context. Missing source provenance cannot authorize mutation of a guessed definition or another open document.
- IN04: Preview an item before changing source. Use 03's transient overlays/tool routing and 08's placement results.
  Parameter changes and placement updates modify only preview state until explicit Commit.
- IN05: Use the provider's contact frame and 08's mating convention for initial orientation; show/allow direction flip.
  Holes and screw shafts enter the surface, while nuts/washers sit against it. Do not infer direction from operation type.
  Support moving in the placement plane, spin and available anchor alternatives with agreed configurable controls.
- IN06: For separate Components prefer meaningful semantic/BOSL2 anchor relationships; otherwise generate explicit
  fixed placement. New Part geometry uses fixed local transforms under IN15. Provider metadata chooses what to
  generate; placement context determines where/how it is inserted.
- IN07: Additive and subtractive operations affect the intended boolean parent. A hole must become a real subtraction,
  including a valid difference/tagged operation where supported. Never represent a hole by appending a positive solid.
- IN08: Handle required includes and name collisions deliberately and minimally. Preserve untouched expressions,
  comments/formatting; never alter a library definition or all repeated instances through accidental targeting.
- IN09: Commit all source changes for one insertion as one guarded 02 transaction and one undo step. Reparse/evaluate
  the result; disk writes remain under normal Save. Cancel, Escape and a failed preview leave source unchanged.
- IN10: Invalidate or explicitly refresh preview after source/result/tab changes. Failed commit preconditions leave
  source untouched and explain the stale/unsupported target. Never silently redirect to the newly active document.
- IN11: Implement an additive primitive and a genuinely subtractive hole first, followed by the approved standard
  component/provider and attachment-aware fixture. Reload independently to prove code fully represents the result.
- IN12: Build without drawings or existing-object manipulation controllers. This branch owns palette/preview and
  include/boolean source edits; 11 owns metadata/fragments and 08 owns placement calculations.
- IN13: Primitives add geometry to the selected Part; holes subtract from its finished geometry. Catalog Component
  entries, including screws/nuts/washers, become separate Components in the containing Assembly or document root.
  Show destination, operation and edit scope. No fusion of hardware into its mounting Part or cross-Component boolean.
  Ordinary SCAD remains editable without converting its existing geometry into semantic Parts.
- IN14: Shared Part/Assembly edits require an explicit shared-edit choice listing affected current instances,
  including differing parameters. No definition cloning, loop expansion or library edits. A unique ordinary source
  call may be edited locally when its complete target/scope is established.
- IN15: New Part geometry has fixed local placement. Components may use live named-anchor relations. Fixed face
  captures follow owner placement, not a changing surface. Display this distinction. Live anchor-driven holes and
  geometric rematching are outside this delivery.
- IN16: Show a movement ghost and asynchronous actual candidate model. Disable Commit while pending, invalid or stale.
  Full preview includes every affected shared instance. Cancel discards all candidates without source changes.
- IN17: Numeric in-plane X/Y offsets, normal offset and spin, configurable G/R/F and Enter/Escape. Select anchors in
  the inspector. Keep navigation available and editor input separate.
- IN18: Helpers/imports/references and geometry for one insertion fit one 02 live-document transaction. Included-file
  edits require an explicitly chosen open editable document. Normal source and Save are the persistent authority.

Automatic structural rewrites accept the forms in the source contract; unsupported targets receive a reason without
partial edits. Guarded preview initially supports deterministic native SCAD with captured include/use inputs.
Uncaptured external geometry/data/font/Python inputs are unavailable for insertion until equivalent capture exists;
normal editor/native evaluation remains available. Verify this boundary before building dependent UI.

## Acceptance cases

| Case | Observable result |
| --- | --- |
| Primitive on a transformed face | Correct world placement and readable local source transform. |
| M4 threaded-hole workflow | Correct approved provider, depth/direction and true subtraction in the intended target. |
| Existing includes/comments/expressions | Minimal include change, no duplicate include or unrelated text rewrite. |
| Repeated module definition | Explicit supported instance/definition target; no accidental all-instance edit. |
| Preview cancel or provider evaluation failure | No source/undo/disk change; normal navigation restored. |
| Commit then undo | Entire insertion, include and boolean wrapper undone together. |
| Source edit/tab switch during preview | Stale operation rejected; no mutation in either wrong or stale context. |
| Save and reopen in an independent session | Generated source recreates intended additive/subtractive geometry. |

## Implementation contract obligations

Consume [11's provider/version contract](../2026-10-03_11_component-provider-adapters/provider-contract.md).
12 supplies captured source/library bytes from 03, preserves the provider's scoped helper imports, allocates helper
names and checks effective module provenance. Compare preview dependency paths/bytes with the bound profile closure;
revalidate immediately before commit. A library update invalidates the draft. Additive screws can point into a surface:
use the returned mating frame and 08's solver, not an extra direction flip inferred from operation type. Catalogs ship
without vendor libraries, so unavailable items retain their dependency/version reason in the Add palette.

Use real 11 provider fragments/schema and 08 placement examples, plus 06's exact source targets and ambiguity states.
Implement the specified preview lifetime/cancellation and source algorithms for includes, collision-free names and
ordinary difference wrapping. Direct rewriting of tagged subtraction internals is outside this initial algorithm.
Use the before/after fixtures, comment/expression/shared-instance cases and explicit unsupported behavior in the source
contract. Use 11's frozen catalog and the accepted controls; do not infer scope from the illustrative M4 example.
