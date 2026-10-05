# Generic foundation refinements required by insertion

Owner: 03, as a separate follow-up to its completed handoff. Specified 2026-10-04 after 12's decisions.
Implemented and separately frozen on 2026-10-04 in the contextual-insertion prerequisite checkout, without edits to
the original 03 checkout. It imports no 12/provider/semantic headers. Owner patch SHA-256:
`74e9d42cc788bfdbf2b1571f70252c22cb7733fece81a3e30637c2e1c4910761`.
Evidence: `D:/openscad/runs/20261004-contextual-insertion/inputs/manifest.json`; 187 unit checks, 123 native rows,
and ten fake-draft rows at 100/150/200% scale passed. Existing 03 behavior and consumers remain.

## Seeded sealed evaluation inputs

Extend EvaluationInputs with an explicit construction mode and captured source seeds:
ReadPolicy {CaptureMissing, RejectMissing}; seed map of complete SourceInput records in addition to captured editors.
Current callers keep their explicit CaptureMissing policy. New sealed callers supply RejectMissing; root and seeds
are validated for canonical key/UTF-8/hash conflicts. A missing resolved key throws MissingCapturedInput(fileKey),
distinct from file-not-found or invalid UTF-8. read never accesses disk in this mode. freeze still prohibits adding
consumed entries after publication. Preserve exact original editor IDs/revisions in the base evidence.

Provide withReplacement(fileKey, candidateUtf8) on a captured source bundle: one exact replacement, recalculated byte
fingerprint, no fabricated editor revision, and a separate base SourceInput record for currentness checks. Candidate
bytes are hypothetical, not an editor snapshot. A worker adapter may construct the equivalent seeded bundle directly.
Conflicting open editors cannot be resolved by choosing the candidate's version. Keep configuration and import-path
ordering captured separately; filesystem source resolution still returns canonical paths before sealed byte lookup.

Fake tests: seeded dirty include wins, missing key cannot invoke a disk reader, conflicting seeds fail, replacement
does not mutate base, original CRLF/BOM round trips, candidate currentness is checked against base rather than itself.
No public network/HTTP endpoint or arbitrary external binary-resource loader is introduced.

## Draft display lease

InspectionPresentationController remains the sole renderer coordinator. Proposed generic addition:
beginDraft(owner QString, QObject* lifetime, Stamp base) -> move-only DraftToken or diagnostic.
Only one draft lease per viewport. DraftToken exposes:
showBase(); showCandidate(serial uint64, shared_ptr<const InspectionMeshSet>, label QString);
setPending(label); reset(). Candidate sets carry a separate draft identity, never impersonate the installed result.

Opening a lease validates the live base. Suspend ordinary inspection provider installation, masks and effects while
retaining their registrations/settings. Source-based consumers may update their state, but cannot replace draft
pixels. Queue/recompute the live presentation on lease release; do not restore a stale raw renderer captured by 12.
A lease invalidates on real source/result/configuration/document changes, not on its own candidate renderer swap.
Emit draftDisplayChanged with active/pending flags so source-dependent controls and capture/export can disable.

EvaluationBinding adds validateModel(expectedBase, detail): compare document/result/source/configuration and consumed
inputs but deliberately ignore viewportGeneration. It is only for already-captured source-bound operations.
Existing validate/pick still require full presentation identity. While candidate pixels are active, SurfacePick and
ordinary result export/capture return unavailable with a draft reason; the retained live result is not replaced.
Explicit ordinary Preview/Render first closes the draft lease, then follows normal evaluation.

Candidate renderer uses InspectionMeshRenderer with picking disabled and no live masks/effects. Show all pieces.
Candidate draw IDs are local to that payload; they never enter SelectionService or the semantic tree.
Navigation/camera/overlay drawing continues. Pending pixels are visibly pending. Deleting the owner releases once,
including while live mesh preparation or candidate completion is in flight.

ViewportToolRouter adds a session focus group (owner + registered viewport/palette/inspector widgets) for an external
tool token. Moving focus inside the group retains the session; focus outside cancels once. Existing callers without
a group retain their current semantics. Drag cancellation due to input/source changes always wins.
No insertion action names, source-writing callback or downstream class appears in the owner API.

Fake native tests under inspection-draft: base -> candidate -> base, real input invalidation while suspended,
late live-provider completion, owner teardown, no picking/export from candidate pixels, same live result ID,
camera navigation, pending status, internal/external focus transfer. Combined provider/effect state restores correctly.
Add sealed-evaluation-inputs unit label. Existing 03 regression labels/native harness must remain passing.
Record follow-up base/patch/head separately from the original completed 03 handoff and from 12's feature patch.

Additional generic seams verified with the same handoff: applied Customizer value capture; captured RenderVariables
and ParameterSet for one ordinary evaluation, cleared on normal/error completion; explicit native library path order;
and optional resolved-native capability rejection. Native parser missing-input errors remain typed across cleanup.
These are generic evaluation facilities. Candidate evaluation and protocol remain feature 12's responsibility.
