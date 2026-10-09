# Phase 2: build from frozen inputs

Covers SK07-SK08 and builder failure behavior in SK10. Implement the exact contract in [the design](3_overall-plan.md).

1. Refactor `Build-ScadmaxxSkill.ps1` to validate explicit frozen paths, copy to fresh staging and generate references
   only there. Update existing callers to pass the new mandatory parameters; locate them with a bounded literal search.
2. Separate validation, staging, provenance and compression into testable script functions where needed. Keep normal
   errors terminating; return one structured success object suitable for Stage consumption.
3. Use a temporary local Git source fixture with a committed `doc/customizer-attributes.md`, a frozen skill fixture
   and control-manifest fixture. Build once and inspect the archive with normal ZIP APIs.
4. Assert one `scadmaxx/` root, required files/relative links, generated document content/hash, source SHA and manifest
   hash. Hash all input files before/after and require equality. The same semantic inputs need identical contents;
   ZIP timestamp-level reproducibility is not asserted.
5. Exercise missing document/manifest/skill, dirty canonical document, existing work/output path and unreadable input.
   Each must fail clearly; no authored references or existing artifacts may change. Use temporary fixture roots only.

Keep a focused PowerShell verification script beside the builder if no existing harness fits, with explicit temporary
root ownership and cleanup checks. This is an artifact/provenance regression test, not a prose test.

Exit: the portable builder can be invoked using only the recorded frozen inputs and fails before claiming success
when provenance cannot be established. Preserve the fixture command and results in handoff evidence.
