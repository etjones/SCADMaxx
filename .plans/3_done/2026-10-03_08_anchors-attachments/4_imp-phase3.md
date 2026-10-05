# Phase 3: native finalization, references and consistent output

Covers AN05-AN07/AN13-AN17/AN20. Requires phases 1/2 and 07's tested pre-publication driver.

1. Register the anchor placement pass. Resolve records/graph against the complete unfiltered native instance set;
   insert one owned transform wrapper per driven Component using K=U^-1*Dworld*U. Preserve original Part roots,
   argument values and semantic identity. Map wrappers to source invocations explicitly; do not mutate source AST
   modifier flags or copy root/highlight flags onto duplicate nodes.
2. Have 07 recompute final placements and 06 source/transform mappings before publishing the immutable result.
   Validate root-tag extraction does not discard an attachment correction; diagnose an unsupported truncated root
   rather than displaying an unplaced child. No CSG consumer can observe the intermediate unplaced tree.
3. Add AnchorResolver/AnchorOperations and register 14's anchor domain. Keep typed values distinct; frame is present
   only for a valid oriented Anchor. Invalid/missing/stale results use the specified states. Canonical drawing-frame
   selection must reject duplicate purposes and non-rigid defaults while supporting explicit rigid anchors.
4. Run the same driver for GUI, CLI and definition-default jobs. Default Assembly jobs resolve their internal relative
   graph; external absolute dependencies fail explicitly. Local Component export omits its own placement correction;
   Assembly local export retains solved child placement. Solve failures abort the new result atomically.
5. Add [anchor-resolution] and [attachment-evaluation] tests and headless CSG/export fixtures. Reuse existing geometry
   bounds/export facilities, not a new dependency on 15.

Execute the source-contract example: peg origins [20,0,10]/[130,0,10], width-a 50 -> [25,0,10] only. Compare GUI
evaluated transforms, CLI CSG and final geometry bounds. Verify pick-display semantic paths/provenance use solved
positions; old results/dirty included inputs are stale. Test Attachments declared before calls, chains, mirrors,
nonuniform ancestors, repeated Assembly definitions, root modifiers, empty Parts, cancellation and close during jobs.

Failed relation -> CLI failure/no usable export and GUI stale last-good indication; it cannot install an unplaced
current result. Hide/solo and a fake inspection effect never change solved positions/exports. Source rerun must start
from baseline placement and never accumulate corrections. Run named labels and affected 07/06/14/CLI regressions.
Exit: every output consumes the same final placement, with native geometry/source ownership intact.
