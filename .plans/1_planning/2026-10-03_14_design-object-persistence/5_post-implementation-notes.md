# Local persistence completion, 2026-10-04

All four phases and DO-01–DO-20 are locally implemented and verified. Source:
`D:/openscad/wt-openscad-design-object-persistence`, branch `feature/design-object-persistence`,
base/HEAD `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Uncommitted by instruction.
Run: `D:/openscad/runs/20261004-design-object-persistence`; next authorized entry: 04.

Verified 02/03 and pinned OEP8/Customizer prerequisite closure:
`eabea931786ddd7cff86c8787a9fd7bf31a1a6af0efb177185f28570d12ca076`.
Feature 06 and downstream 04/07/08/09/15 are excluded. The bounded UTF-8/file-location correction
is an independent parser repair, with no provenance table/runtime dependency.

Native collection reads already evaluated assignment values, publishes detached immutable records,
distinguishes include/use/local scope and invalidates duplicate IDs with no winner. Section/View schemas,
rigid references, dependency closure and precise serialization are defined in `doc/design-objects.md`.
The field scanner verifies captured annotation ownership and edits selected literal fields while preserving
expressions, UTF-8, comments, newlines and comma style. Computed/helper/ambiguous fields remain source-only.

DesignDocument owns shared transient records/drafts and scoped consumer adapters. Consumer opaque keys stay
outside the global document ID registry. Promotion inserts required dependencies first, retains IDs and
uses explicit open destinations. EditorUndoRegistry dispatches both annotation and design container actions.
Prevalidated text/lifecycle changes share one native group. Failed transactions preserve source, lifecycle,
tokens and history. Lifetime guards cover callbacks; clear history and editor closure release participants.

Personal views use shared View definitions with distinct personal backing. Explicit source promotion preserves
ID and undo membership; source definitions never enter the personal companion. Inspector Apply/Promote/Rename/Delete
uses 03's contribution API. Ordinary saves preserve current conflict policy and report partial file outcomes.

Verification uses the shared Windows Release profile: toolset 14.51.36231, SDK 10.0.26100.0,
Qt 6.11.1/QScintilla 2.14.1; actual NVIDIA RTX 3070 Ti OpenGL 4.6, driver 616.92.

- 20 unique design cases and all 48 focused CTest cases pass. Full discovery: 108 cases;
  JUnit: 189 section/generator rows, zero failures/errors.
- Four object/JSON/text-metric echo checks and OEP8/annotation coexistence pass. Declared/plain CSG is
  identical at height 40/60; native offset/rotation/save/reopen preserves `height/2`.
- Extracted full native: 75 results (59 behaviors, 16 setup/cleanup), across eight classes.
  DPR 1.5 and 2 each pass seven design behaviors plus setup/cleanup, without skips.
- Actual Inspector actions, annotation/typing interleaved undo, transient undo, consumer dependency
  promotion/rebinding, callback release, computed fields, read-only/stale includes, camera promotion,
  untitled Save As, Save a Copy, external conflicts and two-file partial-save retry pass.
- Seven Unicode exports pass through each extracted launcher. Dependencies unchanged; original Clipper2
  header restored after builds. Feature replay and CRLF-aware whitespace check pass.

Final feature patch: `1eff9db907b673fd4971b5f8338a433931f242edddb3ca8add5fae1d0696d598`.
Complete input: `56275040c8fde09076ce5ae8510927d5845cf5f882ba27cab5142a59f4ec6c9a`.
Verification evidence: `62717755b051cc4bc8c996e3e532036587d745c723ea9077496da645f8b22cd3`.
ZIP `portable-verification-v3.zip`: `ab23a589d2528e33aae3a7412aff54bde3bf3b3bb8827061a4e1ac3951c6005c`.
Source evidence identifies 54 feature files. HEAD alone is not build identity. Phases 3/4 share the final
checkpoint because their native harness verifies both layers. Failed earlier attempts/packages are retained.

Limits: bounded literal edits, unsupported semantic/topology domains, sequential (not atomic) multi-document
saves. Other platforms, a clean machine and an integrated release remain unverified. Later selected navigation
is a future composition obligation. No staging, commits, pushes, promotion, stack edits or README edits.
Rework choices remain fix forward (bounded correction), replan (revise approach), restart (fresh implementation)
or supersede (replacement feature); none is required to continue the queue.
