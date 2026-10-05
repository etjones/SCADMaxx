# Phase 2: frame mathematics and directed placement graph

Covers AN02/AN04/AN07/AN13/AN14/AN20. Pure C++ tests need neither Qt, a renderer nor BOSL2.

1. Implement AnchorFrames with the precise normal/up/spin/quaternion and affine owner rules from the overall plan.
   Separate point, tangent direction and surface-normal transformations. Add supported-conditioning validation and
   inverse hit capture; return structured errors for missing orientation instead of making a frame from one vector.
2. Implement AttachmentGraph with containment plus placement edges, one driver per child, deterministic topological
   ordering and cycle diagnostics showing paths and declaration spans. Empty/ordinary scenes are valid no-ops.
3. Implement pure solvePlacement and graph evaluation from source-authored transforms. Use target-frame offsets,
   Mate Ry(pi)/Align identity, then a world-rigid correction. Validate finite/orthonormal/determinant residuals before
   returning the candidate transform. Do not mutate native nodes in these unit tests.
4. Add AnchorFrames_test.cc/AttachmentGraph_test.cc/AttachmentSolver_test.cc with [anchor-frames], [attachment-graph]
   and [attachment-solve]. Use analytically known fixtures plus randomized rigid transforms with a fixed seed.

Numerical cases: same-frame Align identity; Mate sends child +Z to -Z and preserves +Y; base example peg Z=10,
X=width/2; positive target Z offset separates anchors; X/Y offset unchanged when spin changes. Spin +90 maps target
local +X toward +Y. Rotated parent, oblique normal/up, zero/nonzero anchor spin and adjustment quaternion must agree
with explicit reference matrix multiplication. Test normal/up rejection, NaN/Inf and positive/negative large angles.

Affine cases: L=diag(2,3,4), mirror X and shear, with oblique normals. Assert unit orthogonal right-handed output,
surface normal perpendicular to both transformed tangents, local/world capture round-trip and child world-space
pairwise distances unchanged by Dworld. Exercise 1e-6/1/1e6 uniform scales and translated coordinates. Matrix relative
residual <=1e-10; point tolerance max(1e-9*sceneDiagonal,128*DBL_EPSILON*coordinateMagnitude). Keep the ill-conditioning
threshold independent of model units. Singular/ill-conditioned required inverses explicitly fail.

Graph cases: sibling chain, attached parent Assembly with attached descendant, cross-branch target, ancestor target,
self-edge, two drivers, sibling cycle and ancestor/descendant cycle. Reordering source records gives equal transforms.
Missing/wrong-kind anchors cannot produce a placement. Exit only when the numerical and graph invariants pass;
do not add nearest-frame recovery, a constraint solver or an unexplained extra rotation to repair failures.
