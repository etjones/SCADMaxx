# Live clipping requirements

These requirements freeze the requested behavior from [the exploration](1_exploration.md). The
[technical design](3_overall-plan.md) specifies eight enabled planes, prepared-mesh GPU clipping, manipulation and
03/14 integration. Initial mesh preparation may take time; plane movement must not trigger repeated evaluation.

- CL01: Provide a dock to create, name/rename, select, edit, enable/disable and delete Sections, plus a global clipping
  toggle. Named persistent Sections use 14's object/lifecycle contract; no private clipping-only store.
- CL02: Support XY/XZ/YZ presets and free orientation, exact numeric angle/offset entry and a bounds-derived slider.
  Movement always follows the plane's current normal, including after rotation. Negative offsets are valid.
- CL03: Initial presets pass through model bounds center. Changing a control updates the same canonical origin/normal;
  angles, slider position and gizmos must not drift into independent definitions. Flip reverses the retained side.
- CL04: One-shot Pick point changes origin while retaining orientation. Pick + align also chooses the surface-relative
  normal sign that removes the clicked outer wall and reveals the interior. Miss/cancel preserves the previous plane.
- CL05: Show an origin marker and optional helper plane. Helper visibility is independent of clipping enablement.
  Manipulate the plane along its normal and rotate around its current origin; dock values update immediately.
- CL06: Multiple enabled planes combine by intersection of their retained half-spaces. Global disable reveals the
  uncut display without deleting definitions or individual enable states.
- CL07: Clip render-side during dragging, without CSG re-evaluation or changing model geometry/source. Retain a useful
  frame rate under supported model/plane limits; measure latency in the renderer proof rather than inventing a target.
- CL08: Remove a model face cleanly when the clipping plane coincides with it. For the retained-positive convention,
  retain dot(p-origin,normal) > epsilon. Derive/verify scale-aware tolerance; do not eat adjacent thin walls.
- CL09: Helper depth bias/visual offset must not move the mathematical section plane. Optional caps/highlights must
  not fight with a coincident face. Expose them only on verified supporting backends; caps are conditional scope.
- CL10: Persist/reopen deliberate named Sections through 14, using normal dirty/save/conflict handling. Temporary
  inspection may remain unsaved; deleting it leaves model geometry/source unchanged. Drawings use the same Section ID.
- CL11: Keep navigation and annotation overlays working through 03's shared tool/overlay routing. Stale picks or
  document switches cannot move a Section belonging to a different result/document.
- CL12: Explain backend/plane-count limits at the affected action; do not silently ignore additional enabled planes.

## Acceptance cases

Exercise all seven workflows in exploration: orthogonal, picked point, surface alignment, angled, direct manipulation,
saved/reopened combined inspection and temporary inspection. Specifically include:

1. Oblique and transformed faces, reversed normals, negative offsets and move-after-rotation.
2. Exactly coincident face removal, adjacent thin wall preservation, very small/large bounds and helper visibility.
3. Two orthogonal planes, global off/on and independent individual toggles; save/reopen retains intended definitions.
4. Instrument evaluation count while dragging: no repeated CSG evaluation or unintended source change.
5. Switch tabs/change source during a pick; cancel safely. Exercise existing annotations/navigation with the dock open.

## Verification gates and exclusions

03/14 must be implemented and their specified interfaces verified before this branch. Prove clipping on the covered
mesh paths with the prescribed tolerance, resource, plane-count and performance fixtures. Caps are explicitly
unavailable in the initial delivery, retaining their previously conditional status.
Computed contours/measurements/export belong to 15 and its consumers; slabs and explicit source-creation actions are
later extensions. This branch must not acquire a dependency on drawings or implement its own numerical section kernel.
