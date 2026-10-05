# Phase 3: tie companion delivery to the application

Covers SK03, SK07-SK10. Depends on phases 1-2, not on unimplemented native features 03-15.

1. Extend `Save-ControlSnapshot` to capture authored skill inputs and its runbook. Verify their hashes appear in the
   existing snapshot manifest and that later live-file changes do not alter frozen inputs.
2. Wire Stage before build-info/inventory finalization, using the frozen builder and the actual integrated source.
   Record companion metadata in build-info; wire Package to verify and copy that artifact alongside the application.
3. Exercise these hooks through the existing build-script test/dry-run facilities where available; otherwise use
   focused temporary run/snapshot fixtures. Extract functions as needed rather than triggering an unrelated full build.
   Verify a missing/changed companion prevents successful Package and the existing HTTP skill is still delivered.
4. Extract the completed skill ZIP outside the repository. Run `Test-ScadmaxxSkill.py --help` to confirm arguments,
   then use its existing `--skill`, `--openscad`, `--extended`, `--bosl-parent` and `--output` options with explicit
   recorded paths and the intended SCADMaxx binary/library. Inspect results, not just exit status.
5. In the next explicitly requested real application composition, verify the delivered companion's source SHA and
   hashes match build-info and the frozen manifest. Record this as release integration acceptance if unavailable now;
   do not claim a fixture proves a real release. Update `docs/scadmaxx-skill.md` with the actual invocation.

Exit: builder and lifecycle fixtures pass, portable skill smoke checks pass against a known supported binary, and
any outstanding real-release acceptance is explicit. No user installation, promotion, push or enabled-stack edit.
Record owned control changes, source/control provenance and checks in `5_post-implementation-notes.md` on completion.
