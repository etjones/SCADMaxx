# Repair: windows-unicode-codepage

- State: reusable; full Release build, failing/passing Unicode regressions, unit and portable runtime checks passed.
- Failure: MSVC CLI exits -1073740791 for non-ASCII filenames; ASCII control succeeds.
- Applies after: baseline, independently of the selected feature PRs; Windows 10 1903+.
- Source repository: `D:/openscad/openscad-master`.
- Repair: `e1984cce105bdf8ab1ffb6b0682e0b385edc570b`.
- Test wiring follow-up: `184b59df756626a7314d21914c677c5046553227`.
- Retained ref: `refs/experimental-repairs/windows-unicode-codepage` (first commit).
- Origin: UTF-8 manifest declaration from nomike's open PR #6726, head
  `b98bca8339a4ac3e87d7981754c5f4e4fd465798`; also present in open PR #6357.
- Upstream PR: https://github.com/openscad/openscad/pull/6726
- Affected base: `31b1430530c295c4b24662b2d5a4b989bbbabc7d`, MSVC 19.51, Windows 11 host.
- Applicability: process manifest lacks activeCodePage UTF-8 and the filename regression fails.
- Application: cherry-pick the repair and test wiring follow-up with `-x`, after checking applicability.
- Touched files: `scripts/winmanifest.xml`, `tests/CMakeLists.txt`, `tests/test_unicode_filenames.py`.
- Regression: `unicode_filenames` CTest, also run directly against staged `.exe` and `.com` binaries.
- Evidence: `runs/20261001-unicode-filename-fix/report.md` and its original upstream API snapshots.

Verified on Windows 11 build 26200 with shared dependencies unchanged. All seven new test cases pass against the
rebuilt `.exe` and `.com`; the old executable fails all six Unicode cases. Existing UTF-8 AST, echo and CSG tests
also change from failing to passing. Catch2 passes 119 cases (75,145 assertions), and Manifold/CGAL STL, PDF and
PNG preview checks pass. The existing shortcut/palette widget checks were rerun successfully against this source.

Only the UTF-8 process declaration is taken from the PR; no stack exception handlers, console changes or unrelated
MSVC changes are included. The active code page declaration is ignored on Windows versions older than 10 1903;
this repair does not claim support there and does not alter machine-wide settings.
