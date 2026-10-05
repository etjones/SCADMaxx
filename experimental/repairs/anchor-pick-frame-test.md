# Anchor pick projection after Inspector opens

The 2026-10-05 native Anchor suite at 150% DPI failed
`nativePreviewRenderAndSolvedPicks` after moving component parameters into Inspector.
Evidence: `runs/20261005-scadmaxx-all-features/native-Anchor-scale-1.5-20261005T194252019Z`.

The test projected the target before calling `SelectionService::pick`, then projected
the returned point using the new live viewport. Picking emits selectionChanged after
the guarded read; semantic selection opens Inspector synchronously. Diagnostic run
`native-Anchor-scale-1.5-20261005T194513602Z` measured logical viewport width changing
from 920 to 648 (physical 1380 to 972). The compared X coordinates were 460 and 324.333.
This is a test coordinate-frame error, not an inaccurate surface pick.

Capture the world-to-clip matrix, physical viewport dimensions and pixel ratio before
picking. Use that snapshot to project both the input target and returned point.
Keep the existing 1.5-physical-pixel tolerance, depth, distance, normal, ownership and
F6 checks. Do not alter picking or Inspector behavior, widen the tolerance, or hide
Inspector to avoid its intended layout effect.

The narrow repair is in `src/guitests/TestAnchors.cc`. The diagnostic patch was removed;
`anchor-pick-frame-repair.patch` in the run records the tested delta against `34b3ecb50`.
It must be a separate integration repair commit and must pass Anchor at 100%, 150%
and 200% before accepting the build. Preserve the original failing evidence.

Repair commit: `dcd732fefa0aef5b12d4e5d0a2097223caf32726` in the shared source repository.
Focused repair attempt 1 passed all 12 Anchor checks at each scale; logs are
`anchor-repair-1.log`, `anchor-repair-1.5.log` and `anchor-repair-2.log`. Their test binary
was built from the parent plus exactly the subsequently committed repair patch
(SHA256 `5e54b563d80cdfdf2d650be1082bafbbf5a361c32f2e9d1082361fa8157383c7`).
