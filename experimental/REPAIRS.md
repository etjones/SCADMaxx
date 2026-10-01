# Reusable integration repairs

This catalog preserves narrowly scoped repairs discovered during experimental runs. It does not select features.
Existing dirty PR worktrees are not a repair library. Only the individually recorded commits below are candidates.

| ID | Applies after | Source repository / full commit SHA | Applicability | Verification | State |
| --- | --- | --- | --- | --- | --- |
| settings-stream-declarations | baseline | openscad-master / `c577f934adade4b762fba095abbad79a3b13df30` | Missing stream declarations before SettingsEntryList instantiation on MSVC | [Build/test passed](repairs/settings-stream-declarations.md) | reusable |
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
