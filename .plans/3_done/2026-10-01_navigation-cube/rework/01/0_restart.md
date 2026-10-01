# Fix forward: cube click jitter

Trigger: clicking Front sometimes rotates slightly and stops short of the exact front view.
Requirements R05/R07 remain valid; this is a bounded input-tolerance correction, with no rollback.
Starting source: `c54886b822ed39ff91369c335472788f106e2c50`.

The native pointer regression reproduces the report: a stationary click completes its snap, while a click moving
3 logical pixels on each axis enters free orbit because Manhattan displacement 6 exceeds the old threshold 4.
Earlier all-target coverage called `snap()` directly and therefore missed pointer click/drag arbitration.
Evidence: `D:/openscad/runs/navigation-cube/phase6/click-diagnostic/test-results.xml`.

Correction: initialize the session drag threshold from `QApplication::startDragDistance()` (10 logical pixels on
the tested Windows profile), preserving the existing live override. Do not disable orbit or change snap animation.
Acceptance: real stationary and slightly jittered Front clicks reach the exact orientation with animation enabled;
intentional drags, disabled orbit and release-outside behavior retain their existing native checks.

Status: complete. Commit `0ff82ec81d46e06c1e15047233c3b2e488d4cc92`; private origin verified at that SHA.
All 15 native cases pass at 100%, and the separately staged runtime passes at simulated 150% with system-only PATH.
Evidence: `runs/navigation-cube/phase6/click-fixed` and `click-fixed-staged150`.
Runnable build: `D:/openscad/artifacts/openscad-navigation-cube-click-fix-win64/openscad.exe`.
The previous application directory is preserved; restart using this executable to obtain the corrected default.
No annotation composition changes were required; the previous composition evidence remains at its recorded revision.
