# OpenSCAD annotations

Read `../.plans/3_done/2026-09-30_openscad-annotations/1_exploration.md` and its post-implementation notes before
continuing this feature. The implementation and Windows build are complete; six reconstructed phase commits end at
`d670fad09` (2026-10-01). Their final source matches the tested palette-fixed delivery.
Keep annotations on a dedicated feature branch and checkout, independent of the experimental composition branch.
Use `D:/openscad/wt-openscad-annotations`, branch `feature/annotations`, prepared from upstream master at
`612e684c2cbbcdcb9a7a8307973f33fd910f9c17` on 2026-09-30. The branch's push remote is now local `origin`
(`E:/Dropbox/bare_repos/scadmaxx.git`); head `d670fad09dba45526487e958b90fd553c6e1ace0` was pushed and verified
on 2026-10-01. The source registry marks this tested revision ready for SCADMaxx integration.
GitHub publication requires an explicit user decision. Recheck checkout status before work.
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
normal OpenSCAD build first. The feature is already selected in `experimental/PR_STACK.md`; its exact source
and readiness are recorded in `experimental/SOURCES.json`. A combined build remains a separate request.
