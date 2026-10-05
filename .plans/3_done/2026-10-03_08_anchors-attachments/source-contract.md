# Anchor and attachment source contract

All six behavior decisions are accepted. This document specifies their source representation for implementation;
Anchor/Point/Axis/Plane/Attachment are new registered kinds, not syntax supported by the audited binary today.
Use the existing @{type: Kind} assignment grammar and 07's annotated modules/calls; no new glyph or expression type.

## Parametric references and live placement

```scad
@{type: Part, id: "plate"}
module plate(width = 40, height = 10) {
    @{type: Anchor}
    mount = {
        id: "mount", position: [width/2, 0, height],
        normal: [0,0,1], up: [0,1,0]
    };
    cube([width, 20, height]);
}

@{type: Part, id: "peg"}
module peg(height = 12) {
    @{type: Anchor}
    base = {
        id: "base", position: [0,0,0],
        normal: [0,0,-1], up: [0,1,0]
    };
    cylinder(r = 2, h = height, $fn = 32);
}

@{type: Assembly, id: "fixture"}
module fixture(width = 40) {
    @{type: Component, id: "plate"}
    plate(width = width);
    @{type: Component, id: "peg"}
    peg();

    @{type: Attachment}
    peg_on_plate = {
        id: "peg-on-plate",
        child: {component: "peg", anchor: "base"},
        target: {component: "plate", anchor: "mount"},
        mode: "mate", offset: [0,0,0], spin: 0
    };
}

@{type: Component, id: "fixture-a"}
fixture(width = 40);
translate([100,0,0]) {
    @{type: Component, id: "fixture-b"}
    fixture(width = 60);
}
```

The peg origins are [20,0,10] and [130,0,10]. Changing fixture-a's width to 50 changes only its peg origin to
[25,0,10]. Both pegs keep their dimensions. Each instance has a distinct mount/base reference and local attachment
ID despite reusing one declaration. Declarations emit no geometry. Attachment assignment order among declarations
does not determine solve order; the live placement graph is resolved after native module evaluation.

An attachment chooses a placement target; it does not reparent the semantic tree. Plate and peg stay siblings.
For source chains, add another Component and an Attachment targeting the peg's named tip anchor. A cyclic chain
or two Attachment records driving the same child is invalid, even if numeric offsets happen to agree.

## Declaration scopes and identity

Reference declarations belong directly to a file scope or the body scope of an annotated Part/Assembly module.
Ordinary helper-function RHS values are allowed; arbitrary nested helper/control/transform scopes are not reference
declaration hosts in this first version. This avoids assigning coordinates to an implicit transform frame. Declare
positions explicitly in the owner's coordinates. Repeated Component invocations evaluate their own module declarations.

Inside a Part/Assembly, omitted owner means that semantic owner; a file-scope declaration without owner belongs to
the document frame. An explicit owner string is permitted in file or Assembly scope and targets one Component path.
Example at root, after the two fixture calls:

```scad
@{type: Anchor}
picked_point = {
    id: "inspection-point", label: "Fixed local point", owner: "/fixture-a/plate",
    position: [12,5,10], normal: [0,0,1], up: [0,1,0], capture: "fixed"
};
```

That addition exists only on fixture-a's plate. It does not replace an inherited anchor with the same ID: duplicates
are invalid. Naming/label editing never changes identity. A root document anchor is available for plain geometry;
its fixed coordinates are document-local and do not track transforms hidden inside anonymous source code.

Component strings in owner/child/target use 07's escaped path segments. An initial / means absolute. Otherwise they
are relative to the enclosing Assembly instance (file scope uses document root). Empty string means the enclosing
owner/document, useful for targeting an Assembly's own anchor. There is no .. traversal or wildcard syntax. A child's
path must identify a Component; the document cannot be moved. A missing path/anchor is an error, never a geometric search.
IDs are nonempty case-sensitive strings evaluated once; equal IDs in different owner namespaces are valid.

Attachment declarations are permitted at file/Assembly-body scope, not within a Part. Their ID is unique among
attachments in that declaring owner. Reusable Attachment declarations normally target descendants of their Assembly.
An absolute external target is allowed in a live document but can make isolated definition export unresolved.
Definition-default export must report that dependency; it cannot borrow an arbitrary document instance's placement.

## Fields and reference kinds

Unknown/duplicate object fields are errors. All vectors have three finite numbers; schema fields are ordinary SCAD
expressions, evaluated once in the native scope. type is registered metadata, never a string-defined kind.

| Kind | Required fields | Optional fields / defaults |
| --- | --- | --- |
| Anchor | id, position, normal, up | label, owner, spin=0 degrees; capture="parametric" or "fixed"; purpose="drawing"; adjust.translation=[0,0,0], adjust.rotation=[0,0,0,1] quaternion xyzw. |
| Point | id, position | label, owner. No implied orientation. |
| Axis | id, position, direction | label, owner. Infinite directed line; no implied spin. |
| Plane | id, position, normal | label, owner. Oriented infinite plane; no implied in-plane up. |
| Attachment | id, child, target | label; mode="mate" or "align"; offset=[0,0,0] in target-anchor axes; spin=0 degrees; adjust.offset=[0,0,0], adjust.spin=0. |

Anchor normal/up must be nonzero and nonparallel; normalize and orthogonalize explicitly. Point/Axis/Plane cannot
be used as Attachment endpoints until an explicit Anchor supplies the missing orientation. An Anchor with
purpose="drawing" sets that owner's canonical drawing frame; at most one per owner. Otherwise canonical axes are
the semantic local axes (document axes for an ordinary model). Feature 09 chooses front/top/projection conventions.
This purpose adds no geometry or automatic drawing. Axis/Plane display uses finite visual helpers without changing
their infinite mathematical meaning.

An Attachment endpoint has exactly component and anchor fields. Attachment offset is a vector in the target's
unspun frame: positive Z means away along its normal, X/Y slide in-plane. Positive spin is a right-handed rotation
around target +Z (degrees in source). Offsets do not rotate when spin changes. Align matches the complete frames;
Mate flips 180 degrees about target Y before matching, preserving the chosen up direction at zero spin.
Source expressions remain in base fields; supported numeric UI changes use literal adjust fields and one source
transaction. Shared module declarations require an explicitly labeled shared edit, never a misleading instance edit.

## BOSL2 bridge spelling

The future shipped helper is libraries/SCADMaxx/bosl2-anchors.scad. It includes BOSL2/std.scad and checks the supported
version; BOSL2 remains external and is not downloaded implicitly. Initial bridge function signature:

```scad
// Proposed helper to implement; the pinned BOSL2 calls are verified separately.
smx_bosl2_anchor(id, geometry, selector, label = undef, placement = ident(4))
```

It returns the ordinary Anchor object fields id/label/position/normal/up; an omitted label becomes id, not undef.
geometry is an explicit BOSL2 attach_geom
description, selector a standard 3-vector or custom name. placement describes the BOSL2 shape's already authored local
placement; it defaults to identity. The generated bridge must not discover arbitrary library modules or use a mesh's
bounds as a substitute for its authored attachment geometry. Example inside a Part, before its geometry:

```scad
g = attach_geom(size = [width,20,10],
                anchors = [named_anchor("mount", [width/2,0,5], UP, 0)]);
@{type: Anchor}
mount = smx_bosl2_anchor("mount", g, "mount");
cuboid([width,20,10]);
```

Use a native Attachment between the resulting semantic anchors. This preserves 07's reusable definitions and
sibling Components: it does not generate a Component child block on a Part or add cross-Part boolean/tag behavior.
Read [the pinned mapping and evidence](bosl2-investigation.md) before implementing the helper.
