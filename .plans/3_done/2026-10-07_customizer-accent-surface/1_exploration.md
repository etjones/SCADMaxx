# Customizer accent surface — accepted follow-up

Status: implemented, validated and privately promoted. See `5_post-implementation-notes.md` for final evidence.
The scope and initial authorization record below are retained as history.

The user approved implementation on 2026-10-07 after reviewing real Qt 6.11.1 Windows 11 style previews
in light and dark mode. This is a bounded fix forward to the completed
`../../3_done/2026-10-01_ui-customizer-polish/` work; its historical acceptance remains historical.

The neutral disclosure headers blend into the dialog. Restore gentle separation using a palette-derived
accent tint: 10% at rest, 16% hover, 22% pressed. Keep expanded/collapsed resting surfaces identical.
Retain the native drawing of borders, labels, disclosure arrows and focus, plus existing accessibility.
Keep dark mode and live palette changes; use the native surface for disabled/high-contrast controls.
Record Qt's drawing guidance and links in both source comments and `docs/ui-conventions.md`.

Implement a dedicated QToolButton subclass within the existing GroupWidget, supplying a temporary
style-option Button brush. Preserve the content area's ordinary background. No QSS or global palette changes.
Use the maintained Qt toolchain directly, without an older-Qt compatibility path.

Approved reference images:
`C:/Users/Roel/.codex/visualizations/2026/10/07/01a1161c-00a8-7d51-9a46-c14fe5296897/customizer-tint-light.png`
and `customizer-tint-dark.png` in the same directory. These are prototype evidence, not a source-build check.

Implementation is authorized. Builds/tests were not requested and must not run under workspace instructions.
Pending verification when authorized: real Customizer resting/hover/press/focus, expansion, disabled state,
light/dark and live switching, accent changes, high contrast and DPI scaling. Historical test results do not
validate this new implementation. This independent follow-up has no unfinished prerequisite.
