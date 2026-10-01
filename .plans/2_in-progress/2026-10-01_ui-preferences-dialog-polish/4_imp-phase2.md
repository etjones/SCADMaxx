# Phase 2 — Preferences hierarchy and spacing

Implemented in `33f734dd7`. Preferences uses native layout gaps/margins, flat native groups on Advanced and Dialogs,
content-driven Dialogs group sizing, and medium AI heading weight that inherits the application font family/size.
Other native framed groups remain intact. No setting, control order or page content was changed.

Evidence: `artifacts/ui-visual-polish/2026-10-01/dialogs-phase2-final-build.log` and
`dialogs-phase2-tests.xml`. Both passed, including live enlarged-font metrics and unchanged editor font settings.
