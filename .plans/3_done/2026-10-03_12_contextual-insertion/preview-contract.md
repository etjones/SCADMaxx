# Candidate preview, evidence and Commit

12 evaluates candidate source independently of live editor state. Normal MainWindow::compile/compileCSG are unsuitable:
they mutate live parsed/root/render state, save backups and use process-global evaluation facilities. GeometryWorker
also borrows a Tree pointer. Do not evaluate candidates by temporarily setting editor text or swapping MainWindow fields.

## Process isolation and protocol

Use an internal --insertion-preview-worker entry point in the same SCADMaxx executable/build, dispatched before GUI
window/HTTP server/settings initialization. Launch through QProcess using the absolute application executable,
separate arguments and hidden Windows process flags; never shell text, a .com relay or PATH-discovered executable.
One worker handles one candidate and exits. Cancel/supersede kills that process; queued output still requires serial
validation. This isolates native parser globals, CWD, RNG, print/progress hooks and geometry caches.

Use length-prefixed CBOR on stdin/stdout (existing QtCore QCborValue). Four-byte big-endian length, then one CBOR map.
Initial protocol version 1; reject any other version rather than add compatibility paths. Handshake includes build
identity and enabled native features. Startup/handshake deadline 5 s. A slow geometry job has no automatic success or
fallback timeout; expose elapsed time and Cancel. Cap a frame at 256 MiB, input closure at 128 MiB, 4096 files, and
returned geometry at 2 million triangles. Exceeding a cap gives LimitExceeded and leaves source untouched.

Request: version, draftSerial, root fileKey/document resolution directory, target fileKey, candidate bytes/hash,
source table (fileKey, exact UTF-8, hash, optional editor ID/revision), ordered library paths, native configuration,
selected backend, provenance expectations and mesh ownership request. Configuration includes the base's actual
$preview value (usually true for an F5 scene), feature
flags, compile defines, global Customizer overrides, fragment controls and warning policy captured from the base.
Use one native configuration encoder and prove the same settings reach worker/root evaluation; no dependence on
a newly launched worker's personal settings. Reject malformed/unknown fields or conflicting source identities.
Post-commit ordinary evaluation must use that same captured configuration; switching Preview/Render mode cancels
the draft first. Do not change $preview just because a candidate is being displayed as an insertion preview.

Freeze candidate source dependencies before successful evaluation. The 03 owner refinement provides a seeded sealed
EvaluationInputs read mode: no disk fallback. If a new include/use is resolved but missing, return NeedInput with its
canonical key/import origin; parent resolves/captures it once through 03's normal dirty-buffer precedence, rebinds 11
if necessary, and restarts. Accumulate a closure, never replace an already captured version. Recheck base inputs after
capture; a changed dependency invalidates the draft. Maximum 32 discovery rounds; cycles/native import errors are
diagnostics, not endless retries. Worker source reads are only from the transmitted table.

This boundary initially covers native SCAD and source-based libraries. A preflight/evaluation capability guard rejects
uncaptured external inputs: import/surface/text-font resources, JSON/data reads, Python execution, external callbacks,
and unseeded random functions. Identify actual native callable/node kinds after resolution, including indirect calls;
do not substring-scan source names. A file loaded only as unevaluated library code is not itself disallowed.
Seeded rands is deterministic. If a required initial catalog invokes a rejected capability, phase 1/3 must stop and
extend the captured-input mechanism with evidence; do not whitelist uncontrolled IO or silently skip its geometry.
An unsupported model remains editable using normal SCAD tools. Do not claim arbitrary existing models are supported.

stdout contains protocol only; route native echo/warnings/errors into response diagnostics and stderr for bootstrap
failures. Response: Success/NeedInput/Invalid/Unsupported/LimitExceeded; echo serial/hash/config/build IDs, consumed
file hashes, resolved generated call bindings, source/semantic diagnostics, affected instance paths and meshes.
Preserve colors/solid/highlight/background roles. For semantic models, evaluate 07's separate Part/residual roots after
08 placement; do not union separate hardware into its parent. Ordinary geometry uses the native complete root.
Return local triangles plus transforms and stable semantic owner paths where available, never raw pointers.
Force lazy Manifold evaluation before success; empty geometry is a valid outcome only with explicit empty status.
Validate all payload lengths, finite coordinates, indices/transforms and identity fields before constructing meshes.

Candidate proof requires successful native parsing/evaluation, no new warning from generated source/calls, correct
semantic/attachment state and generated module provenance matching 11. Preserve unrelated base warnings visibly;
compare diagnostic source locations through the edit offset map so inserted bytes do not create false new warnings.
A missing module/undef output cannot become a successful empty insertion. For subtraction, ensure the selected base
has positive volume and candidate intersects/removes volume when representable; otherwise report NoIntersection and
disable Commit rather than call an external floating mask a hole. Use existing native geometry operations, not 15.
This check belongs to the selected edited target, not a whole model volume that overlapping siblings could obscure.

## Presentation and ghost

Consume 03's generic draft-display lease from insertion-foundation-contract.md; do not install/save/restore raw
renderers from 12. Candidate meshes have their own serial/hash and are NOT a new live EvaluationBinding/result.
While a candidate is displayed, surface picking/export/model-source selection is unavailable on those pixels.
The controller retains the original picked point/reference and input proof. Navigation remains possible.
A source-bound draft does not invalidate itself merely because its own candidate renderer is presented.

During movement show the ghost over the base display, tagged "placement preview"; after a successful evaluation show
the candidate as "Insertion preview — not committed". If shape parameters changed, the old ghost is visibly pending.
A newer pending candidate may retain last successful candidate pixels with a Pending label, but Commit is disabled.
All candidate shared instances are shown. Existing live hide/solo/clipping settings are retained but suspended for the
draft; disable those controls with "Full insertion preview". Restore through 03 when the lease ends. No edits to their
source/settings. This avoids reusing live draw IDs or clipping away evidence of shared edits.

The ghost has no hit identity and does not change the live result. Draw through 03 overlays in WorldDepth/HUD with
RAII state restoration. Do not include overlays in worker geometry, generated source, export or clean capture.
The candidate camera starts at the current camera; geometry refresh does not reset the user's viewpoint.

## Currentness and cancellation

Every callback carries QPointer controller/editor, draftSerial, candidate hash and base document/result/config IDs.
Only the latest active draft may update the UI or proof. Verify current consumed editor revisions AND byte hashes,
closed/replaced paths, current disk hashes for noneditor dependencies, catalog generation/content and effective import
resolution. Catalog/library path-order changes invalidate the binding even if file labels remain equal.
Presentation generation is owned by 03's lease; source/result/config validation uses its separate model-current check.

Cancel kills the worker, removes ghost and ends the draft lease exactly once. No editor, disk, undo history, live
evaluated-result ID or persisted Anchor changes. A source/HTTP edit, failed ordinary evaluation, tab switch/close,
provider reload or application shutdown invalidates late delivery. Worker crashes yield diagnostics, never auto-Commit.
Use bounded asynchronous shutdown; do not block the GUI waiting for process completion.

## Commit transaction

1. Require Ready proof for the exact current draft, candidate bytes/hash, approved shared scope and target editor.
2. Recheck original root/source configuration through 03's model guard, all captured input revisions/hashes and native
   import resolution. Revalidate the exact 11 binding. Regeneration is not a substitute for proving the shown candidate.
3. Recheck target writable/open state and 06 spans/expected bytes. The editor being committed may be an included
   document, but it must be the explicitly selected one captured in this request, not whichever tab is active.
4. On the GUI thread, with no event-loop yield between final checks and apply, issue one SourceEditing::EditRequest.
   Include helpers/imports/wrappers/Components/anchors/attachments in that request; do not promote separate 14 drafts
   in additional transactions. Source is the only persistent state here; generated declarations are discovered normally.
5. On success end the draft display and request normal root reevaluation. Do not publish worker geometry as the
   authoritative live result. Show "Committed; evaluating" until the real source result is installed.
6. A post-commit evaluation failure keeps the successfully edited source with normal error feedback and one Undo.
   Do not secretly revert or retry another patch. Save remains explicit. Undo removes the entire source change;
   redo recreates it, each followed by normal invalidation/evaluation. Do not reopen a cancelled insertion draft.

As with 02's disk conflict checks, an uncontrolled external writer can change a dependency after final hash checks.
State evidence at the checked boundary; normal reevaluation detects later changes. Do not claim cross-process locks.
