# Native geometry-analysis API and optional numerical extensions

Status: postponed by the user on 2026-10-04. No concrete additional consumer/workflow has been established to justify
the broad proposed feature. Existing native cross-sections already use the in-memory model; agent guidance belongs
in 01 and numerical services in 15. Any future API exposure should first demonstrate a specific need and reuse them.
No scope choice was accepted, no implementation is scheduled and no other active feature waits for 13.

Preserve the exploration and [unresolved decision review](0_conversation.md) for a user-requested resumption.
The proposals below are dormant, not an active work queue. Shared basic algorithms have a local implementation handoff
in [15](../../3_done/2026-10-03_15_geometry-services/5_post-implementation-notes.md). See the
[readiness audit](../2026-10-03_00_source-first-cad-overview/planning-readiness.md).

Source: chat E in the [overview](../2026-10-03_00_source-first-cad-overview/1_exploration.md).
This track was proposed separately from skill prose so the skill does not promise operations without actual tools.

## Purpose and scope

Expose application-computed geometry evidence through the existing guarded native HTTP API. A concrete request could
measure one evaluated Part or obtain section contours at an explicit plane, with source/result identity and units.
Agents can use that evidence for inspection or reconstruction; the strategy they follow belongs to feature 01's skill.
Keep generic SCADMaxx distribution free of ParametricDesigns-specific infrastructure.

Scope clarification, 2026-10-04: the user challenged the mixing of agent instructions and native features in the five
proposals. The reconstruction workflow proposal duplicated 01 and is withdrawn as a native-feature decision.
Choosing views, using hybrid models, writing/refining SCAD and interpreting intended differences are skill guidance.
The remaining proposals for new numerical operations are still unaccepted; this clarification approves none of them.

| Owner | Responsibility |
| --- | --- |
| 15 | Reusable native numerical services; bounds, solid measurements and sections already have a local handoff. |
| 13 | Application/API access to explicitly selected numerical services: evaluated target binding, guarded requests, results, limits and discovery. |
| 01 | Agent instructions for choosing tools, planning edits/reconstruction and interpreting measurements/images. |

The retained HTTP contract at D:/openscad/wt-openscad-http-agent-server/contrib/openscad-agent-server/HTTP.md,
lines 175-176 at this review, explicitly advertises no bounds/volume/validity/geometry-summary capability. Its existing
camera/capture endpoints already support obtaining comparable views; repeating that workflow is not a new 13 feature.
15's actual GeometryAnalysis.h exposes bounds, measureSolid and section without HTTP/document state. Thus the API
connection is real missing native work, distinct from adding clearance/comparison/fitting algorithms. Recheck actual
capabilities at implementation preflight; do not duplicate a subsequently implemented endpoint.

Candidate capabilities from the chat:

- Bounds, dimensions, volume/surface area, connected components and watertight/manifold checks where applicable.
- Cross-sections, including adaptive multi-axis slicing, contours, holes and possible SVG evidence.
- Cavities, thickness, clearances and interference, including assemblies once semantic targets are available.
- Mesh-to-mesh comparison, boolean differences or suitable overlap/distance measures; optional IoU for appropriate tasks.
- Feature/primitive recognition, likely extrusion-axis detection and parametric fitting for reconstruction.
- Same-camera renders/overlays to compare original and reconstruction, plus quantitative checks beyond bounding boxes.

These are candidate tool families, not a promise that a single first release implements all of them. Choose actual
operations and numerical definitions during requirements work; preserve every family as intended exploration scope.

## Design constraints

- Reuse existing CLI/native geometry and HTTP observation facilities where appropriate; inventory actual support first.
- Numerical analysis needs the intended evaluated/exported geometry, document/source/result identity and units.
  A screenshot alone cannot establish precise wall thickness or interference.
- Report tolerances, tessellation effects, invalid input, unsupported cases and result uncertainty.
- Distinguish exact methods from sampled estimates. A score is evidence, not universal proof of intent.
- Avoid a universal 95% mesh-match gate or assuming equal bounding boxes imply equivalent solids.
- Recognize intentional semantic changes such as replacing faceted thread meshes with parametric threads.
- Keep tools useful to local mesh edits/hybrid reconstruction; instructions for choosing those workflows stay in 01.
- Package dependencies and helpers reproducibly for product users; do not depend on private repository paths.

## Research and feature relationships

E identifies andreahaku's scripts for slicing/reconstruction/comparison and RobertCoop's OpenSCAD MCP operations for
measurements/cavities/sections/clearance as useful leads. See the links in
[01](../../3_done/2026-10-03_01_agent-skill-workflows/1_exploration.md). Verify implementation, reuse terms and platform/dependency
cost before choosing a backend or copying tools. Other MCP implementations were mentioned as mostly render/export
wrappers; their inclusion was not a decision to install or expose multiple servers.

Live clipping (04) is a viewer facility. Shared geometry measurements and section computation belong to
[15](../../3_done/2026-10-03_15_geometry-services/1_exploration.md), with Section/View definitions in
[14](../../3_done/2026-10-03_14_design-object-persistence/1_exploration.md). This feature consumes those APIs independently of
drawings (09), exposing guarded tool operations and analysis/reconstruction workflows. Semantic assembly inspection
uses 07/08. Basic numerical work can ship first as 15 rather than making this feature own an early shared kernel.

## Suggested order and evidence

Start the inventory alongside skill enrichment and develop numerical primitives in 15. Build the agent-facing branch
on the shared geometry, reference and design-object contracts. Add reconstruction/comparison workflows in bounded
slices; update skill guidance only when the matching tools ship. Reuse the selected guarded HTTP server for the
native tool surface. A CLI/helper entry point can invoke the same services if useful; it must not create a second
independent document/session authority or a dependency on a private Python environment.

Use known-dimension solids, cavities, thin walls, disconnected/invalid meshes, intersecting and separated assemblies,
and intentionally altered reconstructions. Check units, tolerances, false positives, stale identity, reproducibility
and packaged execution outside this workspace. Validate source, geometry and intent separately.

## Branch boundary

Proposed source branch: `feature/agent-geometry-analysis`, with 08/14/15 and the selected HTTP agent server as direct
prerequisites. Own tool orchestration, semantic-target selection, result/evidence reporting, capability discovery
and source-owned API documentation/tests. Shared numerical algorithms go through 15; drawing code is not imported.
The source branch carries required API resources/install rules, with any extra release-script work in a paired
control commit. Test cancellation, stale result/target guards and access from the extracted application package.
See [branch integration and handoff rules](../2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Required operation matrix

The current decision review proposes basic inspection/section API tools, pairwise gap/interference, and explicit-frame
material comparison. It proposes deferring general thickness/cavity automation and native automatic recognition/fitting.
These are recommendations awaiting the user, not scope reductions already decided. Preserve every candidate family
above. Existing constraints on guarded API use, source authority, explicit uncertainty and portable distribution remain.
Agent-assisted reconstruction is already 01 scope and is not an additional native implementation deliverable here.

15 already provides bounds, solid measurements and arbitrary-plane contours with hole classification. It does not
yet provide connected-component reports, pairwise distance/intersection or material-difference comparison. A selected
new algorithm needs a concrete 15-owned extension and verification; 13 must not copy a private numerical backend.
The completed service rejects unresolved GeometryList aggregates. Assembly operations must explicitly choose Part
targets/per-Part results or a specified combined-solid operation; never infer a union from the word Assembly.
Reference-file ingestion, job limits/cancellation, tolerance defaults and schema details remain technical design work
after the operation scope is settled. No additional CLI, MCP server or geometry dependency is selected by this review.

For each first-release operation, specify input target/revision, accepted geometry, units, algorithm, exact versus
sampled meaning, tolerances, invalid/open-mesh behavior, limits/cancellation and result/evidence schema. Distinguish
15's supported bounds/solid measurements/sections from new work such as minimum thickness, signed clearance,
interference volume, mesh-distance distribution or reconstruction fitting. These names imply different algorithms.

Define reproducible positive/negative fixtures, including false positives and deliberately changed semantic features.
Map operations to the existing guarded HTTP server and packaged capability documentation; choose CLI duplication
only for a concrete use case. Scope reconstruction into a bounded workflow rather than an "automatic CAD inference"
task. No fixed similarity percentage proves every reconstruction correct.
