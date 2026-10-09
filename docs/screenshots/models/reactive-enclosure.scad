use <enclosure-cutaway.scad>

@{group: "Housing", min: 40, max: 90, step: 2}
width = 64;

@{group: "Housing", min: 20, max: width, step: 2,
  description: "Depth cannot exceed the housing width."}
depth = 44;

@{group: "Lid"}
include_lid = true;

@{group: "Lid", hidden: !include_lid,
  min: 2, max: 6, step: 0.5}
lid_thickness = 3;

color("LightSteelBlue") housing(width,depth);
if (include_lid)
    translate([0,depth+6,0]) color("Wheat")
        lid(width,depth,lid_thickness);

$fn=48;
$vpt=[0,20,10]; $vpr=[62,0,32]; $vpd=300;
