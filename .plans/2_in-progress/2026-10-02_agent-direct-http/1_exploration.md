# Direct HTTP agent access

Remove the Python client, replace it with short skill instructions and move useful support into the HTTP service.
Extend the v1-only work in wt-openscad-http-agent-server; preserve its baseline and other work.
Checkpoint: D:/openscad/runs/20261002-agent-direct-http/before.patch.

Implement compiled API help/contracts, receipt links/poll guidance, and bounded direct PNG downloads with hashes.
Keep session/target guards, request identity and expiry. Remove the client and client-specific tests; retain live
coverage as direct HTTP tests outside the shipped skill. No compatibility aliases, automatic target selection,
arbitrary server output paths, dependency rebuild, or integrated release build.

During this work the preceding v1-only task committed 991bb09aee1c5d3f432b4e4352ff96254821b4b5 and explicitly
left this follow-up pending. Our changes remain separate working edits atop that baseline.

Verify protocol edge cases and native workflows with shared dependencies. Keep source pending until an explicit
commit request and private handoff. Historical builds and independent annotations checkout remain unchanged.
