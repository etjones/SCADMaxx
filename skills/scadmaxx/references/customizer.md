# Customizer and object syntax

For mainstream models use comment-based Customizer metadata and literal parameter defaults, for example:

```scad
/* [Dimensions] */
// Overall width in mm
width = 40; // [20:1:100]
enabled = true;
```

This remains a useful portable authoring choice; do not add dual syntax or compatibility shims to one model.
Keep derived expressions separate from editable literal defaults. Check the actual GUI widgets, dependency
updates and saved parameter sets; a successful CLI parse does not verify a reactive interface.

For a build with the SCADMaxx #6642 syntax variant, read the generated
[native attribute specification](customizer-attributes.md). Its grammar is `@{ key: expression, ... }`
immediately before an assignment. `hidden` and `locked` are reactive; other fields initialize widget metadata.
`range` has additional literal-AST restrictions. Do not promise dynamically resizing sliders from a changing
`range`, `min` or `max`, or infer that empty groups disappear; group visibility is a separate feature.

Use [reactive-customizer.scad](../assets/reactive-customizer.scad) with its sibling include file. In the GUI,
toggle `advanced` and `readonly`: `detail` should hide/show and lock/unlock. Toggle the special parameter
`$detail_lock` too: its included dependency should lock the same control. A CLI echo does not prove GUI
reactivity. Leave unrelated parameter sets and editor buffers untouched.

Ordinary OEP8 objects are values: `{width: 10}`, `object(width=10)`, property access and object updates.
Native annotation blocks are metadata, not expressions or object-valued variables. The two capabilities
are independent: a build may support one without the other. Use the
[object example](../assets/objects.scad) only after a successful probe with the target build's required
`object-function` feature flag. Computed/quoted keys and comprehensions supported in ordinary objects are
not legal annotation keys. Detect unsupported syntax; do not revive the removed `key = value;` spelling.

Source provenance and content hashes for the bundled attribute specification are in
[bundle-source.json](bundle-source.json). Packaging refreshes it from the implementation's canonical doc.
