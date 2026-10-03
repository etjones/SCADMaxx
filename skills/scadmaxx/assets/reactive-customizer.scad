// Requires SCADMaxx fixed-key native Customizer annotations.
advanced = false;
readonly = false;
@{group: "Controls", description: "Special-variable lock"}
$detail_lock = false;
include <reactive-controls.scad>
cube([20,20,detail]);
