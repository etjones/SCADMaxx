# Reusable integration repairs

This catalog preserves narrowly scoped repairs discovered during experimental runs. It does not select features.
Existing dirty PR worktrees are not a repair library. Only the individually recorded commits below are candidates.

Integration decisions: [PR 6776 camera input policy](repairs/pr-6776-camera-input-policy.md).
PR behavior approved on 2026-10-02; the recorded checkpoint passed build and tests.
See also the [annotations/navigation composition recipe](repairs/annotations-navigation-composition.md).
For the current language/API stack, see the [OEP8, Customizer and HTTP composition recipe](repairs/oep8-customizer-http-composition.md).
For the newer source-editing/modeling stack, see the [source-first composition recipe](repairs/source-first-composition.md).
For Windows exact-byte insertion fixtures, see [insertion golden line endings](repairs/insertion-golden-line-endings.md).
For surface selection at fractional DPI, see [logical viewport bounds](repairs/selection-fractional-dpi-bounds.md).
Pending local viewport performance fixes: [redraw freshness and camera publication](repairs/viewport-redraw-freshness.md).

| ID | Applies after | Source repository / full commit SHA | Applicability | Verification | State |
| --- | --- | --- | --- | --- | --- |
| windows-executable-name | baseline | openscad-master / three commits through `4c325716b94e444637a80df3966197ce110b2b75` (see recipe) | Required packaging support for SCADMaxx executable names | [Recipe and verification](repairs/windows-executable-name.md) | reusable |
| native-ui-test-fixtures | ui-visual-polish, navigation-cube, annotations, http-agent-server | openscad-master / `bcf48145d9ebc7ffdcde0414ddde38ceb62f0b6a` | Deferred UI relayout and native picker invalidate test assumptions | [Native and standard tests passed](repairs/native-ui-test-fixtures.md) | reusable |
| windows-manifest-dependency | baseline, windows-unicode-codepage | openscad-master / `6486d7660b5370efc08795681c9d0098fa2e8436` | Incremental RC build retains an old embedded manifest | [Manifest, Unicode and standard tests passed](repairs/windows-manifest-dependency.md) | reusable |
| preferences-tab-order-test | pr-6878, ui-visual-polish | openscad-master / `61fb8357ad3101852bb2a12fc40421f047f99e68` | UI test assumes Dialogs precedes AI despite inserted Shortcuts page | [Unit/render tests passed](repairs/preferences-tab-order-test.md) | reusable |
| settings-stream-declarations | baseline | openscad-master / `c577f934adade4b762fba095abbad79a3b13df30` | Missing stream declarations before SettingsEntryList instantiation on MSVC | [Build/test passed](repairs/settings-stream-declarations.md) | reusable |
| windows-gui-test-sleep | baseline | openscad-master / `67884e65f4565c1215a88ecdcd0a2daa122e53d7` | POSIX sleep prevents MSVC GUI-test compilation | [Build/native tests passed](repairs/windows-gui-test-sleep.md) | reusable |
| windows-argument-storage | baseline | openscad-master / `e1a798257aeaabb0f82898e477ef8f5e6fd3558d` | Runtime-sized arrays in wmain rejected by MSVC | [Build/test passed](repairs/windows-argument-storage.md) | reusable |
| cairo-link-target | baseline | openscad-master / `b5ef9f6cedaab8bb5087f82bc223dcbe18328c14` | MSVC Cairo pkg-config branch loses its library path | [Build/test/PDF passed](repairs/cairo-link-target.md) | reusable |
| windows-manifest | baseline | openscad-master / `74168dda7953ebd994e81dab6d22574ed24aef4c` | Resource and MSVC linker both embed manifest ID 1 | [Build/test/manifest passed](repairs/windows-manifest.md) | reusable |
| windows-unicode-codepage | baseline | openscad-master / `e1984cce105bdf8ab1ffb6b0682e0b385edc570b` + test wiring `184b59df756626a7314d21914c677c5046553227` | Windows process code page conflicts with UTF-8 filenames | [Build, Unicode regressions, unit and rendering tests passed](repairs/windows-unicode-codepage.md) | reusable |

Use `baseline` or a selected entry ID for "Applies after". For a multi-entry interaction, list all prerequisites
and apply only after the last is integrated. Use states `candidate`, `reusable`, and `retired`. State describes
evidence, not a guarantee that a repair still applies to future revisions.

For each entry, add a record under `experimental/repairs/<id>.md` using the
[repair template](templates/repair-record.md). Preserve its source commit with a named repair ref or an accessible
repository; do not rely solely on an old worktree remaining present. Include submodule patch sources if applicable.

During a run:

1. Snapshot the catalog and relevant records with the other inputs. Consider only repairs for selected features or
   the recorded baseline/toolchain. Do not apply every catalog entry indiscriminately.
2. Check whether the cause and failing condition still exist. Reproduce the failure or provide specific source
   and toolchain evidence. Record `needed`, `already present`, `obsolete`, or `not applicable` for each considered
   repair. Never silently modify the catalog's applicability based on an assumption.
3. Apply a needed repair as its own commit, retaining the original identity and attribution (for example with
   `cherry-pick -x`). A conflicting or adapted repair needs a documented diff and fresh verification.
4. Build and run the repair's focused regression check. Record the new run's repair SHA and passing checkpoint.
   If a candidate is unsuitable, diagnose a new narrow fix rather than repeatedly applying it unchanged.
5. Catalog new reusable fixes and link their failure logs, verification, and any upstream submission. Updating
   evidence does not authorize posting an upstream PR or message.

Re-evaluate repairs on every fresh run. Do not rewrite old records or delete retained commits merely because a
repair was retired. Environment-only repairs belong in the profile/run evidence and need no empty source commit.
