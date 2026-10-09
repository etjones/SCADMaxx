# Test suite organization

The user accepted the 2026-10-07 audit and requested implementation plus agent instructions.
Audit: `D:/openscad/runs/20261007-corpus-expansion/test-suite-audit.md`.

Implement one catalog-driven entry point over existing runners. Separate test purpose from desktop requirements.
Provide everyday, deep-background, desktop, quick/extended performance, real-world verification, distribution and
control-tool profiles. Keep full downloaded-corpus verification outside regular acceptance. Missing coverage must
remain visible. Do not infer test evidence for a current source HEAD from an older binary.

Use controls-level adapters and existing GUI selectors; preserve occupied source feature worktrees.
Run selected GUI features in fresh processes; full GUI still covers classes without individual selectors.
Record that shared-window state within the full GUI suite remains an upstream improvement, not solved by orchestration.
Reuse existing performance and corpus plans instead of duplicating their outstanding native instrumentation work.

Keep AGENTS.md short and route testing decisions to workflows/testing.md. Preserve the existing explicit-user-request
requirement for builds/tests. This implementation request does not launch application tests or desktop windows.
