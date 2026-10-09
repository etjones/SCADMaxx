# Native Customizer attributes

[Back to language features](../README.md#openscad-language-additions)

An `@{...}` block describes the parameter assignment immediately after it. Use attributes to organize
Customizer controls, explain parameters, constrain numeric input and hide or lock conditional options.
This is the SCADMaxx variant of #6642, using OEP8-style `key: value` entries.

## Describe a numeric control

```scad
@{group: "Plate", description: "Plate width in millimetres",
  min: 10, max: 60, step: 1}
width = 30;

cube([width, 20, 4]);
```

Open the Customizer to edit Width. Add `slider: false` to prefer a spinbox. Use literal defaults for editable
parameters; an attribute does not turn an arbitrary computed assignment into a control.

## Show an option only when it applies

```scad
@{group: "Hole"}
with_hole = true;

@{group: "Hole", hidden: !with_hole, range: [2:0.5:10]}
diameter = 5;

difference() {
    cube([30, 20, 4]);
    if (with_hole)
        translate([15, 10, -1]) cylinder(d=diameter, h=6, $fn=32);
}
```

Turning off `with_hole` hides Diameter. `locked: !with_hole` would keep it visible but disable editing.
`hidden` and `locked` reevaluate as Customizer values change. Other metadata, including numeric bounds,
initializes when the controls are created; it does not continuously track those changes.

For choices, use a literal list such as `range: ["small", "large"]` above a string default. Attribute keys
are unquoted identifiers; computed keys, object comprehensions and `each` are not allowed in `@{...}`.
