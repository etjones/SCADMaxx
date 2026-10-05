@{type: Part, id: "plate"}
module plate(width=20) {
    @{type: Anchor}
    mount = {id:"mount", position:[width/2,10,10], normal:[0,0,1], up:[0,1,0]};
    difference() {
        union() {
    cube([width,20,10]);
        }
        translate([10,10,10]) rotate([0,180,0]) cylinder(d=4,h=12);
    }
}
@{type: Component, id: "left"}
plate(width=20);
translate([40,0,0]) {
    @{type: Component, id: "right"}
    plate(width=30);
}
