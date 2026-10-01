# OpenSCAD annotations

Read `../.plans/3_done/2026-09-30_openscad-annotations/1_exploration.md` and its post-implementation notes before
continuing this feature. The initial implementation and Windows build are complete; source changes are uncommitted.
Keep annotations on a dedicated feature branch and checkout, independent of the experimental composition branch.
Use `D:/openscad/wt-openscad-annotations`, branch `feature/annotations`, prepared from upstream master at
`612e684c2cbbcdcb9a7a8307973f33fd910f9c17` on 2026-09-30. The branch's push remote is now local `origin`
(`E:/Dropbox/bare_repos/scadmaxx.git`); its committed starting point is retained there, while implementation edits
remain in the worktree. GitHub publication requires an explicit user decision. Recheck checkout status before work.
Use the existing Blender implementation as the behavioral reference, and adapt it to OpenSCAD's document and
rendering model. It is not a request to install the Blender plugin or operate a running Blender instance.

The Blender reference source is `D:/source/blender-annotations`. The exploration inspects version 0.3.3 at
`f8f84ed4de7efc34dce02b4fbb61cc44d62d1f4e`; read its maintained `docs/usage.md`, `docs/owned-http-api.md`, and
`skills/agent-annotations/references/http-workflow.md` when refining the behavior contract. Record any newer
reference revision used. Follow the user decisions in the exploration: drawing only, companion-file persistence,
and ordinary external SCAD edits picked up by OpenSCAD's existing automatic reload. Keep the agent bridge focused
on annotation access, viewport inspection and read-only status. Do not add picked-object annotations, editor-editing,
reload/compile or document-switching APIs. Preserve the agreed undo behavior while validating the native integration.

Keep native UI, persistence, viewport capture, and agent access changes reviewable. Test annotation behavior in a
normal OpenSCAD build first. Adding the feature to the experimental distribution is a separate manual edit of
`experimental/PR_STACK.md` once a PR or explicitly selected immutable feature revision exists.
