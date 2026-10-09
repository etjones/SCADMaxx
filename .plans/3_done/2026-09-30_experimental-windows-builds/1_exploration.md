# Maintained experimental Windows builds

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

## Intent

Produce an enhanced experimental Windows x64 GUI OpenSCAD distribution from the latest upstream master and a
manually maintained ordered list of PRs, selected PR variants, and our own features. Preserve each integration and the independent
repairs necessary to build it. Package a verified portable ZIP and make it available locally, then through a
selected external destination. Linux and macOS are future extensions driven by demand.

## Foundation now present

- `experimental/PR_STACK.md`: canonical selection input; PR #6878 (shortcuts) and PR #6776 (dark mode) are enabled.
- `workflows/experimental-builds.md`: run isolation, immutable inputs, integration/repair checkpoints, packaging,
  validation, and distribution procedure.
- `experimental/templates/run-report.md`: durable provenance and outcome evidence.
- `experimental/integration-inputs.md`: typed source selection, delta boundaries, and overlap handling.
- `experimental/REPAIRS.md` and its record template: retained, independently verified reusable repairs.
- `experimental/profiles/windows-x64.md`: executable build-tooling contract, dependency and cache rules.
- `experimental/versioning-and-releases.md`: separate control Git history, snapshots, tags, and application identity.
- `docs/worktrees.md`: existing PR/build work that must be preserved.

The control repository and executable tools are implemented. The first full selected-stack build, unit tests,
installed runtime and extracted-ZIP checks passed in `runs/20260930-profile/`. Binary and matching-source ZIPs are
available locally. Windows desktop behavior and clean-machine checks remain before full profile acceptance.

## Local findings

`openscad-master` has the user fork as origin and OpenSCAD as upstream. Existing PR worktrees include #6642, #6776,
#6871, and #6999, plus issue #5425. Several have uncommitted changes. The MSVC checkout has multiple build directories
and a modified Clipper2 submodule; inspect its evidence instead of treating it as a clean reusable build environment.
The main checkout's `scripts/win-msvc-build.bat` defaults to headless and describes GUI setup separately. It is not
yet a verified recipe for the requested portable GUI distribution.

## Implementation sequence and status

Steps 1–3 are implemented. Step 4 passes automated package checks; desktop and clean-machine acceptance remain.
Step 5 is a future opt-in activity, not authorized by the workspace/tooling setup request.

1. Establish the separate workspace control repository with the documented allowlist. The initial selection is
   #6878 then #6776; validate their change boundaries and build-support dependencies without adding unselected PRs.
2. Implement and verify the Windows profile's configure/build/test/stage/package entry points, using the MSVC
   investigation as evidence. Record pinned dependencies, cache identity, commands, and a tested GUI distribution.
3. Implement a repeatable runner around input validation, fetch/locking, isolated worktrees, per-PR checkpoints,
   logs, and resumable run records. Support PR variants and local features; validate dependency deltas and partial
   upstream inclusion. Leave diagnosis and repair as explicit agent work with separate commits and catalog evidence.
4. Complete release identity in the application, matching-source provenance, immutable tags, release notes, and
   extracted-distribution checks. Preserve the exact control snapshot alongside each delivered build.
5. Configure the chosen publication destination and validate downloadable output. Schedule future runs only when
   requested. A GitHub release on the fork is a candidate, not a decision already made.

## Acceptance

A run is traceable from an exact upstream commit through every selected source head/base and repair commit to its ZIP.
It never silently drops a selected PR, imports dirty worktree contents, overwrites old results, or publishes a
partially integrated stack as success. A second fresh run uses a newly fetched master and independently resolves
the selected heads. An interrupted run resumes its own frozen inputs. CLI and GUI checks pass from the extracted
distribution with no hidden reliance on the development environment.
An improved local PR is used only when explicitly selected. Stacked features do not replay dependency changes.
Reusable fixes remain separate and have current applicability evidence. The application identifies its experimental
run; the retained tag, package metadata, and control snapshot identify the same tested source and build inputs.

## Decisions to resolve during implementation

The initial PR selection/order and Windows toolchain/dependency pins are recorded. Matching source is delivered
locally as a ZIP. External hosting, control-repository remote, artifact retention duration, and any future schedule
remain open and require a separate request. Retain
delivered artifacts and evidence until a policy exists. These choices do not prevent documenting the structure.
No automatic upstream posting, recurring automation, or binary publication is configured by this exploration.
