# Shared action icon refresh and toolbar overflow

Run: `20261006-scadmaxx-all-features`. Source repair: `29e39eb92`.
The repaired combined run passes selection 24/24, provenance 9/9 and cross sections
20/20, including the previously stuck overflow-layout transition. Final combined
verification at `569220a50` passed all 196 checks in 15 suites in
`native-All-scale-1-20261006T225916644Z`. Consult the run report for delivery checks.

The combined native run repeatedly spent time in toolbar overflow layout after
navigation and selection resized the window. Cross-section numerical checks and
the GPU performance test passed, but event processing stalled afterward. CDB
evidence `native-clipping-progress-cdb.log` shows QToolBar rebuilding its overflow
menu and IconEvents rewriting shared QAction icons during ActionAdded handling.
Each replacement emits changed() and invalidates toolbar layout again.

The first focused repair stores the generated icon cache key on the action and
skips rebinding when that key still matches. An externally replaced icon is still
converted. Explicit Icons::refresh forces rebinding for appearance changes.
Buttons continue to receive their own palette/state context, including the queued
rebind after Qt copies a default action's icon. Do not remove that behavior to
fix the layout loop: it is required for checked toolbar icon contrast.

Reproduce with the complete native suite in a single window, not only isolated
cross-section tests. Retain exact image assertions. A separate selection fixture
repair `c68d69b45` temporarily hides and restores scale/crosshair guides: four
coplanar guide-intersection pixels varied after selection clearing, while model
captures and selection bounds matched. Selection then passed 24/24 in the combined
run. Removing the cross-section fixture's redundant hide/show cycle alone did not
solve the toolbar loop.
