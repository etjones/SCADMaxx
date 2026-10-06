# Cross sections during insertion previews

Source repair: `569220a50`, run `20261006-scadmaxx-all-features`.

The current cross-section persistence keeps valid source/world-space definitions
available without requiring a current evaluated geometry result. Consequently the
old interoperability fixture's `!clip->frame("cut")` assertion is obsolete during
an insertion draft. Do not invalidate the definition just to satisfy that test.

The same change bypassed the previous effective editing lock during insertion.
Preserve exclusive insertion preview ownership: `Controller::editable` rejects
active display drafts, and `draftDisplayChanged` refreshes the cross-section dock
on entry, candidate changes and release. Ordinary repeated cross-section source
editing remains available when no draft owns the viewport.

The adapted fixture checks the unchanged world-space frame, actual draft renderer,
disabled cross-section editing, and restoration of clipping/visibility and enabled
controls after cancellation. It retains source/Undo and mesh-job assertions.
The focused native check passed 3/3 including setup/cleanup in
`native-insertion-section-repair.log`. Full combined/DPI results belong in the run
report. The initial compile needed a direct InspectionMeshRenderer header for the
test's dynamic cast; no dependency changes were required. Final combined native
verification passed all 196 checks, including 33 insertion checks, in
`native-All-scale-1-20261006T225916644Z` at `569220a50`.
