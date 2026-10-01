# Navigation cube — implementation evidence

Status: phases 1 (`3a60e69bb`) and 2 (`ea9427744`) completed; phase 3 in progress.

## Source and build

Dedicated checkout: `D:/openscad/wt-openscad-navigation-cube`, `feature/navigation-cube`.
Starting HEAD: `464e25dad0c01af5488375c15aa6734190531eb5`; clean before Serena's local project metadata.
Matching initialized submodules were checked. No running application uses this checkout.
All feature phases will be committed individually at the user's request. No remote publication is requested.

Four recorded MSVC repairs were still applicable by source inspection and applied with attribution:

- `2dd7192f4`: stream declarations, original `c577f934`.
- `aa03f8d98`: Windows argument vectors, original `e1a79825`.
- `7dde81712`: Cairo imported target, original `b5ef9f6c`.
- `b6cc333bb`: duplicate manifest fix, original `74168dda`.

Configure succeeded with shared dependencies, MSVC 19.51, Qt 6.11.1, Catch2 and GUI tests enabled.
Baseline build passed; all 119 baseline unit cases passed. Evidence/scripts: `D:/openscad/runs/navigation-cube/phase1/`.
Application build: `D:/openscad/wt-openscad-navigation-cube/build-navigation-cube`.
The experimental composition builder requires a locked PR stack; this standalone feature uses the same profile
through its isolated recorded build script instead. No packages were installed or changed.
The shared gettext executable needed its existing directory added to PATH. GUI tests additionally required a
portable sleep repair (`67884e65f4565c1215a88ecdcd0a2daa122e53d7`), independently committed before feature work.

## Phase 1 integration findings

The renderer applies native Rx * Ry * Rz, then looks along +Y with +Z up. Front is -Y; left is -X;
top is +Z. The adapter uses native Euler values externally and matrices internally, excluding execution flags.
`cameraChanged` feeds Animate and can evaluate source; a distinct display notification is required for interpolation.
Paint-time observation catches direct script/menu/field mutations without triggering evaluation.

TabManager's current save overload always writes source and rebinds filepath. Save As must retain that behavior;
metadata-only ordinary Save needs a separate intent. Source refresh reads only text, so library loading must attach
to initial document ownership rather than refresh. The viewport's rendered editor differs from the active tab.
MainWindow currently assigns renderedEditor before evaluation and again after render; ownership must follow actual
retained results, including empty success, rather than blindly mirroring every assignment.

## Verification

The feature build and all 121 unit cases passed. Native camera-operation, metadata-lifetime and composition probes
passed at 100% and simulated 150% scaling, plus a dark viewport scheme. Screenshots were inspected. Evidence directories:
`phase1/native-3`, `phase1/native-scale150`, `phase1/native-dark`, with JUnit reports and PNGs.
The first composition probe failed because the hidden Windows launcher suppressed initial window exposure;
the harness now explicitly exposes its test window. This was a test setup correction, not an offscreen substitute.
Native test results use explicit JUnit files because the Windows GUI executable does not retain QTest console output.
The native probes establish composition and the metadata lifetime approach; full saved-view transactions, failure/empty
ownership scenarios, physical mixed-monitor DPI, OS dark controls and final visual calibration are tested in their
later phases. The dark probe changes the model viewport scheme, not the Windows desktop theme. No performance claim
or combined annotation-runtime pass is inferred from these probes.

## Phase 2

Implemented a shared 26-facet chamfered cube geometry for painting/hit testing, face-plane labels, axis letters,
single-click directional/roll actions, keyboard access and virtual-trackball drag. Only front-facing polygons hit.
Quaternion transitions use generation cancellation, exact endpoints and one final operation notification;
pan/FOV interpolate linearly, positive distance geometrically, projection switches once at the start.
Settings are session values until phase 3 adds baselines/overrides and their UI. The triangle is intentionally only
an entry-point placeholder at this checkpoint; the actual popup is phase 3.

Build and 123 unit cases pass. Native tests pass for all 26 target poses, preserved camera fields, four-roll cycle,
enabled/disabled orbit, release outside, unchanged widget placement, exact transition endpoints, retargeting,
cancellation and external camera mutation. Geometry tests verify planar facets, hidden-face culling, center hits,
and true isometric axis lengths. Evidence: `runs/navigation-cube/phase2/complete`, `native-final`, `scale150`, `dark`.
The 26-target contact sheet and native screenshots were inspected. Final default-size/font/opacity calibration,
expanded accessibility and physical mixed-monitor checks remain in phase 6, as planned.
