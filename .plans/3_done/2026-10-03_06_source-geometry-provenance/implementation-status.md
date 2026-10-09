# Implementation status

Implementation started on 2026-10-04 in the authorized queue 03 → 05 → 06 → 14 → 04.
03, 05 and 06 are locally complete. All three provenance phases are verified; the queue continues with 14, then 04.

Worktree `D:/openscad/wt-openscad-source-geometry-provenance`, branch `feature/source-geometry-provenance`,
base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Run `D:/openscad/runs/20261004-source-geometry-provenance`.
Prerequisites are the independently verified 02/03 source patches plus the pinned OEP8/Customizer parser inputs.
The reviewed prerequisite working input is frozen at SHA256
`eabea931786ddd7cff86c8787a9fd7bf31a1a6af0efb177185f28570d12ca076`, with individual input identities and
overlap resolutions in the run's `inputs/manifest.json`. The combined baseline passes four echo regressions,
the object/attribute coexistence fixture and 66 native results (52 behavior, 14 setup/cleanup).

Phase 1: exact UTF-8 locations retain file identity through lexer lookahead, token starts through strings/include/use,
and exclusive ends through LF/CRLF. The parser records distinct syntax occurrences without changing effective
assignment semantics. A whole call crossing an include expansion is explicitly unavailable; head/argument ranges
remain known. All nine [source-provenance] cases and all 37 focused CTest cases pass, as do four echo regressions,
the coexistence fixture and the full 66-result native suite. Native evidence:
`native-20261004T010558053Z`. No geometry mapping was accepted before these range checks passed.
Phase 1 feature patch: `cf91f0fd8175c715a7c6da3545f13226a0e63c076da6b55f07badc918625b8a3`;
complete working input: `8df8624f9e161f5e85bec3a7421d145723a8d77aa9543c46af11231467e7a225`.
`phase1-source-evidence.json` binds actual working files and verifies independent patch application.
05, 07, 08, 10, 12, 14 and 15 are excluded. No commits, pushes, promotion or stack changes authorized.

Phase 2: optional session collector, exception-safe invocation frames, actual module definitions and explicit node
creation ownership. Repeated modules, loops and children() retain separate paths. Actual shared Geometry cache hits
and normalized CSG leaves preserve per-instance transforms; mirror, nonuniform/singular frames and subtraction
polarity pass. All 15 provenance cases and 43 focused cases pass, with 66 baseline native results in
`native-20261004T013035066Z`. Phase 2 feature patch: `258afd0435be1e47d24b0fd603e59245e10644e99ef395bf839210f62801ce24`.

Phase 3: window-owned ProvenanceService, Inspector contribution, explicit ancestor/candidate navigation and guarded
02 edit targets. Native tests found and corrected a zero-length module-definition header from a Bison intermediate
action. Actual Inspector buttons now navigate correctly. Published syntax caches are sealed and queued navigation
retains QObject guards. The final extracted package passes all 75 native results (59 behavior, 16 setup/cleanup),
plus seven provenance behaviors at each of DPR 1.5 and 2. Full unit suite: 103 cases, 184 reporter rows, zero errors.
Four parser echo regressions and object/attribute coexistence pass. Seven Unicode exports pass through each launcher.

Final source and runtime are independently bound in `runs/20261004-source-geometry-provenance/verification-evidence.json`,
SHA256 `5de3dbe33a2411d491347542fee5748336497d51727c5f2905bff84897acf09b`.
Final feature patch: `dfc078d2b428df12e5225fa514bd0c6c9d09f45c458a5cbd8f7545032c90ca6c`.
Complete working input: `d05ceecf8601173b7536d5a325436e9b7d5a2c33706fd93c15b9c1f6813db463`.
See [completion notes](5_post-implementation-notes.md) for the public API, evidence and limits. Planning paths are retained;
the local implementation has no commit or selected-stack promotion.
