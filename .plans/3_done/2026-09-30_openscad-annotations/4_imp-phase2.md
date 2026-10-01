# Phase 2: records and companion storage

- [x] Add record validation, immutable PNGs, JSON serialization, version and resource bounds.
- [x] Add document store with independent dirty/save state and reversible record commands.
- [x] Read/write bounded ZIP companions using QSaveFile publication; detect disk conflicts.
- [x] Test round trips, corrupt images, missing and conflicting companions, empty store and failed writes.
- [x] Extend fixtures to unsupported versions, unexpected entries and compressed manifest expansion. Final suite reports 10 passed, including setup/cleanup.

Exit: no failed/invalid load or save can replace accepted records or unreadable on-disk evidence.
