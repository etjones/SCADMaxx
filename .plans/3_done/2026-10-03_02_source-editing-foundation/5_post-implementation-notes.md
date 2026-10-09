# Source editing foundation local implementation handoff

Feature 02's implementation is complete in `D:/openscad/wt-openscad-source-editing-foundation`, branch
`feature/source-editing-foundation`. Base and unchanged HEAD: `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`.
This is the retained HTTP/annotation/navigation prerequisite composition, not a prior full selected-stack build.
Feature and required repair changes remain uncommitted; a base SHA alone does not identify the tested working files.
No staging, commit, push, promotion, enabled-stack change or integrated release was performed.

## Delivered behavior

`SourceEditTransaction` validates the entire original UTF-8 snapshot, document identity, revision/fingerprint,
expected bytes, boundaries, overlap and read-only state before changing text. Descending byte replacements share
one existing Scintilla undo group. Untouched bytes, selection direction and annotation undo are retained.
Normal source revision/fingerprint notifications publish once after the complete transaction. No-op and rejected
requests create no source change or undo step. Captured editors are independent of subsequent active-tab changes.

The synchronous `prepareExternalEdit()` / `externalEditStarting()` seam lets an existing insertion group finish
before a new transaction starts. Rejected/no-op requests do not notify. The transaction guards editor lifetime and
rechecks the request after notification, rejecting observer text/read-only changes or a closed editor. Existing
external edit and annotation-history entrypoints use the same seam. Review found its omission in the first pass;
the bounded fix-forward and real-editor observer tests are included in the final source.

`DiskSourceState` retains canonical identity, file identity and a SHA-256 of raw disk bytes. Save detects equal-length
content edits with restored timestamps, replacement/deletion and unreadable destinations. Cancel retains the buffer;
Save As and Save a Copy protect existing destinations. Explicit overwrite approval applies to the observed version,
with another check before QSaveFile commit and direct-write fallback disabled. Successful Save a Copy retains the
original path, baseline, identity and dirty state. Automatic file observation no longer uses mtime/size as content identity.

Reading still follows the existing QTextStream BOM/EOL decoding policy; the raw-byte disk baseline is separate from
the editor fingerprint. Saved-view and annotation coordination remains, and a later companion failure reports that
source content was saved. A known source conflict is detected before companions are written. No new HTTP source
mutation endpoint, cross-document edit, parser rewrite or persistence format is introduced.

## Source ownership and validation repairs

Owned source is `src/gui/source/` (transaction/disk state and tests), editor/Scintilla, TabManager and MainWindow
integration, new `TestSourceTransactions` native fixtures and conditional CMake/native-runner registration.
The run root is `D:/openscad/runs/20261003-source-editing-foundation`; exact source snapshots, separable patch hashes,
prerequisite and submodule revisions belong to its source-evidence record and handoff.

`source-evidence.json` records 28 final file hashes and canonical LF material at HEAD, Windows-repaired,
native-harness-repaired and final layers. The feature patch applies byte-for-byte to the repaired material.
The repaired-input material hash is `7bd2f81f3b28622beb01c9687aa5dea7df97c4cbbe0cbfa988d9bd76ad7de5cd`.
Completion review independently verified all actual source-file and patch hashes; reverse apply-check with strict
whitespace validation also passes against the working source. Exact patches and SHA-256 values are:

- `feature-source-editing-foundation.patch`: `435890a16d678acd6022685d116bebbdacb59c7ed0670bfced777318dae93462`.
- `windows-repairs.patch`: `e842b3549e34b455170c36c6bf70bebb19f864241c15473fd788dcf3daedf602`.
- `native-validation-repairs.patch`: `96bdba31c9a02b4e9bb1b93c75e254f667da58a25dcab9181cdb4e99152e788b`.
- `complete-working-input.patch`: `aff255284b0e31c75a1a5ecf3f37cb9d960964d22336fd8a7196bd095ed80d0f`.

All six submodules are clean at recorded revisions, including Manifold
`0edd9d54876f3135e431575214dd6d8a72866fee`. The configure-only Clipper header was preserved with before/after hashes
and restored to its original content. The recorded selected later navigation head
`bfd009ef0047452c09e3629d0af25efd6af34700` was not composed here; review that delta during future integration.

The prerequisite already includes the HTTP/navigation/annotation closure. Windows executable-name/Unicode inputs
and the RC manifest dependency correction are separate repair inputs. Unrelated selected keyboard-shortcut/theme/UI
and Customizer/OEP changes were not imported into the feature base. Later selected-stack and Vim integration remains
a composition check, not a test already passed here.

Native validation also exposed inherited fixture defects. Separate validation repairs correct the test-data install
path, live TabManager counts, per-class QTest output, a stack-capturing compilation callback's lifetime, asynchronous
compilation waits and an empty shared cache fixture. Tests now use a nonempty temporary model. The unchanged-content
cache assertion is retained; actual content plus timestamp change replaces the timestamp-only reparse assertion,
matching the new required content-based reload behavior. Navigation's Save All fixture starts from isolated test tabs,
explicitly discarding only closed test-owned buffers so deleted temporary files do not contaminate another test.
New temporary editors are closed before their directories disappear. Production save/conflict behavior is retained.

All failed native/snapshot attempts are preserved. These corrections are not evidence that those earlier runs passed.
Source changes are separated from prerequisite, Windows and native-harness repairs for later review/commit.

## Verification

- Supported MSVC/Qt Release unit and application builds pass using existing shared Windows dependencies.
- All seven explicitly discovered CTest cases pass: five `source-editing` and two `source-save-conflicts` cases.
  Actual QScintilla fixtures cover UTF-8/LF/CRLF, atomic publication, undo/redo, caret/selection mapping, read-only/stale
  requests, open insertion-group separation, no-op/rejected silence and synchronous observer changes/deletion.
  Final inputs were incrementally rebuilt/relinked after the last fixture change and all seven passed again:
  `logs/20261003T194402116Z-BuildUnit.log` and `logs/20261003T194451001Z-Test.log`.
  Initial final discovery is `logs/20261003T193559184Z-Discovery.log`.
- The full ordinary native GUI suite exits zero with 48 passing QTest counts, no failures/skips:
  TabManager 4, SourceTransactions 8, MainWindow 4, ModuleCache 4, Annotations/HTTP 13 and Navigation 15.
  Counts include Qt setup/cleanup where registered; they are not 48 distinct behavioral slots.
  Final full-suite evidence: `logs/20261003T193902501Z-NativeTest.log` and
  `native-20261003T193902860Z` under the run root, with explicit per-class text logs.
- Native source fixtures verify typed edit -> annotation -> transaction undo order, two documents/closed capture,
  read-only HTTP snapshots/stale guards, disk conflict Cancel/Save As/Copy, observed-version overwrite and race,
  existing BOM/CRLF decoding, saved-view persistence and actual filesystem companion failure after source success.
  Annotation/HTTP and navigation persistence behavior also pass in the ordinary suite.

Exact final build/discovery/test commands, exits and patch/source hashes are retained in the run handoff.
Final application build: `logs/20261003T193841998Z-BuildApp.log`. No source changed after these final passing checks.
`handoff.md` supplies the detailed replay/evidence links; SHA-256:
`30c98e237ab23db4194d51c38e3302c9453c8fcc4d26ce82516724f12b6a2e7e`.
`source-evidence.json` SHA-256: `6175545e0d7ca58e0e2bcd6986236fb56acccfe3acec1365359d69b4eeb699ad`.
`verification-evidence.json` SHA-256: `8c54840cecbe92107d3518b35f1c2b8d6e950decf30faa913ca87f3a57e85fd9`.
The verification manifest records executable/log hashes, actual case/slot names and build switches. Native counts
comprise 36 behavioral slots and 12 setup/cleanup results. Shared package status is unchanged at
`2983caf4494a3428f029553e921a862000477e8e1266a8b74846acde80c7c2e1`.
No new native dependency, user installation, release ZIP or clean-machine claim is included.

## Practical limits

Disk checks are snapshot rechecks before commit, not a cross-process compare-and-swap or file lock. Saving source
and companions is not an atomic multi-file operation. Backups remain backups; explicit reload/close choices remain.
Transactions run on the GUI thread and operate on one explicitly captured open document. A later composition must
freeze reviewed committed inputs, replay the isolated feature/repair deltas and test the current selected stack.
Completion does not enable or promote the feature. Available follow-ups are fix forward for bounded corrections,
replan the approach, restart assumptions, or supersede the objective.


## Lifecycle closure — 2026-10-07

Moved to done at the user's request. Existing verification evidence and historical limits are preserved.
