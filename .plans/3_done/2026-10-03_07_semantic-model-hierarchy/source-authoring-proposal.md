# Accepted semantic source notation

Status: accepted by the user on 2026-10-03. This is the source contract to implement, not syntax already executable
in the audit baseline. The six preceding model-behavior decisions remain authoritative. The filename is retained
from the review; the object-valued geometry alternative is no longer an open choice.

## Annotated modules and component calls

Use the existing object-style annotation notation on ordinary geometry module definitions and calls. Part/Assembly
definitions retain normal module parameter lists and geometry bodies; Component calls supply instance identity and
ordinary call arguments. Section/View declarations continue using 14's annotated object assignments.

```scad
@{type: Part, id: "bracket", label: "Bracket"}
module bracket(width = 30) {
    difference() {
        cube([width, 10, 3]);
        translate([width / 2, 5, -1]) cylinder(d = 3, h = 5, $fn = 32);
    }
}

@{type: Assembly, id: "bracket-pair", label: "Bracket pair"}
module bracket_pair(gap = 50, width = 30) {
    @{type: Component, id: "left", label: "Left bracket"}
    bracket(width = width);

    translate([gap, 0, 0]) {
        @{type: Component, id: "right", label: "Right bracket"}
        bracket(width = width + 10);
    }
}

@{type: Component, id: "pair", label: "Bracket pair"}
bracket_pair(gap = 60, width = 35);
```

Expected tree: `/pair`, containing `/pair/left` and `/pair/right`. The reusable definitions are bracket and
bracket-pair; declaring them adds no extra solids. The root uses gap 60 and width 35; left evaluates width 35,
right width 45. Left/right have the same definition and different instance paths/parameter bindings.
Selecting right shows width 45 from the parent's width + 10 expression. It must not offer a misleading single-instance
numeric edit that rewrites a shared expression. Source binding/edit rules are specified in the
[technical plan](3_overall-plan.md#parameter-inspection-and-edits).

Loop sketch inside an Assembly, showing explicit keys rather than synthesized ordinal identities:

```scad
for (side = ["left", "right"]) {
    translate([side == "left" ? 0 : gap, 0, 0]) {
        @{type: Component, id: side}
        bracket(width = width);
    }
}
```

This is a spelling example, not a second root added to the first fixture. Reversing the side list preserves the keys.
A repeated key under the same parent is an error. Separate placements of an Assembly qualify its internal keys by
their parent instance paths.

## Source evidence and implementation boundary

The inspected parser currently permits attribute_block before assignments only. Extending it to module definitions
and calls is new work. The inspected UserModule already holds parameters/body and ModuleInstantiation handles geometry
calls; expressions support function values and objects, but this parser does not provide module-valued expressions.

The accepted route keeps the normal SCAD geometry body and call arguments; writing geometry: bracket() in an
object is not an existing way to capture geometry and is not part of this implementation.
It expands 14's annotation host kinds and collector integration for semantic declarations; it must not silently
relax Section/View's assignment schema or broaden the existing Customizer annotation rules. Exact grammar, module
library/use behavior, source edits and registry encoding are frozen in the technical plan.

## Nested and repeated fixture

Keep both module definitions above and replace the final root call with:

```scad
@{type: Assembly, id: "rack", label: "Rack"}
module rack(width = 20) {
    for (side = ["left", "right"]) {
        translate([side == "left" ? 0 : 150, 0, 0]) {
            @{type: Component, id: side}
            bracket_pair(gap = 60, width = width);
        }
    }
}
@{type: Component, id: "rack-a"}
rack(width = 35);
translate([0, 100, 0]) {
    @{type: Component, id: "rack-b"}
    rack(width = 45);
}
```

There are two root Assemblies, four pair Assemblies and eight Part instances. Paths include
`/rack-a/left/left`, `/rack-a/right/right` and `/rack-b/left/left`. Widths beneath rack-a are 35/45 per pair;
widths beneath rack-b are 45/55. Reversing the loop changes presentation order, not paths. Duplicate side keys fail.

| Selection | Parameters / editable source |
| --- | --- |
| `/rack-a` | width 35, unique literal call override; editing to 36 changes this rack's descendants only. |
| `/rack-b` | width 45, separate unique literal override. |
| `/rack-a/left` | gap 60 from a call site executed four times; width 35 from expression width. Both inspectable; shared call site is not a single-instance numeric edit. |
| `/rack-a/left/right` | width 45 from width + 10; navigate to expression and parent, preserve the expression. |
| Definition bracket | default width 30; deliberate Edit definition defaults affects only calls omitting width. |

Definition/default controls are separate from selection of a placed instance. With the first example, exporting
`/pair/right` locally gives x bounds [0,45], while As placed gives [60,105]. Exporting `/pair` locally retains that
internal translation. Definition bracket exports width 30. Root hide/solo and clipping do not change those bounds.
