# Animation and export integration checkpoint — 2026-10-07

Status: integrated locally on `scadmaxx-20261006`; not built, tested or pushed.
The performance work is owned by the separately forked chat. Do not gather its dirty changes into this work.

## Frozen inputs

Fetched original GitHub PR heads into the shared `openscad-master` repository under
`refs/scadmaxx-review/animation-export/pr-<number>`:

| PR | Head | Purpose |
| --- | --- | --- |
| [6951](https://github.com/openscad/openscad/pull/6951) | `d072ffc145acfd7bc6f75fde875f979ad7abc796` | Transparent PNG export and optional live transparent compositing |
| [6963](https://github.com/openscad/openscad/pull/6963) | `71ab1cf782b92139005f2ff656badcb7d0764b6d` | GIF, APNG and MJPEG/AVI animation export |
| [6964](https://github.com/openscad/openscad/pull/6964) | `b2455385cc04818579fe73f628fdac6c608513c6` | Process-based parallel animation rendering |
| [7091](https://github.com/openscad/openscad/pull/7091) | `f281f9226d046d6e34c5619c3ed4294e5832e2d3` | Preserve model colors in SVG, PDF and DXF |

All four were open and unmerged when queried. API responses, issue/review comments and merge-tree
previews are retained in `D:/openscad/runs/animation-export-integration-2026-10-07`.
PR discussions and linked issues #891, #6648 and #1364 were retrieved. The PR #6964 description
explicitly declares #6963 as a prerequisite; it is not a separate implementation of container export.
The GIF discussion distinguishes export from decoding untrusted images and explains the choice to avoid ffmpeg.
The #6648 discussion points to #6951 as its implementation; #6604 is related color-customizer work,
not a declared prerequisite. #1364 also discusses curves and 3D colors, which are outside #7091's scope.

## Revised strategy: three original PR inputs

The user chose to take #6964 alone for animation. Select #6964, #6951 and #7091;
do not separately select or merge #6963. No local #6964 variant or reconciliation merge is needed.
This supersedes the initial proposal below's ancestry concern: code inclusion suffices here because
we are deliberately selecting the combined upstream implementation, not maintaining two independent inputs.

The current #6963 head is **not** an ancestor of #6964. Thirteen #6963 commit IDs are absent from
#6964, despite their resulting container-export implementation being present. A direct merge has
add/add conflicts in `VideoEncoder.cc`, `VideoEncoder.h`, `video_apng.cc`, plus conflicts in
`openscad.cc` and `tests/CMakeLists.txt`.

Comparing the two complete trees shows differences in only ten files, all in the parallel-rendering
implementation, its registration and tests. `Animate.cc`, the container capture path, GIF/AVI writers
and base encoder tests have identical content. Do not infer dependency readiness from the PR description.

The complete-tree comparison also confirms that #6964 retains GIF frame-delay rounding/warnings,
GUI recording and its save-dialog pause, sequential container export and animation_export test
registration. The difference adds workers and the partial-shard warning rather than removing those features.
Record #6963 as supplied by #6964, not as a missing separately selected ancestor. On future updates,
compare #6963's current implementation against #6964 again; this conclusion applies to the frozen heads.

Recommended merge order: #6964, #6951, #7091, preserving original authorship. No additional build
dependency is introduced by their declared implementation. Neither #6951 nor #7091 declares a
dependency on the animation branch. The three frozen heads are now enabled in PR_STACK.md.

## Completed local integration

Run: `D:/openscad/runs/scadmaxx-all-features-2026-10-07_16-41`.
Parent: `1dae1d07fdfd5094d48e7292cbbdaf24d490bc3b`; final: `e537c7a7840d249ef5c8c0142320e06dc8633eb0`.

| Commit | Change |
| --- | --- |
| `6c48fbaa3762908dd345714a3acf10b71c42acbf` | Merge #6964; preserve provenance arguments, close/pause failed GUI recordings without pausing normal loop completion |
| `7de37fb0c390f4ed93cc0b908721e4ba6c554871` | Merge #6951; combine CaptureContent and transparency, preserve overlays/annotation rules and scoped live-state restoration; retain both GUI test registrations |
| `b91b5c64f05ef2acb89b811b7c390994f9fd9650` | Merge #7091; no conflicts against the existing integration plus the preceding merges |
| `e537c7a7840d249ef5c8c0142320e06dc8633eb0` | Separate repair: shared OffscreenView::captureRGBA for PNG and sequential animation; transparent sequential/parallel APNG regression added, not run |

No feature-owner branch was changed. Existing dirty feature/performance work was excluded. Old executable,
build cache and packaged deliveries are unchanged. Only source/diff/ancestry inspection was performed.
The integration's own source modifications are committed; control documentation is not committed.

## Conflicts with SCADMaxx

Static merge previews used existing integration `scadmaxx-20261006` at
`1dae1d07fdfd5094d48e7292cbbdaf24d490bc3b`. They did not change that checkout.
Recheck its HEAD and ownership before integration because the performance chat may advance it.

- #6964: preserve the existing source-provenance `syntax` argument to `do_export` and add
  the encoder argument alongside it. Update **every** call, including sequential frames and the
  normal single-image path. Replace the old MainWindow numbered-PNG dump block with the PR's
  `Animate::saveFrame` flow; preserve normal preview completion and SCADMaxx capture composition.
- #6951: `QGLView::grabFrame` already takes SCADMaxx `CaptureContent`; the PR replaces it with a
  transparency boolean. Combine these independent options in one API, update all consumers (also
  upstream GUI tests), and retain model-only captures, annotation composition, camera cancellation,
  overlay suppression and scoped restoration. Capture transparency must not leak into the live view.
  Preserve premultiplied-to-straight-alpha conversion and the opaque RGB path from the PR. Review
  annotation composition after conversion. The new live-compositing feature is separate from export.
- #6951 also conflicts in GUI test registration and CMake lists: retain both sets of entries.
- #7091 merged without text conflicts in the standalone preview. This does **not** establish
  compatibility with geometry bounds, geometry caching or selection/provenance: it changes
  Polygon2d, GeometryEvaluator and ClipperUtils as well as the exporters.

## Three-input overlap reevaluation

Pairwise `git merge-tree --write-tree` inspections (not builds or tests) found:

- #6964 + #6951: no textual conflicts, but the alpha-conversion bug below.
- #6951 + #7091: no textual conflicts.
- #6964 + #7091: one MainWindow animation-dump conflict. #7091's upstream ancestry carries the
  numbered-PNG error-handling block; retain the new `Animate::saveFrame` flow and verify its failure
  handling preserves reporting and stops recording. This is not a conflict in colored geometry itself.

**Required integration repair: consistent transparent frame conversion.** #6951 renders transparent
framebuffers with premultiplied RGB. Its `OffscreenView::save` un-premultiplies RGB before writing PNG.
#6964's sequential `export_video_frame` reads the framebuffer directly, flips it and passes it to
the encoder without that conversion. Parallel workers instead save PNGs and therefore get corrected
pixels. A naive merge consequently gives sequential APNG darkened translucent colors compared with
parallel APNG. Share the corrected framebuffer-to-straight-RGBA conversion between still and animation
capture; preserve the ordinary opaque path. Verify both preview and full-render exports later.
Worker argument forwarding preserves `--view transparent` in its original-argument pass-through.

GIF and MJPEG do not offer APNG's full alpha semantics. Do not silently promise transparent output
for them; define rejection or background compositing explicitly if exposing that combination.

The APNG compressed-PNG fast path also needs review: it copies IHDR/IDAT but not palette chunks,
and its different-IHDR fallback encodes RGBA without changing an already established output IHDR.
The Windows lodepng writer disables automatic format conversion and emits fixed RGB8 or RGBA8,
so a run with fixed transparency settings does not normally encounter those cases. Do not claim
generic arbitrary-PNG support or a demonstrated Windows failure from this inspection alone.

The sequential composition is now committed as listed above. Textual integration and source inspection
do not prove the result builds or behaves correctly. Build and runtime acceptance remain pending.

## Validation to run only when requested

- Encoder unit tests and animation_export / parallel-animation end-to-end tests: frame counts,
  ordering, timing, numbered PNGs, worker failures, sharding and one complete container.
- Windows workers launch the actual scadmaxx executable; verify paths with spaces/Unicode and
  temporary-directory cleanup. No ffmpeg or extra vcpkg rebuild is required by the advertised design.
- Transparent PNG tests: RGB default, RGBA opt-in, semi-transparent geometry compositing, restored
  live viewport state, repeated captures, model-only HTTP captures and annotation composition.
- Color SVG/PDF/DXF cases plus uncolored export regressions; inspect current #7091 code rather than
  relying on its description, which still says the F6 view does not use outline colors although the
  current diff changes both PolySetRenderer and CGALRenderer and its latest comment demonstrates F6.
- Relevant geometry-bounds and inspection/provenance regressions after the 2D geometry changes.

No acceptance, performance or runtime claims can be made from the merge-tree previews.
