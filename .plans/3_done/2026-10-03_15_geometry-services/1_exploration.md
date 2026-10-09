# Shared geometry measurements and section computation

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Planning review: [requirements](2_requirements.md), [design and phases](3_overall-plan.md) are prepared for the bounded
core. Use strict analysis conversion, explicit units/frames and documented slice boundary behavior. See the
[readiness audit](../../1_planning/2026-10-03_00_source-first-cad-overview/planning-readiness.md) for source evidence.

Original exploration status: planning. Extracted during the 2026-10-03 branch-composition review from the shared needs of features 09/13.
This is an implementation boundary derived from the chats, not an additional user-facing feature request.
See the [branch integration design](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md).

## Purpose and scope

Give drawings and agent tools one tested implementation of reusable geometry calculations. Persistence defines a
Section; this service computes its intersection with supplied geometry; the clipping renderer displays a half-space.
Those are three separate responsibilities. Neither drawings nor analysis tools should own the other's prerequisites.

Start with bounds/basic measurements and arbitrary-plane section contours, including holes and disconnected contours.
Specify units, frame, precision, degeneracies and invalid/open-mesh behavior. Extend shared operations only for a
concrete consumer. Hidden-line presentation, dimension layout, reconstruction orchestration and interactive clipping
remain outside this service.

## Branch boundary

Proposed source branch and stack ID: `feature/geometry-services` / `geometry-services`.
It builds on the selected upstream geometry baseline without a Qt dock, document editor, semantic hierarchy or HTTP
server prerequisite. It must be usable and testable before drawings or analysis UI is implemented.

The service accepts immutable geometry and explicit transforms/plane values. Callers supply target/result identity
and retain it with the returned result; the service does not read active windows or create a second document registry.
Callers resolve semantic targets, schedule work and reject stale results. Results expose contours/measurements and
diagnostics rather than screen pixels or drawing-layout objects. Shared value types belong here, not in a consumer.

Reuse existing Geometry/PolySet/Polygon2d and selected Manifold/CGAL facilities. The inspected integrated source has
`ManifoldGeometry::slice()`/`project()` and `GeometryEvaluator::projectionCut()`; this is evidence for reuse, not proof
that arbitrary-plane sections or all target backends are already supported. Transform and validate those facilities
behind this branch's contract rather than duplicating projection CSG in each consumer.

The source branch owns implementation, public headers, CMake registration and numerical fixtures. Future changes to
this shared API return to this branch before consumers adopt them. No consumer-local fork or copied geometry kernel.

## Consumers and build requirements

- [09](../../1_planning/2026-10-03_09_technical-drawings/1_exploration.md) builds vector sections and dimensions on these results.
- [13](../../1_planning/2026-10-03_13_agent-geometry-analysis/1_exploration.md) exposes analysis and reconstruction workflows.
- [04](../2026-10-03_04_live-clipping-sections/1_exploration.md) may consume it for a later computed-section action;
  first live GPU clipping does not require it.

Use the existing shared Windows dependencies. A proposed library unavailable in that installation is a design/build
issue to resolve explicitly, not permission for an automatic install or private dependency tree. Keep backend
capabilities explicit; do not label tessellated approximations universally exact.

## Merge acceptance

Build this delta on its recorded upstream/required-repair base, then replay it into the selected SCADMaxx composition.
Verify known-dimension solids, holes, oblique/transformed planes, multiple contours, degeneracies, open/invalid meshes,
and scale/tolerance behavior. Unit fixtures must work without a live GUI/server. Preserve ordinary projection/export
behavior. Include numerical definitions and backend limits with the feature handoff.
