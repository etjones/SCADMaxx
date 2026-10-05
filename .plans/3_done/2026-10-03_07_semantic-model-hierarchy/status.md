# Current implementation state

Locally complete, all six phases accepted, 2026-10-04. Accepted requirements and phases remain authoritative.
Worktree `D:/openscad/wt-openscad-semantic-model-hierarchy`, branch `feature/semantic-model-hierarchy`.
Run `D:/openscad/runs/20261004-semantic-hierarchy`.

Retained native base `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1` is deliberately selected to match verified owner
inputs. 06 complete input and 14 feature delta are hash checked; six shared merge seams preserve both APIs.
Prerequisite-only working patch `386e30092a30f76a469e04e94cebe91ab012dfe25e4977ff3d1ba8aaba46185f` applies independently.
No semantic implementation was included in that snapshot. The prerequisite build, 57 focused foundation cases and
four parser/import regressions pass. Phase 1 now adds annotation grammar, inert template discovery, typed native call
validation and exact declaration spans. Bison retains zero unresolved conflicts. The Release CLI/GUI/unit build,
65 focused cases (eight new semantic cases plus 57 prerequisite cases) and four parser/import regressions pass.
Phase 1 source is frozen separately in the run. Phase 2 adds session-owned instance frames, native parameter binding
observation, geometry partition and the independently tested scope/placement extension hooks before UI work.
The phase 2 Release build and 80 focused cases pass. Feature-only checkpoint
`7acc8cb874f3c3763505a89864a7f40ac6847692af174843e87ea7e34400a6c5` excludes the separately retained 06 hook
`76ba2b8417e8e474c14e374ae21becf9404c77fe38e5ef9433fdd1f4b93ff80d`. Native GUI/default-job pass dispatch will also
be exercised by the downstream target/native checks before 07 completion. Phase 3 begins with captured default jobs,
shared native execution serialization and generic captured-AST seeding recorded as a separate 03 owner follow-up.

Owner worktrees and unrelated controls remain occupied and unchanged. No commits, promotion or release authorized.

Phases 3/4 are retained together in `phase4-feature.patch`, SHA256
`665acb2993b8377e773c401f398f549fc077e4f10e8791f7fff9f5b809a87153`.
The native Release build, 98 focused tests and actual semantic desktop suite (9/9) pass. Independent foundation
desktop reruns pass: Selection 18/18, Provenance 9/9 and Design 9/9. Early native selector attempts and the failing
worker-stack attempt remain recorded and are not counted as semantic passes. Separate generic owner follow-ups
cover captured jobs, per-thread recursion detection and syntax-site navigation; their identities are in the run manifest.
Phase 5 adds native-span literal edits and guarded Customizer controls. Its first Release build and 106 focused tests
pass, including seven semantic source-edit cases and the generic transaction context recheck. Extended desktop
parameter/undo/owner/window-close checks are running; phase 5 acceptance is not yet complete.

Phase 5 acceptance now passes: extended semantic desktop 14/14, including native boolean/string/vector controls,
unchanged double precision, global Customizer refresh, annotation undo interleaving, explicit library edits and
late window-close jobs. Earlier compile/test fixture failures remain recorded. Phase 5 feature patch is
`555f4cc75b97856c0073a2f63cc2e8416d62e18991c0b03a1a30131be8c38383`.
Full unit discovery has 172 cases; the passing JUnit report has 253 rows, zero failures/errors. The full-process
unsupported-domain fixture needed a separate 14 test follow-up, now retained independently. Four parser/import
regressions pass. Extracted full desktop and DPI checks, both Unicode launchers and shader/package checks pass.
Real 04/05/#6878 composition passes its Release build, 130 focused tests and 128 native rows with zero failures/skips.
The separate 04 test follow-up fixes priority collisions and waits for actual asynchronous readiness; owner worktrees
are unchanged. Final evidence SHA-256 `16425437e06b6f8fb1429c3d71dcf27ee93ceabee797340a48c22c41ceec7a31`.
See 5_post-implementation-notes.md for the exact local handoff. The 11 → 07 → 08 → 12 queue is locally complete.
No promotion or release.
