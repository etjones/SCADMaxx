# Geometry bounds

[Back to language features](../README.md#openscad-language-additions)

Included and validated in the 2026-10-07 local integrated build. Enable `object-function` to use it.
The feature commit remains local, pending explicit promotion to the shared bare repository.

This feature makes a shape available as a geometry value and lets SCAD code query its axis-aligned
bounding box. Use it to position another shape beside an existing one, calculate clearances, or size an
enclosure without repeating the geometry's dimension calculations.

## Bounds query

```scad
shape = {{ translate([10, 0, 0]) cube([40, 30, 20]); }};
bounds = geometry_bounds(shape);
echo(bounds.min);    // [10, 0, 0]
echo(bounds.max);    // [50, 30, 20]
echo(bounds.size);   // [40, 30, 20]
echo(bounds.center); // [30, 15, 10]

// Place a second shape 5 units beyond the measured shape's maximum X.
translate([bounds.max.x + 5, 0, 0]) cube(5);
```

`{{...}}` captures geometry; it does not itself display that geometry. Direct output of geometry values is
outside this first version. The example's final `cube(5)` is the only directly emitted shape. Define a module
and call it both inside the capture and normally when you want to measure and display the same shape.

## Measure and display a part

This example cuts a plate shorter, then places a block 5 units beyond its remaining edge. Measuring the
Boolean result avoids repeating the cutting calculation in the placement code.

```scad
module plate() {
    difference() {
        cube([40, 30, 5]);
        translate([25, -1, -1]) cube([20, 32, 7]);
    }
}

shape = {{ plate(); }};
bounds = geometry_bounds(shape);

plate(); // Display the part separately from its capture.
translate([bounds.max.x + 5, 0, 0])
    cube([5, bounds.size.y, 5]);
```

The remaining plate ends at X = 25, so the block starts at X = 30. Its depth follows `bounds.size.y`.
Changing the plate module updates the measurement and the dependent placement together.

## Result and evaluation behavior

The result is an ordinary [object](language-objects.md): `size = max - min`, and
`center = (min + max) / 2`. This center is the box midpoint, **not** the center of mass.
Bounds include transforms inside the captured shape. Exact bounds of Boolean results may require expensive
geometry evaluation. Module references, hybrid literals and raw mesh extraction are outside this feature.

Empty or invalid bounds return `undef` with a diagnostic. Mixed 2D/3D operations are rejected instead of
measuring only the surviving operands. Two-dimensional results use Z zero. Module arguments are captured
when the literal is evaluated; repeated queries on the resulting value reuse its geometry evaluation.

See the [exploration](../.plans/3_done/2026-10-07_geometry-bounds/1_exploration.md) for scope and open design details.
