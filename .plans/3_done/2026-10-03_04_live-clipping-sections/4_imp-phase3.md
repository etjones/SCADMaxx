# Phase 3: picks, normal dragging and rotation

Covers CL04/CL05/CL07/CL11 with 03's actual tool/overlay contracts.

1. Register Pick point / Pick + align as one-shot router tools. Validate captured Stamp and convert world hits into
   the Section frame. A miss retains tool availability; cancel leaves the prior value; stale failure ends the tool.
2. Implement SectionManipulator using closest ray/axis points and ray/ring-plane signed angles. Handle parallel
   degeneracy without jumps. Keep rotation pivot fixed and transport drawing up consistently; Shift snaps 15 degrees.
3. Register plane helper and origin marker with 03 overlays. Depth bias is visual only and never enters source or
   shader plane parameters. Keep helpers out of hit buffers.
4. Native cases: pick/align on outside and cavity walls, rotated/mirrored models, move after rotation, negative offset,
   flip twice, angle poles, near-parallel gizmo drag, Escape mid-drag, tab/source/result change and owner destruction.
5. Verify navigation/annotation/measurement tools can replace/cancel clipping ownership and recover their normal
   gestures. One gesture produces at most one source undo action; 100 move events produce no model evaluations.

Exit: all seven exploration workflows are represented by passing native cases and expected source/geometry outcomes.
Run TestClipping, TestSelection routing and existing navigation/annotation regressions.
