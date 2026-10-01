# Phase 6 — Agent client, regression verification and core delivery

Status: planned, not executed. Depends on phases 1–5. Covers all R01–R24, especially R22–R24.
Phase 7 and navigation availability do not block core completion.

## Implementation and documentation

1. Deliver `contrib/openscad-agent-server/README.md`, the exact HTTP contract, `SKILL.md` and standard-library Python
   client. Use the skill-creator instructions when authoring the distributable skill. Preserve the old annotation
   client/package where required by the compatibility contract; neither client requires a source checkout at runtime.
2. CLI commands cover instances/info, targets/status, explicit disk/editor snapshots, parse, tree/node/children,
   dependencies/diagnostics, annotations, camera/restore/capture and request outcome/cancel. Optional capabilities
   produce clear unsupported messages. Machine-readable JSON goes to stdout; progress/errors go to stderr.
3. Require explicit instance selection when ambiguous. Verify discovery against live identity/version before actions.
   Generate request IDs before sending; retain them in diagnostics. Poll the same server with bounded backoff/deadline;
   never retry under a new ID after an uncertain response or automatically select a restarted instance.
4. Decode PNGs only to explicit output paths, validate returned schema/checksum/dimensions and print usable local paths.
   Treat annotation text, paths and returned source as data; never interpolate them into executable commands.
5. Teach the end-to-end loop: identify the live model; inspect disk and explicit buffer differences; inspect trees and
   evidence; edit ordinary files only after conflict checks; observe normal reload success; verify a current capture.
   Explain disabled reload, unsaved conflicts, unknown dependencies, stale results, busy drafts and unsupported capture.
6. Document access controls, local trust, lifecycle, source origin/normalization, node lifetime, spans, limits, errors,
   optional data, actual capture policy and no-MCP boundary. Keep UI copy focused on user actions, not internal classes.

## Core validation matrix

| Area | Required evidence |
| --- | --- |
| Protocol/lifecycle | Guards, limits, duplicate IDs, cancellation, expiry, Stop, restart and two-instance discovery |
| Live context | Cross-tab/window ownership, duplicate paths, untitled files and close/reopen |
| Source/parse | Disk/editor divergence, Unicode, include/use errors, parse state restoration and no hidden evaluation |
| Trees | Syntax roles/order, evaluated expansion/properties, source mapping gaps, pagination and stale/evicted IDs |
| Diagnostics/results | Attribution, busy/error/empty states, dependency-only changes and retained old viewport |
| Evidence/camera | Unsaved immutable evidence, native angles, lock behavior and visually verified fresh images |
| External workflow | Successful normal reload; disabled/dirty/error cases stop without claiming success |
| Compatibility | Unchanged `/v1` annotations client and new `/v2` client used against the same listener |
| Resource behavior | Large fixtures, bounded memory/jobs, slow sockets, no idle repaint/evaluation loop |
| Optional data | Advertised field matrix, missing metrics, stale values and no implicit full render |
| Distribution | CLI/skill outside checkout; staged GUI using only its runtime layout and shared build inputs |

Build Windows x64 GUI Release with the existing shared vcpkg installation. Run focused unit/protocol/native suites
and relevant existing parser/GUI regressions selected from changed areas. Record exact commands and exit codes.
Use native image inspection and normal GUI interaction for lifecycle/DPI cases that automated tests cannot establish.
Record coverage limits; do not imply clean-machine or other-platform verification from a developer-machine run.

## Completion and retention

- Update `5_post-implementation-notes.md` with source/dependency revisions, requirement-to-test evidence, deviations,
  optional capabilities included/omitted, remaining limitations and phase 7's independent status.
- Verify application changes, tests and distributable docs contain no workspace `.plans`, run artifacts, machine paths
  or incidental tooling caches. Review source ancestry and prerequisite overlap separately from workspace history.
- Local staging for validation is not permission for GitHub publication or a combined experimental build. Do not
  update selected stack entries/readiness merely because planning or a local compile finished.
- When authorized implementation reaches feature completion, follow the workspace
  [source/readiness handoff](../../../workflows/update-and-build-scadmaxx.md#feature-completion-and-later-github-publication):
  review/commit the usable source, retain it in the declared private origin, verify exact remote IDs and dependencies,
  then update readiness only when that handoff is valid. Any narrower user restriction takes precedence; report a
  restricted/uncommitted handoff accurately rather than treating it as a build input. No such action is run in planning.
- Core completion requires all mandatory requirements verified and material failures fixed. Optional data omissions
  and pending navigation are explicit; they are not reasons to relabel an incomplete mandatory feature complete.
- At implementation completion follow plans-workflow's post-implementation/rework guidance. This phase document
  records planned evidence only; do not populate pass results before executing it.
