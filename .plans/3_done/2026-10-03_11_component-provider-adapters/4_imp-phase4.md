# Phase 4: custom catalogs, CLI and portable resources

Requirements: PR05-08, PR12, PR14-15. Prerequisites: phases 1-3.

1. Implement explicit shipped/user/project directory discovery and provider-sources.json configuration as specified.
   Missing optional directories are fine; malformed configuration gets a path-specific diagnostic. No ancestor search.
2. Add diagnostic options/dispatch in src/openscad.cc, using parser_init for actual library search paths and a CLI-safe
   QtCore bootstrap where needed. No window or display connection for provider commands. Follow the specified exits.
3. Add the schema resource and authored example catalog/SCAD wrapper. Provide an authoring example for parameter
   types, frames, operation, helper imports, version/profile hashes and explicit catalog revision after source changes.
4. Add native/install and Apple bundle copies for providers/schema/examples/doc. Extend the existing Windows packaging
   verification to expect catalogs and reject accidentally copied test/vendor libraries; do not change the enabled stack.
5. Document registering external library roots/import prefixes, native search-path precedence and version mismatch
   repair. A root selection must resolve the emitted imports in normal OpenSCAD; diagnostics do not change search paths.

## Meaningful checks

- providers-cli: --provider-list returns built-ins plus disabled missing-library statuses with no model argument.
- --provider-check detects unknown schema, same-ID catalog collision and absent/unsupported library independently.
- --provider-emit consumes JSON values and returns deterministic fragment/preview source; invalid values emit only errors.
- Register the example under a temporary project directory, query/emit it without recompiling, and render its generated
  source. Rename the project to a Unicode/spaced path and repeat through correct native path handling.
- Change example wrapper without revising its profile: mismatch. Update the author-owned fingerprint and version
  explicitly in the fixture, then match again; no automatic catalog mutation.
- Relocate a staged resource tree away from developer paths. Catalog discovery and missing-library reporting work;
  package manifest contains authored catalogs/examples and no external BOSL2/BOLTS code or planning run files.

Run providers-cli and affected schema/match/source cases once. Verify command output is valid JSON with UTF-8 paths and
separate stderr diagnostics. Usage errors must not accidentally start the GUI.

Exit: users can register catalogs and diagnose their installed library match from a portable application package.
