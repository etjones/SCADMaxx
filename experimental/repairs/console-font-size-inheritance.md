# Console default font size

2026-10-09: user requested that Console default to application font size, unless an explicit
Console size is selected. Implementation is uncommitted in `D:/openscad/wt-openscad-ui-visual-polish`
on `codex/ui-visual-polish`, based on `d52e03649893fffb487976c36e4e0e028176b701`.

`Preferences::getValue` resolves absent `advanced/consoleFontSize` to the current application size.
Application font changes update existing consoles and the Preferences size selector only while
the size is inherited. Console font family remains independent. Explicit size preferences survive
default-settings cleanup, including values equal to the default. The size selector handles user
activation so reselecting its currently inherited value also records an explicit preference.
Existing Ctrl-wheel zoom remains transient; explicit-size consoles retain that zoom across UI changes.

Changed source: `src/gui/Preferences.{cc,h}` and `src/gui/Typography_test.cc`. Regression coverage
includes live inheritance, independent family, selecting the inherited size, settings reload and
fresh-process/default-cleanup persistence. Existing independent-font tests now explicitly select
an independent Console size. No build or tests were run, and no commit, merge, push or new package
was made. Existing branding/title and Clipper2 working changes are preserved.

The delivered `62b78cb87` executable is unchanged. Commit and merge this owner change normally when
requested; no copies into downstream branches or cherry-picks. Previous readiness/validation pins
still describe their recorded committed revision, not this pending change.

## Requested integration/build, 2026-10-09

Committed locally in the owner and merged normally into `f4f87a8eea11172037c459dd5ae9848b566fd044`, with prerequisite closure updated. See [run evidence](../../../runs/scadmaxx-all-features-2026-10-09_19-45/report.md). Incremental build, everyday (516 unit case rows), tool checks and extracted package checks passed. New native initial-open cases were not compiled/run in the release configuration; desktop validation remains pending. Quick performance comparison was interrupted twice by an unrelated artcraft-hub linker and remains incomplete. No push/promotion or full-validation tag. Hierarchy/integration test conflicts are resolved by retaining both independent sets of includes and slots.
