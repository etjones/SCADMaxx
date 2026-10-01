# Phase 1 — Dependency boundary and service foundation

Status: implemented and validated; source commit `a638ae7d3`. See implementation evidence.
Execution evidence is in [post-implementation notes](5_post-implementation-notes.md).

## Entry conditions

- Implementation must have been requested. Verify the dedicated branch/worktree, submodules and local instructions.
- Read annotations' current implementation/verification record and inspect its actual Git state without editing it.
- Identify a reviewed committed annotation prerequisite or focused extraction, recording source SHA, delta base,
  included paths and baseline repairs. An uncommitted reference is not an integration input. If unavailable, report
  the prerequisite and limit independent work to service contracts/DTO tests; do not claim this phase complete.
- Reuse the shared dependency tree. Establish a fresh attempt record under `runs/http-agent-server/`.

## Implementation

1. Record the dependency strategy: annotations-first reviewed delta is the default, followed by a shared-service
   refactor in this feature. Account for separately selected annotation content in future composition to avoid double
   application. Do not merge the combined experimental stack or modify another feature's branch.
2. Write the exact `/v2` contract and JSON fixtures under a proposed `contrib/openscad-agent-server/` folder. Freeze
   full routes, identity headers, error codes, versions, snapshot/node references, budget and job envelopes before adapters.
   Capture current `/v1` responses and the unchanged Python client as compatibility fixtures.
3. Factor annotation transport into a process-level service and worker transport. Register the existing annotation
   controller through an adapter. Start only one listener; existing `/v1` routes retain their header/shape semantics.
4. Add a global Agent Access action/dialog using existing Qt settings/action conventions. It offers enable, stop,
   copy connection and current capability/endpoint state. Keep annotation controls synchronized with the same owner.
5. Migrate old annotation enablement as legacy-only access until explicit broad-service enablement. A fresh install
   remains disabled. Persist broad consent outside document files. Stopping either UI entry point stops the service.
6. Implement `/v2/info`, strict local request validation, capability registration and discovery additions without
   altering legacy discovery fields. Document that the legacy directory name is retained for compatibility.
7. Implement bounded request registry, queued/running/terminal receipts, immutable request fingerprints, expiry,
   tombstones and Stop/restart invalidation. Late callbacks check the original server ID before publishing or acting.
8. Apply the overall-plan connection/body/result budgets before adapter work; register protocol tests in existing
   CMake/Qt test infrastructure. Ensure a headless build does not acquire new GUI-link dependencies.

## Validation

- Enable/stop/restart in fresh and legacy-preference fixtures; assert new source/parse routes are inaccessible under
  legacy-only consent while existing annotation behavior remains available.
- Two instances publish distinct live records. Test stale records, port reuse, incorrect server/protocol headers,
  non-loopback Host, Origin/fetch metadata, wrong media type, malformed JSON and request-size/connection limits.
- Lost response plus identical request does not redispatch; changed body conflicts. Expiry retains tombstones;
  tombstone exhaustion rejects fresh requests. Queued work cannot start after Stop; old completion cannot reach restart.
- Run the unchanged annotation client against retained `/v1` info/list/get/capture/view/restore/status fixtures and
  a native instance when the prerequisite is available. Compare behavior, not only route presence.

## Exit evidence and handoff

Retain dependency provenance, reviewed diff boundaries, versioned contract/schema fixtures, protocol test output and
lifecycle/compatibility evidence. No core release claim yet. Phase 2 consumes the stable service registry and envelope.
If transport extraction changes annotation capture ownership, fix compatibility here rather than deferring a second
listener or undocumented migration. Record evidence in post-implementation notes when work is performed.
