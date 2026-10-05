# OEP8, Customizer and HTTP composition

Run `20261002-scadmaxx-updated` starts from upstream `7d44e5796cd489bcbfb8cef0720abe4db60ce35e`.
Its frozen patches, original author logs, commands and checkpoint ledger are in the sibling run directory.
This recipe explains conflict resolutions; it does not enable inputs or select an aggregate branch.

## Inputs and integration commits

- HTTP source `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`, base `85829fa71870c4aa6945d3cd4abbc932faeab392`;
  integration `5e30ea90031d58fd0543810553597347e739f49f`.
- OEP8a #6081 source `07b22af25704af0db39959773751fb5c6e4debbe`, base `895cd8f96a1b86584dbeee2a2860e1b1208f88cc`;
  integration `ad121fc69ef7aa88da718e81981605675f0e9dd9`.
- #6642 variant source `8ea44273775f3c7720f2ff607e6d4ea5215422a6`, base `612e684c2cbbcdcb9a7a8307973f33fd910f9c17`;
  integration `786df0ba96fb7d46d38481f6933849cd553472fe`.

Always compare the next run's frozen heads and bases before reusing these individual integration deltas.
Do not copy this run's complete tree over a newer upstream baseline.

## Conflict resolutions

1. Apply HTTP after navigation and annotations. The previous reviewed HTTP integration `77199153a`
   plus source follow-ups `991bb09ae` and `6a5dc9d15` applied cleanly, squashed as one entry.
   The follow-ups consolidate v1 and replace product Python clients with direct HTTP discovery and PNG routes.
2. OEP8 conflicts in `Value.cc` and `Value.h` are mostly formatting around existing object methods.
   Keep master's get/set/del/contains/keys/values implementations and the StackCheck guard; add merge and
   the OEP8 serializer. The four reviewed file resolutions in `ae5e50d7a` for Value.cc/.h,
   import-json-expected.echo and object-tests-expected.echo contained only the intended OEP8 delta here.
   Review a diff before reusing them on another base.
3. Keep the HTTP `ParserInspection *parserInspection = nullptr` declaration when OEP8 inserts a blank line
   at that location. Retain the rest of the HTTP parser and lexer changes.
4. Retain the later object-method assertions in object-tests-expected.echo; update only serialized objects.
   All three JSON object-output lines need colon/comma formatting and quoted hyphenated keys.
   Preserve fresh master's textmetrics activation and test placement.
5. #6642 appends `ObjectExpression` and dependency methods where OEP8 appends its object-comprehension
   classes. Keep both families, with each function/class correctly closed. They serve different grammars.
6. `ParameterWidget.cc/.h` needs both `annotationValues()` and the reactive Customizer methods.
   Keep the author's retained `CustomizerContext` and out-of-line destructor, plus the UI branch's
   `updateSpacing()`, `changeEvent()` and native font handling. Do not replace the whole widget from either side.
   Uncommitted group-visibility work is not part of this selected variant.

## Verification and limits

Each entry passed Configure/Build/Test at its checkpoint. Both HTTP store/transport suites passed.
OEP8's standalone fixture and all four echo regressions passed (`language-20261003T003300`).
The combined Customizer checkpoint passed six cases/67 assertions, the OEP8/attribute coexistence fixture,
and all four echo regressions (`language-20261003T003736`). Parser errors in the rejected-syntax cases are expected.
The final delivery unit suite passed 78,118 assertions with zero failures, errors or skips.
See the run report for subsequent native GUI, package and extraction results; these checkpoint results alone
do not establish a complete release.

On final source `8a8eee8c2d7312449b994cfa1152c296617b93f4`, the native annotation/HTTP suite passed
13 checks, including 33 direct HTTP requests, and the navigation suite passed 15 checks including tuning.
Evidence: `native-annotations-20261003T005106808` and `native-navigation-20261003T005139064`.
The separate GUI validation build enables test hooks; the delivery build leaves them disabled.

Use `language-tests.ps1 -Customizer` in the run as the concrete command reference. It uses the matching
Test-step runtime and copies its `openscad.com` beside the build executable for CTest. The selected fixture
is `experimental/fixtures/oep8-customizer.scad`; require its PASS marker and no ERROR output.

HTTP syntax inspection has an explicit incomplete/unsupported-native-kind representation. These integrations
do not add visitors for new OEP8 object nodes or Customizer attribute AST nodes; do not claim complete traversal
of those nodes. The feature-native HTTP workflow must also run against the final combined GUI build.

Existing independent Windows, Unicode, preferences-order and native-fixture repairs remain separate commits.
The run-local checkpoint helper initially unwrapped a one-record JSON array: wrap the entire conditional read
in `@(...)` before appending. That bookkeeping failure did not invalidate its passing Build/Test logs; record
the existing exact-SHA test result without rebuilding merely to repair the ledger.
