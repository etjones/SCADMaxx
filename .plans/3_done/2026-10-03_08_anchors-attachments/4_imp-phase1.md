# Phase 1: schemas, scoped collection and source fixtures

Covers AN01/AN03/AN06/AN12/AN17. Freeze the actual prerequisite base and inspect implemented 03/07/14 headers.
Require the [scoped dispatch/finalization hooks](../2026-10-03_00_source-first-cad-overview/semantic-extension-contract.md)
in their owners. Missing hooks stop preflight for an owner follow-up; do not duplicate those systems in 08.

1. Add ReferenceKinds/Collector/Scene and typed payloads. Register the five assignment kinds with 14's Consumer sink;
   decode every field in source-contract.md, reject unknown/duplicate fields and invalid values. Keep scope checks
   separate from kind checks and require the direct Part/Assembly body or supported file scope.
2. Read evaluated native values once, clone required data and source ownership into the evaluation-owned collector.
   Capture declaring owner and invocation before resolving explicit owner/endpoint paths. Do not keep borrowed native
   Context pointers in immutable records. Use-only top-level declarations must not leak into the model registry.
3. Resolve local/full paths after native instances exist; build per-owner reference namespaces, source-use counts and
   one-driver-per-child index. Validate duplicate inherited/explicit anchor IDs and attachment IDs with both source
   locations. Ordinary Section/View and unannotated source behavior must stay unchanged.
4. Add ReferenceKinds_test.cc/ReferenceCollector_test.cc with [anchor-schema] and [anchor-collection]. Copy the complete
   source-contract example into testdata/scad/anchors and enumerate its reference/attachment records headlessly.

Fixtures: width 40/60 produces mount local X=20/30 in different owner keys; equal local anchor IDs across owners work;
instance-only root declaration affects only /fixture-a/plate; root document Anchor works with ordinary geometry.
Cover computed helper RHS, Unicode IDs/paths, escaped slash/tilde keys, label rename, duplicate IDs, unknown fields,
wrong host/type, nested helper/control/transform declaration rejection, zero/nonfinite vectors, imported module
parameters, unused use-library metadata, deleted owner and an expression with observable echo evaluated exactly once.

Include Point/Axis/Plane records with no fabricated frame and explicit Anchor conversion source; Attachment in a Part
must fail. A reused Assembly yields two relative relation sets, not one document-global overwritten Attachment.
Run named labels and affected 14 declaration/object/Customizer regressions using the shared verification contract.
Exit: schema/ownership and source spans are proven. Do not proceed with guessed owner paths or collector reevaluation.
