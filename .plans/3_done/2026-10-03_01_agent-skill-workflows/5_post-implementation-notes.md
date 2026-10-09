# Agent skill workflow implementation and verification

Implemented locally on 2026-10-03 in control worktree `D:/openscad/wt-scadmaxx-agent-skill-workflows`, branch
`feature/agent-skill-workflows`. Base/unchanged HEAD: `a05b64c17a2e0b95fbeb44fe6a5cdbc7c3979a8c`.
Feature source is uncommitted; a base SHA alone does not identify these edited inputs. No installation, push,
promotion, enabled-stack change or final application composition was performed.

## Delivered changes

The maintained skill now routes six task intents independently of operating surface, evidence and interaction
policy. Six references cover task routing, design reasoning, local mesh editing, mesh/image reconstruction,
comparable visual verification and inspection. Modeling/validation link to those references. Existing BOSL2
revision checks, two-pass construction, edge-helper constraints, Customizer and guarded live targeting remain.

The companion builder requires explicit frozen skill/work/manifest inputs, stages without changing authored
files, refuses existing outputs and validates the complete skill inventory. Generated documentation/provenance
come from the selected clean canonical source. Control snapshots include the skill and its build instructions.
Stage uses the frozen builder and records companion provenance before final inventory; Package validates and
delivers that exact ZIP/checksum. Source HTTP skill delivery is retained through a shared tested helper.

Owned implementation: `skills/scadmaxx/SKILL.md`, its six new references and modeling/validation references;
`experimental/scripts/{Build-ScadmaxxSkill,Common,Build-Windows,Test-SkillCompanion}.ps1`; `docs/scadmaxx-skill.md`.
Existing unrelated copied edits are baseline inputs, not newly authored feature changes.

## Inputs and preservation

Existing dirty skill/script inputs were copied to the isolated worktree and retained under
`D:/openscad/runs/20261003-agent-skill-workflows/input`, including `preexisting-control.patch`.
`preserved-inputs.json` confirms the primary control skill/scripts stayed byte-identical to those inputs.
The completion check again verified all 13 skill and 13 script inputs. `feature-handoff.json` records the
14 feature-owned paths, input/final hashes and frozen control snapshot; its SHA-256 is
`2b9b31a9fc80274e437c5c378899106729c9487fc4ba89f3efcbdb8d9090b001`.
The hand-maintained README was not edited. The shared dependencies and user skill installation were unchanged.

Final frozen control snapshot: `runs/20261003-agent-skill-workflows/portable-reviewed/control/attempt-3/snapshot.json`.
Manifest SHA-256: `baf2c2faa6b3f3421b6ee2d9d44f96f4cd334bbdc7226308d910bc779acaf6d8`.
Canonical source: `wt-scadmaxx-20261002`, commit `4c325716b94e444637a80df3966197ce110b2b75`.
Document SHA-256: `b56d39cba821f5e160ce1b5a2df9a937462b093105584f78fb4e8e0fa185263f`.
This retained source was a validation input, not the base of a new native feature branch.

## Verification

- Authored and extracted skill validators passed with `uv run --with pyyaml .../quick_validate.py`.
- Six decision-path walkthroughs are recorded in `runs/20261003-agent-skill-workflows/workflow-review.md`.
- An independent read-only agent evaluated local STL editing, image replication and A/B live-target handling.
  It identified the obsolete fixed `openscad.com` instruction and consequential-depth ambiguity; guidance now
  selects the actual delivered console launcher and distinguishes permitted visual inference from required fit.
  This was a decision-path evaluation, not executed modeling or live HTTP evidence.
- All 23 artifact/provenance/lifecycle checks passed. Final fixture evidence:
  `companion-tests/1d530bf0968d4478b4b1d1fc13b5eb54/evidence.json` under the feature run.
  This includes changed/missing/extra/unreadable inputs, unidentified/dirty canonical source, preserved existing
  outputs, altered ZIP/manifest/source metadata, snapshot isolation, delivery hashes and the existing HTTP bundle.
- Changed PowerShell scripts parse and their whitespace checks pass. Packaging details are recorded in
  `runs/20261003-agent-skill-workflows/package-handoff.md`. The broader existing `Test-BuildTools.ps1` was not run;
  the focused suite exercises the changed snapshot/lifecycle behavior directly.
- The complete portable smoke suite passed against upstream `OpenSCAD-2026.09.27-x86-64/openscad.com` and the
  matching retained-source SCADMaxx executable in `artifacts/20261003-scadmaxx-executable-name/attempt-2/extracted-check`.
  Existing BOSL2 `2.0.766` was supplied explicitly from `runs/20261002-scadmaxx-skill/libraries`.
- Six exported plate variants passed bounds, positive volume, watertightness, winding, component and bore-ray
  checks; the invalid parameter limit failed as expected. Mainstream extension probes were rejected and the
  SCADMaxx object/annotation probes passed. Base/rounded PNGs were rendered and visually inspected.
  The complete suite passed again against the final reviewed bundle after those guidance corrections. Actual
  commands/results are in `runs/20261003-agent-skill-workflows/portable-reviewed/smoke/report.json`. Final PNG hashes
  equal the visually inspected images. Canonical/provenance hashes were independently verified.
  Earlier `portable`/`portable-final` evidence is retained; no smoke or fixture is represented as a real release.

## Portable artifact and remaining acceptance

Artifact: `D:/openscad/artifacts/20261003-agent-skill-workflows/attempt-3/scadmaxx-20261003-scadmaxx-skill.zip`.
SHA-256: `3419b0a12a08087b7024678a5bf5bcd1b1adaed04ba69c644eaaf894481f0b5b`.
Adjacent checksum and `portable-reviewed/companion.json` identify its exact provenance. Earlier attempts are retained.

Feature 01's bounded implementation and portable checks are complete. Real application Stage/Package acceptance
remains deferred to the next explicitly requested composition, as phase 3 specifies. No current binary has been
rebuilt or claimed to ship these changes. Desktop Customizer interaction and clean-machine portability were not
newly exercised by this skill workflow task.

For later commit review, isolate feature-owned changes from the retained copied-input patch. Controls and native
feature branches have separate ownership. Available follow-ups are fix forward for bounded corrections, replan
the approach, restart assumptions, or supersede the feature.


## Lifecycle closure — 2026-10-07

Moved to done at the user's request. Existing verification evidence and historical limits are preserved.
