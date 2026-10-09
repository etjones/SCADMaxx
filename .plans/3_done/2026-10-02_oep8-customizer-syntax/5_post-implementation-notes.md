# OEP8 / Customizer syntax handoff

## Sources and scope

- Upstream OEP8a: #6081 head `07b22af25704af0db39959773751fb5c6e4debbe`, containing
  `d5fd4ed345c16af423bbdb13a2d55fb47a3d529d` and the object echo fixture follow-up.
- Upstream #6642 head: `ac910eb97b4f620ed06589dca5a369bbf9bb2648`.
- Local #6642 starting point: `a8083eb97`, based on master `612e684c2` and the
  author's context-lifetime fix. Existing group-visibility GUI changes are excluded.
- Syntax source: `8ea44273775f3c7720f2ff607e6d4ea5215422a6`, committed on `codex/pr6642`
  and verified in `E:/Dropbox/bare_repos/openscad.git` at the same ref.
- Syntax patch: fixed identifier keys, `:`, commas, optional trailing comma and empty block.
  Values remain expressions; only the annotation member construction is restricted.
  Existing reactive hidden/locked behaviour and special-variable tests are retained.
- Ordinary #6081 object syntax and object() are separate from the restricted annotation grammar.

## Integration recipe

Select upstream #6081 first and the declared #6642 variant second. The #6642 source does
not contain #6081 in its ancestry: this is a composition order, not a stacked source delta.
Use auto-merge-base for #6081. The #6642 variant has the explicit delta base
`612e684c2cbbcdcb9a7a8307973f33fd910f9c17` (its current master foundation), excluding
unrelated upstream changes. Retain the original authors' commit identities.

On current master, #6081 conflicts with formatting changes in Value.cc/Value.h. Retain
current implementations of get/set/del/contains/keys/values and add the proposed merge()
declaration/definition. Retain the StackCheck guard in tostring_visitor and switch its body
to the new object serializer. Keep the formatted ObjectObject::del and add merge beside it.
Apply #6081's four echo expectation changes without removing later object-method test lines.
Current master also added two object echo lines to `import-json-expected.echo`; convert
both to OEP8 colon/comma formatting and quote the hyphenated keys. The first run caught
these stale expectations; the corrected four-test echo suite passed.

When composing with #6642, Expression.h/cc both append classes/functions at the same location:
retain OEP8's Object and ObjectComprehension classes AND #6642's ObjectExpression and dependency
collection methods. The latter remains an attribute AST; these are different classes.
The two parser grammars coexist without Bison conflicts.

The isolated verification checkout also applies these existing Windows baseline repairs:
`c577f934adade4b762fba095abbad79a3b13df30` (settings stream declarations),
`b5ef9f6cedaab8bb5087f82bc223dcbe18328c14` (Cairo link target),
`74168dda7953ebd994e81dab6d22574ed24aef4c` (manifest), and
`e1a798257aeaabb0f82898e477ef8f5e6fd3558d` (argument storage).
These repairs are not part of the annotation source variant.

## Verification

Evidence directory: `D:/openscad/runs/20261002-oep8-customizer`.
`verify.ps1` records the shared-dependency Windows Release configure/build/test commands.
`combined.patch` records the complete tested change over `a8083eb97`;
`annotation-syntax.patch` records the focused source change (documentation is in the source commit).
`objects-and-annotations.scad` exercises normal literals, object(), computed keys,
comprehensions, merging and an adjacent fixed-key annotation.
The complete verification source is retained privately as
`ae5e50d7aeb13c4fcfa42ae09126434fefbd69a2`, branch `codex/oep8-customizer-check`.
Do not select that aggregate branch for future builds: integrate each declared input independently.
Clipper2's generated version header has an incidental line-ending-only working-tree change.

Windows GUI Release build passed using the shared vcpkg installation. Both the standalone
annotation grammar and combined OEP8/annotation grammar passed Bison without conflicts.
All six Customizer cases passed (67 assertions), including acceptance/rejection, printer
round trips, widget configuration and ordinary/special-variable updates through includes.
The coexistence fixture passed its assertions and emitted OEP8_AND_ANNOTATIONS_PASS.
All four echo regressions passed: object-tests, import-json, import-json-relative-path,
and text-metrics-test. Logs are in the evidence directory. Source group-visibility edits
and launcher control edits were excluded throughout.

The reusable coexistence fixture is `experimental/fixtures/oep8-customizer.scad`.
Run with `--enable=object-function -o result.echo` and require the PASS marker with no ERROR.
This is feature verification, not a new combined SCADMaxx distribution or full-stack
GUI/packaging acceptance. OEP8a remains an upstream draft; only the recorded paths were tested.


## Lifecycle closure — 2026-10-07

Moved to done at the user's request. Existing verification evidence and historical limits are preserved.
