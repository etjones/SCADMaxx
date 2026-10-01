# Quiet Customizer — requirements

Status: implemented and Windows-verified; see [results](5_post-implementation-notes.md). On the existing
`codex/ui-visual-polish` branch after icon commit `67101788f`.

- Match the accepted quiet Customizer reference using native Qt controls/palette, inherited fonts and existing
  spacing helpers. No QSS, custom chrome, hand-painted header skin or rearrangement of controls/workflows.
- Expanded and collapsed headers share their resting appearance; use the disclosure arrow for expansion state.
  Preserve native hover/press/focus, keyboard toggling, accessible expansion state, Expand/Collapse All and expansion
  during rebuilds. Keep original group identity separate from the displayed label.
- Rename Hide Details to Help Icons, retaining its selector position and making it the initial default. Retain
  Show Details, Inline Details and Description Only unchanged. No new mode persistence or migration is required.
- Help Icons mode hides persistent explanations and shows the shared monochrome question-mark glyph beside labels
  only when a description exists. Full author-provided text appears in a native tooltip on mouse hover only.
  No focus, Tab stop, click action, Enter/Space activation or F1 behavior. Other modes omit redundant help icons.
- Keep parameter controls' existing keyboard behavior and focus order. Help glyphs use native compact icon sizing
  and palette-aware rendering, with enough hover area to target comfortably without enlarging every row.
- Capitalize displayed parameter labels and section headers conservatively. Preserve acronyms/internal casing,
  original variable/group keys, preset names, enumeration values and author descriptions. Continue existing
  underscore-to-space formatting for parameter names; do not introduce camelCase splitting.
  Precisely: uppercase the first cased letter only if the first word has no uppercase letters. Leave all other
  characters unchanged. Thus `show_USB_port` becomes `Show USB port`, while `iPhone` and `showUSBPort` stay intact.
  Use Unicode-aware casing; uncased scripts remain unchanged. Do not normalize author-written section separators.
- Apply sentence case to application-owned Customizer captions (for example Automatic preview and Collapse all)
  through normal translatable strings, not by modifying translated text at runtime. Mode names in these documents
  are identifiers; UI captions use Show details, Inline details, Help icons and Description only. Existing
  translations may require ordinary catalog updates; do not fabricate translations.
- Reuse the completed font hierarchy and native-derived row/group spacing; preserve long-label wrapping and
  explicit Customizer font overrides. Remove the remaining checkbox-indicator stylesheet and use native sizing.
- Preserve all parameter types, values, presets, auto-preview and reset behavior. Editor/Console content, viewport,
  Preferences category layout and other dialog polish remain outside this feature.

Acceptance: meaningful state/identity/mode/focus regression checks plus native light/dark screenshots at simulated
100/125/150/200%, narrow docks, enlarged fonts and live palette changes. Exercise missing/long/multiline descriptions,
all parameter types, group-name capitalization collisions and rebuilds. Report physical DPI and platform limits.

Additional acceptance details: mode changes must preserve edited values and expanded groups without causing a new
preview solely from presentation changes. Native tooltips must preserve literal punctuation, units, line breaks and
angle brackets rather than accidentally interpreting author text as HTML. Whitespace-only descriptions get no icon.
Help icons sit beside the label, not at the far edge of the panel; they must not displace the checkbox or control.
Keep passive descriptive metadata available without introducing any help action or keyboard interaction.
