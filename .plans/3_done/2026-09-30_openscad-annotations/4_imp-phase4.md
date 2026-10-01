# Phase 4: drawing, capture and review

- [x] Publish render ownership/input identity at evaluation/install boundaries.
- [x] Add dock, review/search/thumbnail, comment edit/delete and camera restoration.
- [x] Add draft overlay, palette, stroke history, navigation locking and input cancellation.
- [x] Capture native framebuffer and composite strokes with the overlay painter; validate DPR and target revision.
- [x] Native viewportWorkflow passes; capture and fresh PNGs visually inspected. Camera lock, no historical strokes in fresh capture, selection neutrality and resize cancellation verified.

Final audit passes cross-tab routing, 100/125/150/200% scaling, Add/Back/Cancel/empty acceptance and F6 capture.
Hidden Windows tests drive real GL painting; they
acknowledge frameRendered through a queued connection rather than relying on compositor swaps.

Exit: complete manual draw/comment/review/save/reload/restore flow without stale image ownership or palette capture.
