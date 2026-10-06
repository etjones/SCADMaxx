# Reopen the last-used model on startup

Status: planning only. Requested on 2026-10-06; implementation has not started.

## User intent

Starting SCADMaxx should reopen the last-used model so the user can resume work without finding the file again.

## Proposed behavior

- On an interactive launch without an explicit document, reopen the last-used saved model.
- Treat last-used as the most recently active file-backed model, rather than merely the last file opened.
- An explicit file supplied by the launcher, command line or operating system takes precedence.
- Use the normal document-loading path and library resolution.
- If the remembered file is missing or inaccessible, start normally with a brief explanation; do not block startup.
- Exclude command-line exports, headless invocations and automated test runs.

These are planning proposals, not additional user-approved implementation decisions.

## Boundaries and decisions to resolve

- Restore one model; restoring all tabs, window layouts or a full session is outside this initial feature.
- Define the opt-out preference and its default before implementation.
- Decide whether automatic reopening should trigger preview. Avoid silently adding expensive startup rendering.
- Define ordering across multiple windows/processes and what happens when the last-used document is explicitly closed.
- Untitled buffers and unsaved edits belong to recovery; do not overwrite recovery content with the on-disk file.
- Establish whether remembered state is shared across SCADMaxx builds, considering the launcher and existing settings.
  Moving an installation should not invalidate an absolute model path.

## Implementation exploration

Inspect startup arguments, OS file-open events, active-document changes, recent-file persistence and recovery before
choosing hooks. Reuse existing settings and document-opening mechanisms. Avoid a parallel loader or dependence on
launcher working directories. Restore only once; explicit file-open events must not produce an unwanted extra tab.

No hard dependency on Sections or the model-tree feature is identified. Select a source worktree only when
implementation is requested. No source edits, builds or new worktrees are requested by this planning item.

## Acceptance scenarios

- Normal startup restores the last active saved model, including paths containing spaces or Unicode.
- Switching between saved models records the last active one correctly.
- Explicit startup files suppress restoration through CLI, launcher and OS file-open entry points.
- Missing files, unavailable drives and disabled restoration leave the application usable.
- Unsaved-edit recovery remains intact; untitled documents do not accidentally erase a valid remembered path.
- Multiple windows/processes follow a documented deterministic policy.
- CLI exports and tests neither restore documents nor change the user's remembered startup document.
- Restoration follows the agreed preview policy without an automatic reevaluation loop.
