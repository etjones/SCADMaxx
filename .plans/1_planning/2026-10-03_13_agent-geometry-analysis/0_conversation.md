## Agent geometry tools: first-delivery decisions

Postponed by the user on 2026-10-04. These unresolved proposals are retained for reference, not questions currently
awaiting an answer. Resume only when requested, starting with a concrete missing capability and consumer.

Review opened 2026-10-04. Feature 15 has a local completion handoff for bounds, closed-solid area/volume and planar
sections. Feature 13 exposes guarded agent operations and may add explicitly scoped numerical services through 15.
The five recommendations below are pending user answers. They are not accepted requirements or implemented tools.

Scope correction after the user's follow-up: feature 13 concerns native geometry API operations. Reconstruction
strategy, matched-view selection and SCAD editing guidance already belong to 01. The former question 5 mixed that
workflow guidance into native scope; its replacement below asks only about additional native inference operations.
Existing camera/capture APIs should be reused. No proposed numerical extension has been approved.

Carried constraints: use the existing guarded HTTP agent surface and portable capability/skill packaging, preserve
source/result/target identity, report tessellation and tolerance, never silently repair meshes, and do not use a
universal similarity percentage as proof. Operations are observational; source edits use the existing separate tools.
Return structured measurements with optional visual evidence. These constraints do not need to be reselected.

1. What should the basic agent inspection toolkit contain?
   Recommended: bounds/dimensions, area/volume where valid, connected-component counts and mesh-validity diagnostics,
   one-plane sections and regular batches of sections along a specified axis. Return contours, holes and net areas,
   with optional SVG evidence. Reuse 15's implementations; add topology/count/batch orchestration only where absent.
   Analyse explicit live model/Part/Assembly targets or explicitly supplied reference meshes. Keep per-Part and combined
   assembly meanings distinct; do not silently union an Assembly to answer every measurement.
   Alternative: expose only 15's existing three operation families in the first delivery.

-> 

2. Should the first delivery include pairwise fit/interference checks?
   Recommended: yes. For two selected solids, report minimum surface gap when separated, contact within the stated
   tolerance, and intersection volume when they overlap. Include containment as overlap even when boundaries are
   separated. These are measurements of the evaluated solids, not a claim that a part can be inserted along a path.
   Do not label boundary distance inside overlapping/nested solids as usable clearance or invent a penetration depth.
   Alternative: defer these new numerical services and use sections/comparisons initially.

-> 

3. How should original-versus-reconstruction comparison work?
   Recommended: compare geometry in an explicitly shared coordinate frame; report bounds and volume differences,
   missing material (original minus candidate) and extra material (candidate minus original), with matching-camera
   renders/overlays. Require valid solids for material-volume comparisons. Do not automatically align, rescale or repair
   inputs, or collapse results into a universal pass score. Explicit transforms remain possible and recorded.
   Alternative: include automatic alignment as additional first-delivery work, with its own ambiguity policy.

-> 

4. Should general wall-thickness and automatic cavity analysis wait?
   Recommended: defer global minimum-thickness maps, automatic cavity classification and adaptive feature-finding
   slices. Keep explicit sections and pairwise checks in the first delivery so an agent can investigate a chosen area
   without reporting a sampled thickness estimate as an exact global minimum. Preserve the deferred families here.
   Alternative: select a specific thickness or cavity workflow to specify now before implementation planning.

-> 

5. Should dedicated native recognition/fitting remain outside the initial geometry API scope?
   Recommended: yes; no automatic STL-to-parametric conversion, primitive fitting or thread recognition in the initial
   API delivery. Agent-assisted reconstruction is already feature 01's workflow, not new native work in 13.
   Alternative: select a concrete additional numerical operation, such as fitting a cylinder to a selected region.

-> 
