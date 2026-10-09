# Coordinated UI implementation

The user authorized implementation, both builds, necessary pushes and the README screenshot audit.
UI polish owns shared dock titles, palette surfaces, Preferences layout and category feedback.
PR #6878 is maintained on feature/shortcut-presets; presets merge normally into UI polish,
Vim, cross sections and insertion. No integration history is merged back into owners.

Standalone composition: wt-openscad-ui-consistency-build / codex/ui-consistency-build.
Full integration: wt-scadmaxx-20261006 / scadmaxx-20261006, source
659f5abf0e8959bc03c62155b436b1b6b44a8aca. Existing integration cache is reused.
Exact 24-input composition, checks and delivery are in
../../../../runs/scadmaxx-all-features-2026-10-09_22-34/report.md.

Focused native surface and preset checks pass. Ordinary integrated correctness passes.
The tools profile's descendant-timeout cleanup test failed once with a Windows sharing violation;
all 19 focused harness checks pass on retry. Performance evidence was interrupted by an unrelated
link.exe process; do not call it a successful speed comparison. Desktop and package evidence follows
in the run report. Preserve existing owner branding and concurrent control research edits.

Native startup inspection found the existing Dock visibility path restored a default Qt title.
Owner 08b0f6e repairs it and adds a regression against the real Dock class. It was normally merged
into both builds. Five feature inputs and the integration were pushed and verified in Dropbox and
GitHub; exact revisions are recorded in the run publication manifest. The initial 29c325d package
is superseded and retained as a checkpoint.

Presets retain alternative bindings, explicit unbound actions and unknown optional-action entries;
new actions use defaults. Invalid/conflicting imports are rejected before activating anything.
Import stores a named preset; Load activates it. Active binding changes continue to persist automatically.
Saved sets and exports use portable JSON and atomic QSaveFile writes.
