# Scoped references and semantic placement extension contract

Owners: 14 (typed declaration dispatch) and 07 (semantic evaluation/finalization). Consumer: 08. Specified 2026-10-03
after the six anchor/attachment decisions. Require verified owner hooks before freezing 08's prerequisite-only base.
If an owner implementation has already finished, make a focused owner follow-up and record its tested delta. This
document is not evidence that the hooks exist. 14/07 must build and test without 08; no reverse dependency is added.

## 14: evaluated declaration dispatch

Keep Section/View file-only discovery and global ID rules unchanged. Extend KindHandler with RecordDestination
{DocumentRegistry, Consumer} and an optional synchronous consumer callback for Consumer kinds. A consumer kind must
provide its callback; DocumentRegistry kinds cannot intercept a record. A callback receives a move-owned decoded
Record, immutable evaluated-declaration context and the current EvaluationSession. Invalid decoding reports the
usual diagnostic and never calls the consumer with an apparently valid record.

EvaluatedDeclaration contains DeclarationKey, DeclarationScope, the native Context and LocalScope identity for this
evaluation, and source-file origin (root/include/use-library). Borrowed context pointers are valid only during the
callback; a consumer copies/clones values into session-owned backing. Keep this interface free of semantic/anchor
types. Run dispatch after native effective assignments in each actually initialized scope, reading the same values;
never reevaluate an RHS to collect it. Preserve duplicate marked-assignment diagnostics before deduplication.

The registered handler still decides allowed host/scope. Native use-library file initialization does not export its
top-level records; a semantic module invoked from that library can dispatch local declarations normally. 08's callback
uses 07's scope API below to require file or direct semantic-module body ownership. 14 does not infer semantic scopes.

Consumer-owned local IDs are not inserted raw into the document registry. Their consumer validates qualified owner
keys; ordinary Section/View/Part definition IDs keep the established document registry contract. Source-backed
consumer records still carry DesignSourceMap/DeclarationKey and diagnostics. Generic assignment edit dispatch must
check supported kind as well as host: a typed Attachment is not a Section merely because both are assignments.
08 registers its own edits/resolver and never borrows Section-specific adjustment semantics.

For GUI source/lifecycle reuse, add DesignDocument::registerLifecycleAdapter(kind,lifetime,callbacks), returning an
RAII token. Callbacks provide resolveConsumerRecord(opaqueKey,currentBinding), prepareInsert(draft,stamp),
prepareEdit(opaqueKey,change,stamp), and locatePromotedRecord(draft,currentBinding). The consumer owns opaque keys and
returns the existing immutable Record / 02 EditRequest / diagnostic types; 14 never parses the consumer's owner path.
14 owns draft snapshots and its existing EditorUndoRegistry participant for promotion/undo. After reevaluation it
uses locatePromotedRecord to bind the source record, rather than looking up a local ID in its global record map.
Duplicate kind registration fails; owner destruction unregisters and cancels affected drafts. Unknown consumer kinds
cannot be edited/promoted through Section defaults. Test a fake local-ID consumer, including same ID under two owners,
joint source/lifecycle undo and stale promotion, without importing 08. Implement this in 14 phase 3.

Tests in 14 phase 1: synthetic consumer kind receives native actual values once, two local invocations are distinct,
callback lifetime is bounded, DocumentRegistry behavior/collisions remain unchanged, use-top-level exclusion,
invalid host/scope and missing callback fail. No 07/08 header or implementation is needed for these tests.

## 07: scope access and pre-publication placement passes

Provide `Semantic::currentScope(session, nativeContext, localScope)` returning optional ScopeOwner with document,
definition ID, instance path, invocation ID and isDirectModuleBody. Establish the owner before UserModuleContext
initializes its body assignments and pop it with RAII on every exit. Capture the declaring Assembly/file context
for downstream source-relative references; do not resolve a relative path using whatever item is selected later.

Provide `Semantic::registerPlacementPass(id, order, callback)` with duplicate-ID rejection and deterministic order.
Callbacks receive a mutable per-evaluation PlacementContext after native modules/arguments/geometry are instantiated,
but before final semantic/provenance maps, root-tag pruning, CSG compilation or immutable scene publication. Context
contains the owned unfiltered root, all instances, original local transforms, source/parameter ownership and an API
to insert an instance-bound placement transform. It retains synthetic node/provenance backing until the scene dies.
Consumers may transform existing Component placements only; they cannot reevaluate source, add/remove Components,
change IDs/parameters or mutate shared cached Geometry. Recompute final transforms/provenance after passes succeed.

07 owns the native finalization driver around its evaluated tree. Call it once from the common root instantiation
path in SourceFile::instantiate, before returning to GUI/CLI root-tag/Tree creation, and from the separate definition
default evaluation path before that target job becomes usable. Keep 03's capture/binding interfaces unchanged: its
successful binding receives the already finalized tree. Native syntax-only inspection never invokes geometry passes.

Pass outcomes are Success or structured Failure. On any failure, discard the new mutable result and publish neither
an unplaced current tree nor a partial semantic index. GUI may keep an explicitly stale last-good result; CLI fails.
No pass reruns on a cached/immutable scene; fresh evaluations start from source-authored transforms, never accumulated
corrections. Retain the full instance set for solve/edit multiplicity, then apply 07's ordinary displayed-root policy.

An inserted TransformNode uses a synthetic ModuleInstantiation retained in the evaluation backing, with the original
call's source location, no copied root/highlight/background flags, and explicit provenance linking the original
invocation. It wraps the returned module GroupNode. The Component's local
Part geometry is unchanged. Every consumer (preview, final geometry, pick display, provenance, local/placed export)
must use the same finalized placements; no renderer-only matrix patch or second attachment transform table.
If native root-tag extraction would discard a required correction wrapper, fail with an explicit unsupported-root
diagnostic and offer source/tree-Solo guidance. Do not publish geometry in its pre-attachment position or duplicate
root tags. An unmodified root retaining the complete placement envelopes keeps normal behavior.

07 phase 2 tests use a fake placement pass: move one repeated instance, recompute deepest-owner/provenance transforms,
preserve its Part-local root, verify GUI/CLI/default-job invocation exactly once, failure atomicity and no consumer
registered behavior. This provides independently buildable hooks; the graph and Anchor math belong entirely to 08.
