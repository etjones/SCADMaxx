# Geometry bounds integration into maintained SCADMaxx

Observed in `runs/20261007-geometry-bounds-reintegration` (workspace relative).
Feature input: `cbf75e737de7f4f36882a23968298bdabdcb699d`, based on selected OEP8 #6081.
Parent integration: `569220a50377c705a4c3af5cc21fd106b2e91662`.

## Merge adaptation

Merge `2c0cda639` preserves both evaluator constructor options: existing `includeBackgroundRoot` remains the
second argument; new `strictGeometry` is third. The bounds builtin passes `(tree, false, true)`. Do not replace
the existing second parameter: Inspector/export callers rely on its behavior. Other conflicts retain current
integration includes and add GeometryPtr alternatives/visitors, capture methods and strict error handling.
The run's `Resolve-Merge.ps1` records the reviewed conflict resolutions for these exact inputs only.

## Shared scope repair

First build failed with C2039 on `body->scope.instantiateModules` and `body->scope.print`.
Current integrated ModuleInstantiation owns `std::shared_ptr<LocalScope>`; OEP8's older base owns a value.
Repair commit `80194e4c5` passes `body->scope` to ScopeContext and the parser scope stack, and uses
`body->scope->instantiateModules` / `body->scope->print`. Preserve shared ownership; do not revert the
integration's source-lifetime fixes or blindly copy the old owner files.

Apply these only where the incoming feature still uses the older interfaces. A re-integration already containing
these commits inherits them. Validation results belong in the run report; this record does not claim a passing build.
