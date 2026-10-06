# Source-first feature composition

Run `20261004-scadmaxx-all-features` freezes 22 native entries on upstream
`81ade7d33a8ed14fc6817a1cf0d44334592bb9fc`. Consult its `inputs.json`, original patches,
commit lists, `report.md` and `integrations.json` for exact inputs and passing checkpoints.
This is a composition recipe, not an additional selected feature or a claim of final validation.

## Source editing with UI polish

Selected delta: `179f2d528ef32bfcdde3ad70f3094a1a2472a8c6` to
`3131a23d6ec04f4405952d8804a41dd8296b2dc5`. Apply only that feature delta, not its
prerequisite snapshot. Two conflicts occur in `src/gui/TabManager.cc` when UI polish is present:

1. Remove the old `saveError` implementation. The feature removes its declaration and routes
   write failures through the new guarded `saveSource` path.
2. Remove the suffix-only manual overwrite prompt from `saveAs`. The new `saveDocument` flow
   handles all existing destinations using an observed disk snapshot and rechecks it before writing.
   Retain `QFileDialog::DontConfirmOverwrite`; otherwise there would be duplicate/conflicting prompts.
3. Use the existing `StatusMessageBox` for the new save-conflict box and error warnings. It derives
   from `QMessageBox`, keeps the same buttons/default/escape choices, and supplies the selected UI
   artwork. Preserve Save As, observed-version overwrite, cancellation and race rejection.

Integration commit: `166a0e643` in the shared local source repository. Configure/Build/Test passed,
including the source transaction/save-conflict unit cases and controlled-PATH rendering checks;
verification: `logs/20261004T225850934Z-test.json`. Native save-dialog and full consumer-composition
checks remain separate obligations. The original unmerged file/index evidence is retained under
`conflicts/source-editing-foundation/` in that run. No push was performed.

## Existing native fixture inputs

The feature-only source editing commit excludes its development fixture repairs. Review
`runs/20261003-source-editing-foundation/native-validation-repairs.patch` separately before full
native validation: installed test-data layout, live tab counts, scoped callbacks, asynchronous
cache checks, per-class logs and test-owned document cleanup. Preserve production behavior and
record any adaptation as a separate repair commit. The UI relayout/native-picker repair remains
in the existing `native-ui-test-fixtures` catalog entry. Do not treat earlier native results as
proof that this new integrated source passed them.

## Vim with selection and UI polish

Apply only `657aeead6534583964bec8797ae99f445404714c` to
`1c48233689c4582754784c66fd23ed4273d56981`. Preserve both the selection service entries
and the three Vim source entries at the `GUI_SOURCES` append conflict in CMakeLists.txt.
In `TabManager::saveDocument`, retain the styled `StatusMessageBox` saved-view error warning
and add the incoming `if (!self || !captured) return false;` immediately after it. The lifetime
check is needed because a modal dialog can destroy the captured objects; styling does not replace it.
Other incoming guards and the native editor/undo behavior remain intact.

Verified integration `dc5e80a071d457966d85ea87dff02560420bd209` passed Configure/Build/Test
(`logs/20261004T231248314Z-test.json`). Also run `VimEngineTests.exe` explicitly: the normal Test
step only runs OpenSCADUnitTests. Its separate suite passed 217 assertions without failure or skip
(`feature-checks/vim-engine.xml`). Native Vim/restart and complete consumer checks remain separate.

## Provenance and design-object persistence

Integrate provenance `bb68db75a8d0fb259d17f50322306007d3750ebe` after Vim by retaining
both source registrations in CMake and both native test includes. Checkpoint `d1793f675`
passed complete unit and controlled-runtime tests; see `logs/20261004T232244440Z-test.json`.

Persistence `015aa3172759c00979830ab178cc3515b4e7fd50` then overlaps seven files.
Keep all source/header/test registrations, both collector declarations and evaluation-session
members, and both provenance and saved-view services. Destroy services before the inspector.
In `parser.y`, `handle_assignment` must return the shared assignment occurrence and retain
the name/expression location arguments. Record that same occurrence for provenance, design
assignment occurrences and HTTP syntax order. Attribute parsing uses the return value;
ordinary assignment parsing retains the location arguments. Do not pick one side of the parser
conflict or duplicate assignments. The resolved parser matches retained prerequisite
`29c7ce594716b0fb2bb851b685113cd9248496bc` exactly.

Checkpoint `53ddc36b803096236a0cc0162ba5433235a28858` passed Configure/Build/Test
(`logs/20261004T233506604Z-test.json`). Conflicted originals are retained under the run's
`conflicts/design-object-persistence/`. Final native consumer validation remains required.

## Clipping, geometry and provider registration

Live clipping `3e81b46a5` composes additively with provenance: retain both service teardown
paths before saved-view/inspector destruction and all native test includes/selectors/runs.
Checkpoint `cbbfd472c` passed (`logs/20261004T233948569Z-test.json`). Geometry `4e1286c7b`
adds its analysis unit registration beside the existing viewport and clipping lists; checkpoint
`5bd3e77ce` passed (`logs/20261004T234348039Z-test.json`). Provider `9d0cb2097` needs both
the existing generated UI includes and the new dependency on OpenSCADExe for CLI unit tests.
Its checkpoint passed (`logs/20261004T234916219Z-test.json`), including pinned BOSL2/BOLTS
external geometry fixtures, with zero failures/errors/skips. Original conflicts are retained
under each entry's run conflict directory.

For projection/cut image regressions, configure the source `tests` directory as a standalone
CMake project using the deployed test runtime's scadmaxx.com as OPENSCAD_BINPATH. Normalize
that path to forward slashes. The in-build executable lacks installed shader resources, and
backslashes in OPENSCAD_BINPATH break generated CTestCustom.cmake strings. Do not repair
production rendering for these harness failures. The run's geometry-tests.ps1 records the
working invocation; all eight CGAL/Manifold/DXF/SVG checks passed in geometry-20261005T014715.

## Semantic foundations and hierarchy

Foundation `e1d33c876` applies cleanly on the clipping composition; retain the clipping-aware
GeometryEvaluator constructor while adding the native execution guard. Checkpoint `fa9155340`
passed (`logs/20261004T235403824Z-test.json`). Hierarchy `7e50bf157` overlaps provider/core and
clipping/GUI source registrations, and native includes/runs. Keep all entries. The incoming
unit C++ standard assignment duplicates an existing baseline assignment; retain the baseline
assignment once. Checkpoint `5dd47314983f8d6d62e2e1bcad4f87da0d0e6741` passed
(`logs/20261005T000231990Z-test.json`). Native consumer checks remain separate.

## Anchor foundations with clipping

Apply `af0948f5d` after hierarchy. In DesignDocument::updateDraft, keep clipping's loop that
replaces earlier built-in absolute fields by kind. Its `!consumer` predicate preserves the ordered
consumer stream. Follow that loop with the incoming consumer preview callback, isolated input/output,
lifetime checks and identity validation. Remove the old single-line consumer early return and the
incoming unconditional append, which would respectively skip validation or lose clipping coalescing.
Checkpoint `f3d48b7994c8c1b0257596ef896097c3e29a74d0` passed
(`logs/20261005T001131217Z-test.json`). Anchors `629a6d7c8` then applies cleanly; checkpoint
`a70de3070ace4344557331fb626c2b74a92d76a2` passed
(`logs/20261005T001727767Z-test.json`, 685490 assertions, zero failures/errors/skips).
Supply SCADMAXX_PROVIDER_BOSL2_ROOT for its required real BOSL2 bridge checks.

## Insertion foundations with UI and camera behavior

Apply `2895ab7f8` with these explicit resolutions: RenderVariables::applyToContext uses
cameraVariableRotation.value_or(camera.getVpr()), preserving ordinary camera normalization while
allowing exact retained preview inputs. In compileEnded, exceptionCleanup and UnknownExceptionCleanup,
reset evaluationOverrides at entry, then preserve existing statistics/banner updates and a single
annotation finishEvaluation call at its existing position. Keep both Vim and draft test selectors.
The requested Windows resource-list wiring already exists in this baseline; do not duplicate it.
Checkpoint `eb1f2f0337f7d06754eee756808b499f105e12bd` passed
(`logs/20261005T002751908Z-test.json`). Original conflicts are in the run's matching entry directory.

## Contextual insertion and final native fixtures

For `9db25842d`, keep the provider source entries already present and add only the five insertion
core sources at the CMake conflict. Keep Vim selectors plus the filtered insertion selector and
per-class output. In main_wrapper, add the preview-worker dispatch but do not import the older
prerequisite's test-settings block: current openscad_gui already isolates test settings, and the
catalogued test-picker repair is separate. Integration `af68f8823` then needed the scoped
[insertion LF fixture repair](insertion-golden-line-endings.md). Checkpoint `29cb12ee6` passed
(`logs/20261005T004325905Z-test.json`, 687685 assertions, zero failures/errors/skips).

Before final native validation, apply these separately reviewed test changes:
- `bcf48145d` replays cleanly as `862133799` (quiet viewport / fixed capture dimensions / Qt test picker).
- The source-editing native fixture patch adapts as `ac266f5c9`: install tests/data at tests/data;
  use actual tab counts, scoped callbacks, async content reload, and isolated dirty-tab cleanup.
  Keep both QElapsedTimer and QTabWidget includes. Per-class filtered logs already exist after
  insertion, so omit that incoming dispatcher hunk and only remove the unreachable return.
- Semantic/clipping fixture priorities and Ready waits replay as `6aca33101`.
- Retained actual clipping/Vim insertion fixtures (SHA256
  f613ba6bf9ec5a068a5794a9be6cc620b63907a697e2322aeb5c2d2e0f4195ec) replay as `ed23c24b5`.

These source identities describe replay, not native acceptance. Consult the run report for current
GUI build/test results and any later repair. Production GUI test hooks stay disabled.

The final 150% DPI check exposed a selection edge-rounding bug. Apply the
[logical viewport bounds repair](selection-fractional-dpi-bounds.md) when absent;
do not change the existing exterior-edge test expectation to Miss.

### 2026-10-06 forward-merge verification

The frozen current owners still lack the semantic/clipping fixture priorities.
`d0da90316` assigns priority 200 to the four explicit test mesh providers; production
provider priorities remain unchanged. The isolated cross-section suite passed
20/20 in `runs/20261006-scadmaxx-all-features/native-clipping-provider-repair.log`.
`180c92a04` also restores the Ready wait instead of treating an inactive transient
state as completed preparation. These are manually reviewed integration repairs,
not cherry-picks of an earlier aggregate.

The logical selection bounds repair is absent too and is restored as `0bfece13f`.
Its native DPI verification remains pending in that run. Do not mistake source
replay for passing verification or package an earlier staged candidate.
