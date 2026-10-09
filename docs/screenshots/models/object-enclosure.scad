// Keep a component's dimensions and material together.
use <enclosure-cutaway.scad>

case_spec = {
    name: "Desk sensor",
    size: [64, 44, 26],
    wall: 3,
    material: "LightSteelBlue"
};

color(case_spec.material)
    housing(width=case_spec.size.x,
            depth=case_spec.size.y,
            height=case_spec.size.z,
            wall=case_spec.wall);

echo(case_spec.name, case_spec.size);
$fn = 48;
$vpt = [0,0,12];
$vpr = [62,0,32];
$vpd = 230;
