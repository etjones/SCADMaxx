# Phase 2: resolve and match installed library revisions

Requirements: PR06-11, PR14-15. Prerequisite: phase 1. Matching never downloads or executes a library.

1. Implement ContentDigest with UTF-8 validation, BOM/line-ending normalization, per-file SHA-256 and aggregate digest.
   Reuse existing QtCore; explicitly link the test target. Verify standard SHA-256 known vectors before file fixtures.
2. Implement LibraryResolution using native resolver semantics and callbacks. Preserve source directory, ordered search
   paths, canonical selected roots, effective import spellings and captured revision tokens.
3. Validate profile import-edge reachability against its complete file set, then resolve the frozen edges using native
   path rules after verifying all file hashes. Include nested include-relative precedence; do not parse runtime SCAD.
4. Implement LibraryMatcher's availability states and exact single-profile selection; use library-fingerprints.json
   as the authoritative initial lists. Extract readable version markers only for reporting.
5. Implement ProviderBinding capture/revalidate. A newer snapshot, changed import target or changed captured bytes
   produces StaleBinding. No stat-only cache shortcut at commit/revalidation boundaries.

## Meaningful checks

- providers-match: exact profile available; BOM/CRLF conversion still matches; changing one non-newline byte fails.
- Same Git HEAD/version label with edited file fails; newer unlisted version fails; BOLTS development label with
  matching released closure succeeds. No library installed leaves built-ins usable.
- A document-local incompatible library shadows a valid search-path copy: ResolutionMismatch, never later-copy selection.
- An internal import resolves outside the matched root or to a second installation: reject even if the root file matches.
- Fake immutable byte reader returns changed unsaved library bytes while disk is unchanged: mismatch/revalidation
  failure. A read that reports not-captured cannot trigger a disk fallback. Library update during capture is rejected.
- Duplicate candidate profile fingerprints produce AmbiguousProfile; resource/canonical path escapes are rejected.

Build and discover/run providers-match plus affected schema checks. Record exactly which resolver fixtures prove native
precedence; API names alone are not proof. No external libraries are needed for fake filesystem fixtures.

Exit: bindings identify the effective matched bytes and cannot be reused after a content/resolution change.
If the profile's edge set cannot reproduce native resolution, stop with the failed import evidence before weakening
matching to sentinel files, evaluating arbitrary library code during discovery or borrowing another feature's parser.
