// Planning evidence: real installed-library calls, not the future provider implementation.
include <BOSL2/std.scad>
include <BOSL2/screws.scad>
include <BOLTS/BOLTS.scad>

probe_case = 0;
probe_size = "M4";
$fn = 48;

module provider_threaded_hole(size,depth) {
    screw_hole(spec=size,head="none",thread=true,length=depth,tolerance="6H",
        counterbore=0,bevel=false,anchor=[0,0,-1],atype="shaft",orient=[0,0,1],$slop=0);
}
module provider_screw(size,length) {
    include <BOLTS/BOLTS.scad>
    ISO4017(key=size,l=length);
}
module provider_nut(size) {
    include <BOLTS/BOLTS.scad>
    ISO4032(key=size);
}
module provider_washer(size) {
    include <BOLTS/BOLTS.scad>
    ISO7089(key=size);
}

assert(BOSL_VERSION == [2,0,766]);
assert(BOLTS_date() == [2021,9,13]);
echo(bosl_version=BOSL_VERSION, bolts_version=BOLTS_version(), bolts_date=BOLTS_date());

if (probe_case == 0) cube([10,20,30]);
if (probe_case == 1) sphere(r=5);
if (probe_case == 2) cylinder(d=10,h=20);
if (probe_case == 3) difference() {
    cube([20,20,10],center=true);
    translate([0,0,-6]) cylinder(d=4,h=12);
}
if (probe_case == 4) provider_threaded_hole(probe_size,12);
if (probe_case == 5) provider_screw(probe_size,20);
if (probe_case == 6) provider_nut(probe_size);
if (probe_case == 7) provider_washer(probe_size);
if (probe_case == 8) difference() {
    translate([-10,-10,0]) cube([20,20,10]);
    translate([0,0,-1]) provider_threaded_hole(probe_size,12);
}
if (probe_case == 9) ISO4762(key="M4",l=20); // Candidate audit; vendor warning expected.
