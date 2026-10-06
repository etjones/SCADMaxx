# Control-file history and release identity

## Separate workspace control repository

SCADMaxx's workspace control history and application source history are private/local by default. The installed
local bare origins and per-feature publication workflow are recorded in [the Git layout](../docs/git-layout.md).
Publishing a usable feature is a separate user decision; it does not publish the composed build or workspace.

Version workspace instructions and build tooling independently of the OpenSCAD source repository. The
control repository is `D:/openscad/scadmaxx`, on `main`, with origin `E:/Dropbox/bare_repos/scadmaxx.git`.
Initial control history was established on 2026-10-01. Source checkouts remain independent
repositories/worktrees, not submodules of this control repository.

Maintain the allowlist `.gitignore` that admits only `AGENTS.md`, `README.md`, the ignore
file, `docs/`, `workflows/`, `experimental/`, and `.plans/`. Review added tooling for generated outputs and secrets.
Exclude source checkouts, installed applications, dependencies, build trees, `runs/`, and `artifacts/` by default.
Inspect ignored/untracked paths before staging; never add nested repositories or rely on a broad `git add .`.
Follow the git-workflow skill for commits; this document does not itself create a commit or remote.

At run start, record the control repository commit and the exact stack, repair, profile, and script files used.
Record local modifications too: a commit ID alone cannot identify dirty inputs. Snapshot the consumed files with
relative paths and SHA-256 hashes in `runs/<run-id>/control/`. Until the control repository exists, record that fact
and retain the same complete snapshot. Preserve these snapshots with delivered build evidence outside control Git.
If profile establishment or a tooling repair changes a consumed control file during the run, preserve the original
snapshot and take a new hashed revision. Associate each attempt with its actual revision; final build info must
identify the revision used to produce and verify the delivered package.

## Build and release identity

- Name integration branches/worktrees using the
  [creation-date naming rule](../docs/git-layout.md#integration-branch-and-worktree-names), and record their mapping
  to the unique run ID. Use the unique run ID throughout logs, package, and application identity. The application should display
  `experimental-<run-id>` alongside its OpenSCAD version and source revision in About/version information.
- Implement this through the locked source's supported version mechanism where possible. Any needed source change
  is a separate packaging-metadata commit before the final build; do not put a self-referential commit SHA into a
  source commit. Generate final-SHA metadata at build time.
- Include a build-info file with upstream SHA, every entry's source/head, accepted dependency SHAs and merge SHA, repairs, final
  source SHA, submodules, control snapshot identity, profile, and toolchain. Keep validation results and limitations
  in the run report; do not create or bundle release notes.
- After final validation, create an annotated, never-moved source tag `experimental/<run-id>` at the exact final
  commit. This tag convention is separate from the branch naming rule; tools must use full `refs/heads/` and `refs/tags/` names.
  Record the tag object and target commit. A failed attempt gets no success tag.
- Retain referenced feature, repair, and submodule objects along with matching source/build material. A local tag
  alone is not an accessible source-delivery mechanism; provide a matching source archive or verified hosted refs
  when distributing outside this machine.
- Never rebuild different inputs under an existing successful run ID or move a release tag. A correction is a new
  run/release linked to the earlier one. A future "latest successful" alias may advance only after verification;
  it must not replace immutable build identities.

External hosting and artifact retention duration remain unconfigured. Keep delivered artifacts and matching
evidence/source until a retention policy is selected; no automatic deletion or publication is authorized here.
