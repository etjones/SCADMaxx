# Windows GUI test sleep

Discovery: navigation-cube phase 1, GUI tests enabled on upstream `464e25dad` with MSVC 19.51.
`TestModuleCache.cc:44` calls POSIX `sleep(1)` without a Windows implementation and fails with C3861.

Repair: `67884e65f` in the shared OpenSCAD repository replaces it with `QTest::qSleep(1000)`.
The test already includes QTest; this preserves a blocking one-second timestamp delay without adding a dependency.

Failure log: `D:/openscad/runs/navigation-cube/phase1/20261001T143107-Build.log`.
Verification: GUI-enabled Release build passed; all 119 baseline unit cases passed. The native navigation harness also
links and runs with Qt Test enabled. The unrelated module-cache GUI test itself has not been executed by this feature.
