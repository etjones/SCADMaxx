# Phase 1 — native Preferences categories

Implemented in `677442341`. QTabBar occupies the existing category location and reuses category actions and icons.
Native selection, focus and scrolling replace the checked toolbar tile. Action/page synchronization and conditional
category removal are covered by focused tests. The final audit corrects presentation order independently of page
registration order and adds a regression against the original toolbar action order.

Evidence: `artifacts/ui-visual-polish/2026-10-01/dialogs-phase1-final-build.log` and
`dialogs-phase1-tests.xml`. Both passed. Final native screenshots supersede intermediate captures.
