# Phase 5: agent bridge

- [x] Add opt-in process localhost service, discovery and connection controls.
- [x] Add immutable annotation/status reads, queued capture/camera operations and polling/idempotency.
- [x] Enforce bounds, explicit target identities, stale/busy errors, Host and Origin validation.
- [x] Add companion skill/client; skill validator passes, CLI help/discovery run.
- [x] Protocol tests pass. Native HTTP capture, worker reads while GUI is blocked, timed root/include/use reload, annotation retention and failed evaluation pass.

Evidence: transport-tests.txt, final/native-tests.txt and standalone/native-tests.txt. Final audit passes cross-tab
action routing, camera set/restore and bundled Python client execution against the standalone application.

Exit: agent reads evidence and verifies externally edited files without any editor, reload or tab-switch API.
