module tile(){difference(){cube([16,12,5]);translate([8,6,-1]) cylinder(h=7,r=3,$fn=32);}}
for(i=[0:5]) translate([i*20,0,0]) tile();
