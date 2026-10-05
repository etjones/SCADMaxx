# Extensible component providers and placement/source adapters

Planning review: all three product decisions accepted; requirements, provider/version contract, technical plan and
five implementation phases are prepared. Executed library-call probes support the selected recipes; native registry
and matcher implementation remains unstarted. See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Status: planning. Source: chat A in the [overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md).

The user postponed 09/10 and accepted 11's three decisions: a bounded catalog of primitives/holes/BOSL2/BOLTS,
declarative custom catalogs, and shipping catalogs without bundling libraries. They explicitly added version tracking
so catalog adapters can match the installed library revision. No automatic library download/update is included.
12 remains independently responsible for its UI, placement and source edits.

Read [requirements](2_requirements.md), [provider/version contract](provider-contract.md),
[technical plan](3_overall-plan.md) and [executed evidence](library-investigation.md). The exact initial entries are
cube, sphere, cylinder, plain-hole mask, BOSL2 metric threaded-hole mask and BOLTS ISO4017/ISO4032/ISO7089 hardware.
Catalog descriptions and an authored project example ship; external vendor implementations remain user-supplied.

## User intent and abstraction

The user wants modular component-library insertion without repeatedly looking up APIs. They corrected the referenced
standards library to BOLTS, while accepting NopSCADlib as another valid example. Support a neutral catalog/provider
system, not only a hard-coded list of SCAD module names.

Separate three questions:

1. What is being inserted: a provider defines the component, standard/variant and configurable parameters.
2. Where/how it attaches: shared geometric context, anchors and placement adapters define placement.
3. How it is expressed: a source adapter generates suitable OpenSCAD/library calls and required imports.

BOLTS is the intended standards/specification example; BOSL2 can supply attachment semantics and modeled items.
Those roles must not be conflated. NopSCADlib exemplifies modeled hardware; project/user catalogs contribute local parts.

## Selected provider contract

Display name, category/icon, stable item identity, parameter schema, variants/standards, module or source generator,
required includes/dependencies, supported placements, child-anchor preferences and operation semantics.
Declarative parameter metadata drives a common insertion inspector rather than per-library hard-coded UI.

The selected initial libraries are OpenSCAD built-ins, a bounded BOSL2 threaded-hole recipe and three BOLTS hardware
families, plus support for user/project module catalogs. NopSCADlib and exhaustive library coverage are deferred.
Native catalog schema1 describes typed parameters, structural source recipes, imports, contact frames and explicit
library fingerprint profiles. Full BOLTS structured-data/backend generation is unnecessary for this bounded adapter.

Distinguish additive components, subtractive masks and attachment behavior. A threaded-hole entry is a subtractive
operation, not merely a call to a function whose output happens to look like a hole. Providers may expose suitable
default direction/child anchor, while core placement remains reusable across catalogs.

## Placement and source generation

Providers describe supported attachment/operation semantics as data and generate source fragments for supplied
parameters. The consuming [12](../2026-10-03_12_contextual-insertion/1_exploration.md) branch combines them with
[08](../2026-10-03_08_anchors-attachments/1_exploration.md): semantic anchor, suitable custom anchor, relative
transform or explicit ordinary transform. Keep normal OpenSCAD useful without forcing BOSL2 into every document.

Generate readable source fragments plus required-include and additive/subtractive metadata. 12 owns selecting the
target scope, resolving include/name collisions, arranging boolean/attachment context and committing through
[02](../2026-10-03_02_source-editing-foundation/1_exploration.md). This provider service never edits a live document.
Catalog discovery, declarative extensions and dependency/version matching are specified in the provider contract.
Catalog version and supported library version are distinct, with actual loaded-file fingerprints deciding the match.
Installing an arbitrary library does not automatically make discoverable parameter/operation metadata available.

## Order and evidence

Define and deliver the registry/metadata/source-fragment contract independently of source editing and placement.
Use a small built-in provider set and a direct contract fixture to make this branch useful/testable before the palette.
Integrate it with [12](../2026-10-03_12_contextual-insertion/1_exploration.md), then broaden coverage. Neither anchors
nor existing-object manipulation is a build prerequisite of the registry itself.

Verify standards/variant parameterization, additive/subtractive intent, includes, supported library revisions,
parent/child anchors and ordinary transforms. Demonstrate a provider addition through the registry without editing
the core insertion UI. Record unavailable libraries/items honestly; arbitrary runtime application plugins are deferred.

## Branch boundary

Proposed source branch: `feature/component-provider-adapters`, without new-feature compile prerequisites. Own catalog
types, discovery, parameter schema, source-fragment generators, portable resources and provider contract fixtures.
Placement-specific integration belongs to 12. Keep vendor metadata/license/version requirements with each adapter;
do not silently bundle or auto-install every example library. Build with the shared Windows dependency set and
verify discovery from an extracted package rather than development paths. See
[branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Research and handoff

Checked 2026-10-03: the old [BOLTS repository](https://github.com/boltsparts/BOLTS_archive) points to
[boltsparts/boltsparts](https://github.com/boltsparts/boltsparts), which contains data/backend/OpenSCAD material.
The subsequent audit selected the official OpenSCAD 0.4.1 release asset still linked from the current downloads page;
its provenance is explicit despite being hosted in the archived repository. It is not an assumption about current main.

The current upstream README distinguishes the development repository from generated CAD-specific distributions.
The downloaded research-only asset and existing pinned BOSL2 copy passed the bounded call probes.
[BOSL2's screw_hole documentation](https://github.com/BelfrySCAD/BOSL2/wiki/screws.scad#module-screw_hole)
documents both threaded and clearance masks. This supports the selected threaded recipe; it does not establish a
tested native provider implementation or replace the pinned 08 bridge compatibility checks.

The contract freezes the item matrix, parameter bounds/defaults, operation/placement distinction, import scopes,
profile identity and unavailable-version behavior. Implementation must run source produced by the actual registry;
the planning probe uses hand-authored equivalent calls and does not replace that acceptance check.
