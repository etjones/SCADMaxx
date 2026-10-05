# Surface selection at fractional display scaling

Applies when `SelectionService::pick` validates only framebuffer coordinates and
`QGLView::resizeGL` rounds logical size times DPR with `qRound`.

In run `20261004-scadmaxx-all-features`, the complete native suite passed at 100%,
but `native-Selection-scale-1.5-20261005T010931981Z/TestSelection.txt` failed
`resizedBordersAndInstances`: picking at logical y == widget height returned Miss
instead of InvalidViewport. At an odd logical height and DPR 1.5, the framebuffer
rounds up; flooring the supplied pixel coordinate incorrectly admits the extra
half physical pixel. This is a production boundary check, not a weakened test.

Repair `SelectionService::pick` immediately after obtaining `view`: reject negative
logical coordinates and x >= view width or y >= view height before framebuffer
conversion. Keep SurfacePickMath's finite/DPR/framebuffer validation unchanged.
Existing interior-edge, resized-instance and exterior-edge native checks cover
the behavior. Run the Selection native suite at 100%, 150%, and 200%, then the
production build/tests. Repair commit: `c5d03a05c1f45ce8ada0538eeb4e6e36c8b9054d`
in the shared OpenSCAD repository. First focused repair attempt passed all 20
Selection checks at each scale: run evidence directories ending `011605495Z`,
`011621854Z`, and `011638354Z`. The native runtime was built from parent
`ed23c24b5` plus the exact `selection-boundary-repair.patch` subsequently committed;
its embedded revision still names the parent. Final production validation is
recorded separately at the committed SHA in the run report.

Final production checkpoint passed at that commit:
`logs/20261005T012154078Z-test.json`, 687685 assertions, zero failures/errors/skips,
plus Manifold/CGAL STL, PDF and PNG smokes. The repaired binary also passed all
seven scale-sensitive native suites at 150% and 200% (112 checks per scale).
Local retention ref: `refs/scadmaxx/repairs/selection-fractional-dpi-bounds`.

Replay only if the bounds check is absent. Preserve all evaluation, draft,
inspection, lifetime and stale-result checks around it. No dependency changes.
