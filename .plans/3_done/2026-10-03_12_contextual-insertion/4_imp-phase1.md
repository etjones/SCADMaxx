# Phase 1: Isolated candidate evaluation and prerequisite gates

Requirements: IN03-04, IN10, IN12, IN16. Read 3_overall-plan.md and both source/preview contracts first.

1. Read the actual 02/03/06/07/08/11 headers/handoffs. Record the prerequisite-only base and tested deltas. Before
   freezing it, finish the separate 03 owner follow-up in insertion-foundation-contract.md and 11 insertionRole.
   Verify fake draft display/focus/input tests. Missing contracts block 12; do not copy competing owner services.
2. Add InsertionTypes, CBOR protocol and internal worker bootstrap with strict version/build/length/field validation.
   Factor the native headless instantiation path needed from openscad.cc without changing ordinary export semantics.
   Worker has no MainWindow, HTTP server, backup/save, settings mutation or file-output operation.
3. Add seeded source/configuration transport and NeedInput closure discovery. Root/candidate bytes remain in memory.
   Use canonical original source directories and path order. Probe a dirty included buffer plus relative nested use.
4. Add resolved-native capability guards for uncontrolled IO/nondeterminism; establish every initial catalog's
   actual dependency/call path can run inside the guard. Hard failures cannot be converted into successful emptiness.
5. Add QProcess lifetime, asynchronous cancellation and serial checking. Evaluate concrete boolean geometry and
   return validated meshes/provenance/diagnostics. No UI other than a test harness yet.

Checks: insertion-preview label; discovery must list sealed_include_no_disk, dirty_nested_use, conflicting_editors,
configuration_parity, serial_mismatch, oversized_payload, worker_crash, cancel_during_geometry,
external_input_rejected, seeded_random_repeatable and base_state_unchanged.
Use a fake delayed protocol peer only for transport faults; use the real executable for geometry/input tests.
Compare base source bytes/revisions/undo count/result identity before/after success, failure and cancellation.
Assert a same-name shadowing module fails generated-call provenance. Test worker path with spaces/Unicode.
Run the applicable owner sealed-evaluation-inputs/inspection-draft checks; record their separate source ownership.

Exit: real candidate difference evaluates and can be cancelled without changing the live model/editor. A current
successful result includes exact consumed-source and configuration evidence. No insert menu depends on unproven IPC.
If native global state leaks, flags cannot reproduce the base or catalog code needs uncontrolled IO, stop with evidence
and refine capture/evaluation design. Do not silently enable disk fallback or run candidates inside MainWindow.

Use the overview verification-contract.md with the actual isolated build path: build OpenSCADExe and
OpenSCADUnitTests, run ctest -N, then the named CTest labels. Native cases use the registered GUI harness selector.
No zero-test result counts as passing; retain commands, discovery and logs in the feature run directory.
