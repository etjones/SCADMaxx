# Phase 3 — remaining application-owned surfaces

Implemented in `2e41da9f1`. Removed residual Qt stylesheets from Welcome, AI controls/bubbles, input indicators,
search fields and color controls. Native roles, fonts, frames and metrics replace the presentation overrides.
About paragraphs inherit the application font. Library information uses literal text with modest label emphasis.
Welcome retains its logo/wordmark; native Window background replaces the decorative stylesheet wave.
Swatch colors and AI diff syntax colors remain content. Input readouts retain numeric and dead-zone information.

An initial regression changed swatch size when selected. Explicit zero QLabel indentation plus compensating native
frame/margin widths keep size stable. The focused test caught the problem and passed after correction.

Evidence under `artifacts/ui-visual-polish/2026-10-01/`:

- `dialogs-phase3-fixed-build.log`: full executable and unit-test build passed.
- `dialogs-phase3-fixed-tests.xml`: focused dialog/foundation/icon/Customizer regression passed.
- `dialogs-phase3-native/light-1` and `dark-1`: native captures passed and representative surfaces inspected.
- Source audit found no remaining `setStyleSheet()` calls or Designer stylesheet properties under `src/gui`.

Native offline fixtures cover optional AI and print authorization without credentials or network requests.
Final-phase captures include the final source and broaden scale/state coverage.
