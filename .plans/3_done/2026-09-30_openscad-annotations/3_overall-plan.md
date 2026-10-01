# Overall implementation plan

Implement sequentially in `D:/openscad/wt-openscad-annotations` on `feature/annotations`.
Keep these plans and run evidence outside the upstream source checkout. Preserve all other worktrees.

| Phase | Deliverable | Exit evidence |
| --- | --- | --- |
| [1](4_imp-phase1.md) | Reproducible Windows build and integration design | Configured baseline; compile failures diagnosed |
| [2](4_imp-phase2.md) | Validated record/store and companion persistence | Round-trip, corruption/conflict and dirty-state tests |
| [3](4_imp-phase3.md) | Editor lifecycle and native undo integration | Save/copy/reload and container-undo tests |
| [4](4_imp-phase4.md) | Viewport drawing, capture and review dock | Controller/camera and GUI checks |
| [5](4_imp-phase5.md) | Owned HTTP service and companion workflow | Protocol, routing and external-edit verification |
| [6](4_imp-phase6.md) | Integration review, final full build and delivery evidence | Focused tests and application smoke tests |

Use a document-owned store attached to each EditorInterface, with immutable image bytes and revisioned commands.
Keep QScintilla container actions behind the editor interface. The GUI controller belongs to each MainWindow and
binds to the displayed result; a process-level service routes explicit targets to controllers. All GL/widget access
stays on the GUI thread. HTTP parsing and immutable reads run independently of rendering.

Use existing dependencies; introduce no editor-control API. Keep capture result attribution separate from active
editor selection. Lifecycle changes must preserve annotation-only dirty state through automatic source reload.

Build directory: `wt-openscad-annotations/build-annotations`. Reuse installed vcpkg dependency binaries read-only
from `openscad-6991/build/vcpkg_installed`; record that dependency source and exact configure options. Source repairs
needed by the baseline must be distinguishable from annotation implementation in the final notes.

Update each phase checklist as work completes. A failed exit check is repaired before proceeding where it blocks the
next phase. Final notes list remaining limitations honestly. No commits or pushes are required by this request.
