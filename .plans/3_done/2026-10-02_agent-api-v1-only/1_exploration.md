# Agent API v1 only

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Original exploration status: implemented, validated, committed and retained privately on 2026-10-02. See the source handoff notes.

Replace the dual annotation v1 / agent v2 API with one full agent API at `/v1`. Remove obsolete
protocol dispatch, headers, response adaptations, annotations-only access and the old client bundle.
Keep explicit instance/document/window/viewport identities, current-result/view guards, bounded
inspection, request receipts and all full agent operations. Do not add redirects or compatibility shims.

Update the maintained client, contract, schemas and tests together. Reject `/v2`, old headers and
unguarded capture requests. Verify protocol and client tests and native multi-document/capture/access
behavior using the existing shared dependencies. Preserve unrelated edits and historical evidence.

Source: `D:/openscad/wt-openscad-http-agent-server`, branch `codex/http-agent-server`, starting head
`498c4774d26e7235fbc4cbb9b34f56afb39ca645`. Existing dirty Clipper2 generated content, Serena metadata
and Python caches are excluded. The completed HTTP feature remains historical; this is its follow-up.

Add the project-wide no-backward-compatibility rule to `AGENTS.md`. Keep the broader product skill in
planning, with this API contract as its future input. No release composition or installation is requested.
