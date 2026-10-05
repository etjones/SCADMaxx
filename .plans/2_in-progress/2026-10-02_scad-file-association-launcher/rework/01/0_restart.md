# Restart: file-type-owned sources and automatic selection

Trigger: the user requested a consolidated redesign after discussing latest-build resolution and a global chooser.
The original global library duplicates setup and cannot express independent source/executable filters per file type.
Baseline control HEAD: 3c0f893a61219be4d1de2067d68179ff8e40ace9. Original launcher commit: eb86b2c.
Retain: visual language, Windows registration/startup, safe process arguments, atomic settings, manager locking,
version.xml and PowerShell packaging work, shared icon, and independent-installation requirements in PACKAGING.md.
Replace: global mappings/builds/folders schema, global discovery UI, dispatch resolution, affected tests.
No Git rollback/reset: replace only launcher files. Keep unrelated edits and the prior plans; snapshot old source
under D:/openscad/runs/scadmaxx-launcher/rework-01-before. Existing schema-1 settings remain untouched; no migration
is authorized by repository instructions. Explain unsupported settings and provide explicit backup/start-fresh UX.
No commits requested. Version remains 0.1.0. Installer/public distribution work remains a separate follow-up.
Lessons: source ownership, latest semantics, and fixed-vs-rebuilt-path distinctions must be explicit and testable.
