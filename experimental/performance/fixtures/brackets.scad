$fn=32;
module bracket(){difference(){union(){cube([18,12,3]);cube([3,12,16]);} translate([10,6,-1]) cylinder(h=5,r=2);translate([-1,6,10]) rotate([0,90,0]) cylinder(h=5,r=2);}}
for(x=[0:3],y=[0:2]) translate([x*24,y*18,0]) bracket();
