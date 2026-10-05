# Contextual insertion implementation and local handoff

2026-10-04. All six phases are implemented and locally accepted. The 11 → 07 → 08 → 12 queue is complete.
Final source, extracted runtime, DPI and actual clipping/Vim composition checks passed.

## Source and dependency boundary

The occupied source checkout is `D:/openscad/wt-openscad-contextual-insertion`, branch
`feature/contextual-insertion`, at retained HEAD `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1` plus reviewed uncommitted
working input. Run evidence is `D:/openscad/runs/20261004-contextual-insertion`.

The minimal closure contains 02/03/06/07/08/11/14, OEP8, Customizer and selected #6878. The run's
`inputs/manifest.json` locks exact input hashes, six indexed submodule revisions and additive registration overlaps.
04/05 are checked separately; 09/10/13/15 and integrated-release work remain outside this source boundary.

Generic prerequisite follow-ups were independently frozen before the consumer delta: Windows unit UTF-8 manifest
propagation; 03 sealed input, draft display, focus groups and captured ordinary evaluation; native parser capability
guards; and an explicit bounded inspection budget for the large BOLTS closure. Their owner patches, complete
prerequisite material and independent apply checks remain in `inputs/`. The final prerequisite-only input is
`prerequisite-final-v4-complete.patch`, SHA-256
`d41a5015c3fc16432284208971a6c270e49273ca49aa05b0a28c614b18fbca3b`.
The separate 07 foreign-mesh ownership lookup and native regression follow-up is
`07-semantic-ownership-followup.patch`, SHA-256
`f3987b382a910f75c16d6823febb7720497cce282a2c72977f7685f058134bd8`; its 15-row native owner suite passes.
Original owner checkouts remain preserved. Consumer files do not include clipping, Vim, drawing or manipulation
controllers. The optional composition contains the actual frozen 04/05 implementations and its own interop fixture.

The final minimal source is frozen in `final-v2-source-evidence.json`: 320 affected files, with 33 consumer files.
The feature-only patch SHA-256 is `78a2eea6c88d81be251946efd412a81243df3c0d05fe92d04a917089ab930191`;
the complete working input SHA-256 is `41cf37d49217ac09de4140664880f6d39cbd32a7987b31e6843e816c7a8cc1c1`.
Both were independently applied and compared with canonical final bytes; per-file actual hashes bind the live tree.
Historical phase-5/final snapshots remain retained, including binary resources without EOL normalization.
The optional 381-file composition is frozen in `composition-check/final-v3-source-evidence.json`, complete input
`42382c2da5d748dc9141c6bfb4b2f43f89f9a8ea5c7f9481a69d5ad50c486ea5`; its separate two-case consumer interop patch is
`f613ba6bf9ec5a068a5794a9be6cc620b63907a697e2322aeb5c2d2e0f4195ec`. Both composition patches also replay independently.

## Implemented behavior

Shift+A picks or uses a current surface, opens a searchable provider palette, and offers only proven editable
destinations. Provider roles distinguish finished-Part add/subtract geometry from separate Assembly/root Components.
Shared definitions list all affected instances and require explicit approval. Included targets require an open,
writable user editor; Open source uses a proven range and requires a fresh evaluation/selection before authoring.

Typed parameter controls, numeric plane/normal offsets, spin, G/R/F, Enter/Escape and existing named anchors share
the same placement state. Fixed captures retain the original plane; Components can emit live named attachments.
Navigation remains available. Parameter changes debounce the candidate, show a movement ghost and replace older
worker jobs. Pending, invalid, cancelled and stale drafts cannot Commit.

The internal worker executes the captured native SCAD candidate in a separate process through bounded CBOR frames.
It binds executable SHA, configuration, source/editor versions, consumed dependency bytes, generated-call
provenance, shared instance coverage and actual meshes. Candidate pixels hold 03's exclusive transient display
lease and cannot become the live evaluated scene, a pick target or an export authority.

Source planning retains native AST/provenance ownership, allocates collision-free helpers and semantic IDs, verifies
effective import bindings and preserves untouched byte ranges. Required imports stay at their original safe prefix;
helpers follow original Customizer declarations. Unsupported interleaved geometry/parameter structure receives a
reason. Genuine hole subtraction must remove positive volume from each intended affected target.

Commit checks the exact shown candidate and all current inputs, then applies one 02 source transaction without an
event-loop yield across its synchronous pre-edit boundary. Imports, helpers, wrappers, geometry and references share
one Undo group. Disk writes remain under Save. Successful source apply ends the lease and starts one ordinary root
evaluation with captured configuration; a later native evaluation failure retains source and Undo.

## Requirement evidence

| Requirements | Behavioral evidence |
| --- | --- |
| IN01-02 | Native palette, unavailable reasons, category filtering, real metadata and configured action registration. |
| IN03, IN10 | Exact provenance/target identity; late delivery, source/tab/library/catalog changes and read-only/pre-edit rejection. |
| IN04, IN16 | Isolated candidate/base identity, asynchronous cancellation, latest candidate, movement ghost and sole display lease. |
| IN05-06, IN15, IN17 | Plane drag, spin, flip, navigation, numeric controls, fixed and named placement; reflected/nonuniform owner tests. |
| IN07-08 | Actual cut volume, retained source golden fixtures, import/symbol collisions and original Customizer preservation. |
| IN09, IN18 | Atomic Commit, preceding typing history, Undo/Redo, included-editor targeting, separate Save and later failure behavior. |
| IN11, IN13-14 | All eight real catalog entries, explicit shared-instance coverage, separate hardware Components and independent reopen. |
| IN12 | Minimal consumer closure plus separate actual clipping/Vim composition; no reverse consumer includes. |

Each catalog native fixture retains original/committed source, candidate SHA, configuration and mesh signatures,
CBOR proof, world bounds and cut-volume evidence. Native ordinary evaluation and independent source-only reopen
compare world triangles and roles with the worker candidate. Both extracted launchers additionally compare STL
bounds and actual hole volume under the same `$preview`, `$fn` and Manifold configuration.

## Verification and retained corrections

The full unit suite discovered and passed 295 cases. The focused owner/consumer regression pass passed 194 tests;
the later placement pass passed nine tests. Four standard native parser echo regressions passed. The optional
composition passed all 66 insertion/clipping/Vim unit cases. Commands, CTest discovery, JUnit and logs are retained.
Final native/package counts and exact final source hashes belong to `handoff-verification-evidence.json`.
All final native suites passed with zero failures or skips:

| Final check | Result | Run-relative evidence |
| --- | --- | --- |
| Full core unit suite | 295 cases / 394 JUnit rows | `full-unit.xml`, `logs/unit-discovery.txt` |
| Extracted insertion at 150% | 31 rows | `native-Insertion-scale-1.5-20261004T203407197Z` |
| Extracted insertion at 200% | 31 rows | `native-Insertion-scale-2-20261004T203633661Z` |
| Full extracted native suite | 13 classes / 155 rows | `native-All-scale-1-20261004T203932162Z` |
| Actual clipping/Vim composition | 15 classes / 184 rows | `composition-check/native-All-scale-1-20261004T204652605Z` |
| Eight authored catalog sources, both launchers | 16 checks | `handoff-cli-v4/results.json` |
| Source, package and dependency audit | Passed | `handoff-verification-evidence.json` |
| Composition replay and acceptance audit | Passed | `composition-check/acceptance-evidence.json` |

The actual composition includes clipping/visibility suspension and restoration, and a Vim typing/Commit/Undo
boundary fixture. With builds and CLI jobs idle, clipping's 100,000-triangle fixture passed the unchanged 33 ms
threshold: p95 11.883 ms for one plane and 15.147 ms for eight planes; preparation took 229.270 ms.

`portable-verification-v4.zip` is the matching development package, SHA-256
`754fa3aa1f5240d30364a5e8e4edbc9e2bc9bb89dd90840d2bf8dec5aee4b368`.
It was extracted to `portable extracted 測試-v4` and tested with a clean process PATH. The audit verifies matching
executables and installed documentation, shaders, provider metadata and SCADMaxx anchor bridge; no external library
was bundled. Original 11/07/08 handoff files remain unchanged (40/205/246 files respectively), and the source index
and shared dependency status are unchanged.

The retained runners are `build-feature.ps1`, `Verify-Core.ps1`, `Verify-Parser.ps1`, `Verify-Native.ps1`,
`Verify-HandoffCLI.py`, and the composition's matching build/native runners. Native command records live beside
each test report. To repeat native acceptance, run a fresh PowerShell process:

```powershell
$taskRuntime = 'D:/openscad/runs/20261004-contextual-insertion/portable extracted 測試-v4'
& D:/openscad/runs/20261004-contextual-insertion/Verify-Native.ps1 -Suite All -RuntimeRoot $taskRuntime -CleanRuntime
```

Use `-Suite Insertion -Scale 1.5` / `-Scale 2` with that runtime for DPI checks. Preserve existing evidence;
CLI/package/source-capture
scripts need a new output suffix or label for a new attempt. Run GUI suites sequentially with builds/CLI idle.

The real libraries are external, unbundled and unchanged: BOSL2 2.0.766 at
`e173fa0ae45f9e2082e0d8c0382dae98621b7c20`, and the retained BOLTS 0.4.1 release. Catalog profiles and captured
dependency hashes are included in provider and candidate evidence. No library or private dependency installation ran.

Early failures remain retained. Corrections preserve Customizer fields before generated helper braces, explicitly
consume included editor inputs when starting/reselecting an item, and supply the inspection parser's dependency
callback. Native fixture corrections handle Windows Save EOLs, existing-tab activation, a one-shot synchronous
pre-edit observer, parser abort without a success completion signal, and the suspended clipping resolver. The
desktop host can take native test foreground focus; the harness keeps its Qt window active during long geometry
cases and starts each case with the intended Qt window active. Intentional editor focus cancellation remains a
separate native behavioral check. The broader DPI run also exposed the semantic controller's unsafe assumption
that every presented draw ID was in its own map. The separate 07 follow-up treats foreign IDs as unowned, with a
native regression that replaces presentation meshes and restores the semantic provider. Critical exception dialogs
are recorded and fail the native fixture rather than silently hanging or passing.
An incomplete composition run discovered only Vim because empty inherited test selectors still count as set to Qt.
Its report was rejected by the class-discovery guard. The runner now removes all inherited selectors from the child
environment; the final accepted run discovered all 15 classes. Earlier failures and incomplete runs remain retained
and do not count as accepted evidence.

The existing HTTP API supplies source snapshots and remains read-only for source mutation, as owner 02's accepted
requirements specify. Native checks verify original-source snapshots during a draft, rejection of an absent HTTP
source-patch endpoint, and cancellation on an actual concurrent 02 source transaction. No new HTTP mutation API was
added to satisfy the phase plan's illustrative HTTP-patch wording.

## Verification limits and handoff disposition

The Windows Release profile uses MSVC 14.51.36231/compiler 19.51.36257, SDK 10.0.26100.0, Qt 6.11.1 and QScintilla
2.14.1 with the existing shared vcpkg installation. Manifold candidate meshes and the actual NVIDIA OpenGL viewport
are tested. Other operating systems, other GPU drivers and a dependency-free clean machine remain unverified.
The portable development runtime verifies an extracted spaces/Unicode path and clean process PATH, with shipped
catalogs, shader resources and the same worker executable. It is a feature verification package, not a new selected
SCADMaxx distribution.

The full unit evidence predates final native harness and generic GUI ownership corrections. The final hash audit
confirmed every core file and CMake registration matches the full-unit checkpoint; affected native owner and
consumer suites passed against the final package. No passing unit result is attributed to changed core code.

Deterministic captured native SCAD is supported. Uncaptured external geometry/data/font/Python inputs, unseeded
random calls, ambiguous ordinary repeated leaves, interleaved Part declarations, tagged subtraction internals,
definition cloning, loop expansion, live anchor holes and surface rematching remain outside the accepted delivery.

No source/control index staging, commits, pushes, promotion, stack/readiness registry changes or release publication
are part of this handoff. README and unrelated work remain preserved. The feature can be committed or promoted
later under a separate explicit request using its frozen feature delta and reviewed prerequisite closure.
