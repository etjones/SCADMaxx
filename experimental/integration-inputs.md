# Integration inputs and dependency ancestry

The enabled table in [PR_STACK.md](PR_STACK.md) selects product features. The reviewed dependency graph is
[DEPENDENCIES.json](DEPENDENCIES.json); repositories, readiness and historical validation live in
[SOURCES.json](SOURCES.json). Read [feature ancestry](../docs/feature-ancestry.md) before feature maintenance.

This contract supersedes the old patch-application wording in `scripts/README.md`. That hand-maintained README
is unchanged; its build commands remain useful, but native integration follows the merge procedure below.

## Entry fields

| Field | Meaning |
| --- | --- |
| Order / ID | Unique ascending order and stable dependency ID. |
| Kind | `pr`, `feature`, or `pr-variant`. |
| Source | Original PR URL, or explicit source key in SOURCES.json. |
| Revision | Full accepted commit SHA, or `latest` resolved once from the declared source. |
| Integration | `merge`: integrate the complete frozen head with normal Git ancestry. |
| Depends on | Direct prerequisite IDs, selected earlier and matching DEPENDENCIES.json. |
| Reason | User-selected behavior. |

Fetch original PR heads from `refs/pull/<number>/head`, never synthetic merge refs. A PR variant uses its named
repository/ref and replaces the original PR's selection. Never substitute a local variant for an original PR.
Private feature sources remain in the Dropbox bare repository until the user explicitly chooses another source.

## Freeze and check the complete closure

1. Inventory local branches, dirty work and unpromoted commits before preparing. Preserve occupied worktrees.
2. Require selected sources to be ready. New local commits do not become validated or promoted automatically.
   Keep `localHead`, `acceptedHead`, `validatedHead` and `promotedHead` distinct. A push needs explicit authorization.
3. Freeze upstream master and every selected head under `refs/experimental-runs/<run-id>/`. Pinned revisions stay
   pinned. Record the original PR head/state for comparison. Freeze the dependency manifest and controls too.
4. A native feature's frozen head must equal its reviewed `acceptedHead`. Each direct dependency's selected SHA
   must equal that consumer's recorded accepted prerequisite and must actually be its ancestor. A newer selected
   PR/foundation is not silently accepted: merge it into the owner, review conflicts, validate when authorized,
   and update the manifest/selection/readiness before starting a new composition.
5. Reject known feature markers contained in a selected head when that feature is excluded and is not already
   part of upstream. Merging a consumer imports its ancestors, regardless of which rows were unchecked.
   Exclude its dependent closure as well, or explicitly redesign the dependency.
6. Retain binary-capable upstream comparisons and source commit lists for review. `*-review.patch` is evidence,
   not a feature-only patch to apply. The old fixed B..H boundary becomes invalid after prerequisite merges.

New-ExperimentalRun enforces the native merge contract and writes `contractVersion: 2`. It prepares an isolated
checkout; it does not merge, build, test, push or promote. `-ValidateOnly` only parses/reports selection metadata;
it does not establish ancestry or readiness. Historical runs retain their frozen scripts and original contract.

## PRs already merged upstream: ask before changing the stack

Before integrating, check the current GitHub merge status of each selected upstream PR, including
the original PR behind a selected variant. A closed PR is not necessarily merged. Record the PR URL,
merge commit and evidence of whether the change is included in this run's locked upstream revision.
Check ancestry where applicable; squash/rebase merges may require content comparison instead of
testing whether the original PR head is an ancestor.

If a PR has been merged upstream, flag it to the user and ask what to do with its stack entry
(normally, remove it from future selections). Stop and end the turn until the user explicitly answers.
Do not silently remove, disable, replace or reorder the entry, or treat a build/update request as
permission to retire it. This applies to full integrations and re-integrations.

Do not attempt to merge a change already included in the locked upstream revision; record
`already-present` with evidence instead. If GitHub has merged it but this run retains an older upstream
revision, explain that distinction in the question: removal alone does not supply the change to that
older base. Do not silently advance upstream or omit the feature. For a local PR variant, identify
any additional local changes not covered by the upstream merge before proposing retirement.

After the user's decision, update the future selection and affected dependency/source records
consistently, preserving frozen historical runs and existing integration history. Do not remove a
shared prerequisite record still required by another selected feature without resolving that dependency.

## Merge one input at a time

For a full new integration, start from freshly frozen upstream master. For
[re-integration](../workflows/reintegrate-scadmaxx.md), start from the retained successful integration and merge
only changed inputs; inherit and record unchanged inputs. Do not base a feature on an integrated release.
For each enabled row, use its retained ref with `git merge --no-ff --no-commit <retained-ref>`. Inspect all changes,
resolve conflicts without dropping selected behavior, then commit the merge. If the source is already an ancestor,
record `already-present`; no empty commit is needed. Do not squash, cherry-pick or apply the review patch.

Record source/before/after SHAs, merge parents and resolutions. First-parent history gives the concise sequence;
full history preserves owner attribution. Keep subsequent build repairs in separate commits. Build and run tests
only when requested. Stop for a user decision if resolving a conflict requires choosing feature behavior; preserve
the checkpoint if a failure remains after two focused repair attempts. No automatic feature selection or reordering.

Branding and feature-title patches remain canonical control assets under their existing workflows. They are not
API dependencies. The skill/launcher companions belong to the control repository and are not native merge inputs.
