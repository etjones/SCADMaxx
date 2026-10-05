// A finished plain-SCAD target; dimensions stay source-authored.
$fn = 32;
width = 20;
difference() {
    union() {
cube([width, 20, 10]);
    }
    // Fixed local placement; diameter 4, depth 12, into the top face.
    translate([10, 10, 10])
        rotate([0, 180, 0])
            cylinder(d=4, h=12, center=false);
}
