# Pinned BOSL2 anchor mapping: evidence and adapter boundary

Source reviewed 2026-10-03 in the clean existing checkout
`D:/openscad/runs/20261002-scadmaxx-skill/libraries/BOSL2`.
Version 2.0.766; HEAD `e173fa0ae45f9e2082e0d8c0382dae98621b7c20`.
attachments.scad SHA-256: `fd401f60d680fcff06b6c17576fce17f42428ef7c94bdd90e34365907bfc3d2e`.
The installation was located through prior workspace validation evidence; the configured Everything CLI was absent.
No library was installed, changed, fetched or repinned.

Primary references: [pinned source](https://github.com/BelfrySCAD/BOSL2/blob/e173fa0ae45f9e2082e0d8c0382dae98621b7c20/attachments.scad),
[official attachment API](https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad).
The actual pinned file, not the moving wiki, determines adapter behavior. Source locations inspected:
attach at line 961, reorient at 2614, named_anchor at 2675, attach_geom at 2868, _attach_transform at 3271 and
_find_anchor at 3366. _find_anchor is internal; confine that dependency to one version-checked SCAD bridge.

## Mapping

At this revision, _find_anchor(selector, geometry) returns name/selector, position, direction and spin as the first
four entries. Additional info may follow and must not be mistaken for orientation. named_anchor supports a custom
position/direction/spin or a rotation matrix. Standard anchors come from the explicitly supplied attach_geom record.
The basis-to-local matrix for an anchor is:

`B = translate(position) * rot(from=UP,to=direction) * zrot(anchorSpin)`.

For two 3D anchors, the verified basic Mate transform is:

`B_parent * translate([0,0,gap]) * zrot(attachmentSpin) * yrot(180) * inverse(B_child)`.

This corresponds to BOSL2's two-argument attach(parent, child, spin=s, overlap=-gap), with normal/default placement
on the child. Its convention preserves up for the 180-degree mate flip. The native Anchor representation stores
normal and up from B's Z/Y columns, so native frame reconstruction agrees without duplicating BOSL2's direction/spin
interpretation in C++. Child shape anchor/orient parameters have special handling in two-argument attach; do not
assume those arguments provide additional placement or flatten them into a guessed correction.

BOSL2 inside=true also applies a default removal tag. Therefore native Align is implemented by the native frame
solver, not by generating inside=true. Initial adapter scope excludes align/inset/shiftout, anchor lists, 2D attachment
modes, tagged booleans and arbitrary module introspection. The explicit descriptor's stored override callable is
handled by BOSL2 itself; the bridge validates its resulting position/direction/spin instead of inspecting that function.

The SCADMaxx bridge consumes an explicit geometry description plus a supported selector and exports ordinary Anchor
values. Native Attachment objects then place semantic Components. Do not generate a Component child block on a Part:
07 deliberately disallows that host form. Plain legacy BOSL2 models keep their own normal library behavior.
Generated bridge imports use only current argument names, without deprecated from/to/norot aliases.

## Executed probe

[bosl2-frame-probe.scad](bosl2-frame-probe.scad) uses existing BOSL2 geometry descriptions and actual attachable/attach
evaluation. It asserts the proposed mapping against the library's observed $transform, including a transformed
parent. It does not implement any future SCADMaxx kind or solver.

Executable: `D:/openscad/artifacts/20261003-scadmaxx-executable-name/attempt-2/extracted-check/scadmaxx.com`;
reported version `2026.10.03-experimental-20261003-scadmaxx-executable-name`.
Audit source for this executable: `4c325716b94e444637a80df3966197ce110b2b75`.
Run outputs: `D:/openscad/runs/20261003-anchor-attachment-planning/attempt2.echo` and `attempt2.stderr.txt`.
Command, with OPENSCADPATH temporarily set to the existing libraries directory and restored afterward:

```powershell
& '<recorded-executable>' -o '<run>/attempt2.echo' '<feature-plan>/bosl2-frame-probe.scad'
```

Exit 0; six passing transforms and two passing anchor-position assertions; no warning/error diagnostics:

SHA-256 identities: probe `20d5dfa883b6f8befa42fa449b9678a85f392e9ab8bb0b8049b0ad9812a31aac`;
attempt2.echo `03f863febf52e30cce5591eae6022146a3cbbd5425ce67eeeea5df4c2cb27b4e`;
executable `8b7834a99c7bb74a48ab93780293aa1e79ccabb7b6bd579c9ae04ae522230f05`.

| Case | Observed result |
| --- | --- |
| TOP/BOT | Translation Z=9, unchanged orientation. |
| RIGHT/BOT, spin 30, gap 2 | Translation X=16 and expected side-facing rotation. |
| BOT/TOP, spin -45, gap -1 | Translation Z=-8 and expected spin. |
| Rotated/translated parent | Full matrix agrees with outer * local placement. |
| Oblique custom anchors on both objects | Full position/orientation/spin matrix agrees. |
| Standard parent / named child | Full matrix agrees. |

Tolerance: BOSL2 approx(..., eps=1e-8) inside the evaluator; echo's rounded decimal matrices are not the comparison
inputs. The first probe used a bare block where attachable requires one explicit second child, triggering its
two-child assertion and excessive trace output/process failure in the audited binary. The corrected fixture uses
union() to make that child explicit. The failed output is retained as attempt1-invalid-child-group.echo in the run;
it is not evidence against the placement formula. Error-trace handling is outside this planning feature.

Native feature acceptance remains outstanding: capture/evaluate Anchor objects, transformed-frame math, graph solve,
publication/exports, GUI edits and live source changes. Nonuniform/mirrored-owner behavior is specified in the native
plan and has not been validated by these rigid BOSL2 cases.
