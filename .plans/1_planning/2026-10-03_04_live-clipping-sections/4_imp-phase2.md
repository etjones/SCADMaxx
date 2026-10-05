# Phase 2: clipping dock and shared Section lifecycle

Covers CL01-CL03/CL06/CL10/CL12.

1. Build ClippingController/Dock rows and actions from valid 14 Section records plus transient objects. Store only
   enable/helper/global state in personal backing. Add no independent saved-plane schema.
2. Implement presets, bounds-projected slider, numeric offsets, derived azimuth/elevation, flip/reset and separate
   helper/global toggles. Enabling plane nine is refused without changing earlier planes or their saved definitions.
3. Wrap each source-backed control gesture in one 14 draft/commit; transient changes remain transient. Preserve
   base expressions and source-only field limitations. Promote explicitly; normal Save handles disk conflicts.
4. Native TestClipping: create/name/enable/disable/delete/promote/reopen, combine two planes, global off/on, empty
   model, stale/missing reference, an invalid Section and source-only adjustment expression. Slider negatives and
   out-of-bounds numeric entry must work. First enable shows cancellable preparation status when needed.
5. Undo/redo source-backed offset and deletion with another feature referencing the same Section ID. Verify no copy
   was created and missing-reference behavior comes from 14. Dirty Save cancellation preserves the source buffer.

Exit: the dock drives one canonical Section model; named persistence and transient inspection remain coherent.
Run [clipping-math], TestClipping and the relevant TestDesignObjects persistence/undo cases.
