# Background evaluation in the full integration

Run: `D:/openscad/runs/scadmaxx-all-features-2026-10-08_15-30`.
Incremental build and everyday checks passed; full acceptance is recorded in the run report. The user accepted the remaining measured performance overhead; this run
integrates the existing fixes and does not start another optimization pass.

The selected local owner closure is retained in `owner-heads.json` and `inputs.json`. Normal forward
merges advance Inspector, background evaluation, provenance, persistence, Cross sections, hierarchy,
anchors and insertion. Diagnostic compositions are not owner inputs. No push or promotion occurred.

## Overlaps to preserve

- MainWindow's synchronous parse/compile/geometry callbacks are replaced by the background pipeline.
  Persistence and hierarchy subsequently bring their collectors and provenance into that pipeline.
  Retain integrated consumer initialization and initialize the background controller after consumers.
- Preserve existing precise lexer locations while adding worker cancellation, including long tokens.
  Keep one ObjectExpression implementation; add its cancellation checkpoint to the retained function.
- Keep thread-local progress state and the existing ScopedProgressCallback used by mesh consumers.
- Worker-side PolySetRenderer preparation must retain the colored 2D contour union from #7091.
  CGAL's prepared-geometry fallback delegates polygon preparation to PolySetRenderer.
- Keep UI spacing/style handling, but use the background feature's asynchronous Customizer metadata,
  retained parameter ownership and safe destruction. Keep updateParameterStates and its declaration.
- Keep the plural GUI function filter, all feature selectors, owned-window dialog cleanup, current
  asynchronous clipping assertions/provider priorities, and LF-only insertion fixtures.
- Most importantly, move the integrated animation completion behavior into EvaluationController:
  nextFrame(), then (if still dumping) Animate::saveFrame(grabFrame()), disabling dumping and pausing
  on failure. The owner's old direct QImageWriter path silently loses GIF/APNG/AVI selection even
  when the textual merge is clean. This is an integration repair because the minimal background
  owner does not depend on the animation PR.
- #6964 captures original worker arguments before parsing. Source-cache initialization extracted
  initializeNativeRuntime(), causing Git to leave that capture in a helper with no argc/argv.
  Keep original_args.assign(argv, argv + argc) in openscad_main(), before parsing. The initial
  MSVC failure and combined integration repair `5cff4aa53` are retained in this run.

Raw conflicts, per-input merge commits, resolution script and validation evidence belong to the run.
Keep the inherited animation straight-RGBA conversion repair as well. Source inspection is not runtime
acceptance; final build/test/package results are recorded in the run report.

## Build environment

The first linked executable reached translation-make.sh, but `dirname` was not on the inherited PATH.
Prepending `C:/Program Files/Git/usr/bin` before the canonical Build-Windows invocation repaired that
environment-only failure. No source change, toolchain change, dependency install or clean rebuild was
needed; the run's build.ps1 retains this exact environment. The canonical script separately adds the
shared gettext tools. A future shell with Git utilities already on PATH does not need another repair.

CTest commands use the build-directory executable, unlike installed-runtime smoke checks. This reused
build directory lacked shaders: four 3MF export/import PNG cases failed with "Cannot open shader source
file: ViewEdges.frag". Matching installed shaders/color-schemes/fonts/locale and other application
resource directories were copied into that build directory. All 228 checks in the retried first CTest
batch then passed. Preserve binaries and evidence; this does not require recompilation or a source fix.
The standalone Customizer target's UIUtils link limitation is already covered by
[the integrated group visibility test](customizer-group-visibility-test.md); do not duplicate it.

## Mixed-color rendering discovered during deep validation

The first complete binary exposed an existing overlap defect in the inherited #7091 contour path:
`Polygon2d::unionedContours()` and `tessellate()` erased colors then called EvenOdd sanitation.
Overlapping colors consequently cut holes out of each other. Direct and CSG-file CGAL rendering of
`examples/Advanced/module_recursion.scad` failed the unchanged golden with a tiny branch-join difference.
Removing only color() from that fixture made the old and new executables match, isolating the path.

Separate integration repair `18686c66650ba212a06298b649c61f7da1063993` preserves outer/hole membership,
normalizes winding (including mirrored outlines), and uses NonZero union. Tessellation reuses that
union, while export retains its colored contours. The new Polygon2d unit case checks overlap area,
holes and reversed winding. Both originally failing image tests and all 514 everyday unit cases pass.
This repair belongs to the color-export integration, not the minimal background feature owner.

The DXF export/import round trip remains a separate issue: export preserves overlapping colored
outlines, while DxfData::toPolygon2d discards color and imports them as uncolored contours. Do not
claim the direct-render repair fixes DXF import, silently flatten exported colors, or rewrite its golden
to hide the difference. See the run report for its acceptance disposition and remaining evidence.

Final built checkpoint: `2050f336a7289002d8d8ca189e9367e7eb19ccc3`. The last commit only corrects
the transparent animation test's invocation to `--render=force`; a bare `--render` before a filename
consumed that filename as its optional argument. Sequential and parallel animation tests then pass.
All 514 unit cases/everyday and all 24 quick performance comparisons pass. ZIP packaging is held:
the minimal two-overlapping-colored-squares DXF round trip confirms lost overlap on import. The
source and run report retain the exact checkpoint, reproduction and resume steps. No remote promotion.

## DXF true-color round-trip repair (subsequent authorized resume)

Repair `62b78cb87b2e12fd8465fe5b34301b4184e5109d` preserves DXF group 420 RGB on
imported lines, assembled paths and Polygon2d outlines. Do not join lines of different colors;
the existing color-aware polygon sanitation must receive separate color groups so their overlap
is unioned rather than interpreted as an uncolored hole. Reset entity color at every entity boundary,
and preserve explicit block color when applying INSERT. This is explicit true-color support for the
selected exporter's output, not a complete ACI/BYLAYER palette implementation.

`src/io/DxfData_test.cc` exercises actual DXF export and import for overlapping colors, shared
endpoints, nested colors, a differently colored filled hole, color reset and a legacy uncolored hole.
The incremental build and everyday profile pass at this commit. The retained two-square image
reproduction now matches before/after DXF round trip (`dxf-roundtrip-fixed/results.json`).
Final focused DXF, performance and packaging evidence is in the same run's report. The historical
held checkpoint above remains evidence of the original failure, not the current delivery disposition.
