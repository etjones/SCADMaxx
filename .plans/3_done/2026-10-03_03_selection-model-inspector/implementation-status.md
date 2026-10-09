# Implementation status

Implementation started on 2026-10-03 after the user authorized the queue 03 -> 05 -> 06 -> 14 -> 04.
Implementation is complete; all four phases and final review passed. The final source/API is frozen for 06/14/04.
See `5_post-implementation-notes.md` for complete behavior, exact patches, verification and composition limits.

Source: `D:/openscad/wt-openscad-selection-model-inspector`, branch `feature/selection-model-inspector`.
Base/unchanged HEAD: `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`, the retained prerequisite-only
HTTP/annotation/navigation composition. Feature 02 and 15 source edits are excluded from this independent foundation.
Windows and native-harness repairs are separate inputs, verified against feature 02's recorded patch hashes.
Exact prerequisites, exclusions and repaired baseline patch are in
`D:/openscad/runs/20261003-selection-model-inspector/inputs/manifest.json`.

The later selected navigation revision `bfd009ef0047452c09e3629d0af25efd6af34700` is not in this development
base; its UI/default delta must be reviewed in the later selected-stack rehearsal. No commits, promotion,
enabled-stack change, push or integrated release are authorized.

Phase 1 verification: isolated application/unit targets build; all six discovered [evaluation-inputs] cases pass.
The ordinary native Windows harness passes 46 QtTest cases (34 behavior, 12 setup/cleanup), including four new
TestSelection cases and existing annotation/HTTP/module-cache/navigation behavior. Final native evidence:
`D:/openscad/runs/20261003-selection-model-inspector/native-20261003T204941826Z`.
The source snapshot and independent patch apply check are in `phase1-source-evidence.json` in the run.
Feature-only patch SHA256: `a3100cb5682d7a323ea43376dc0457b1905f79bbc878720ed1b8d941a08b5978`.

Native checks caught and corrected a test-helper global-cache access, a dangling secondary-window inventory entry,
and request scoping during ordinary Customizer file setup. Parse failure retains the last-good renderer while
rejecting its binding. A retained worker scene survives document close and a replacement compilation.

Phase 2: all 12 discovered core cases pass (6 evaluation-inputs, 3 surface-pick-math, 3 inspection-presentation).
Native selection harness: 10 behavior cases plus setup/cleanup pass at DPR 1, including OpenCSG preview and
Manifold/CGAL final position/normal fixtures, background exclusion, transparency, recentering and unsupported modes.
Evidence: `D:/openscad/runs/20261003-selection-model-inspector/native-20261003T213706685Z`.
GPU: NVIDIA GeForce RTX 3070 Ti, OpenGL 4.6.0 NVIDIA 616.92; depth24/stencil8 and RGBA32F picking verified.
Phase 2 feature-only patch SHA256: `c6b3f626b4776523f33bdbe3d31ed8d47c258b6f1ac61aec4b9f8a9f80d11ed6`.
The independent patch apply check and actual file hashes are in `phase2-source-evidence.json` in the run.

The newly added shared inspection-presentation contract is implemented by this owner: provider priority, shared
job/request lifetimes, exact intersecting masks, deterministic effect wrapping, 64-bit piece identity through compact
GPU tokens and central default renderer restoration. A native mirrored/rotated/nonuniform two-piece provider proves
front/rear masking, matching color/hit effect predicates, generation/serial behavior and registration teardown.
Worker completions after replacement or lifetime destruction cannot install stale meshes; failure does not fall back.
No 04/07 consumer is imported or claimed tested.

Native verification found that VBOBuilder's established triangle normal is the negative of the conventional face
cross product. The renderer-owned surface normal sign therefore corrects that convention, subtraction polarity and
mirrored winding once. It also found that OpenCSG visibility must enter with the ordinary fixed-function program
before binding the surface shading pass. Both fixes retain ordinary rendered pixels, checked before/after each pick.

Final verification: 15 discovered core tests pass; full native clean-PATH extracted runtime passes 58 QtTest results
(46 behavior, 12 setup/cleanup), plus 18 selection results at each of DPR 1.5 and 2. Seven Unicode filename cases pass
through each extracted executable/console entrypoint. Native resize checks corrected logical/physical framebuffer
dimensions and verify target samples against visible model pixels. Inspector screenshots were visually inspected.
Final feature patch SHA256: `fc9f0e8da7fa019447700bee498b09a689f00152d8ae965a106341a0569290bb`.
`final-source-evidence.json` and `verification-evidence.json` identify actual final source and passing cases.
No commits, promotion, enabled-stack update or integrated release. Next authorized feature: 05.
