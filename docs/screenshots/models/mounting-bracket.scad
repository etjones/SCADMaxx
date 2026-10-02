// SCADMaxx README demonstration: mounting hole too close to the edge.
/* [Bracket dimensions] */
// Overall base width in millimetres.
base_width = 64; // [50:2:90]
// Overall base depth in millimetres.
base_depth = 44; // [30:2:70]
// Thickness of the base and rear wall.
wall = 6; // [3:1:10]
// Height of the upright mounting face.
back_height = 30; // [20:2:50]
/* [Mounting holes] */
// Diameter of the two base mounting holes.
hole_diameter = 9; // [4:1:12]
// Right hole is intentionally too close to the outer edge.
right_edge_distance = 3; // [2:1:15]
/* [Hidden] */
$fn = 80;
$vpt = [0, 0, 12];
$vpr = [62, 0, 32];
$vpd = 190;
module rounded_plate(w, d, h, r=3) {
    linear_extrude(h)
        offset(r=r) square([w-2*r, d-2*r], center=true);
}
difference() {
    union() {
        rounded_plate(base_width, base_depth, wall);
        translate([0, base_depth/2-wall/2, wall])
            rounded_plate(base_width, wall, back_height, 2);
        for (x=[-base_width/2+8, base_width/2-8])
            translate([x, base_depth/2-wall, wall])
                rotate([0,90,0]) linear_extrude(4, center=true)
                    polygon([[0,0],[-18,0],[0,-18]]);
    }
    for (x=[-base_width/2+12, base_width/2-right_edge_distance])
        translate([x,-7,-1]) cylinder(h=wall+2,d=hole_diameter);
    for (x=[-18,18])
        translate([x,base_depth/2+1,wall+back_height/2])
            rotate([90,0,0]) cylinder(h=wall+2,d=7);
}
