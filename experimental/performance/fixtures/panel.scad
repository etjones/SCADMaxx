$fn=24;
difference(){cube([100,65,3]);for(x=[6:8:94],y=[6:8:60]) translate([x,y,-1]) cylinder(h=5,r=2.5);}
