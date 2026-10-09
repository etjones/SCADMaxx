# Agent API v1-only implementation and verification

Status: implemented, validated, committed and retained in the private origin. No installation, release composition
or public publication performed.

## Changes

- The full agent API uses `/v1` exclusively. Removed the old annotation route handler, dual-version
  dispatch, annotations-only access mode, old headers and running-to-queued response adaptation.
- One remembered `agentServer/enabled` setting controls the service through both access UI entry points.
  No old setting migration or fallback. Discovery uses `OpenSCAD/AgentServer`, `api_version:1` and
  `schema_version:1`; removed redundant compatibility fields and version lists.
- Retained explicit runtime target identities, immutable source/tree inspection, request receipts,
  source/result/view guards, camera/capture and saved views. Native captures now use the qualified
  `result_id` directly; removed the duplicate numeric `id` from evaluation/result records.
- Removed `contrib/openscad-agent-annotations`; updated the maintained agent client, contract, schema,
  examples and tests. The packaging script now selects only the full agent-server bundle.
- Added the project rule in `AGENTS.md`: backward compatibility requires explicit user authorization.
  The broader SCADMaxx product skill remains in planning and now links this current API handoff.

## Verification

Evidence: `D:/openscad/runs/20261002-agent-api-v1-only/`, including `verify.ps1`, build/test logs and
`source.patch`. Native run: `native-20261002T160349`.

- Windows GUI Release incremental build passed using existing shared vcpkg dependencies.
- Protocol/store CTest suites: 2/2 passed. Transport checks reject `/v2`, annotation headers and capture
  without view guards; verify full v1 capabilities, running receipts, identity, expiry and cancellation.
- Python client tests: 5/5 passed, including multiple instances, discovery, redirects, receipts and PNG checks.
- Native GUI tests: 13/13 passed, no skips. Includes two windows opening the same path, active untitled
  versus displayed owner, invalidation after closure, unsaved source inspection, guarded camera/capture,
  saved views and automatic reload. The updated client executed 23 real commands from the evidence directory.
- Packaging script PowerShell syntax and source diff whitespace checks passed. No new distribution ZIP
  or clean-machine installation was tested; existing release artifacts were not overwritten.

Built executable: `D:/openscad/wt-openscad-http-agent-server/build-http-agent-server/openscad.exe`.
SHA-256: `12B54DCADFF6107BC50876292B6CEEE051F53E42E0A57A555F16EAA1E6C9827A`.
Shared dependency status SHA-256 remained
`2983CAF4494A3428F029553E921A862000477E8E1266A8B74846ACDE80C7C2E1` across validation.
Compiler warnings in existing headers remain; no new dependencies were installed.

## Source/readiness handoff

Source checkout: `D:/openscad/wt-openscad-http-agent-server`, branch `codex/http-agent-server`.
Baseline: `498c4774d26e7235fbc4cbb9b34f56afb39ca645`.
Source commit: `991bb09aee1c5d3f432b4e4352ff96254821b4b5` (Agent API cleanup: Consolidate the full service under v1).
The original prerequisite boundary remains `85829fa71870c4aa6945d3cd4abbc932faeab392`.
The user explicitly requested the commit on 2026-10-02. The staged patch was checked byte-for-byte against
the retained tested `source.patch`, so concurrent direct-HTTP changes were excluded even in overlapping files.
Pushed this exact revision without force to `E:/Dropbox/bare_repos/openscad.git`,
`refs/heads/codex/http-agent-server`; `git ls-remote` verified the full SHA.

`experimental/SOURCES.json` now records this validated head. Readiness remains false because the concurrent
[direct-HTTP follow-up](../2026-10-02_agent-direct-http/1_exploration.md) is still being implemented in the
same checkout. That work must provide its own validated commit and private handoff before integration.
No existing passing verification here is a claim about that later working-tree state or a subsequently rebuilt binary.

Pre-existing Clipper2 generated changes, Serena metadata, Python caches and concurrent direct-HTTP edits remain
excluded. Unrelated control README, launcher, tools and build-workflow edits are preserved.
The preceding completed HTTP plan and its retained evidence remain historical.


## Lifecycle closure — 2026-10-07

Moved to done at the user's request. Existing verification evidence and historical limits are preserved.
