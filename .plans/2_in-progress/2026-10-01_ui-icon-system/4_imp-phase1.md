# Icon system phase 1 — artwork and coverage

Completed in source commit `258e9c4f3`. Assets and mapping live in `resources/icons/tabler/`.
Pinned Tabler revision/license retained; custom CAD/projection/camera/export/animation symbols use matching SVG paths.
The final map has 83 semantic names, including help and a distinct AI category symbol. Branding and OS chrome excluded.

Native Qt contact sheets and 20/24/28 toolbar comparisons:
`artifacts/ui-visual-polish/2026-10-01/status-icons/contact-light.png` and `contact-dark.png`.
All SVGs rendered successfully. Inspection retained 24 logical pixels and caught/fixed the start/end versus
single-frame-step collision. Capture uses simulated 200% DPI, Segoe UI 10 pt, Qt 6.11.1 Windows11.

Consumer audit: `artifacts/ui-visual-polish/2026-10-01/icon-use-audit.txt`.
Direct compile-result pixmaps, OctoPrint's cached image rendering, dynamic animation icons, input assignment errors,
Preferences images and application-owned QMessageBox paths require integration beyond theme-file replacement.
User content images, color/font drag previews and branding are not replacement icons.

Mode 3 derives hues from native standard-icon saturated pixels; foreground fallback if no tint exists.
Native hues may need brightness adjustment for outline contrast. High-contrast mode keeps system foregrounds.
