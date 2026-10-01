# Fix forward: arrow scaling

User report: rotation arrows do not scale correctly. Existing requirements remain valid; no rollback.
Starting source `6e8e2f37fc7f988b228a9c907556bfaf591a0fc6`.

The Arrow size setting changed button bounds but not glyph size. A fixed minimum font size also defeated small
navigation scales, and top-left anchoring clipped enlarged right/top buttons. Font-only resizing still failed a
native ink-bounds check at small sizes (`phase6/arrow-scaling`), so arrows now use proportional vector artwork.
Buttons keep their centers where possible and clamp inside the widget. Larger arrows reserve extra axis-label
clearance; the menu triangle also follows navigation scale.

Source commit `8fbde4053f6d721e6fd745690bb26a7fde054d70`.
Native coverage exercises scale 0.35/0.75/1.5/3.0 with arrow sizes 12/30 and verifies all six buttons remain contained.
The contact sheet in `runs/navigation-cube/phase6/vector-arrow-scaling/arrow-scales.png` was inspected.
A premature test launch briefly locked the build executable; the test exited and the link was rerun successfully.
`arrow-scaling-final` therefore covers the vector version before the extra axis clearance; final packaged evidence
is recorded separately as `arrow-scaling-staged150`.

Latest application: `D:/openscad/artifacts/openscad-navigation-cube-arrow-scaling-win64/openscad.exe`.
All 15 native cases pass in the final staged runtime at simulated 150% DPI with system-only PATH.
Private origin verified at the source commit above. This is a completed bounded correction.
