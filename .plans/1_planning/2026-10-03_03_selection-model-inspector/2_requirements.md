# Selection and Inspector requirements

Behavior and the [technical design/phases](3_overall-plan.md) are specified. Runtime surface-hit verification remains
an explicit implementation obligation. Preserve [the exploration](1_exploration.md).

- SI01: Provide one geometric selection service for Inspector and registered viewport tools. A hit exposes world
  position, surface normal, available local frame/object identity and document/evaluated-result identity.
- SI02: Distinguish a geometric hit from source provenance and semantic ownership. Missing layers remain explicitly
  unavailable; never fabricate editability, an instance path or a semantic node from a triangle/node integer.
- SI03: Support one-shot point picking and point-plus-surface picking. Success restores ordinary navigation; a miss
  keeps the tool available for another pick; explicit cancellation exits without changing the consumer's value.
- SI04: Reject stale hits after source/result/document changes. A tool cannot apply a hit from another tab or a result
  that no longer belongs to its captured request. Existing guarded document identities remain authoritative.
- SI05: The basic Inspector shows available geometric selection properties. Properties are observational until a
  consumer registers a supported edit. Contributions from provenance/hierarchy/views are owned by those features.
- SI06: Provide small interfaces for selection enrichment, Inspector contributions, transient overlays and exclusive
  viewport tool input. Navigation, annotations and measurements retain usable input routes and overlay ordering.
- SI07: Selection, visibility, solo and model suppression are distinct actions/state. Selecting an item never
  suppresses geometry or edits source. Transient origin markers are visual aids, not persisted semantic anchors.
- SI08: Define and expose renderer hit capabilities. Required position/normal behavior must be proved on supported
  preview and final-render paths; unsupported modes report unavailable rather than returning misleading substitutes.
- SI09: Compile the feature without 06/07/08/14. No consumer headers, private duplicate selection stores or placeholder
  semantic data. Contributions added later consume this service and keep its lifetime/identity rules.

## Acceptance matrix

| Case | Observable outcome |
| --- | --- |
| Translated/rotated/nonuniformly scaled object | Correct world point and normalized transformed surface normal. |
| Repeated geometry at different positions | Correct geometric target; no claimed source instance without provenance. |
| Front/back faces and overlapping geometry | Documented visible-surface selection; no hit through an occluding object. |
| High-DPI/resize/perspective/orthographic viewport | Correct screen-to-world mapping in every supported mode. |
| Miss, Escape and tool switch | No unintended value change; ordinary navigation recovers. |
| Tab switch or re-evaluation during pick | Captured request is invalidated; no wrong-document update. |
| Annotation/measurement/navigation interactions | Existing actions remain accessible; no competing drag consumers. |
| Foundation built alone | Basic Inspector and geometry picking work with no future features installed. |

## Implementation proof and shared contract

Inspect `MouseSelector::select`, `QGLView::pickObject/findObject`, renderer selection and current input controllers.
The former returns a node index; current PolySet measurement picking finds vertices/edges, not general surfaces.
The overall plan specifies a two-pass ID/depth/normal renderer, exact DTOs and lifecycle/input contracts. Its phases
must prove actual hits on supported renderers and the depth/culling/DPI transforms before consumer integration.
Prepared algorithms are not runtime evidence; a failing invariant stops that phase for correction.
