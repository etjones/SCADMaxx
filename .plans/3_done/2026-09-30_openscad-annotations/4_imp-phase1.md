# Phase 1: build and integration foundation

- [x] Verify clean annotations branch, initialized submodules and applicable instructions.
- [x] Configure Windows Qt6/MSVC/vcpkg build with existing dependency installation.
- [x] Build baseline, diagnose and repair upstream/MSVC integration failures. Complete application links; final notes distinguish baseline repairs from annotations.
- [x] Identify lifecycle, undo, capture and dock insertion points; native container-undo spike passed.

Record configure/build logs under `runs/annotations-implementation/`. Native undo uses QScintilla container tokens;
source reload drops the tokens while retaining the store. Sidecars use bounded ZIP entries with a JSON manifest.
