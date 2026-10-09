# Anchors and attachments

[Back to language features](../README.md#openscad-language-additions)

Named references describe points, axes, planes or oriented **Anchors** on a model. An **Attachment** places
one Component by matching its Anchor to another's. Use this for lids, pegs, brackets and other connections
that should follow parameter changes without repeating placement calculations.

This feature builds on [Parts, Assemblies and Components](language-parts-assemblies.md).

## Place a peg on a parametric plate

```scad
@{type: Part, id: "plate", label: "Plate"}
module plate(width=40) {
    @{type: Anchor}
    mount = {id: "mount", position: [width/2, 10, 4],
             normal: [0, 0, 1], up: [0, 1, 0]};
    cube([width, 20, 4]);
}

@{type: Part, id: "peg", label: "Peg"}
module peg() {
    @{type: Anchor}
    base = {id: "base", position: [0, 0, 0],
            normal: [0, 0, -1], up: [0, 1, 0]};
    cylinder(d=6, h=12, $fn=32);
}

@{type: Component, id: "plate"} plate(width=40);
@{type: Component, id: "peg"} peg();

@{type: Attachment}
peg_mount = {
    id: "peg-mount",
    child: {component: "/peg", anchor: "base"},
    target: {component: "/plate", anchor: "mount"},
    mode: "mate",
    offset: [0, 0, 0],
    spin: 0
};
```

The peg sits on the plate at `[20, 10, 4]`. Change `plate(width=40)` to `plate(width=60)` and its mounting
point moves to `[30, 10, 4]`. Anchor positions are local to the owning Part; normal and up define orientation.

`mate` opposes the anchor normals, like two contacting faces. `align` matches their orientations.
`offset` is expressed in the target anchor's coordinate frame; `spin` rotates about its Z axis in degrees.
For example, `offset: [0, 0, 5]` separates this peg from the plate by 5 units.

Paths beginning with `/` identify absolute placed Components. Within an Assembly, relative paths identify
its children. Keep IDs stable and use only one driving Attachment per child; missing endpoints and cycles
are errors. Attachment endpoints require oriented Anchors, not Point-only references.

## Declare a point without driving placement

Inside a Part body, a reference can simply describe a useful location:

```scad
@{type: Point}
tip = {id: "tip", position: [0, 0, 12]};
```

This adds a named reference for inspection; it does not move the Part or create visible solid geometry.
