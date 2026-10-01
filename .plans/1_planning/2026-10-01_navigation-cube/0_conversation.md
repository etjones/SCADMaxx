## Remaining behavior decisions

The visual design and explicit user choices in `1_exploration.md` are settled. These questions resolve behavior before
moving beyond exploration. Suggested answers below are recommendations, not decisions; other answers are welcome.
Experimental pixel sizes, opacity values and timings do not need to be fixed now.

1. What does recalling a saved view restore?

   Recommended: the complete camera (orientation, pan/target, zoom/distance, field of view and projection), with no
   automatic fit and no changes to display overlays. Alternative: restore the camera while keeping current projection.
   The existing preserve-projection decision still applies to cube clicks and arrows.

-> 

2. How is a saved view recalled from the list?

   Recommended: double-click or Enter recalls it and leaves the popup open; single-click selects for Remove/Rename.
   Alternative: single-click immediately recalls, which also moves the camera when selecting an entry for management.

-> 

3. When are Add/Remove/Rename changes written to the document's companion file?

   Recommended: ordinary document Save/Save All/Save As/Save a Copy, matching annotation behavior; track unsaved metadata
   and prompt on close. Untitled-document views remain in memory until first Save. Alternative: immediately save view
   changes for named documents, with an explicit policy still needed for untitled documents. Manual copying needs both
   the SCAD source and companion in either case.

-> 

4. Should dragging the cube orbit the camera in this version?

   Recommended starting scope: clicks, roll and arrow navigation only; ordinary viewport dragging already orbits.
   Alternative: include cube drag-orbit now, with a movement threshold separating drags from clicks. Neither option
   makes the cube draggable to a new screen position; developer position controls are already included.

-> 

5. What snapping and arrow behavior should be the baseline?

   Recommended: exact axis-aligned faces, 45-degree bisector edge views and true isometric corners, with world Z upward
   where possible and deterministic top/bottom up directions. Clicking a facet resets roll to that target's standard
   orientation. Preserve pan/target, distance, field of view and projection. Use 90-degree roll and 15-degree directional
   steps (both tunable), one step per click; no hold-repeat, modifier shortcuts or separate opposite-view button yet.
   Alternatives: 90-degree directional steps, or preserve current roll as closely as possible when snapping.

-> 

6. How far should this version replace View-menu usage?

   Recommended: retain the existing menu/shortcuts and use shared actions; add a compact Center / View All / Reset row
   to the popup. Keep rendering modes, zoom buttons, toolbar visibility and model Animate in existing UI. Reset keeps
   current OpenSCAD semantics; no separate configurable Home. Alternative: the accepted popup exactly as pictured,
   with these additional camera actions staying in existing UI. A wider replacement needs an explicit command list.

-> 

7. Which preferences persist, and where are camera-animation controls available?

   Recommended: remember ordinary viewport overlay choices, popup size and camera animation on/off/duration globally;
   expose camera animation through normal Preferences as well as dev controls. Keep temporary position/scale/appearance
   experiments session-only, with Copy settings for retaining an experiment. Provide a normal show/hide-navigation
   preference outside the popup so hidden navigation is easy to restore. Alternative: also persist dev tuning across
   restarts. Saved camera entries remain per-document regardless.

-> 

8. What should appear in model-image exports and annotation captures?

   Recommended: exclude the cube, triangle, popup, dev window and statistics text from model PNG exports, animation
   frame images and annotation/agent viewport captures; preserve existing axes/edges/etc. capture semantics. Full-window
   screenshots include visible UI. Alternative: include statistics when enabled, while still excluding interactive UI.

-> 
