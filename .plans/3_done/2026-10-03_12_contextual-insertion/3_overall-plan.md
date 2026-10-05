# Contextual insertion: technical plan

Status: all five choices and all six implemented phases are locally accepted on 2026-10-04.
See [the source, verification and handoff record](5_post-implementation-notes.md); the executed plan follows.
Read requirements, source-edit-contract.md, preview-contract.md, source-investigation.md and phases 1-6 in that order.
The first phase proves the risky candidate-evaluation boundary before palette development.

## Branch, inputs and ownership

Branch feature/contextual-insertion. Direct prerequisites: 02/03/06/08/11; 07/14 arrive through 08, plus the selected
OEP8/Customizer and configurable-shortcut baseline. No 04/05/09/10/13/15 dependency. Verify 04/05 in later composition.
At implementation preflight record exact prerequisite commits or verified uncommitted deltas, repairs, compiler and
shared vcpkg inputs. Preserve occupied trees. The audit integration 4c325716b94e444637a80df3966197ce110b2b75 is not a base.

03's completed handoff was read: its source is the recorded feature patch fc9f0e8d... in its own worktree. Its existing
headers supply captured inputs, retained scenes, routing and presentation coordination. It does NOT yet supply the
draft display/frozen-input refinements in the overview's insertion-foundation-contract.md. Implement those as a
separate 03-owned follow-up, with fake-consumer tests, before freezing 12's prerequisite base. Keep generic owner
changes out of 12's feature delta. 11 must include the newly specified insertionRole metadata before its handoff.

New core files under src/core/insertion/:
InsertionTypes.h, SourceInventory.{h,cc}, InsertionPlanner.{h,cc}, PlacementDraft.{h,cc},
InsertionPreviewProtocol.{h,cc}, InsertionPreviewWorker.{h,cc}, and focused *_test.cc files.
New GUI files under src/gui/insertion/:
InsertionController.{h,cc}, InsertionPalette.{h,cc}, InsertionPanel.{h,cc},
InsertionPreviewProcess.{h,cc}, InsertionGhost.{h,cc}, and lifecycle/widget tests.
Native harness: src/guitests/TestContextualInsertion.{h,cc}, registered in guitests.cc and CMake.
Fixtures: tests/data/scad/insertion/ plus tests/data/insertion/ protocol/expected-source fixtures.
Modify MainWindow registration/destruction, action registration, openscad.cc internal worker dispatch and CMake lists.
Use current paths discovered at preflight, not the obsolete testdata/scad spelling in older plans.

02 owns editor transactions. 03 owns source/input/result binding, tool routing, overlays and presentation.
06 owns spans and invocation/definition provenance. 07 owns semantic hierarchy. 08 owns frames and attachments.
11 owns typed recipes, version matching and item roles. 12 owns source planning, interaction and candidate evaluation.
No reverse includes or competing live document/result registry.

## Concrete values and interfaces

Proposed namespace Insertion; the following names are new, not existing native APIs:

- BaseIdentity: 03 Stamp, root fileKey, immutable base inputs/configuration, target editor ID/revision/fingerprint.
- SourceTarget: Kind {PartBody, OrdinaryStatement, AssemblyBody, DocumentBody}, 06 span/syntax key, owner frame,
  insertion scope locator, optional definition ID/selected path, vector of affected instance paths, shared-edit flag.
- PlacementDraft: Mode {FixedGeometry, FixedComponent, NamedAttachment}, local fixed frame or 08 ReferenceKey,
  offset Vector3d, spinDegrees double, flipped bool, provider contact frame.
- Draft: monotonically increasing draftSerial, BaseIdentity, SourceTarget, 11 ProviderBinding, typed parameters,
  PlacementDraft, reserved names/IDs and source candidate. Serial identifies a draft, never an evaluated model.
- EditPlan: vector of original-byte patches, exact candidate target UTF-8, SHA-256, generated syntax identities,
  provider binding and chosen shared-edit scope. All patches address one document.
- PreviewProof: draftSerial, candidate hash, executable/build identity, config hash, complete consumed input evidence,
  expected generated-call provenance, affected instance set and immutable candidate mesh payload.
- Diagnostic: code, source span/field when available, plain-language reason and optional source-navigation action.

SourceInventory::capture(retainedScene, provenance, semanticScene) returns a read-only native AST/scope inventory.
InsertionPlanner::targets(hit, inventory) returns eligible destinations and explicit unsupported/ambiguous reasons.
InsertionPlanner::plan(target, fragment, placement, inventory) returns EditPlan or Diagnostic.
InsertionPreviewProcess::start(request, callback) returns a cancellable job handle.
InsertionController::commit checks PreviewProof/current identities then adapts EditPlan to SourceEditing::apply.

Public source spans and frame math are consumed from their owners, not redeclared. SourceInventory stores immutable
native AST locators only while retaining scene backing; no Editor/AST raw pointer crosses the process boundary.
Use a bounded trivia/token scanner solely for comments, whitespace, BOM and insertion points. Statements, scopes,
definitions and attribute boundaries come from the native AST and 06 spans; do not write a regex SCAD parser.

## Controller and interaction

One controller per window and one draft at a time. Shift-A uses a current valid selected surface; without one it arms
03's pick tool, then opens the palette after a valid hit. Miss remains armed. Missing provenance gives inspection plus
a reason; choosing an explicit eligible source ancestor is allowed, guessing a definition is not.

States: Idle -> Picking -> Choosing -> Configuring -> PreviewPending -> Ready -> Committing -> Idle.
Configuring/Ready changes return through PreviewPending. Failed preview returns Configuring with diagnostics and
disabled Commit. Source/configuration/tab/root-result change -> Cancelled -> Idle. Library/catalog mismatch -> Stale
with disabled Commit; explicit refresh starts a fresh capture and candidate. Never silently refresh a stale click.
Escape/close/focus outside the insertion UI cancels. Moving between viewport, palette and its inspector is internal
focus, not cancellation. Use the router's exclusive external token for the session, registered widget focus group and
its drag API for manipulation; the generic owner refinement specifies focus transfer behavior.

The palette is searchable by label/category/provider ID. Unavailable items stay visible with dependency/version
reason. Only role/operation/typed schema drive controls. Show destination, shared scope, placement mode, library/profile,
parameter fields and preview state. No download/install button. One Commit ends the session; no repeat-stamping mode.

Numeric offsets are millimetres and spin degrees. G starts a left-button plane drag; intersect camera rays with the
captured placement plane, ignore parallel/behind-camera intersections with visible feedback, preserve normal offset.
R measures atan2 about that plane origin; freeze on near-zero radius. F toggles Mate/Align as specified by the source
contract. Navigation and camera movement are available when not dragging. Do not rederive up from a moving camera.
Inspector spin edits use the same formula as drag. Enter in a numeric field finishes that edit; Enter in the viewport
or Commit button commits only a Ready draft. Escape cancels the entire insertion. Register stable action IDs
insertion.add/move/spin/flip/commit/cancel through the existing shortcut system; no global key event grab or Vim changes.

Debounce candidate generation by 150 ms after the latest valid parameter/placement change; update ghost immediately
using the last item mesh and new placement. Mark stale-shape ghost while new size geometry is pending. Only one worker
per controller; terminate superseded workers and ignore stale callbacks. Camera-only changes do not regenerate geometry.

## Planned phase order

1. Prerequisite seam verification, isolated evaluator/protocol and stale/cancel proof, no insertion UI.
2. Source inventory, target policy, exact byte edits and source fixtures for geometry.
3. Provider roles, generated Components, fixed/named anchor authoring and placement.
4. Search palette, parameter controls, routing, ghost and actual candidate display.
5. Atomic Commit/Undo, dependency/provenance checks and multi-document lifecycle.
6. Real-library, native interaction, composition and portable handoff verification.

Each phase is buildable and has named checks in its phase file. Use the overview verification-contract.md commands.
No zero-discovery pass, mock production provider, automatic library installation or unrelated complete build.
Runtime falsification of input isolation, source scoping, shared-edit coverage or frame math stops the affected phase
for a documented correction. Do not reduce accepted behavior to get a green test.
