# SCADMaxx skill implementation

Implemented 2026-10-02. Product entry point: [SKILL.md](../../../skills/scadmaxx/SKILL.md).
The companion packaging procedure is [docs/scadmaxx-skill.md](../../../docs/scadmaxx-skill.md).

## Delivered

- Short skill entry point with unconditional BOSL2 preference, install-if-missing behavior, conceptual-shape
  first pass and dedicated-helper edge-treatment second pass. Manual ring/profile/mesh `skin()` edge
  workarounds are explicitly prohibited; legitimate lofted bodies are distinguished.
- Focused references for modeling/library setup, edge treatments, Customizer, build capabilities, direct HTTP
  and validation. Multi-document guidance distinguishes editor identity, displayed-result ownership, saved
  versus unsaved source, target/revision guards, job receipts, and capture freshness.
- Runnable parametric plate, reactive controls across an include, and ordinary OEP8 object examples.
- Expanded canonical `doc/customizer-attributes.md` in the #6642 source checkout. It documents actual accepted
  values, literal range limitations, widget/default behavior, evaluation timing and syntax differences.
  No language implementation or existing group-visibility edits changed.
- Packaging script generates the bundled canonical reference and records source HEAD, dirty-doc status and
  SHA-256. The skill has no dependencies on workspace paths. A test script exercises an extracted bundle.
- `.gitignore` admits the new product-owned `skills/` directory. Existing application release packaging and
  the hand-maintained README were not edited by this task.

## Artifact and validation

Final companion: `D:/openscad/artifacts/20261002-scadmaxx-skill/scadmaxx-skill-20261002.zip`.
SHA-256: `24ebe215ef86432ef27407f1bae3a454a2808586a66eb4869a6f0efb33b20b14`.
The earlier undated ZIP is the first validation draft; deliver the dated ZIP.
Evidence root: `D:/openscad/runs/20261002-scadmaxx-skill`.

- Official BOSL2 cloned into a previously absent `libraries/BOSL2` in the isolated run. Verified version
  2.0.766, commit `e173fa0ae45f9e2082e0d8c0382dae98621b7c20`; actual include/render passed through that
  process-local path. Existing user libraries, including `BOSL2-master`, were preserved.
- Skill-creator validator passed for the authored and final extracted skill. Relative links, canonical-doc
  hash and source/extracted example identity checks passed. Extraction/testing took place outside the source
  and control checkouts, under the run directory.
- `validation-2/report.json`: six plate exports passed on upstream OpenSCAD 2026.09.27: untreated, zero,
  rounded, chamfered, near-limit 7.49 mm and alternate small dimensions. Checked bounds, positive volume,
  watertightness, winding, one component and through-bore/material ray intersections. The 7.5 mm limit failed
  explicitly as intended. Untreated and zero volumes match; finished variants remove material.
- Base and rounded PNGs rendered and were visually inspected. Four holes and the intended vertical-edge-only
  treatment are visible. There is no handmade `skin()` geometry in the examples.
- Upstream 2026.09.27 rejected both extension examples; 2026.10.02-oep8-check accepted them. Final changed
  special-variable example and object example also exported STL cleanly from the final extracted bundle;
  logs are in `final-checks/`. The plate file is byte-identical to the six-case validated version.
- Existing Customizer unit suite rerun on the combined executable: 6 cases, 67 assertions passed, including
  ordinary and special-variable dependencies through includes and rejected annotation grammar.
- Fresh direct-HTTP native suite: 13 passed, no failures/skips, in `native-20261002T165843/`. This includes
  source/target inspection, guarded viewport, direct HTTP, document lifecycle and reload cases. Source was
  subsequently retained by its owning task as `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`.
- Reviewed an unsupported-treatment scenario: a requested fillet on an arbitrary post-Boolean intersection
  cannot be implemented by naming that new edge in `cuboid(edges=...)`. The reference directs the agent to
  a verified profile/mask construction when suitable, otherwise a concrete unmet requirement, and expressly
  disallows a `skin()` workaround. This is a decision-path review, not an independent agent behavior test.

The first test invocation exposed a missing mesh graph dependency; the validation script now declares
`networkx` as well as numpy/trimesh/rtree. The subsequent complete run passed. Product usage needs none of
these Python packages. Source documentation whitespace checks passed; unrelated README whitespace was preserved.

## Limits and handoff

Stable OpenSCAD 2021.01 is a documented comparison, not an executed build here. No macOS/Linux run or full
aggregate SCADMaxx build was performed. Customizer reactivity is backed by the existing core tests; manual
GUI acceptance of every widget in this particular example was not performed. The native HTTP suite exercises
the relevant multi-document semantics; no independent skill-following agent was launched.

This task did not install the skill into user agent configuration, commit/push these new changes, publish a
release, or change feature selection/readiness. The canonical doc is an uncommitted documentation-only change
atop #6642 source `8ea44273775f3c7720f2ff607e6d4ea5215422a6`; bundle provenance explicitly records that fact.
On a later commit request, commit only the owned doc in its source repo and the skill/scripts/docs/plan in the
control repo, regenerate provenance against the retained doc revision, and preserve unrelated concurrent work.
No change to selected source readiness is necessary for runtime code: this task changed documentation only.

Available follow-ups: fix forward for bounded corrections, replan for another implementation approach,
restart if assumptions change, or supersede with a replacement skill.

## Acceptance and retention, 2026-10-03

The user accepted this feature as complete and requested commits. The skill was installed into
`D:/source/agents-mgmt/skills/scadmaxx`, exposed by the existing Codex skills junction; all 13 files were verified.
Canonical documentation is now committed as `41d92671b6040959caa036a886be1f245bc32f5f` on `codex/pr6642`.
The generated provenance now records this commit and `document_modified_from_commit:false`; documentation
and example contents are unchanged from validation. The installed copy receives the same provenance update.

Updated companion artifact: `D:/openscad/artifacts/20261003-scadmaxx-skill/scadmaxx-skill-20261003.zip`.
SHA-256: `a63a59ab78df97ff29c7917874837048ed524511f35f0eefc6e0fee8a5a78d2c`.
This artifact supersedes the earlier dated ZIP for delivery. Retain source and control commits in their
private Dropbox origins under the workspace workflow; the installed skill is committed separately in
agents-mgmt. Unrelated source, launcher, build and shared-agent changes remain excluded.
