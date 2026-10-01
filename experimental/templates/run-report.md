# Experimental Windows run: <run-id>

Status: preparing | integrating | failed | blocked | verified-local
Publication: not configured | pending | published | failed
Started (UTC):
Finished (UTC):
Requested scope:
Profile status: establishing | previously verified (reference) | verified this run

## Locked inputs

- PR stack snapshot path and SHA-256:
- Control repository commit (or not initialized) / dirty state / complete control snapshot and hashes:
- Repair catalog and record snapshot / profile and script snapshot:
- Upstream repository / master SHA:
- Integration branch / worktree:
- Toolchain/dependency versions and submodule SHAs:
- Build profile / exact commands / environment record:
- Build/cache directory ownership / compatibility fingerprint:
- Baseline outcome / log / repair commits:

| Order / ID | Kind / source repository and ref | Locked head / delta base | Dependencies | Source diff / commits record | Integration commit | Passing checkpoint | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |

For each entry record its PR URL if applicable, original PR head for variants, retained run refs, source-worktree
dirty state excluded from inputs, source authors, patch checksum, and already-present or residual-change evidence.

## Repair decisions

| Repair ID / applies after | Original source commit | Applicability evidence / decision | Applied or adapted commit | Verification / checkpoint |
| --- | --- | --- | --- | --- |

Include baseline repairs and uncataloged new fixes. Link new reusable repairs back to their catalog records.

## Attempts and evidence

| Step | Source SHA | Command/log path | Exit code | Diagnosis and action | Verification |
| --- | --- | --- | --- | --- | --- |

Record exact patch application commands and conflict resolutions, including their effect on earlier entries.
Never leave an omitted entry unexplained. Record the checks made before resuming an interrupted run.

## Final validation

- Final source SHA / source and submodule cleanliness:
- Configure and GUI Release build:
- Automated tests:
- CLI render:
- GUI startup, preview, and render:
- Included feature/PR behavior checks and affected earlier-feature regressions:
- ZIP extraction smoke check / runtime environment:
- Known limitations:
- Experimental identity observed in the running application:
- Profile verification result / reproducible scripts and evidence:

## Deliverables

| Artifact | Local path | SHA-256 | Size | Published URL (if any) |
| --- | --- | --- | --- | --- |

- Matching source and build/repair material:
- Build-info and notices:
- Release notes / control snapshot included with evidence:
- Retained source tag / tag object SHA / target commit (only after validation):
- Upload verification:
- Remaining blockers / recommended next action:
