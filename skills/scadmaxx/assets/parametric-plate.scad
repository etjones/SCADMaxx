// Requires BOSL2. Nominal envelope: length x width x thickness, base at z=0.
include <BOSL2/std.scad>
length = 60;
width = 40;
thickness = 8;
hole_inset = 10;
hole_diameter = 5;
finish = true;
treatment = "round"; // [round, chamfer]
edge_size = 2;
$fn = 48;

assert(length > 0 && width > 0 && thickness > 0);
assert(hole_diameter > 0 && hole_inset > hole_diameter/2);
assert(2*hole_inset + hole_diameter < min(length,width));
assert(edge_size >= 0 && edge_size < min(length,width)/2);
assert(edge_size < hole_inset-hole_diameter/2, "Edge treatment enters the hole clearance zone");
assert(treatment == "round" || treatment == "chamfer");

module blank() {
    if (!finish || edge_size == 0)
        cuboid([length,width,thickness], anchor=BOTTOM);
    else if (treatment == "round")
        cuboid([length,width,thickness], rounding=edge_size, edges="Z", anchor=BOTTOM);
    else
        cuboid([length,width,thickness], chamfer=edge_size, edges="Z", anchor=BOTTOM);
}

difference() {
    blank();
    for (x=[-length/2+hole_inset,length/2-hole_inset])
        for (y=[-width/2+hole_inset,width/2-hole_inset])
            translate([x,y,-0.01]) cyl(d=hole_diameter,h=thickness+0.02,anchor=BOTTOM);
}
