# Local checkpoints, 2026-10-05

The user requested grouped commits across all worktrees. Full before/after inventory and commit ledger:
`D:/openscad/runs/20261005-commit-all-worktrees/`. No push or new integrated build was performed.
Only generated Clipper2 version-header changes and two HTTP Python bytecode caches remain uncommitted.
The enabled PR stack and existing promoted readiness remain unchanged.

## Selected feature follow-ups awaiting promotion

| Source | New local head | Observed Dropbox head |
| --- | --- | --- |
| UI visual polish | `2217d2c7d54743c93cefb9418b208825168ddc1c` | `8f5b3ae4707a8718db28722deb2fd723fd9415ab` |
| Navigation cube | `6b42cbf3f95bfe1ad2ff4b845a6dc20f4ed336fe` | `bfd009ef0047452c09e3629d0af25efd6af34700` |
| PR 6642 local variant | `1dad283e17be06380f2ff6b23daca68719d1f70c` | `41d92671b6040959caa036a886be1f245bc32f5f` |

These are fast-forward descendants, but commits alone do not change the declared Dropbox inputs.
Promotion requires the explicit authorization described in the update-and-build runbook. After promotion,
verify the exact remote IDs and reconcile validation evidence before updating readiness for the new heads.
The `localHead` fields record availability, not promoted/validated status. PR 6642's prior validated head
predates its already-promoted documentation commit; do not confuse that with divergence.

- UI: four follow-up commits include toolbar icon refresh, Customizer help, Preview/Render artwork and optical
  toolbar weight. Prior measurement/help tests passed 77,593 assertions; final optical assets rendered through
  Qt at four DPI scales. A full application relink with the latest assets remains integration work.
- Navigation: close-on-second-click fix, tested with all 15 native navigation checks passing.
- PR 6642: empty-group visibility restoration plus a standalone Qt regression fixture; the fixture explicitly
  excludes ParameterWidget's preset/dependency integration, which requires composed-build acceptance.

Keep the existing delta bases and dependency ordering. The three entries use `latest`, so properly promoted
heads can be selected without changing their stack revisions. The eleven pinned source-first feature owners
were already clean; their selected revisions did not change.

## Other retained work

PR 6776/6999 and openscad-6991 contain distinct header experiments, PR 6871 contains stack/trace changes,
and the evaluation-performance branch is a benchmarked experiment. These remain unselected. The selected
PR 6776 row still fetches GitHub's PR, not our local variant. Do not substitute it implicitly.
The anchors, insertion and semantic verification branches now have aggregate checkpoint commits, not new
feature deltas. README capture branches and issue 5425 fixtures were also committed separately.

Control commits retain the launcher redesign/versioned packaging, source-first skill, stable delivery and
companion pipeline, repair catalog, benchmark tools, plans and workspace records. Build-tool tests pass
(19 checks); launcher version parsing/validation/read-only checks pass. No version bump, full rebuild or
fresh feature acceptance was performed during this commit-only pass. Existing whitespace issues were
recorded in the run rather than silently editing checkpoint source or plan answer markers.

The control main branch is also ahead of its Dropbox origin. Its current checkout supplies local build
controls; promotion of control history is separate from source-feature promotion. Keep the selected skill
companion's declared source/boundary distinct from these local control commits.
