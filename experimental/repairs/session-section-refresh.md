# Session cross section refresh and validation fixtures

Discovered during `runs/20261006-validation-promotion` on 2026-10-06.

## Session edits lag by one event-loop turn

`DesignDocument` sets `sourceMutation` on `externalEditStarting`. Session-only edits
also emit that signal, although their undo participant completes synchronously and
does not write text. The guard remained true until a zero-delay timer, suppressing
Cross sections refresh during subsequent numeric edits/deletions. The model record
changed while clipping uniforms, restored direction text and list rows lagged.

Owner repair: persistence `6f20eeb69`. Both transient undo callbacks clear the guard
before notifying consumers, matching the existing source-record undo participants.
Use normal forward merges from the owner; do not patch copied consumer files.
The existing consecutive-button, deletion and direction regressions cover this.
Cross sections `clipping-repair1/TestClipping.txt`: 20 passed, 0 failed.

Fixture follow-up `a8383e90e` expects the intentional retained rendering pipeline
when clipping is disabled (zero active clipping planes), and explicitly invalidates
the empty-document evaluation for the before-first-preview scenario. Do not restore
full reevaluation or remove assertions to bypass these cases.

## Persistence test window lifetime

CDB confirmed the design lifecycle suite called `TabManager::actionNew` on a freed
object after a preceding fixture closed the last tab. A spare empty tab alone was
insufficient because `open()` legitimately reuses it. Persistence `cdfc439c1`, after
`85d178f68`, retains a modified sentinel tab for the suite. Production close/open
behavior is unchanged. `design-repair2/TestDesignObjects.txt`: 10 passed, 0 failed.
Two focused fixture attempts were used; do not repeat the empty-sentinel approach.

These passes do not validate the entire integrated release. Keep readiness tied to
the final selected revision and actual remaining evidence. The run report preserves
exact build logs, crash dump and all failing/passing test reports.

## Inspector-created independent cross sections

After removing Section target/frame fields, SemanticController::createSection still
emitted those old fields. Owner `9bf60e5c7` copies world origin, normal and up once
from the resolved target instead; no attachment dependency remains. The regression
asserts empty dependencies, absent target/frame fields, and the copied world pose.
Initialize its ResolveContext as a named aggregate with an explicit live Records
reference; default construction and a temporary context both fail to compile.
Correction `aca9bcd54` was merged forward through anchors and insertion. Semantic
native checks pass (17), anchors pass at three scales (12 each), and insertion passes
(31), in the resumed validation run. Future compositions inherit the owner fix by
merge; no integration-only duplicate patch is needed.
