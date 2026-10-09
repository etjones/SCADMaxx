# Visual checks against retained Slant 3D videos

Frames are retained under `D:/openscad/artifacts/slant3d-research/frames` with source video ID, timestamp and
SHA-256 sidecars. This record describes what was visible, rather than treating every extracted frame as useful.
Full acquired videos remain under `media`. The frame times below are seconds from the video's start.

| Source | Frames inspected | Observation and implication |
| --- | --- | --- |
| [Basic tips](https://www.youtube.com/watch?v=-gm6hzbAqLk) | 62, 135 | The bottom recess has sloping faces and a surrounding contact rim. The diagonal illustration alone does not demonstrate a stable finite bed-contact patch. T003/T005 remain conditional. |
| [Tolerance design](https://www.youtube.com/watch?v=XKrDUnZCmQQ) | 337, 643 | Relief is visible beneath a mating flange; rows of fin slots are visible in the later CAD view. Neither frame establishes a universal clearance. |
| [Support fins](https://www.youtube.com/watch?v=vnn4XeKQobs) | 499, 690, 830 | The first two frames show the presenter. The later CAD view shows an edge fin and connecting tines; it does not establish exact dimensions. |
| [CAD brim](https://www.youtube.com/watch?v=4GxZXxNraY0) | 132, 355 | The slicer view shows a thin brim; the later CAD section shows a bottom chamfer. No dimension is adopted from the images alone. |
| [Printed hinges](https://www.youtube.com/watch?v=BWsUk1xSSn4) | 90, 145, 210, 325 | The 90 s frame shows a flexible slotted sheet; 145 s shows two hinge pieces with tapered pivot geometry. The other two show the presenter and add no geometric evidence. |
| [Magnet retention](https://www.youtube.com/watch?v=BwUzOJ8B_H0) | 270, 420, 540 | A disk pocket has a mouth narrower than its cavity; the cylindrical-magnet sketch has two retaining lip regions. The later presenter frame does not resolve detailed sphere-pocket geometry. |
| [Bore reinforcement](https://www.youtube.com/watch?v=UfJIMn4nvsA) | 221, 240, 260 | The 240 s slicer view shows dense local paths in a bracket end near the bore, while other portions retain sparse infill. This supports the toolpath mechanism, not a measured strength result. The other frames show the presenter. |
| [Vase-mode structure](https://www.youtube.com/watch?v=mHRQkreuuDA) | 185, 199 | The CAD view shows a folded prism-like shell. The overview does not by itself establish continuity at every height; retain the slice-continuity requirement in T122. |
| [Dome interiors](https://www.youtube.com/watch?v=udEeJjzEQZI) | 75, 145, 195 | At 75 s, the section shows a rounded outside and a pointed inner roof with a thicker apex, confirming T125. At 145 s the support profile is still being drawn; the later revolution view shows a flattened inner crown region. No universal support gap is inferred. |

When a needed detail is still unclear, revisit another timestamp or a higher-resolution version before adding
a precise geometry rule. A presenter-only frame is not a visual verification of the model.
