# Background evaluation source implementation

Status: initial implementation checkpoint, 2026-10-07. The source-only record below is historical.
The subsequent readiness pass built and tested this source and fixed runtime failures; see the current
[handoff](5_post-implementation-notes.md) and `runs/20261007-background-integration-readiness/report.md`.
The user authorized implementation after confirming that committed freshness/Customizer prerequisites need not
be validated first. Workspace instructions require separate explicit authorization for builds and tests.

## Source and ancestry

- Checkout: `D:/openscad/wt-openscad-background-model-evaluation`.
- Branch: `feature/background-model-evaluation`.
- HEAD, Inspector owner: `b93c9c219198630a2fde3822f2b90c29d88d9180`.
- Pending normal merge, Customizer owner: `13697aa98f18e1d1b26187d2cf5a253e8b6dce07`.
- The prerequisite merge is resolved and staged, with `MERGE_HEAD` retained. Feature changes are unstaged and
  new files are untracked. No commit, push, build promotion, source registry or selected-stack change was made.
- The prerequisite-only index and feature working changes are separately captured under
  `D:/openscad/runs/20261007-background-evaluation`. Read `source-identity.json` for hashes and submodule revisions.

## Implemented source paths

`src/gui/evaluation` now contains the application-owned serialized service, immutable request/owned result pipeline,
and per-window controller. Preview, Render, parameter metadata, completion extraction and HTTP parsing use background
work. Explicit requests take priority; queued requests coalesce by document. Atomic cancellation is checked during
native gate acquisition, parsing, language evaluation, traversal, CSG preparation and supported operation boundaries.
Closing the last window cancels and drains work before application exit.

The pipeline captures feature/render settings and uses job-local input/cache/context ownership. Progress and output
routing are scoped per thread. CPU geometry conversion, inspection and triangle statistics move ahead of GUI
publication. Renderers and OpenGL resources remain on the GUI thread. The old GeometryWorker and synchronous
MainWindow compile/continuation paths have been removed; CLI renderer consumers use the revised constructor inputs.

The Customizer receives effective values and dynamic attributes computed in the worker. Unchanged definitions update
existing controls. Changed definitions retain their AST backing until old controls are destroyed. Parameter changes
schedule metadata even when automatic Preview is off. Source editing itself does not enable automatic geometry work.

Publication performs exact consumed-input validation on the worker, followed by document/revision/configuration and
watcher-epoch checks on the GUI thread. Cancelled and obsolete results cannot replace the display through this path.
The controller retains one inactive completed result and revalidates on activation. Last-good geometry stays available
during work, and camera changes made during evaluation take precedence over the captured camera. These are intended
source behaviors; runtime races, thread affinity and responsiveness have not been validated.

Lifecycle signals record capture, queue, computation, validation, publication and first-frame observations. New GUI
test source covers priority/coalescing, responsive cancellation, language cancellation/recovery and stale queued
Preview rejection. Existing Customizer/module-cache tests were adapted to asynchronous completion and owned ASTs.
The optional native benchmark wrapper lives at
`experimental/performance/native/BackgroundEvaluationBenchmark.h`; its companion validation document explains use.
Neither the tests nor benchmark have been executed.

## Scope and phase status

Phases 1-4 have source implementations without runtime exit evidence. Phase 5 has the minimal Inspector/Customizer
composition, publication and HTTP adaptations; downstream owner composition and remaining action-admission work are
outstanding. Phase 6 has test/harness source and a reproducible checkpoint, without builds or measured evidence.
The feature remains in progress; do not treat this record as acceptance or promotion readiness.

Generic input/Customizer/annotation interface edits currently reside in this feature working tree. Before promotion,
review their ownership and place reusable foundation changes in the appropriate owner history with normal forward
merges, as required by the overall plan. Do not copy or cherry-pick owner deltas into consumers.
