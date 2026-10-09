# Agent skill workflow implementation design

Target: GPT-6.1 Sol. Read [requirements](2_requirements.md), the
[handoff standard](../../1_planning/2026-10-03_00_source-first-cad-overview/implementation-handoff.md) and
[branch composition](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Ownership and inspected integration points

Work on the control repository's proposed `feature/agent-skill-workflows`; no OpenSCAD source delta or stack row.
Preserve the existing uncommitted skill/build-script edits by choosing an isolated, explicitly recorded input state.
Existing files: `skills/scadmaxx/SKILL.md`, its references/assets, `docs/scadmaxx-skill.md`,
`experimental/scripts/Build-ScadmaxxSkill.ps1`, `Test-ScadmaxxSkill.py`, `Common.ps1` and `Build-Windows.ps1`.
The current builder mutates authored references. `Save-ControlSnapshot` omits the skill tree. Stage copies the source
HTTP bundle and writes build-info/inventory; Package subsequently copies that evidence into the distribution.

## Documentation design

Create six references under `skills/scadmaxx/references/`:

| File | Required content |
| --- | --- |
| task-routing.md | Six task intents; independent surface, evidence and interaction axes; links to the right workflow. |
| design-reasoning.md | Interfaces, datums, envelopes, mating surfaces, natural construction, invariants and evidence. |
| mesh-editing.md | Baseline inspection; local wrapper/CSG; when reconstruction is justified; compare affected features. |
| reverse-engineering.md | Mesh versus image inputs; scale/uncertainty; axes/sections/features; hybrid models; comparisons. |
| visual-verification.md | Informative coverage, matched cameras, affected interfaces, final evidence and limitations. |
| inspection.md | Source/geometry/intent validity; available numerical tools; capability-gated advanced analyses. |

Update the entry routing plus existing modeling/validation references; retain specialized maintained references.
Write original guidance from the recorded decisions. Research repositories are leads, not vendored dependencies.
Do not copy their scripts, fixed scores or licenses into this skill. Do not edit the hand-maintained README.

## Frozen companion build contract

Retain the existing mandatory `CustomizerSourceRoot` and `OutputZip` parameters. Add mandatory `SkillRoot`,
`WorkDirectory` and `ControlManifestPath`; update all callers/runbook examples in the same phase. There is no fallback
to the current live control checkout. Inputs must resolve to existing frozen files; `WorkDirectory` must be a new,
empty, explicitly supplied attempt-local directory. Refuse an existing output ZIP.

1. Validate all inputs before writing. Resolve the canonical document inside `CustomizerSourceRoot`; record Git HEAD
   and its content hash. Release mode rejects a modified canonical document or an unidentified source revision.
2. Copy `SkillRoot` to `WorkDirectory/scadmaxx`. Replace the generated Customizer reference only in that staging copy.
3. Generate `references/bundle-source.json` in the copy, with `schema_version: 1`, `source_revision`,
   `canonical_document`, `document_sha256` and `control_manifest_sha256`. Hash the actual snapshot manifest file;
   do not invent a second snapshot inventory or place an absolute/private workspace path in the distributable.
4. Compress the staged `scadmaxx` directory to `OutputZip`. Return a single structured PowerShell result containing
   `path`, `sha256`, `source_revision`, `document_sha256` and `control_manifest_sha256`; send progress to Verbose.
5. Verify the output exists and its SHA-256 matches the result. Retain attempt-local intermediates as build evidence.
   Never clean or mutate a path derived from an unvalidated caller value.

The existing canonical document is required for this enriched companion. A composition lacking it receives a clear
missing-capability/input error, never documentation silently taken from the feature's unrelated development checkout.

## Build lifecycle integration

Extend `Save-ControlSnapshot`'s existing owned-file enumeration to include `skills/scadmaxx/**` and
`docs/scadmaxx-skill.md`; use its existing manifest/hashing conventions. Exclude temporary ZIPs/staging files. Retain
the exact frozen paths in the run record using the existing snapshot structure rather than a new global registry.

In `Build-Windows.ps1` Stage, after the source capabilities/canonical document are known and before build-info and
the staging inventory are finalized, invoke the frozen snapshot's builder with the frozen skill tree, integrated
source and attempt-local output/work directory. Name the companion from the same version/attempt identity as the
application plus `-scadmaxx-skill.zip`. Keep it outside the application staging tree to avoid nested artifacts.

Add a `skillCompanion` object to build-info containing the companion filename, SHA-256 and builder provenance fields.
The filename is relative to the delivery folder. Reuse the run's existing artifact/attempt path conventions. Package
verifies that exact file/hash and places it next to the application archive and its evidence. It must not regenerate
the companion from live files. A changed/missing ZIP invalidates packaging. Existing HTTP bundle packaging stays intact.

Use the release's existing control-snapshot machinery to prove the invoked builder itself was frozen. Do not change
enabled features, source selection, installer state or promotion. Integration evidence includes both repository SHAs.

## Ordered implementation and verification

1. [Phase 1](4_imp-phase1.md): authored workflow guidance and six task walkthroughs.
2. [Phase 2](4_imp-phase2.md): nonmutating frozen-input builder and artifact checks.
3. [Phase 3](4_imp-phase3.md): snapshot/Stage/Package integration and portable smoke evidence.

If the actual snapshot API cannot provide its immutable manifest/skill paths, resolve that control-flow gap before
writing the release hook. Do not fabricate provenance fields or package whatever live files happen to exist.
