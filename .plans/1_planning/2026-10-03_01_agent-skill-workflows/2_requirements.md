# Agent skill workflow requirements

Scope: enrich and distribute the existing generic SCADMaxx skill. These requirements follow
[the exploration](1_exploration.md); they do not install the skill or start source-feature implementation.

## Required behavior

- SK01: Route create, source-edit, mesh-edit, reconstruct, image-replicate and inspect tasks independently of the
  live/CLI surface, required evidence and the user's interaction policy. Refinement and export remain workflow steps.
- SK02: Teach interfaces, frames, envelopes/voids, mating surfaces, construction choices and parameter invariants
  before selecting API calls. Preserve the existing base-geometry then detail/edge-treatment approach.
- SK03: Preserve capability detection, installed BOSL2 revision checks, supported edge helpers, Customizer dialect
  guidance and server/document/source/result/viewport guards. Never advertise tools merely because they are planned.
- SK04: Preserve source intent during edits. Distinguish local imported-mesh CSG from parametric reconstruction;
  support hybrid reconstruction. Image replication records known scale and uncertainty in inferred dimensions.
- SK05: Choose informative views, repeat comparable cameras and compare geometry where tools permit. Distinguish
  source validity, geometry validity and intent validity. No universal view count, reconstruction score or stock-solid rule.
- SK06: Keep the entry skill short, with task-specific references. Exclude private design-library paths, ownership
  rules and agent-specific setup. Respect explicit user instructions about questions and approvals.
- SK07: Build a portable companion ZIP from a frozen control skill and the corresponding integrated source's
  canonical Customizer document. Building must not modify authored inputs or borrow files from another checkout.
- SK08: Record source revision, canonical-document hash, frozen-control manifest hash and companion SHA-256. A release
  companion must correspond to its application build. General guidance must still detect capabilities at runtime.
- SK09: Include the authored skill in control snapshots. Stage creates the companion before build-info/inventory are
  finalized; Package verifies and delivers the recorded companion alongside the application. Never overwrite a ZIP.
- SK10: Missing inputs, mismatched hashes and unsupported capabilities produce explicit failure/limitations. Keep
  existing source HTTP bundle delivery working and do not install or enable anything in the user's environment.

## Acceptance cases

1. Six representative task walkthroughs select the appropriate reference and evidence, without inventing new tools.
2. Enlarge one hole in an imported STL: choose a local wrapper when viable; do not demand whole-model reconstruction.
3. Replicate from an image with one known dimension: retain inferred dimensions as uncertain and compare matched views.
4. Read-only live inspection retains wrong-tab/stale-result checks; source modification retains the dirty-buffer rules.
5. Build from temporary frozen inputs: authored input hashes stay identical, ZIP has one `scadmaxx/` root, all relative
   links resolve, generated reference matches the integrated source, and recorded hashes match extracted contents.
6. Missing canonical document or modified companion during packaging fails before reporting a deliverable.
7. Extract away from this workspace; run the existing skill smoke suite with explicit executable/library paths.

## Exclusions

No geometry-analysis implementation, third-party script import, user skill installation, application promotion,
private project rules or new native stack feature. Later implemented capabilities receive separate guidance updates.
