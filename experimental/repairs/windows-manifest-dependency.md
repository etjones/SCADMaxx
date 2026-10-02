# Repair: track embedded Windows manifest changes

- State: reusable; first repair passed the manifest check, fourteen filename cases and standard tests.
- Applies after: Windows baseline; required with the Unicode manifest repair for incremental builds.
- Source commit: `6486d7660b5370efc08795681c9d0098fa2e8436` in `D:/openscad/openscad-master`; retained ref
  `refs/experimental-repairs/windows-manifest-dependency` in the private source origin.
- Failure: ASCII filename export passes, Unicode cases fail even though `scripts/winmanifest.xml`
  declares UTF-8. `mt.exe` extraction proves the executable still embeds the old manifest.
- Cause: Ninja's resource compiler dependency scan lists included headers, but not the manifest
  referenced as resource data by the generated `openscad_win32.rc`.
- Repair: add `OBJECT_DEPENDS` on the source manifest to `WINDOWS_RESOURCE_PATH` in CMake.
  Do not merely delete the resource object: that hides the problem on the next incremental update.
- Replay: check whether this explicit dependency exists; if absent, cherry-pick the repair with `-x`.
  Reconfigure and build. Extract resource `#1` with the Windows SDK manifest tool and check UTF-8.
  Run all seven Unicode filename cases against both `.exe` and `.com`, plus the ordinary Test step.
- Evidence: run `20261001-scadmaxx-all-features`, `feature-checks/embedded-manifest-before.xml`
  and `feature-checks/unicode-exe/run-iwvpbn8a/results.json`. First repair attempt is recorded in report.md.
- Passing evidence: `feature-checks/embedded-manifest-after.xml`,
  `feature-checks/unicode-repair1-exe`, `feature-checks/unicode-repair1-com`,
  and `logs/20261002T090236043Z-test.json` in the same run.
