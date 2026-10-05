// Future 07/08 native syntax. Small dependency-free fake Component catalog fixture.
@{type: Part, id: "plate"}
module plate(width=20) {
    @{type: Anchor}
    mount = {id:"mount", position:[width/2,10,10], normal:[0,0,1], up:[0,1,0]};
    cube([width,20,10]);
}
@{type: Part, id: "insert-peg-1"}
module smx_insert_part_1() {
    @{type: Anchor}
    smx_contact_1 = {id:"contact", position:[0,0,0], normal:[0,0,-1], up:[0,1,0]};
    cylinder(d=4,h=12);
}
@{type: Assembly, id: "fixture"}
module fixture(width=20) {
    @{type: Component, id: "plate"}
    plate(width=width);
    @{type: Component, id: "peg-1"}
    smx_insert_part_1();
    @{type: Attachment}
    smx_attachment_1 = {
        id:"insert-peg-1", child:{component:"peg-1",anchor:"contact"},
        target:{component:"plate",anchor:"mount"}, mode:"mate", offset:[0,0,0], spin:0
    };
}
@{type: Component, id: "fixture-a"}
fixture(width=20);
translate([50,0,0]) {
    @{type: Component, id: "fixture-b"}
    fixture(width=30);
}
