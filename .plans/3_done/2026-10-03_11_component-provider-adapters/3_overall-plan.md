# Component providers: technical implementation plan

Status: locally implemented and verified, 2026-10-04. All five phases are complete. Read
[implementation handoff](5_post-implementation-notes.md) for exact source, checks and contract refinements.
The design below retains the accepted implementation strategy. No commits or promotion were performed.

Branch feature/component-provider-adapters has no new-feature prerequisites. Start from a frozen upstream/native
base under the workspace rules. The reference audit used wt-scadmaxx-20261002 at
4c325716b94e444637a80df3966197ce110b2b75; never silently use that complete integration as the feature base.
No 03/08/12 headers in this branch. 12 adapts the value/byte-reader interfaces after its prerequisites exist.

## Inspected implementation seams

- src/core/parsersettings.cc: get_library_path returns ordered paths; parser_init adds OPENSCADPATH, user libraries,
  then resource libraries. find_valid_path_ resolves relative to source first, then search_libs. Reuse that behavior,
  including nested relative import resolution; checking a configured installation alone can miss local shadowing.
- src/platform/PlatformUtils.h/.cc: resourcePath, userConfigPath and native application resource discovery exist.
  Windows discovery recognizes the resource root using color-schemes; add providers beneath the same root.
- src/ext/json/json.hpp already provides nlohmann JSON; do not install another parser. Its default object parser
  does not itself provide our duplicate-key policy: use a SAX builder with per-object key sets and JSON-pointer stack.
- src/openscad.cc owns boost program options and the CLI branch that calls parser_init. Add provider diagnostic modes
  to that branch before ordinary geometry export. They must work without opening a GUI or requiring an input model.
- CMakeLists.txt globs core/utils/io *_test.cc; sources/resources still need explicit registration. Its regular install
  rules include libraries/templates but have no provider directory. The Apple bundle has separate resource-copy rules.
- Existing GUI files use QtCore QCryptographicHash. Use QtCore directly for SHA-256, never import AnnotationStore or
  another feature's GUI hash wrapper. The selected Windows profile already supplies Qt6 Core; no new dependency install.

## Files and concrete ownership

New src/core/providers/:
ProviderTypes.h, CatalogLoader.{h,cc}, CatalogValidator.{h,cc}, ProviderRegistry.{h,cc},
LibraryMatcher.{h,cc}, LibraryResolution.{h,cc}, ProviderRecipe.{h,cc}, ScadFragmentWriter.{h,cc},
ContentDigest.{h,cc}, ProviderCommands.{h,cc}, and matching *_test.cc files.
New resource providers/: builtin.json, bosl2.json, bolts.json and schemas/provider-v1.schema.json.
New examples/providers/: project-provider.json, MyParts/bracket.scad and instructions.txt.
New doc/component-providers.md and tests/data/providers/ fixtures/expected source/geometry checks.
Modify src/openscad.cc and CMakeLists.txt for commands/build/install; no dock or preferences redesign.

Use std::string UTF-8 paths/IDs at public boundaries, std::filesystem::path for filesystem operations,
std::variant for ScalarValue/Expression/Statement, and shared_ptr<const RegistrySnapshot> for registry lifetime.
Only ContentDigest/CLI bootstrap needs existing QtCore. Core headers expose no Qt widget or editor types.
Wire QtCore explicitly for provider sources/tests, including command-only invocation; build configurations without
QtCore cannot enable this feature. This does not introduce GTK/GLib or install/upgrade a package.

Public ProviderTypes holds ParameterSpec, ItemDefinition, LibraryRequirement, LibraryProfile, ImportRequest,
HelperDefinition, LocalFrame, Diagnostic and the snapshot/binding/fragment types specified in the contract.
RegistrySnapshot: generation uint64, vector<ProviderDefinition>, ordered map<QualifiedId, ItemDefinition>, diagnostics.
ProviderBinding: shared snapshot, qualified ID, selected recipe index, catalog digest, vector<ResolvedLibrary>, and
contextRevision string. ResolvedLibrary: profile ID/label, canonical root, import prefix, ordered FileEvidence list.
FileEvidence: relative/canonical path, normalized SHA-256, rawRevision token. GeneratedFragment: imports/helpers,
geometry statements, Operation enum, frame, validated map<string,ScalarValue>, and immutable binding/provenance.
No references into transient JSON objects or borrowed source buffers survive catalog loading.
ItemDefinition and GeneratedFragment carry InsertionRole {Geometry, Component}; omission means Geometry. Validate
that Component is additive. Carry this refined metadata through shipped catalogs, CLI JSON and fake-consumer tests;
the registry still imports no semantic/12 classes.

## Load, discover and diagnose

CatalogSources is an explicit list of directories/files and optional sourceDirectory. Built-in application directory:
PlatformUtils::resourcePath("providers"); user directory: userConfigPath()/providers; project directory:
sourceDirectory/.scadmaxx/providers. Do not walk upward guessing a project root. Additional explicit paths come from
userConfigPath()/provider-sources.json (schema 1, catalogPaths[], libraryBindings[]). Paths in that configuration are
absolute or relative to its containing directory. A catalog itself contains portable library-relative paths only.
Registry API callers can supply project roots explicitly. Absent optional directories are harmless.

Enumerate direct *.json files only, sort canonical paths by UTF-8 order, validate limits and schema, then build one
immutable snapshot. Canonical duplicate path is read once. Different catalogs claiming the same provider ID disable
that ID and report every contender, including a user file shadowing a shipped ID; never last-wins override.
Invalid catalogs do not prevent unrelated valid providers from loading. schema/ and examples/ are separate resource
directories, never accidentally loaded as catalogs. Validate values/defaults and resolve profile/parameter/helper
references at load time. A recipe refers only to libraries/profiles declared by its own provider.

## Match and freeze library inputs

Implement the exact normalized-file hash algorithm from provider-contract.md. The initial manifest was measured,
not inferred from version text. Turn its entries into library profiles without copying vendor SCAD files into source
or packaging. Cache by catalog generation, canonical paths and actual content identity. File watcher/time/size may
trigger refresh but cannot authorize reusing stale hashes at a mutation boundary.

Standalone LibraryResolution adapts find_valid_path/get_library_path and filesystem reads. During matching, resolve
declared roots from the target document context and verify canonical root and all expected content. Resolve the
profile's recorded import edges from their originating directories and require their expected canonical targets.
At catalog load, graph traversal from declared roots must cover exactly the file-hash set. Catalog/profile hashes
bind these edge records as well as the content expectations. No runtime regex parser or library execution is needed.
Reject outside-root resolution, missing imports or unexpected shadow files. Paths inside a profile cannot escape
via traversal or symlinks. Hash only files referenced by the profile; unreferenced extras are OK.

The audited parserInspection seam belongs to existing HTTP work and has a small token budget unsuitable for these
complete libraries. Do not import or loosen that API in this independent feature. Profile authoring freezes import
edges from the pinned source and checks completeness against native -d output; 12 checks actual preview dependencies.

12 supplies equivalent resolveImport/readBytes callbacks backed by 03's immutable EvaluationInputs. Bind and preview
must use the same captured effective paths and bytes. If inputs change, return StaleBinding; invalidate and regenerate
the draft. Do not fall back to disk for a missing captured dirty buffer. A callback may report not-captured explicitly;
12 must obtain a complete new capture before retrying. LibraryMatcher itself has no dependency on 03.

Only one recipe may match. Distinguish absent, unlisted marker/revision, changed files at an expected marker,
resolution mismatch and duplicate/ambiguous declarations. A same-label modified file fails matching. BOLTS's generic
development marker can still yield Available when the full released closure matches. User catalogs use the same
hash/profile rules; the diagnostic output assists authors in making explicit revisions after validating changes.

## Generate and serialize

1. Validate the exact supplied parameter-key set, apply declared defaults and validate types/ranges/enums.
2. Evaluate recipe expression trees with checked finite arithmetic. Validate frame lengths/normal-up independence.
3. Substitute value nodes in statements. Keep identifiers/imports structural. Return the recipe's scoped helper
   definitions and global imports separately. Emit BOLTS import inside the helper and BOSL2 includes at file scope.
4. Request concrete helper names from the caller's SymbolBindings; require valid unique identifiers. Serialize with
   deterministic argument order and escaping. No source-editor access or regex substitution inside arbitrary code.
5. Return the operation, local contact frame, profile/captured-input proof and required module bindings. The latter
   identify expected module names and defining library files; 12 checks provenance if an existing model shadows them.

The scoped BOLTS helpers prevent its mode/unit globals from leaking into the document or being inherited incorrectly.
Do not rewrite vendor code. The ISO4762 candidate triggers a real undefined-h warning in the pinned distribution;
the selected ISO4017 family is the tested screw entry. This is catalog selection, not a hidden per-version fallback.
Preserve millimetres and the built-in analytic frame choices; do not derive insertion anchors from mesh extrema.

## Diagnostic CLI and test access

Add --provider-list (JSON statuses), --provider-check <catalog.json>, --provider-emit <qualified-id>,
--provider-values <values.json>, --provider-source <path> and repeatable --provider-catalog <path>.
Only one list/check/emit operation at a time; disallow export/animation together. provider-source supplies resolution
context without modifying or evaluating that document. Without it, use cwd explicitly and state that in output.
Normal configured/shipped catalogs load; provider-catalog adds explicit inputs under the duplicate-ID rule.

list exits 0 for a successful report even if optional libraries are missing; invalid catalog diagnostics remain in
JSON. check exits 0 only if its catalog and dependencies match, 1 for invalid/unavailable, 2 for usage errors.
emit requires values only when defaults do not suffice; output a JSON GeneratedFragment plus standalone preview SCAD
using deterministic helper names. Exit 1 with diagnostic JSON and no fragment on failure. No downloads or writes.
check includes detected per-file hashes so authors can deliberately revise their own profile; it never edits it.

## Phases and acceptance

1. Catalog/schema/value types and deterministic validated generation with built-in fixtures.
2. Native resolution, version/fingerprint matching and immutable bindings, including shadow/dirty-source cases.
3. Shipped library recipes, import-edge/dependency-trace and geometry validation on separately supplied test libraries.
4. User/project discovery, diagnostic CLI, example catalog and portable resource install rules.
5. Consumer handoff tests, extracted-package checks and evidence/branch composition record.

Use [verification commands](../2026-10-03_00_source-first-cad-overview/verification-contract.md) and Catch tags
[providers-schema], [providers-match], [providers-source], [providers-cli]. Add CTest label providers-external for
real-library cases; external test libraries are supplied explicitly, never downloaded by tests or bundled in a ZIP.
Their absence may skip the optional suite in ordinary CI, but cannot satisfy feature handoff: record the actual suite
passing with both pinned distributions. Include geometry comparisons, since exit 0 alone allowed a wrong BOM cube.

12 is not a prerequisite. A fake consumer using the public binding/fragment APIs proves the handoff in this branch;
real source insertion, preview, placement and undo remain 12's responsibility. Record that distinction at completion.
No commit/push, promotion, enabled-stack change or complete application build is authorized by this planning work.
