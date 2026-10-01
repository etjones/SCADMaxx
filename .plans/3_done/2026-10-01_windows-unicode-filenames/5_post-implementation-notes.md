# Windows Unicode filename repair

Implemented in `wt-openscad-fix-windows-unicode`, branch `fix/windows-unicode-filenames`, based on the exact
previous experimental composition. Source commits: `e1984cce105bdf8ab1ffb6b0682e0b385edc570b` and
`184b59df756626a7314d21914c677c5046553227`. The checkout is clean and submodule revisions match.

The requested upstream search found open PRs #6726 and #6357 containing the relevant process UTF-8 manifest fix.
The earlier filename PR #6136 is merged and already present. Applied only the UTF-8 declaration, with attribution
to nomike. The manually selected PR stack remains #6878 and #6776; no upstream PR or message was created.

The MSVC target uses `mainCRTStartup`, supplying narrow arguments in the process code page. OpenSCAD expects
UTF-8. The per-process manifest declaration resolves this mismatch without changing machine or console settings.
Windows supports this declaration starting with Windows 10 version 1903; older versions are not claimed fixed.

The new seven-case regression covers ASCII, Latin, Chinese, supplementary characters, Unicode directories with
spaces, combined input/output paths, and include/use lookup. It verifies successful exit, no warnings/errors, and
identical valid STL geometry. The old executable fails all six Unicode cases; a manifest-only binary probe and
the source-built executable pass. The console launcher passes too. Existing UTF-8 AST, echo and CSG tests also
change from failing to passing.

Full Release build, 119 unit-test cases (75,145 assertions), CGAL/Manifold STL, PDF, PNG preview and the isolated
shortcut/palette tests pass. Both staged launchers pass all seven regression cases with only Windows directories
on PATH and external Qt plugin paths cleared. The shared vcpkg dependency records are unchanged; no dependency
install or rebuild was performed. The PNG preview was visually inspected.

Delivery and fresh extraction evidence: [run report](../../../runs/20261001-unicode-filename-fix/report.md).
The repair catalog records applicability, exact commits and retained provenance for future experimental runs.
Desktop theme switching, full-process shortcut persistence and clean-machine portability remain the existing
experimental-profile limitations, outside this filename repair.

Follow-up choices: **fix forward** for small corrections; **replan** to change implementation strategy;
**restart** to revisit requirements; **supersede** to replace this work with a new feature.
