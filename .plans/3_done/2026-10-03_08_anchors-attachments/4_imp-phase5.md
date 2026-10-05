# Phase 5: inspection, capture and explicit source authoring

Covers AN01/AN02/AN04/AN09/AN11/AN18-AN20. Requires current result/reference services and 02/06/14 ownership guards.

1. Add AnchorController/InspectorContribution/Overlay. Show reference type/name, owner, source, frame/position and
   validity; distinguish parametric definition anchors from Fixed local/document captures. Helpers use 03 overlays,
   not model geometry/hit IDs. Reference selection does not alter eye/solo state or start a source transaction.
2. Implement Pick anchor via 03 routing and camera-up convention. Keep drafts transient; Save anchor creates one root
   assignment with explicit selected Component owner/full path or document ownership, stable ID and literal local
   values. Use 14 lifecycle undo with 02 source insertion. Reject stale/ambiguous inverse-owner capture honestly.
3. Implement AnchorSourceEdits for permitted label and literal adjustment patches and Attachment offset/spin/mode
   controls. Preserve base expressions and other source bytes. Require the explicit Edit shared declaration action
   before changing a declaration used by several invocations; show its actual use count. Closed/read-only/library
   owners stay source-only until the owner file is explicitly opened for editing.
4. Implement source navigation and pure validateAttachmentDraft/solvePlacement entrypoints for later 10/12. Do not
   build provider menus, full attach-by-drag/insertion controllers or drawing layouts in this phase.
5. Add [anchor-source-edits] unit cases and native TestAnchors runner with OPENSCAD_ANCHOR_TESTS_ONLY.

Native cases: pick known Part and anonymous geometry; normal/up correct under rotated/scaled/mirrored owners; singular
Save disabled; point remains transient until Save; move camera after Save and preserve up; source remains unchanged
on cancel. Reopen saved source, undo/redo promotion including draft lifecycle, select hidden owner and keep it hidden.

Parametric position width/2 and attachment offset expressions survive numerical adjustment edits verbatim. Test
UTF-8/CRLF/comments/computed object RHS, read-only files, closed tabs, stale results, concurrent source/include change
and widgets destroyed mid-edit. Shared Assembly declarations cannot be mutated through an unlabeled instance edit.
Interleave source/annotation/anchor undo and, when composed with 05, a Vim insert session and external transaction.

Run [anchor-source-edits], native TestAnchors and affected 02/03/06/14/Customizer checks. Exit: source is the sole
persistent authority, one undo step corresponds to each committed action and failures have no partial mutation.
