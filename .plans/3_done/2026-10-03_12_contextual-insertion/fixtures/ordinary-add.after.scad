// A finished plain-SCAD target; dimensions stay source-authored.
$fn = 32;
width = 20;
union() {
cube([width, 20, 10]);
    // The new cube's bottom centre meets [10,10,10].
    translate([5, 0, 10]) cube(size=[10,20,30], center=false);
}
