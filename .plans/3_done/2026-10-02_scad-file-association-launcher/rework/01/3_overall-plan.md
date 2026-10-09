# Implementation plan

1. Core: replace schema with FileType/BuildSource/Selection; strict persistence and extension lookup. Retain OS helpers.
2. Resolver: shallow source enumeration, exclusions, canonical deduplication, metadata cache, comparators and reasons.
3. UI: type editor with direct source creation and review, fixed/latest controls, main summary, tray shortcuts, chooser.
   Retain existing visual treatment and one-manager IPC. Batch dispatch scans each needed type once off the GUI thread.
4. Verification: core fixtures for scope, filters, cache changes, ordering, isolation, schema and real Unicode dispatch;
   UI smoke for editing/save/revert, chooser accept/cancel, tray toggle and fixed/latest choices. Rebuild/deploy to the
   existing local launcher location and inspect native UI and icon. Keep full installer validation separate.
5. Record results and limitations in 5_post-implementation-notes.md, leave changes uncommitted for user review.
