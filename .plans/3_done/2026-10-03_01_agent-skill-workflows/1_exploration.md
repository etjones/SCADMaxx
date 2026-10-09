# Enrich the distributable SCADMaxx agent skill

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Planning review: [requirements](2_requirements.md), [design and phases](3_overall-plan.md) are prepared for the bounded
delivery. See the [readiness audit](../../1_planning/2026-10-03_00_source-first-cad-overview/planning-readiness.md) for source evidence.

Original exploration status: planning. Source: chat E in the [overview](../../1_planning/2026-10-03_00_source-first-cad-overview/1_exploration.md).

## Purpose and decisions

Augment the existing generic SCADMaxx skill with useful concepts from other CAD skills. The user explicitly wants
integration, not replacement. ParametricDesigns rules, catalogs, ownership and private project paths must stay out.
The bundle must be distributable with SCADMaxx and work outside this workspace.

Preserve capability detection, installed BOSL2 revision checks, supported edge helpers, Customizer dialect knowledge,
two-pass modeling and guarded live-agent operation. This follows the
[completed skill feature](../2026-10-02_scadmaxx-skill/1_exploration.md).

## Workflow structure proposed in the final exchange

Separate four independent dimensions: task intent (create/source-edit/mesh-edit/reconstruct/replicate/inspect),
operating surface (live SCADMaxx or verified CLI), evidence (preview/validated geometry/fabrication-ready output),
and interaction policy (reversible assumptions or requirements-driven work).

These are branches and policies, not persistent modes. Refinement is the normal inspect/change/render/compare loop.
Export is a completion phase; live HTTP is an observation/control mechanism. Interaction policies must respect the
user's explicit instructions, including stopping after questions.

Teach design reasoning before API syntax: requirements, functional interfaces, frames/datums, envelopes and voids,
mating surfaces, repetition/symmetry, natural construction, parameters/invariants, then evidence. Consider primitives,
profile extrusion, rotational profiles, sweeps/lofts, shells and hybrid imports. Keep the base-geometry pass followed
by detail/edge treatment inside applicable workflows.

## Details to retain

- Source modification preserves design intent and obtains baseline evidence before editing.
- Local STL changes use an imported-mesh wrapper and local CSG where appropriate. Editable parametric reconstruction
  is a separate inverse-modeling task; do not reconstruct a whole object just to enlarge a hole.
- Mesh reconstruction: analyze first, infer axes, inspect slices, separate outer contours and holes, recognize
  primitives, name dimensions, compare identical cameras/overlays and actual meshes. Hybrid reconstruction is valid.
- Image replication: inspect all references, establish scale from a known dimension, distinguish inferred dimensions,
  identify proportions/features/symmetry, model rough form, match the reference camera, compare and refine.
- Visual verification: broad initial coverage, repeat cameras plus affected views during changes, final coverage of
  important interfaces. Select views that reveal errors instead of requiring six views universally.
- Inspection includes bounds, dimensions, volume, components, watertightness, holes/cavities, thickness, sections,
  clearances, interference, feature locations, symmetry and parameter sensitivity. Printability is one optional use.
- Measure exact geometry when possible instead of visually estimating measurable quantities.
- Separate source validity (parse/dependencies/assertions), geometry validity (nonempty/bounds/topology/features),
  and intent validity (requested form/interfaces). A watertight mesh or matching bounding box is insufficient alone.

Do not adopt universal subtraction-from-one-solid rules, a fixed 95% reconstruction target, or mandatory view counts.
Deliberate semantic reconstruction, such as replacing triangulated threads, needs intent-aware comparison.

## Documentation and tool boundary

Keep `skills/scadmaxx/SKILL.md` short. Proposed references are `task-routing.md`, `design-reasoning.md`,
`mesh-editing.md`, `reverse-engineering.md`, `visual-verification.md`, and `inspection.md`. Augment `modeling.md` and
`validation.md`; preserve maintained edge-treatment, Customizer, capability and agent references.

Retain server/document/source/result/viewport guards, wrong-tab and dirty-buffer protection. Annotation corrections
use the same fresh-result/evidence loop. Adaptive slicing, primitive/feature extraction, mesh differences/IoU,
thickness and interference need real tools in [13](../../1_planning/2026-10-03_13_agent-geometry-analysis/1_exploration.md).
Skill instructions must not promise unavailable tools.

## Research leads from the chat

- [andreahaku/openscad_claude_skill](https://github.com/andreahaku/openscad_claude_skill): workflow distinctions,
  reconstruction, image replication and comparisons.
- [swh/openscad-skill](https://github.com/swh/openscad-skill): BOSL2 conventions and API pitfalls.
- [jmwright/cadquery-llm-skill](https://github.com/jmwright/cadquery-llm-skill): separate geometric reasoning from APIs.
- [mojzis/skill-build123d](https://github.com/mojzis/skill-build123d): natural-language geometry decomposition.
- [gladfelter OpenSCAD skill](https://github.com/gladfelter/agent_skills/blob/master/skills/openscad/SKILL.md):
  systematic visual feedback.
- [ModelRift/openscad-skill](https://github.com/ModelRift/openscad-skill): cross-agent distribution.
- RobertCoop's OpenSCAD MCP: numerical inspection inspiration; verify the exact repository and operations.

CAD-Bench-Claude-Skill, freecad-ai, opengis-skills and a Roblox-oriented solid-modeling skill were secondary leads.
These are research candidates, not selected dependencies. Verify current source and reuse terms before adapting.

## Branch and delivery boundary

This is a control-repository feature on proposed `feature/agent-skill-workflows`, not an OpenSCAD source-stack entry.
Own `skills/scadmaxx`, its references/tests and the companion build/delivery hook. The existing application Stage
only copies the source HTTP skill bundle; it does not package this control-owned skill automatically. Deliver the
versioned companion ZIP alongside the application and tie its capabilities/canonical documentation to the frozen
integrated source. Keep generated documentation tied to its source revision, not separately hand-maintained.
See the [branch integration design](../../1_planning/2026-10-03_00_source-first-cad-overview/3_overall-plan.md) for the two-repository
handoff. Update tool guidance as implemented capabilities arrive, without delaying the initial reasoning improvements.

## Order and evidence

Start immediately without native feature prerequisites. Exercise representative tasks from every branch, checking
preserved safeguards, appropriate evidence and honest capability limits. Test the bundle outside this workspace.
