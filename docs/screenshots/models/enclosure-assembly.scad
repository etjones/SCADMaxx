// A ventilated sensor enclosure with a removable lid.
$fn = 48;
$vpt = [0, 0, 12];
$vpr = [62, 0, 32];
$vpd = 240;

@{type:Part, id:"housing", label:"Sensor housing"}
module housing(width=64, depth=44, height=26, wall=3) {
    difference() {
        translate([-width/2,-depth/2,0]) cube([width,depth,height]);
        translate([-width/2+wall,-depth/2+wall,wall])
            cube([width-2*wall,depth-2*wall,height]);
        for (x=[-20:8:20]) translate([x,-depth/2-1,10])
            cube([3,wall+2,10]);
    }
    for (x=[-width/2+7,width/2-7], y=[-depth/2+7,depth/2-7])
        translate([x,y,wall]) difference() {
            cylinder(d=8,h=height-wall-2);
            cylinder(d=3,h=height);
        }
}

@{type:Part, id:"lid", label:"Removable lid"}
module lid(width=64, depth=44, thickness=3) {
    difference() {
        translate([-width/2,-depth/2,0]) cube([width,depth,thickness]);
        for (x=[-width/2+7,width/2-7], y=[-depth/2+7,depth/2-7])
            translate([x,y,-1]) cylinder(d=3.5,h=thickness+2);
        for (x=[-16:8:16]) translate([x,-10,-1])
            cube([3,20,thickness+2]);
    }
}

@{type:Assembly, id:"sensor", label:"Sensor enclosure"}
module sensor_enclosure() {
    color("LightSteelBlue")
        @{type:Component,id:"housing",label:"Housing"} housing();
    translate([0,50,0]) color("Wheat")
        @{type:Component,id:"lid",label:"Ventilated lid"} lid();
}

@{type:Component,id:"sensor",label:"Sensor enclosure"} sensor_enclosure();
