# Parts, assemblies and components

[Back to language features](../README.md#openscad-language-additions)

These annotations give ordinary SCAD modules and calls an explicit model structure. A **Part** defines a
finished piece of geometry, an **Assembly** arranges pieces, and a **Component** is a placed instance of
either definition. Use them for named model-tree entries, inspecting repeated parts and exporting individual
pieces. The tree describes your source structure, not a history of modeling operations.

## Define one part and place two instances

```scad
@{type: Part, id: "plate", label: "Plate"}
module plate(width=30) {
    difference() {
        cube([width, 20, 4]);
        translate([5, 10, -1]) cylinder(d=3, h=6, $fn=24);
    }
}

@{type: Assembly, id: "pair", label: "Plate pair"}
module pair() {
    @{type: Component, id: "left", label: "Left plate"}
    plate();

    translate([40, 0, 0])
        @{type: Component, id: "right", label: "Right plate"}
        plate(width=35);
}

@{type: Component, id: "pair", label: "Plate pair"}
pair();
```

Evaluate the model to see `/pair`, `/pair/left` and `/pair/right` as placed instances. Select one to inspect
its identity and parameters, or use the model-tree visibility and export actions. Defining an annotated module
alone creates no geometry; the final Component call places it.

Definition IDs must be unique across the document and consumed libraries. Component IDs must be unique
within their parent, including calls produced by loops. Labels can change without changing identity.

Put cuts and unions **inside** a Part, as above. Assemblies arrange Components using transforms and colors;
Boolean operations across Component boundaries and anonymous geometry inside an Assembly are diagnosed.
Call annotated definitions with Component metadata. Ordinary unannotated modules remain usable as usual.

For placement driven by named connection points, see [anchors and attachments](language-anchors-attachments.md).
