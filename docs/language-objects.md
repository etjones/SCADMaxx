# Object literals and comprehensions

[Back to language features](../README.md#openscad-language-additions)

Objects group named values into one value. Use them for component specifications, configuration records,
lookup tables and functions that return several related results. This is SCADMaxx's selected OEP8 feature;
use a build that includes it and enable **object-function** in Preferences > Features if disabled.

## Group and read values

```scad
spec = {width: 30, depth: 20, height: 4, "display name": "Plate"};
cube([spec.width, spec.depth, spec.height]);
echo(spec["display name"]); // "Plate"
```

Use dot notation for identifier keys and bracket notation for a string key, including a computed one.
Objects may contain vectors, other objects and other SCAD values.

## Derive a changed specification

```scad
base = {width: 30, depth: 20};
wide = object(base, width=45);
echo(base.width, wide.width); // 30, 45
```

`object()` creates a new value; it does not mutate `base`. Object literals use `key: value`, while named
arguments to `object()` use `key=value`, like other function calls.

## Generate a lookup table

```scad
holes = {for (i = [1:3]) (str("hole", i)): i * 5};
echo(holes.hole2); // 10
```

Parenthesized expressions supply computed keys. This general object syntax is different from the fixed-key
`@{...}` metadata used by [Customizer attributes](language-customizer-attributes.md).
