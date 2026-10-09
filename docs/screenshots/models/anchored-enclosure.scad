// The lid follows a named reference on the enclosure rim.
use <enclosure-cutaway.scad>
$fn=48;
$vpt=[0,0,18]; $vpr=[65,0,32]; $vpd=260;

@{type:Part,id:"case",label:"Sensor housing"}
module sensor_case() {
    @{type:Anchor}
    rim={id:"rim",position:[0,0,26],normal:[0,0,1],up:[0,1,0]};
    housing();
}

@{type:Part,id:"cover",label:"Ventilated lid"}
module sensor_cover() {
    @{type:Anchor}
    underside={id:"underside",position:[0,0,0],normal:[0,0,-1],up:[0,1,0]};
    lid();
}

@{type:Component,id:"case",label:"Housing"} sensor_case();
@{type:Component,id:"cover",label:"Lid"} sensor_cover();

@{type:Attachment}
lid_mount={
    id:"lid_mount",
    child:{component:"/cover",anchor:"underside"},
    target:{component:"/case",anchor:"rim"},
    mode:"mate",
    offset:[0,0,12],
    spin:0
};
