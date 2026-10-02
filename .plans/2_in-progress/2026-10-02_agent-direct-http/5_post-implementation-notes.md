# Direct HTTP access — implementation and verification

Implemented in `D:/openscad/wt-openscad-http-agent-server`, branch `codex/http-agent-server`, atop
`991bb09aee1c5d3f432b4e4352ff96254821b4b5`. Committed on explicit request as
`6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1` and pushed to the private source origin; remote SHA verified.
No GitHub publication, installed skill changes or release build.
The preceding v1-only task retained its own commit while this work was underway; its changes are preserved.

## Delivered behavior

- Removed the shipped Python client and client-specific tests. The earlier annotation-only bundle was already
  removed by the v1-only change. Historical artifacts/independent feature checkout remain historical.
- The skill now explains direct HTTP bootstrap, discovery-file locations, identity verification, target selection,
  polling and image download. No Python or installed package is required to use the service.
- `/v1/info` advertises help/schema/contract/status links. `/v1/help` supplies operation routes, field groups,
  examples and workflow rules; `/v1/schema` supplies record schemas; `/v1/help/contract` serves the full contract.
  All three are compiled Qt resources and work without a source checkout. Session and browser-origin guards apply.
- Receipts expose `status_route` and pending `poll_after_ms`; errors point to help. Existing request identity,
  replay, expiry and queue semantics remain. Port discovery uses existing local records or copied connection info.
- Annotation metadata/capture results link to raw PNG downloads with byte counts and server-computed SHA-256.
  Downloads include content type/length/hash. Removed base64 payloads, with no compatibility path. Captures retain
  binary data within the existing 128 MiB budget and release it on expiry/Stop; image responses cap at 32 MiB.
- No arbitrary server-side output file writing or source-edit/evaluation API was added. Save images with normal HTTP
  tools. Existing native evidence validation/capture encoding supplies PNGs; transport hashes the bytes it serves.
- Live acceptance driver moved to `tests/annotations/LiveHttpWorkflow.py`: test-only direct standard-library HTTP,
  no product client import or command wrapper. Updated native tests download images directly too.
- Packaging selects tracked Markdown/JSON guidance rather than executable client/test files. The broader SCADMaxx
  skill exploration links this handoff. The hand-maintained root README and its concurrent user edits were untouched.

## Verification and reproduction

Evidence: `D:/openscad/runs/20261002-agent-direct-http/`.
Run `verify.ps1 -Step Build`, `ProtocolBuild`, `ProtocolTest`, and `NativeTest` from that directory.
The script uses existing shared Qt/MSVC/vcpkg dependencies and isolated native test settings.

- Windows Release GUI build passed; existing compiler warnings remain.
- Protocol/store CTest: 2/2 passed. New cases exercise compiled help/schema/contract, raw annotation/capture bytes,
  hashes, receipt links, pending/absent/expired images, restart invalidation, wrong-server and Origin rejection.
- Native GUI: 13/13 passed, no skips. Direct HTTP workflow executes 33 requests against the live server, including
  source snapshot/parse/tree, camera/capture/image, and saved-view operations. Existing multi-window, unsaved-source,
  annotation persistence and external reload cases also pass. Native F6 capture verifies nonblank image content.
- Final schema resource refresh was rebuilt; protocol tests and native suite rerun against that executable.
- JSON parse, source whitespace and packaging PowerShell syntax checks passed.
- Shared dependency status SHA-256 unchanged:
  `2983CAF4494A3428F029553E921A862000477E8E1266A8B74846ACDE80C7C2E1`.
- Executable `build-http-agent-server/openscad.exe` SHA-256:
  `DEAADE7CD7698B2BE362226817046B3A95FC83D18EB02248750CF43BB190D4A5`.

`before.patch` preserves the starting dirty state; `source.patch` plus `new-source/` retain this follow-up relative
to the v1-only baseline. No integrated ZIP, public release, macOS/Linux or clean-machine test was performed.

## Source handoff

`experimental/SOURCES.json` is `ready:true` and points here. Source commit and remote branch match at
`6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1` in `E:/Dropbox/bare_repos/openscad.git`.
Unrelated Clipper2 generated changes, Serena metadata and old Python caches remain excluded.
The original prerequisite boundary `85829fa71870c4aa6945d3cd4abbc932faeab392` remains applicable.
Control changes (packaging selection, readiness, worktree/skill-plan pointers and this plan) are separate from source.
The next aggregate build must use this retained follow-up; no existing distribution was silently overwritten.

Available follow-ups: fix forward for bounded corrections, replan for a different approach, restart if assumptions
change, or supersede this feature with a replacement.
