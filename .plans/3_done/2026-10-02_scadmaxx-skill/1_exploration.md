# SCADMaxx agent skill

Status: implemented; see post-implementation notes for verification and limits.
Requested on 2026-10-02 as a broader home for agent guidance,
including documentation for the OEP8-compatible Customizer annotation patch.

## Purpose and scope

Provide a reusable skill for agents using SCADMaxx to author, inspect and validate parametric
OpenSCAD models. Cover ordinary product use as well as the additional capabilities shipped
in SCADMaxx. Keep the skill useful for models that do not use experimental language features.

Include guidance for:

- Structuring and parameterizing models, selecting relevant language features and reading diagnostics.
- Using BOSL2 as the default modeling library and establishing the conceptual shape before edge treatments.
- Modeling bevels/chamfers and fillets/roundovers, including approach selection and dimensional checks.
- Previewing, rendering and exporting, with checks appropriate to the requested deliverable.
- Customizer design, supported annotations, and parameter-dependent visibility/locking.
- OEP8 objects versus object(), including the restricted annotation subset.
- Using the shipped HTTP agent server and other automation capabilities when the task benefits from them.
- Checking the actual installed build's capabilities and choosing compatible alternatives when needed.
- Following an explicit agent workflow, including safe targeting when multiple documents are open.
- Distinguishing SCADMaxx capabilities from mainstream OpenSCAD releases and development snapshots.

Keep source development, private repository management and SCADMaxx release composition in the
existing workspace workflows. Product users should not need this development workspace or its paths.

## Agent workflow and multiple documents

Document a repeatable discover -> target -> inspect -> edit -> preview -> render/export -> validate
workflow, choosing the HTTP API, CLI or UI according to the actual available capabilities. Verify
document and operation semantics against the shipped implementation rather than assuming API support.
The full agent API uses `/v1` with direct HTTP access and no shipped Python client; use the
[direct-HTTP follow-up](../2026-10-02_agent-direct-http/5_post-implementation-notes.md)
as the current source handoff. It has no source-write, tab-switch, save or forced preview/render endpoint.
Explain how file-based editing and observed native reload fit those limits; do not invent HTTP operations.

- Discover application instances and open documents; identify the intended target using available
  document identities and paths, including untitled documents and similarly named files.
- Distinguish the active editor tab from the document targeted by an API or CLI operation. Establish
  whether an operation uses the in-memory buffer or the saved file, and handle unsaved edits and
  external file changes without overwriting unrelated work.
- Explicitly target edits, preview, rendering, exports and diagnostics wherever supported. If an
  operation requires activation, verify the active document before acting and preserve other documents.
- Associate results and asynchronous job completion with the intended document and source revision;
  detect stale results after edits or tab changes and inspect errors before retrying.
- Avoid silently closing, saving or replacing unrelated documents. Explain recovery from missing or
  closed targets, failed operations and unavailable automation, including safe CLI alternatives.

## SCADMaxx versus mainstream OpenSCAD

Provide a versioned capability comparison covering mainstream stable releases, relevant upstream
development snapshots and the matching SCADMaxx build. Distinguish upstream functionality, selected
unreleased PRs, SCADMaxx additions and changed behavior; do not equate upstream master with a stable release.

- Cover language syntax, Customizer behavior, rendering backends and exports, HTTP automation,
  annotations and relevant UI features. State prerequisites, feature flags and platform limits.
- Record the compared versions/builds and evidence for each difference. Separate implemented or
  selected source features from features actually present and enabled in the installed executable.
- Explain capability discovery using available version information, feature reporting and small
  non-destructive probes. Treat unknown support as unverified rather than inferring it from branding.
- Label examples by their required capabilities, offer mainstream-compatible alternatives where
  practical, and explain portability limits when a model or workflow relies on SCADMaxx extensions.
- Keep comparisons synchronized with the distributed skill and build as upstream support evolves.

## Proposed home and documentation ownership

Author the product-owned skill at `skills/scadmaxx/SKILL.md` in the SCADMaxx control repository.
Keep the entry point concise and route to supporting references only when relevant. Avoid a separate
Customizer-only or experimental-language-only skill and avoid expanding AGENTS.md into a user manual.

Maintain feature semantics beside their implementation. The #6642 variant already includes
`doc/customizer-attributes.md`, committed in source revision
`8ea44273775f3c7720f2ff607e6d4ea5215422a6`. Complete that reference as part of this feature and
keep future language changes and documentation in sync. The skill should reference the same maintained
material; a distributable skill bundle may include a versioned copy generated from the selected source.
Avoid separately hand-maintained copies of the syntax specification.

Package a self-contained skill bundle with SCADMaxx or as a matching companion artifact. Resolve that
packaging detail during implementation. The bundle must work outside this workspace, with relative
references and documentation matching the shipped build. Installation/discovery for supported agents
is part of this feature; writing into a user's agent configuration requires their chosen installation action.

## Required #6642 and OEP8 documentation

- Explain `@{ key: expression, ... }` and attachment to the immediately following assignment.
- Document fixed identifier keys, commas, optional trailing commas and empty blocks.
- Provide an attribute table covering supported names/aliases, accepted values, widget effects,
  defaults and evaluation timing, verified against the actual implementation.
- Explain that fixed keys do not require literal values: hidden/locked remain reactive, while other
  attributes configure the widget initially. Include ordinary and special-variable examples across includes.
- Distinguish ordinary OEP8 objects and object() from annotation metadata. Computed/quoted keys,
  `each`, and comprehensions are excluded from annotations; ordinary objects retain their own syntax.
- Provide complete runnable examples, common errors, and the migration from the original `key = value;`
  annotation spelling. Identify which builds support the new syntax and how to recognize older builds.
- Keep empty-group visibility a separate feature; do not imply it is part of this syntax patch.

## Required modeling approach: BOSL2 and two passes

Put the following rules in the main skill entry point so they apply before an agent selects a modeling
technique. Keep detailed helper selection, examples and limitations in the modeling/edge-treatment references.

- Use BOSL2 as the default modeling library for general model construction, not only edge treatments.
  Reuse its primitives, attachment facilities and relevant geometry helpers instead of reimplementing
  functionality it already provides. Use ordinary OpenSCAD constructs where they are the straightforward
  building blocks of that design; do not introduce complexity merely to use a library call.
- Check the available BOSL2 installation and the documentation for that revision before using its APIs.
  If BOSL2 is missing, install it from its official upstream source into a library location resolved by
  the intended OpenSCAD/SCADMaxx instance. Installation is part of the modeling workflow and does not
  require a separate confirmation merely because the library is absent. Preserve existing installations
  and local modifications, record the installed revision, and verify a minimal include-and-render example
  with the target executable before proceeding. Request permission only if an actual environment access
  restriction requires it; report a concrete installation failure rather than silently abandoning BOSL2.
  Use its supported chamfering, rounding and filleting helpers for edge treatments. Do not manually
  construct rings, profiles or vertex meshes and loft them with `skin()` to manufacture chamfers or fillets.
  Choosing BOSL2's `skin()` for that hand-built workaround does not satisfy the requirement to use its
  dedicated helpers. This rule concerns edge treatments, not legitimate lofted model bodies.
- First pass: approximate the conceptual shape using simple, readily editable geometry. Establish the
  silhouette, proportions, component arrangement, major cutouts and functional interfaces. Keep nominal
  dimensions and mating constraints explicit even while simplifying the shape. Inspect it from useful
  viewpoints and resolve structural mistakes before adding edge details.
- Second pass: apply the intended chamfers and fillets using BOSL2 helpers once the base form is sound.
  Keep edge-treatment parameters separate from the base dimensions and retain a way to inspect the
  untreated form. Choose a base construction that can accept those treatments without a wholesale rewrite.
  Recheck the envelope, wall thickness, clearances and selected edges after adding treatments.
- If BOSL2 installation is blocked or no suitable helper supports the requested treatment, state the specific
  limitation. Do not silently replace the intended approach with bespoke `skin()` geometry. Prefer a
  simpler supported construction where it meets the request; surface any remaining unmet requirement.

The two passes are a modeling sequence, not an automatic user-approval gate between them. Continue through
both when the requested form is clear; ask only when an unresolved design choice actually needs user input.

## Bevels and fillets exploration

Explore practical guidance for bevels/chamfers and fillets/roundovers as part of ordinary modeling,
not only experimental features. Cover:

- Distinguishing flat bevels from rounded fillets, inside versus outside corners, and rounding a 2D
  profile versus selected edges of a 3D solid.
- Selecting the appropriate verified BOSL2 helper for the shape and intended edges. Explain when a
  profile-first construction makes its supported treatment simpler. Discuss native offsets, hulls or
  Minkowski operations only where they have a concrete advantage or fill a verified library limitation;
  do not present them or hand-built lofts as interchangeable defaults with BOSL2's dedicated helpers.
  Do not assume a general arbitrary-edge fillet operator is available.
- Preserving nominal dimensions, wall thickness, mating clearances and the intended edge selection.
  Explain radius/width conventions and how operation order affects the result.
- Handling convex and concave corners, intersecting blends, small features, excessive radii,
  degenerate geometry and self-intersections.
- Comparing local edge treatment with whole-solid rounding, including tessellation and render cost.
  Account for manufacturing and print-orientation constraints when relevant to the deliverable.
- Providing runnable examples and geometry checks across different dimensions and radii, including
  zero and limiting cases. Validate rendered/exported geometry as well as preview appearance.

## Acceptance and implementation outline

Inventory the product's existing documentation and capability reporting, then write a short skill entry
point and the references needed for real modeling and automation tasks. Use authoritative OpenSCAD
documentation for the established language and document SCADMaxx differences explicitly.

Validate the skill structure and reference links. Exercise representative tasks from the bundle alone:
an ordinary parametric model, a beveled/filleted model with dimensional checks, a model with reactive
Customizer annotations, object/object() usage, and a render/export or automation task.
For modeling tasks, verify BOSL2 is used where applicable and that the agent establishes and inspects the
base form before adding edge treatments. Retain untreated and finished examples with dimensional checks;
inspect the source to confirm chamfers/fillets use supported helpers rather than manually constructed
`skin()` meshes. Include a missing-library case that requires installation and verifies loading/rendering
with the target executable. Include an unsupported-helper or blocked-installation case to check that
concrete limitations are reported rather than hidden behind a custom workaround.
Include a multi-document task with unsaved edits and active-tab changes, checking that operations and
results stay associated with the intended target and unrelated buffers remain intact. Exercise capability
detection and fallback behavior against identified mainstream and SCADMaxx builds; report unavailable
comparison builds as validation gaps rather than claiming compatibility.
Compile runnable examples against the matching build and
verify that an agent does not assume experimental capabilities exist in every OpenSCAD installation.
Test the packaged bundle from a directory outside the development workspace.

Existing implementation and test evidence:
[OEP8/Customizer handoff](../2026-10-02_oep8-customizer-syntax/5_post-implementation-notes.md).
The language patch is already selected and verified; this skill/documentation feature is separate work
and does not reopen its implementation or delay existing selected builds.
