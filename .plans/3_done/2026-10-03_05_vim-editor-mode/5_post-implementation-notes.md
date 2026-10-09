# Vim editor mode: local completion, 2026-10-04

The default-off, globally persisted Editor preference enables a bounded Normal/Insert/Visual character/Visual line
mode in each source editor. Counts, Unicode-aware motions, operator/text-object edits, unnamed register, paste,
native undo/redo, relative insertion journal and dot repeat are implemented. Literal case-sensitive wrap search
and the explicitly permitted save/open/close/reload commands have a document-local prompt and mode indicator.
Unsupported Normal edits are consumed with feedback; unrelated application shortcuts and other fields retain
their established behavior. The command reference is `src/gui/vim/engine/CommandRunner.cc` and
`doc/vim-editor-mode.md`, with conformance tests under the same engine directory.

## Source and dependency boundaries

Worktree `D:/openscad/wt-openscad-vim-editor-mode`, branch `feature/vim-editor-mode`, base and unchanged HEAD
`6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Run `D:/openscad/runs/20261004-vim-editor-mode`.
02's actual `prepareExternalEdit()`/synchronous `externalEditStarting` API closes insertion before the caller's
UndoGroup and invalidates the native insertion journal. Annotation container actions remain in native undo.
Selected shortcuts #6878 head `3014fb55405759bfa1871e79f50cbee4c2a2c638`, retained adaptation
`0fb6e6591ec3bbc55b6b45e4432478c67fe9853b`, is included as a prerequisite. The frozen manifest records all
three verified 02 patch hashes and the shortcuts delta. Its canonical prerequisite working input SHA256 is
`30446397d82fbb722520f932906990bca59c611efc54f2873c560069c73467f6`.

Geany vimode is pinned at `8d1838869cfdebbeb8469193119839f7ffae0052`, source archive SHA256
`26cb78f4e2d19645e8f28669ea0329ad94b9623abd0590bdc50deb01dcc76257`. Selected engine families were inspected
and substantially adapted to C++, Qt and pointer-sized Scintilla messages. This is not a claim of compiling
unchanged Geany code. `ORIGIN.md` maps the retained command/motion/edit/context/utility families and adaptations;
their author notices and GPL-2.0-or-later license are retained in source and extracted runtime notices.
GTK, GDK, GLib and Geany/viw adapters are excluded from the eleven-file engine compile/import closure.
The existing application already uses GLib: its imports and toolkit runtime additions match feature 03, with
`addedVsFeature03: []`. Shared vcpkg package status is unchanged at
`2983caf4494a3428f029553e921a862000477e8e1266a8b74846acde80c7c2e1`.

No named registers, macros, broad Ex commands, Replace/Visual block, substitutions or folding commands were added.
Generation is bounded to 64 MiB with atomic refusal. Literal search uses `SCFIND_MATCHCASE`: Scintilla flags zero
means case-insensitive, so the planned zero-flags spelling was corrected to preserve the requested behavior.
The installed Win64 QScintilla API required `SendScintillaPtrResult` for direct-function pointers; `long` would truncate.

## Native integration and corrections

Native shortcut override runs before QActions. Tests prove Vim wins Ctrl+R and printable bindings while enabled,
then the real application Ctrl+R action resumes on disable. Completion/calltip Escape, completion acceptance,
IME/non-BMP text, AltGr, native paste, tab/window switches, prompt cancellation and source transactions are covered.
Modal save/close/reload callbacks capture their originating editor and revalidate it after each dialog; switching
tabs does not redirect the operation. A native test exposed destruction of a prompt during its Return handler;
Ex dispatch now uses a guarded queued callback, preventing that lifetime fault. Save cancellation, conflicts,
failed writes, dirty reload, Unicode paths, read-only state and an origin closing during Save As pass.
The fixture waits for main-window activation after modal closure before sending shortcuts. The test uses the
real disabled-mode action instead of adding a second ambiguous Ctrl+R QAction. Failed attempts remain in the run.

Vim reference fixtures from the already installed executable establish cw/cc, counted insertion/open-line and
missing-final-EOL line operations. LF/CRLF, escaped/nested objects, logical folded lines, Unicode boundaries,
large insertion replay, visual-line repeat and autoindent are verified. Preferences preserve dirty source,
revision and native history. Fresh-process tests apply the actual enabled INI and the untouched default-off state.

## Verification and exact handoff

Windows Release profile: MSVC toolset 14.51.36231, SDK 10.0.26100.0, Qt 6.11.1, QScintilla 2.14.1,
shared existing vcpkg. Phase source snapshots and independent feature-patch application checks passed.
Final `final-v2-source-evidence.json` identifies 73 files, including 44 feature files; the base SHA alone does not
identify this uncommitted build. Generated Clipper2 version header bytes used for compilation are retained, and
the original checked-out header was restored after the last build. Whitespace check passes.

- 20 unique engine cases cover VC01–VC17 and boundary/atomicity regressions. CTest executes these in two actual
  targets plus seven foundation cases: all 47 discovered focused executions pass.
- Complete unit discovery contains 87 cases; JUnit contains 209 section/generator rows with zero failures/errors.
  Reporter assertion totals are not presented as additional independent test cases.
- Final clean-PATH extracted runtime `native-20261004T001724254Z`: all 61 QtTest results pass, consisting of
  47 behavior and 14 setup/cleanup results across seven classes. The screenshot confirms the native mode row.
- Enabled/default restart directories `native-20261004T001821016Z` and `native-20261004T001823443Z` each pass
  one behavior plus setup/cleanup. Seven real Unicode export cases pass through each extracted launcher.

Final feature patch `final-v2-feature.patch`: SHA256
`05946cc5b49ba36b979fe556298299213298e360a82408c936a05c7f5955c724`.
Complete working input `final-v2-complete-input.patch`: SHA256
`bb6cbc33ee0d84b747525f93e6e268e380dfde0067f16f186a9aa640106ae4bd`.
`verification-evidence.json`: SHA256 `bd14903630581650c68c97aaa73df488376c0b2617a7a87a34a9b6015630e9f3`.
Final application SHA256 `0f8765f89c7cf6b41de1125b07ccaacb3c9122b483d8f355a6d0263674bf7f6c`;
console launcher `3f46d0f4acfd00cf4a4a71e041eed654317c8e2f720dc8416a16807f3d8adf8a`.
Feature verification ZIP `portable-verification-v3.zip`: SHA256
`287c9480164a87da3ca1d9f20ba73cb0805a4317b79047285098a22121580c5a`.

Existing Windows machine and Qt 6 are verified; clean-machine portability and other profiles are not claimed.
This is a local feature verification package, not a selected-stack release. The later selected navigation head
remains a future composition obligation. No commit, push, promotion or enabled-stack change was performed.
Next authorized work is 06, followed by 14 and 04.


## Lifecycle closure — 2026-10-07

Moved to done at the user's request. Existing verification evidence and historical limits are preserved.
