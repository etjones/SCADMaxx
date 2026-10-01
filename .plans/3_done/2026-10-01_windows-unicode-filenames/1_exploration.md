# Fix Windows Unicode filename crashes

The user requested fixing the crash observed in the shared-dependency rebuild, checking upstream PRs first.
Scope: the same experimental composition at `31b1430530c295c4b24662b2d5a4b989bbbabc7d`, using shared vcpkg.
Worktree: `wt-openscad-fix-windows-unicode`, branch `fix/windows-unicode-filenames`, from `openscad-master`.
Evidence: `runs/20261001-unicode-filename-fix/`.

## Upstream findings and cause

- [PR #6136](https://github.com/openscad/openscad/pull/6136), non-ASCII filename fixes, is merged and already in our base.
- [PR #6356](https://github.com/openscad/openscad/pull/6356), Nowide conversions, is also merged.
- Open [PR #6726](https://github.com/openscad/openscad/pull/6726) and
  [PR #6357](https://github.com/openscad/openscad/pull/6357) include a UTF-8 active-code-page application manifest.
  Both contain unrelated changes, so retain only the manifest fix and its attribution.
- Our MSVC build selects `mainCRTStartup`, which supplies arguments in the process ANSI code page. OpenSCAD expects
  UTF-8. A C++ exception occurs on non-ASCII arguments; the current manifest does not opt into UTF-8.
- Applying the upstream manifest to an isolated copy of the failing executable makes the original ö/Chinese
  input and output filename reproducer pass. No source/runtime dependency changes were needed for that probe.

## Implementation and acceptance

Add the focused process UTF-8 declaration to the Windows manifest without changing system/console code pages.
Keep the PR stack unchanged. Add a portable CLI regression test for Latin, Chinese and supplementary Unicode
characters in input/output filenames and directories, including a space and include/use lookup.
Verify failure before the fix and success after it. Rebuild the GUI and tests with shared dependencies; run unit
tests, relevant existing UTF-8 tests, CLI rendering and packaging/extraction checks. Preserve prior deliveries.
Record Windows version support explicitly: activeCodePage UTF-8 requires Windows 10 version 1903 or newer.
