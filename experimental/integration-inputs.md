# Integration inputs and change boundaries

The enabled table in [PR_STACK.md](PR_STACK.md) is the authoritative ordered selection. These rules apply to every
fresh run and to the frozen input snapshot when resuming. Examples below do not enable anything.

## Entry fields

| Field | Meaning |
| --- | --- |
| Order / ID | Unique order and stable ID, such as `pr-6878` or `annotations`; use IDs in dependencies and repairs. |
| Kind | `pr`, `feature`, or `pr-variant`. |
| Source | PR URL for `pr`; a key in `SOURCES.json` for other kinds. |
| Revision | `latest` resolves the declared ref once; a full commit SHA pins that source. |
| Delta base | `auto-merge-base` or a full commit SHA defining the start of the intended change. |
| Depends on | Earlier entry IDs or `none declared`; verify this against source history at run start. |
| Reason | The behavior the user wants included. |

A `feature` or `pr-variant` definition in [SOURCES.json](SOURCES.json) must provide `repository` (URL or absolute local
repository path), `ref` (for example `refs/heads/feature/annotations`), and, for a variant, `prUrl`. A local source is
valid without publishing it. Retain its selected commits in the shared clone under run-specific refs.

For explicitly selected but unfinished features, set `ready: false` and a nonempty `pendingReason` in the source
definition. Selection validation reports these entries; actual preparation stops before fetching or creating a run.
After the feature's development task commits and pushes a usable revision to its declared repository, review its
delta base/dependencies and set `ready: true`. Omitted `ready` defaults to true for existing definitions. This flag
records readiness; it does not replace revision, diff, build or behavior verification.

For example, the selected annotations source uses repository `E:/Dropbox/bare_repos/openscad.git` and ref
`refs/heads/feature/annotations`. Resolve only committed history. Dirty source worktrees may remain occupied:
record their state and exclude their edits, index contents, untracked files, and dirty submodule working files.
Do not commit those edits as part of an integration run. A selected submodule commit must also be obtainable.

## Original PR versus our version

- `pr`: fetch `refs/pull/<number>/head` from the PR's upstream repository. The PR URL is the source identity.
- `pr-variant`: use the explicitly selected repository/ref instead. Record both its locked head and the original
  PR head for comparison, showing what our version changes. Never silently substitute a local branch for a PR.
- Treat a variant that includes the whole PR as a replacement for that PR's row, not an additional full integration.
  If selecting only an incremental fix, declare its actual delta base and dependency instead.
- Reusable narrow Windows repairs can remain separate entries in the repair catalog rather than full PR variants.

Validate pinned commits against the declared source. If a ref was force-pushed and a pinned commit is no longer
reachable, use retained provenance to establish its identity or stop; do not silently switch to the ref's new tip.

## Lock the intended delta

1. Resolve upstream master, every source head, dependency, and delta base before modifying the integration checkout.
   Retain refs under `refs/experimental-runs/<run-id>/` and record full SHAs in the run input record.
2. For an independent entry, `auto-merge-base` means the unique merge base of its locked head and the locked upstream
   master. Record that SHA. Multiple merge bases or unrelated histories need an explicit reviewed boundary.
3. For a stacked feature, require an explicit base SHA at the dependency revision on which it was developed, plus
   the dependency ID. Verify the base is an ancestor of the source head. If the selected dependency has since
   changed, compare the revisions and record the adaptation; do not treat them as equivalent automatically.
4. Preserve the source commit list and binary-capable diff from delta base to head. Inspect merges and unrelated
   branch history. A simple commit range is insufficient if it would import changes outside the selected feature.
5. Compare the intended delta with upstream and earlier entries, including earlier repairs. Ancestry can prove
   containment; squash/rebase cases need patch/content evidence and relevant behavior checks. Patch IDs are useful
   evidence, not proof that behavior is equivalent. Record fully present entries without empty commits.
6. For partially present changes, document which parts already exist and preserve a reviewed residual patch.
   Never apply the entire old delta blindly or infer that a whole feature is present from one matching commit.
   If the intended residual or dependency is unclear, ask the user and stop.

## Apply one integration at a time

Apply the reviewed delta with three-way context where supported, inspect the resulting diff, and make one squash
integration commit per entry. Do not use `git merge --squash <head>` blindly for stacked entries: earlier squash
integrations do not retain the original dependency ancestry, so a later merge may replay that dependency.

Record the exact application command, patch checksum, before/after SHAs, source authors, and any conflict
resolutions. Resolve conflicts needed for integration in that commit; subsequent build repairs remain separate.
Check both the newly added behavior and affected earlier features so a conflict resolution cannot silently undo
an earlier integration or repair. No automatic dependency insertion, row reordering, or functionality removal.
