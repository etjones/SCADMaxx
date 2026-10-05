# Verification commands for the prepared native feature plans

These commands describe future implementation checks, not checks executed during planning. Use the actual isolated
feature build and executable paths recorded at branch preflight; placeholders below must be replaced, never guessed.
Configure with the workspace Windows profile/shared vcpkg, GUI enabled, Catch2 and `ENABLE_GUI_TESTS=ON` for native
tests. Do not start a complete SCADMaxx build or install dependencies merely to validate a planning document.

```powershell
cmake --build <feature-build> --config Release --target OpenSCADExe OpenSCADUnitTests
ctest --test-dir <feature-build> -C Release -N
ctest --test-dir <feature-build> -C Release -L <phase-label> --output-on-failure
```

Catch tags are CTest labels through the inspected `ADD_TAGS_AS_LABELS` setup. Require every named phase case to appear
in discovery; zero selected tests is failure. Register core/gui tests under actual globs and explicitly append glview
or geometry tests not covered by them. Widget unit tests need a QApplication fixture and isolated temporary settings.

Native test classes register in `src/guitests/guitests.cc`, following TestNavigation/TestAnnotations. For each feature
add its specified environment selector; retain the full test runner. Invoke a real desktop GL context for GPU/input
tests. Example after replacing the executable path:

```powershell
$env:OPENSCAD_SELECTION_TESTS_ONLY = '1'
& '<feature-executable>' --run-all-gui-tests
Remove-Item Env:OPENSCAD_SELECTION_TESTS_ONLY
```

Other selectors specified by plans: `OPENSCAD_VIM_TESTS_ONLY`, `OPENSCAD_PROVENANCE_TESTS_ONLY`,
`OPENSCAD_DESIGN_OBJECT_TESTS_ONLY`, `OPENSCAD_CLIPPING_TESTS_ONLY`, `OPENSCAD_SEMANTIC_TESTS_ONLY`,
`OPENSCAD_ANCHOR_TESTS_ONLY`.
12 adds `OPENSCAD_INSERTION_TESTS_ONLY` and labels insertion-preview, insertion-source, insertion-placement,
insertion-providers, insertion-ui and insertion-commit. Its separately owned 03 prerequisite refinement adds
sealed-evaluation-inputs and inspection-draft. Verify real candidate isolation, one-document Undo and dependency
guards; a plain generated-source probe cannot establish those native features. Later composition includes 04/05
without creating new branch dependencies. External library checks use 11's pinned separately supplied distributions.
03 also supplies [inspection-presentation] tests for the shared mesh provider/effect/mask contract.
These are specified implementation tasks, not claims that all selectors exist in the current source. Always remove
only the selector set for that run, including after failure; retain exit code and logs.
Do not claim an offscreen platform run proves Windows focus, shortcut overrides, display DPI or OpenCSG behavior.

11 has no GUI selector: use providers-schema, providers-match, providers-source and providers-cli CTest labels, plus
providers-external for the separately supplied pinned libraries. Catalogs ship but vendor libraries do not. Its
diagnostic CLI and exact command behavior are specified in its overall plan. External tests must execute for handoff;
an optional CI skip is not passing evidence. For the audited executable, use --summary all for geometry JSON because
--summary bounding-box alone returned null; validate bounds/geometry as well as exit status.

Record feature base/head, configured options, compiler/Qt/QScintilla versions, relevant GPU/driver, command, discovered
case counts, actual pass/fail and limitations. Early phases implement bounded verification harnesses and the specified
algorithm; they do not ask Sol to choose an architecture. A failing algorithmic invariant stops the affected phase
for a documented correction. Prepared plans are not runtime proof, and implementation prerequisites mean completed,
verified source features rather than the existence of their plan directories.
