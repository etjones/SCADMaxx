# 3D print design tips

Use the [trick inventory](3d-print-tricks-inventory.md) to select a technique by purpose and inspect its evidence.
The source is [Slant 3D](https://www.youtube.com/@slant3d), a channel focused on FDM production printing.
The initial channel capture contains 640 videos, 115 livestreams and 685 Shorts. Acquisition and review are
in progress; do not interpret this reference as a completed review of the whole channel.

## Apply a technique deliberately

Establish the part's function, mating dimensions, intended load, material, build orientation and assembly sequence.
Name the specific problem being solved before choosing a trick. A cavity needed for electronics, a tool or a
mating part remains a functional cavity; advice against injection-molding-style hollowing does not remove it.

Treat CAD solid geometry separately from slicer infill. A solid CAD envelope does not require 100% infill.
Keep nominal dimensions, clearance per side, interference, compliant-member thickness, extrusion width,
layer height and cosmetic details as separate parameters. Do not encode video demonstration dimensions as
universal tolerances. Record dimensions that remain to be calibrated on the intended process.

Preserve [design reasoning](design-reasoning.md) and the skill's two-pass
[edge-treatment](edge-treatments.md) workflow. Establish the untreated functional part first; apply supported
BOSL2 treatments separately. Check whether a treatment near the build plate creates an unsupported underside
or removes a functional contact surface.

## Choose by purpose

| Design problem | Start with | Inventory |
| --- | --- | --- |
| Sagging holes, ledges or roofs | Change the roof or underside while keeping its functional region | T016-T017, T024, T058, T124-T127 |
| Fits that bind or vary | Lead-ins, short locating lands and local compliant members | T007-T022, T103-T108, T144-T151, T170-T171, T186-T188 |
| Thin part tips over | Stable build contact, broad-foot fins or support combs | T025-T030, T045-T048 |
| Warping or difficult bed removal | Deliberate contact area, local hold-down and shrink-path relief | T002-T003, T036-T048, T052-T055 |
| Weak root, bore or bracket | Align layers with loads and reinforce the stressed region | T049-T063, T109 |
| Moving printed joint | Free travel, in-plane springs and printable pivot roofs | T073-T085, T131-T133 |
| Fasteners, magnets or glue | Retention geometry plus insertion and tool access | T086-T102 |
| Uneven visible finish | Orientation, repeat texture and deliberate text placement | T004-T005, T064-T072, T110-T115, T123 |
| Rain-exposed enclosure | Service-oriented lips, baffles and low drainage | T116-T118 |
| Stable feet or efficient thin wall | Printable foot roots or a continuous folded perimeter | T119-T122 |
| Impact-tolerant enclosure or hand grip | Compliant envelope, broad mounts and printable handles | T128-T130, T134-T143 |
| Vent routing or a captive drawer | Sloped passages, retained separating walls and deliberate sliding stops | T152-T163 |
| Curved object with difficult bed contact | Intentional flat, controlled support or changed envelope | T164-T169 |
| Compliant cushion or low-load drive | Explicit material distribution and functional contact/load surfaces | T175-T179 |

## Parameter contract

Use millimeters unless the design declares another unit. Distinguish these values even if several initially
share a number:

- `nominal_*`: required part, hardware and mating-envelope dimensions.
- `clearance_per_side`: positive free space; a circular pocket diameter is nominal diameter plus twice this value.
- `interference`: intended overlap at a rib, fin or detent; do not apply it to the whole locating surface by accident.
- `lead_in`, `engagement_length`, `stop_position`: entry, working contact and final seating.
- `flex_length`, `flex_thickness`, `flex_width`, `root_radius`, `travel`, `travel_stop`: compliance and its limits.
- `line_width`, `layer_height`: selected process values used to judge small features; these are not geometric clearances.
- `support_gap`, `break_neck_width`, `break_neck_height`, `support_embed`: release interface and deliberate attachment.
- `min_wall`, `skin_thickness`, `texture_depth`, `texture_pitch`: structural continuity and cosmetic relief.
- `boolean_epsilon`: only for robust CSG overlaps; never substitute it for a moving-joint gap or calibrated tolerance.

Unknown process values remain explicit assumptions. A clearance value must say whether it is radial, per side
or total. A slope must state its reference plane; evaluate it after the final build transform. Keep service
orientation and build orientation separate, especially for drains and feet.

## Geometry recipes

These are refinements of the inventoried ideas for agent implementation. They are conditional design
instructions, not additional claims of physical performance.

### Printable bore or roof

Keep the circular or flat region that locates the mating item. Add a triangular or peaked roof above the
horizontal bore, retaining the nominal bearing diameter and center. For a ledge, add a permanent underside
chamfer or gusset outside the mating keep-out volume. For a dome, first try a pointed inner cavity under the
required exterior; allow a thicker apex rather than forcing constant wall thickness. If the exact inner roof
is functional, use a removable support or controlled contact landing instead.

In OpenSCAD, build the bore cutter as a circular section united with a roof relief, then subtract it along
the bore axis. Check the transformed section: an upright teardrop in the modeling frame may face sideways
after rotation. A rectangular opening may bridge well over a short span but still sag over a long one.
Record the chosen span and roof slope as process-dependent. See T016, T024 and T124-T127.

### Tolerant removable fit

Start with a clearance envelope, a lead-in and a seating stop. Add only enough short lands to locate the part.
Relieve corners and other incidental contact regions. Add flexible fins or a U-shaped spring locally when
retention must accommodate variation. Cut relief around and underneath the spring so it has a real free
length; keep the spring attached at its intended root.

Tune spring length and thickness independently from detent interference. Longer and thinner members are
usually more compliant, but root strain, layer direction and material creep still limit travel. Keep the
working bend mostly within the layer plane when possible. For disassembly, include a release route and a
travel stop. A one-time crush rib deforms plastically; do not describe it as a reusable compliant fit.
See T007-T022 and T103-T108.

### Snap, hinge or printed spring

Declare whether the mechanism is assembled after printing or captive during printing. For a captive pivot,
use tapered/conical bearing surfaces and printable roofs; avoid a circular horizontal ceiling that sags into
the axle. Maintain actual clearances through the complete motion. Keep independent bodies separate across
moving interfaces; union only their intended structural attachments.

For a latch, put the detent on a free spring and reserve space for the entire insertion and release travel.
For a flat spring, choose a leaf, serpentine or spiral path whose bending direction matches the intended load.
For a living hinge, distinguish a thin sacrificial link from a repeated-flexure design. Slotted sheets and
curved flexures change stiffness but do not establish fatigue life. Avoid sharp cut ends at highly strained
roots. See T073-T085.

### Stable diagonal or tall print

Compare a flat, side and diagonal orientation against loads, visible faces, supported area and bed contact.
When choosing an edge-down orientation, create a finite contact flat. Add fins where motion would otherwise
twist or tip the part. Give each fin a broad rounded bed footprint and a thin web. Join it with short
horizontal breakaway tines oriented parallel to the build plane, rather than perpendicular to the model face.

Control connector width and height relative to the selected extrusion width and layer height. A nominally
thin feature that disappears in slicing is not a support. Put attachments near hidden faces or edges and
allow cutters to reach them. For a tall slender wall, use a nearby pillar with short comb fingers. Keep
sacrificial geometry in a separately named module, with explicit connectors where fusion is intended.
See T025-T035.

### Hold-down and bed release

Choose bed contact for both adhesion during printing and the intended removal method. An underside recess
reduces contact; retain a stable continuous rim and self-supporting recess walls. A corner brim or mouse ear
adds local adhesion without encircling every edge. Put a removable brim connection inside a bottom chamfer
when trimmed remnants must stay within the nominal envelope.

For a CAD raft, separate raft stiffness, part contact and release gap. Use controlled break necks or corner
ties when a gap alone does not provide enough hold-down. Keep a path for peeling, cutting or extracting it.
Interrupting long first-layer paths or adding internal relief can reduce shrink interaction, but must not
damage sealing surfaces or loaded sections. These choices depend on bed, material and thermal conditions;
they do not replace process control. See T002-T003, T036-T048 and T052-T055.

### Strength at a root or fastener

Sketch the applied force and the likely fracture path. Add a broad root gusset, a thicker local envelope or
a bore boss/ring that places material along that path. Preserve screw-head seating, mating datums and tool
access. Rotate the part if the current orientation loads a thin root by peeling between layers.

Thin internal slits can cause a slicer to generate extra perimeter walls around them. Treat that as an
optional toolpath strategy, controlled by slit width, depth, spacing and direction. Keep a continuous outer
skin where needed. A slit can instead disappear, create disconnected islands or become a crack path; reject
those outcomes. Do not use a strength multiplier or default zero infill from a demonstration. See T049-T063.

### Hardware and adhesive assembly

Use actual hardware dimensions. Provide the complete installation path for a heat-set insert, screw, nut
or magnet, including soldering-tool and screwdriver clearance. For side-loaded nuts or magnets, retain a
printable roof and a stop or throat that prevents escape. Separate bearing/locating faces from intentionally
deformable retention ribs. Specify magnet polarity or use a compatible steel target when polarity would
otherwise complicate assembly.

For glue, let short lands locate the part while relief pockets hold adhesive. An undercut pocket can give
mechanical capture, but still needs a reachable inlet and an escape or witness path. Avoid a sealed cavity
that traps displaced adhesive or air. Keep access after all preceding assembly steps. Glue-filled internal
reinforcement is a proposed variant requiring separate verification. See T086-T102.

### Finish and text

Protect fits, datums, bed contact, sealing surfaces and minimum wall thickness from texture. Pattern a small
repeat on selected visible faces; limit pitch, relief and facet count. Raised and recessed repeats produce
different feel. Texture can hide a shrink line without fixing the dimensional error beneath it.

For lettering, control stroke width, stroke height, relief depth and unsupported projection. Prefer a
supported sidewall or shallow engraving where it serves the required readability. Use a continuous pattern
on an engraved floor for contrast; isolated dots create extra islands. For two colors, consider a retained
label plate or backing insert. Treat bottom-face text as a deliberate exception to a simple first layer.
See T064-T072, T110-T115 and T123.

### Rain shedding, feet and thin continuous walls

For a rain-exposed enclosure, set the service orientation first. Use overlapping lips and baffles to divert
water, keep drains at low points and prevent a direct path into the protected region. Bridge-shortening ribs
must leave the intended airflow and drainage paths open. These geometries do not establish airtightness,
submersion resistance or an IP rating. See T116-T118.

For feet, preserve the service contact plane while giving protruding feet printable undersides in the build
orientation. If friction matters, design a pocket for the actual rubber pad and assembly method. See T119-T120.

For vase-mode structures, fold/corrugate the outline to create section depth. Keep each height traversable
as one continuous perimeter; deliberately opening a wall can preserve that route, whereas a closed internal
island breaks it. Preserve the intended fit and check how the outline evolves through the complete height.
See T121-T122.

## Design handoff

Include the chosen inventory IDs, purpose, key parameters and their units, build/service orientations,
functional keep-outs, assembly and support-removal sequence, and the expected failure to look for.
Describe process assumptions and which outcomes have actually been inspected. Keep structural, mating,
cosmetic and sacrificial modules identifiable in the source. Avoid applying every trick to every design.

## Evidence and scope

See the [visual evidence record](3d-print-visual-evidence.md) for the inspected frames and their limitations.
Inventory rows distinguish reviewed captions, inspected video frames and pending sources. English automatic
captions can misrecognize geometry names and dimensions. Resolve an ambiguous statement against the retained
video at the same timestamp before turning it into geometry instructions. Label any remaining inference.

Retain acquired videos, extracted audio, captions, metadata and the timestamp-to-frame relationship.
Use the source links and evidence intervals to revisit details. A video review is not a physical print test;
do not promise strength multipliers, perfect tolerances, watertightness or repeatable fatigue life without
relevant process evidence.

Do not run builds or tests without the user's authorization. When authorized, choose checks that demonstrate
the relevant outcome: slicer toolpaths for a microfeature, assembly for a fit, breakaway behavior for supports,
load direction for strength, and the intended exposure for water resistance. Report what remains unverified.
