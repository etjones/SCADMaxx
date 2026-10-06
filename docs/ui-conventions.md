# UI conventions

## Help icon

When the user says "help icon", use the Customizer's circled-question-mark icon and interaction.
Do not substitute a platform-standard help button, a text question mark, or a newly drawn symbol.

- Artwork: `resources/icons/tabler/stock/help-circle.svg`, mapped to `help` in the UI-polish
  checkout's `resources/icons/tabler/mapping.json`. Preserve the adjacent Tabler MIT license.
- Reference implementation: `ParameterDescriptionWidget` in
  `D:/openscad/wt-openscad-ui-visual-polish/src/gui/parameter/ParameterVirtualWidget.cc`.
- Use `Icons::setLabelIcon(..., "help", ...)` where the shared icon library is present.
  Size with the style's small-icon metric, use the theme foreground color, and keep the background transparent.
- Display the explanatory text as a native, wrapping tooltip on hover (250 ms delay) or click.
  Hide it on leaving or hiding the icon. Provide an accessible name and description.
- Keep it visually lightweight and beside the control or group it explains.

The standalone Cross sections branch embeds the same unmodified SVG and uses a small local tooltip button
because it does not depend on UI polish. This does not introduce a UI-polish ancestry dependency or copy its
icon framework. When composing branches, preserve the identical artwork and theme-aware rendering.
