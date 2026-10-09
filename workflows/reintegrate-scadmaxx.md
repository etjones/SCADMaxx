# Re-integrate changed branches into an existing SCADMaxx integration

Use this workflow to add or update selected features in a maintained integration. Continue from its successful
composition; do not reconstruct unchanged merges or repairs. A documentation/workflow request alone does not
authorize integration, building or tests. A requested integrated build includes relevant validation and packaging.
Apply [the separate-operation rules](repository-operations.md): retain the recorded upstream baseline for a
build-only request. Updating master/feature bases, pushing to Dropbox and publishing to GitHub are separate work.

## 1. Identify and preserve the starting checkpoint

Read the existing run report, frozen inputs, final source SHA, repairs and Windows profile. Locate the actual
integration branch/worktree and compatible build directory. Compare Git HEAD, working files and submodules with
that evidence. Do not assume the newest directory is the intended integration.

Preserve dirty work and active checkouts. Stop if the target is ambiguous or contains unfinished work that cannot
be safely separated. Do not reset, clean or rebase it. Keep feature development in owner branches; never base
a feature on the integrated composition.

Inherit the stable `buildName` (normally `scadmaxx-all-features`) and use `<buildName>-YYYY-MM-DD_HH-mm` for the
new run ID. Record what changed separately in `purpose`; never rename the edition after the feature being merged.
Follow [build identity](../experimental/versioning-and-releases.md#build-and-release-identity).
Create a new update record under `runs/<new-run-id>/`, with the previous run ID and full successful integration
SHA as its parent checkpoint. Retain that SHA under `refs/experimental-runs/<new-run-id>/previous-integration`.
Keep previous run records, frozen inputs, tags and deliveries unchanged. Advance the existing integration branch
in its existing worktree; its creation-date name remains unchanged. The new run ID identifies this update.

## 2. Freeze the changes and effective composition

Apply the [merged-upstream PR check](../experimental/integration-inputs.md#prs-already-merged-upstream-ask-before-changing-the-stack)
before merging: flag merged PRs, ask the user about retiring their stack entries, and stop for the answer.

Follow the branch inventory, control reconciliation and promotion rules in
[update-and-build-scadmaxx.md](update-and-build-scadmaxx.md). A build request does not authorize pushes or
substitution of local unpromoted work for declared inputs.

Compare the parent composition with the selected stack and report:

- Every changed or added feature: previous and proposed full SHA, declared repository/ref and readiness.
- Every unchanged feature: the exact inherited SHA, with its original evidence.
- Upstream: the inherited SHA, or the newly frozen SHA if an upstream update was requested.
- Local-only commits and dirty work excluded from this build, and any unresolved source/dependency changes.

For a request to re-integrate a named branch, update only that input and explicitly required prerequisites.
Leave other inputs, including upstream, frozen. For "update everything and build", record the explicitly requested
maintenance separately before freezing the resulting eligible inputs. Pinned selections remain pinned;
do not silently replace them with current branch tips. A conflict between
the requested revision and a pinned selection requires an explicit decision before merging.

Require the effective selection to be ready and validate its full dependency closure using
[integration-inputs.md](../experimental/integration-inputs.md). New unready selections are blockers, not silently
omitted features. If a prerequisite advances, update affected owner branches and their reviewed dependency pins
first; inclusion in the integration alone does not establish consumer compatibility.

Retain changed heads in new run-specific refs. Snapshot the controls, manifest, source definitions, profile and
repair records. Record a complete effective input table, including inherited inputs, and present it before merging
or compiling. Compare each changed head with its previously integrated head: normal forward development qualifies;
rewritten or unrelated history requires a fresh composition or an explicit reviewed maintenance decision.

Do not call `New-ExperimentalRun.ps1` for this operation: it creates a fresh upstream-based worktree. There is
currently no dedicated re-integration orchestration script. Follow this procedure using normal Git/CMake commands
and the established build/deployment tools only after checking their assumptions against the update record.

For `Build-Windows.ps1`, pass `-ReuseBuildFromRun <build-owner-run-directory>` alongside the existing `-Build`
directory and new `-Run` directory. New `inputs.json` must include `parentRunId`, `parentIntegrationSha`, the
same source/branch, complete inherited-plus-updated entries, and current hashes of the frozen PR_STACK and
dependency files. Copy those frozen files and source definitions before Configure. Preserve the old
`experimental-state.json` in the update evidence before reuse. The option verifies the parent source and
ancestry; the normal profile/toolchain/dependency fingerprint and source-revision guards still apply.
The build-owner directory can belong to an older run than `parentRunId`: repeated re-integrations retain the
original build directory while their immediate parent checkpoint advances.

## 3. Merge only changed inputs

Merge frozen changed inputs in dependency/stack order, using `git merge --no-ff --no-commit <retained-ref>`.
Review and commit each merge separately, recording its before/after SHA, parents, input and conflict resolutions.
If already an ancestor, record that fact without an empty merge. Preserve previous integrations and repairs;
Git ancestry handles their shared history. Never replay unchanged feature patches or cherry-pick their fixes.

If requested, merge the frozen newer upstream revision as a separate checkpoint before feature updates. Review
existing integration repairs for overlap with incoming fixes; retain or adapt them based on current source behavior,
without blindly applying them again. Make new repairs separate commits.

Stop for a behavior choice when resolving conflicts would change a feature's meaning. If a failure remains after
two focused repair attempts, preserve the checkpoint and report the blocker with commands, logs and attempted fixes.

## 4. Build incrementally and deliver separately

Reuse the existing integration's own build directory if its source path and compatibility fingerprint still match
the [Windows profile](../experimental/profiles/windows-x64.md#cache-rules). Reconfigure when needed; never copy
a CMake cache from another worktree. Use the existing shared vcpkg installation without rebuilding dependencies.
An incompatible toolchain/profile requires a fresh build directory, not automatically a fresh Git composition.

Let the build system determine what needs recompilation and relinking. Shared header, parser or build-system
changes may rebuild many files; do not promise a small compile based solely on the number of changed branches.
Do not rebuild the old upstream baseline or retest every unchanged integration checkpoint. Carry forward their
identified evidence, run checks for changed behavior and affected consumers, then final integrated and extracted
package smoke checks. Do not claim inherited evidence was rerun against the new binary.

Select correctness coverage using [testing profiles](testing.md): everyday for the final integrated binary, plus
deep-background for shared evaluator/geometry/export changes. Record inherited desktop evidence separately; do not
launch windows without explicit desktop-test authorization. The full internet corpus is separate opt-in verification.

Run the [integration performance checks](../experimental/performance/USAGE.md) before packaging. Compare the candidate
against the last accepted delivery and retain the results with this new run; do not automatically advance the baseline.
Use a new timestamped delivery under `artifacts/scadmaxx-all-features/<delivery-id>/`, following
[experimental-builds.md](experimental-builds.md#package-and-verify). Produce the flat ZIP, matching source,
build metadata and checksums; no release notes. Metadata must describe the complete effective composition and
new final source SHA, not only the changed branch. Preserve earlier deliveries and final source checkpoints.

## When to use a full new integration instead

Use [experimental-builds.md](experimental-builds.md) for an explicitly requested clean composition, a first build,
removing/replacing features whose history must be absent, or incompatible/rewritten source histories that cannot
be carried forward safely. Deleting a stack row does not remove its already-merged code from an existing integration.
Do not silently turn a re-integration into a full composition; report the reason when a fresh composition is needed.
