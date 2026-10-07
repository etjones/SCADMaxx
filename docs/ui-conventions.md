# UI conventions

## Qt drawing and Customizer section surfaces

Qt palette roles are semantic inputs to a style, not an inventory of all colors rendered by Windows.
The style can derive brushes from those inputs; there need not be a dedicated pale accent palette role.
See [Qt style drawing](https://doc.qt.io/qt-6/style-drawing.html).

For Customizer disclosure headers, use the existing `GroupWidget` with its dedicated `GroupDisclosureButton`:

- Blend the current `Window` color with `Accent`: 10% accent at rest, 16% on hover, 22% while pressed.
  Press takes precedence over hover. Expanded and collapsed headers use the same resting surface.
- Recompute from the style option's current palette each paint. Never cache a light-mode RGB value or
  install the blend on the widget/application palette. Child controls retain their own semantic colors.
- Set only the temporary option's `Button` brush, then draw `CC_ToolButton` through `QStylePainter`.
  Retain native borders, arrow, text, focus, metrics, keyboard activation and accessible disclosure state.
- Keep the button non-checkable: an expanded group is not a selected item. Leave the content area untinted.
- Use native drawing without tint for disabled controls and the platform's high-contrast preference.
  The implementation uses the current Qt 6.11.1 toolchain (accessibility hints require Qt 6.10).

This localized surface treatment was approved on 2026-10-07. It is not a global palette or stylesheet change.
The previous checkable toolbutton received a strong checked/accent fill from the Windows 11 style;
removing checkability removed that fill but made the section header too neutral.

Qt's Windows 11 `controlFillBrush()` honors an explicit `Button` brush before its own state fills, so the
custom control must supply its hover and press colors as well. Other styles decide how they consume roles;
do not assume this produces identical pixels across all platforms.

References (also kept beside `GroupDisclosureButton::paintEvent` in the source):

- [QWidget palette semantics](https://doc.qt.io/qt-6/qwidget.html#palette-prop)
- [Live color scheme and palette updates](https://doc.qt.io/qt-6/qstylehints.html#colorScheme-prop)
- [QStylePainter complex controls](https://doc.qt.io/qt-6/qstylepainter.html#drawComplexControl)
- [Platform contrast preference](https://doc.qt.io/qt-6/qaccessibilityhints.html#contrastPreference-prop)
- [Qt 6.11.1 Windows 11 style source](https://github.com/qt/qtbase/blob/v6.11.1/src/plugins/styles/modernwindows/qwindows11style.cpp)

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
