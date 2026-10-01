# OpenSCAD annotations requirements

This specification implements the agreed exploration. Initial delivery is Windows x64, Qt6, MSVC and vcpkg.

## Scope and acceptance

| ID | Required behavior | Verification |
| --- | --- | --- |
| R01 | Draw annotations on the displayed viewport; no picked objects or mesh anchors. | GUI drawing in preview and rendered view |
| R02 | Multiple outlined strokes; twelve colors; fixed palette excluded from images; arrow cursor over palette; remembered session color. | Image/controller tests and GUI check |
| R03 | Navigate before marks; lock the view while marked; undo/redo strokes; undo-all permits navigation and navigation clears redo. | State tests |
| R04 | Tiny clicks ignored; exiting the rectangle discards only the active stroke; Escape/right-click cancel. | Input tests |
| R05 | Enter captures and opens an immediately focused optional Unicode comment; Add/Back/Cancel; empty strokes/comment allowed. | Dialog tests |
| R06 | Captures are immutable PNGs of the actual viewport with the draft strokes composited exactly once at native resolution. | Framebuffer/overlay comparison |
| R07 | Draft callbacks bind their owner/result/camera/size; invalidation cannot publish stale evidence. | Resize/reload/close tests |
| R08 | Dock has newest-first list, case-insensitive search, fitted thumbnail, wrapped comment, edit/delete and explicit restore. | Review tests |
| R09 | Record selection changes neither camera nor model; edit changes only comment; delete confirms. | Record/UI tests |
| R10 | Restore affects only live camera of the matching document; historical strokes/geometry are not restored. | Camera round trip |
| R11 | Ordinary source plus `model.scad.annotations` companion; normal Save/Save As/Copy/All, close and backup integrate both. | File lifecycle tests |
| R12 | Acceptance never saves; unsaved annotations are agent-readable. Annotation-only Save does not rewrite source. | File timestamps and API reads |
| R13 | Missing companion means no annotations; corrupt/unsupported data is preserved and diagnosed. Conflicting external writes cannot be overwritten silently. | Failure tests |
| R14 | Companion writes are atomic individually; partial source/companion failure is reported and dirty state retained. Copies retain evidence and original dirty state. | Failure/copy tests |
| R15 | Source reload retains current annotation contents and dirty state, without prompting for annotation-only dirtiness. | Actual automatic reload |
| R16 | Accepted annotation commands interleave with editor undo. Native source-history reset clears annotation history too. No history reconstruction. | QScintilla integration |
| R17 | Source, annotation and Customizer dirty state stay distinct. Save/undo in annotation context target the displayed owner. | Cross-tab tests |
| R18 | Each result identifies document/session, input source hash, generation, backend and outcome. Active tab is not capture ownership. | Successful/failed/empty compile cases |
| R19 | Opt-in localhost access, discovery, connection info and Stop. One process service identifies multiple windows/documents explicitly. | Service tests |
| R20 | API lists/reads accepted annotations, reports status, captures viewport and sets/restores camera. | HTTP contract tests |
| R21 | No source-edit/read-buffer, save, reload/compile, execution or document-switching endpoint. | Route rejection tests |
| R22 | External agent edits files normally; existing Automatic Reload and Preview updates root/include/use changes. Captures identify the actual installed result. | External-file correction loop |
| R23 | Explicit request/session/target IDs, idempotent retries, bounded jobs/images/memory, stale/busy outcomes, numeric-loopback and Origin/Host checks. | Malformed/stale/duplicate request tests |
| R24 | Accepted evidence reads remain available while drawing. Camera/capture requests are busy during drafts and compilation. | Busy-state tests |
| R25 | Companion client/skill explains discovery, reading images, external edits, waiting for reload, and verification. | Documented runnable example |
| R26 | Full Windows application builds; focused automated tests and CLI/GUI smoke checks are recorded with limitations. | Final build and test logs |

Draft stroke coordinates use logical viewport pixels; stored positions are normalized, with physical image dimensions
and DPR recorded. Same painter supplies overlay and final composition. General source/dependency snapshots, picked
selection, issue statuses, web UI and agent-controlled editor actions are excluded.

Baseline bounds: 32 MiB per PNG, 64 megapixels decoded, 256 MiB per companion, 1,024 annotations per document,
256 KiB HTTP request bodies, 32 outstanding jobs and five-minute result retention. Exceeding limits returns a clear
error without partial publication. Performance measurements can tighten implementation budgets without dropping records.

All requirements must be traced to verification or explicitly reported as incomplete; passing compilation alone
does not establish UI or workflow parity. Publishing, PR creation and adding to the experimental stack are excluded.
