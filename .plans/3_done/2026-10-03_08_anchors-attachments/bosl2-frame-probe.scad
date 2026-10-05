// Planning evidence: run against BOSL2 e173fa0ae45f9e2082e0d8c0382dae98621b7c20.
// Uses existing BOSL2 only; this does not implement SCADMaxx Anchor/Attachment declarations.
include <BOSL2/std.scad>
assert(BOSL_VERSION == [2,0,766], "Unexpected BOSL2 version");

function anchor_frame(g, selector) =
    let(a = _find_anchor(selector, g))
    move(a[1]) * rot(from=UP, to=a[2]) * zrot(a[3]);

function mate_transform(gp, gc, pa, ca, spin, offset) =
    anchor_frame(gp, pa) * move([0,0,offset]) * zrot(spin) * yrot(180)
        * matrix_inverse(anchor_frame(gc, ca));

module check_case(name, gp, gc, pa, ca, spin=0, offset=0, outer=IDENT) {
    expected = outer * mate_transform(gp, gc, pa, ca, spin, offset);
    multmatrix(outer)
    attachable(anchor=CENTER, spin=0, orient=UP, geom=gp) {
        cuboid([1,1,1]);
        attach(pa, ca, spin=spin, overlap=-offset)
        attachable(anchor=CENTER, spin=0, orient=UP, geom=gc) {
            cuboid([1,1,1]);
            union() {
                assert(approx($transform, expected, eps=1e-8),
                       str(name, " transform mismatch: ", $transform, " vs ", expected));
                echo(case=name, passed=true, transform=$transform);
            }
        }
    }
}

gp = attach_geom(size=[20,30,10]);
gc = attach_geom(size=[4,6,8]);
check_case("top-bottom", gp, gc, TOP, BOT);
check_case("right-bottom-spin-offset", gp, gc, RIGHT, BOT, spin=30, offset=2);
check_case("bottom-top-negative-offset", gp, gc, BOT, TOP, spin=-45, offset=-1);
check_case("rigid-parent", gp, gc, BACK, FRONT, spin=75, offset=3,
           outer=move([10,20,30])*rot([20,30,40]));

np = attach_geom(size=[20,30,10], anchors=[named_anchor("mount",[2,3,4],[1,2,3],35)]);
nc = attach_geom(size=[4,6,8], anchors=[named_anchor("plug",[1,-2,3],[2,-1,1],20)]);
check_case("named-oblique", np, nc, "mount", "plug", spin=15, offset=2);
check_case("mixed-standard-named", gp, nc, RIGHT, "plug", spin=-60);

assert(approx(_find_anchor(TOP, gp)[1], [0,0,5]), "Standard anchor position");
assert(approx(_find_anchor("mount", np)[1], [2,3,4]), "Named anchor position");
echo(anchor_positions_passed=true);
