# Integration recipe: annotations with navigation and UI

Verified input boundaries for run `20261001-scadmaxx-all-features`:
navigation `bfd009ef0047452c09e3629d0af25efd6af34700`, annotations
`d670fad09dba45526487e958b90fd553c6e1ace0`, and HTTP prerequisite
`85829fa71870c4aa6945d3cd4abbc932faeab392`.

The prerequisite already contains tested annotation/navigation glue. Inspect its delta against the
selected navigation head before reusing it; do not substitute whole files blindly with newer inputs.
Run integration commit: `923af0334` (resolve its full SHA in the source repository).

- `Editor.h`: retain saved-view dirty checking and annotations' out-of-line constructor/store/undo interface.
- `QGLView`: retain navigation/statistics, renderer-change notification and annotation camera lock.
  Suppress annotation frame notifications during internal captures. Navigation is disabled during drawing.
- `AnnotationController`: retain the optional annotation-composition hook for ordinary exports;
  annotation evidence starts from `CaptureContent::ModelOnly` to avoid painting strokes twice.
- `TabManager`: check both annotation and saved-view dirty state for tabs, close and Save All.
  Route Save/Save As/Copy through the combined companion-save implementation. Metadata-only saves
  must not rewrite unchanged source. Retain the UI branch's `StatusMessageBox` changes.
- `MainWindow`: keep navigation cancellation, annotation evaluation hooks, statistics/banner updates,
  and backups for both companions. These hooks complement one another.
- Register both native test suites. Preserve separately applied baseline stream, argument, sleep,
  Cairo and manifest repairs instead of replacing them with alternate fixes from the feature patch.

The run report and exact patches retain conflict resolutions. Verify with the combined unit/render tests,
annotation store/protocol tests and native navigation/annotation/HTTP suites before delivery.
