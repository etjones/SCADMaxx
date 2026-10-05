# Provider and version contract, schema 1

This is a new API/specification for 11, not an existing native capability. All names below are proposed implementation
names. [Requirements](2_requirements.md) define behavior; [tested fingerprints](library-fingerprints.json) identify the
initial external inputs. 12 consumes this contract without including provider-specific controller code.

## Catalog shape and validation

UTF-8 JSON. Root: schemaVersion=1, providerId, providerVersion, label, items and libraries. IDs use lowercase ASCII
segments [a-z][a-z0-9-]* separated by dots; an item's qualified ID is providerId + ':' + item.id. Versions are exact
three-integer release labels for catalog authors, never automatic SemVer compatibility ranges. Reject duplicate keys,
unknown fields, duplicate IDs, unresolved references and nonfinite numbers. Report JSON pointer and catalog path.
Resource limits: 4 MiB/catalog, 1,000 items/catalog, 128 parameters/item, expression depth 32, 64 KiB emitted/item.

Parameter fields: id, label, type (number/integer/bool/string/enum), default, optional unit (mm/deg), min/max,
exclusiveMin and enumValues. Enum values are strings. Optional string maxLength defaults to 1,024. No implicit
string-to-number conversion or implicit unit conversion. All first-release insertion inputs are explicit values;
future expression entry in 12 would require a separately specified input form, not string interpolation here.

Item fields: id, label, category (array of labels), description, parameters, operation (additive/subtractive),
insertionRole (geometry/component; omitted means geometry),
recipes (one per matching library profile; built-ins have one dependency-free recipe). All recipes for an item expose
the same parameters. Subtractive items require geometry role. The three BOLTS entries declare component role; the
five other initial entries declare geometry role. This refinement follows 12's accepted choices but is metadata only:
user catalogs select the same roles without per-library palette code or a dependency on 12.
Recipe fields: profileIds, imports, helpers, moduleBindings, geometry and placement. A dependency-free recipe
cannot call library functions. Catalog revision and exact catalog hash travel with every returned binding.

Expression tree: {"constant": scalar}, {"parameter": id}, {"vector": [expressions]}, or
{"operator": "add|sub|mul|div|neg", "arguments": [expressions]}. Numeric arithmetic only; unary neg has one operand,
all others two. Reject division by zero/overflow/type mismatch. This is a bounded value evaluator, not arbitrary SCAD.

Statement tree: {"module": identifier, "arguments": [{"name": identifier,"value": expression}],
"children": [statements]}. Optional empty children. A module identifier may instead be {"helper": symbolicId}.
Identifiers are literal validated SCAD identifiers, not interpolated user strings. Named arguments preserve catalog
order. Values are serialized as SCAD literals: round-trip finite doubles in classic locale, normalize negative zero,
escape string quotes/backslashes/newlines/tabs, reject NUL and unsupported control characters. Emit no raw templates.

Imports: {libraryId, path, kind:include|use, scope:file|helper, helperId?}. Paths are relative slash-separated paths
inside the declared library root, with no traversal or absolute path. A helper is {id, parameters:[ids], body:statement};
helper-scoped imports are emitted at the start of its body. 12 allocates collision-free concrete helper names through
the SymbolBindings map before serialization. 11 never searches/patches the current source for names or include sites.
For built-in parameters that share a SCAD builtin name, emit the named argument explicitly rather than a global assign.
moduleBindings lists {module, libraryId, path} for each called library module; built-ins use an empty list. Initial
bindings are screw_hole/BOSL2/screws.scad, ISO4017/BOLTS/classes/hexscrew2.scad,
ISO4032/BOLTS/classes/hexagonnut1.scad and ISO7089/BOLTS/classes/plainwasher1.scad (use the actual libraryId fields).
The path must belong to the matched profile. This supplies 12's expected defining-file identity without requiring
11 to inspect or edit the user's model. The native generated-source tests verify the actual definitions used.

Placement: {origin:[three numeric expressions], normal:[three expressions], up:[three expressions], label}.
Evaluate and validate a nondegenerate frame. 11 returns its numbers; 08 owns frame solving. It is the mating frame
on the new item. With a target surface's outward normal and 08 Mate, its orientation determines into/outward behavior.
There is no second automatic direction flip based solely on additive/subtractive purpose. 12 owns explicit Flip.

## Initial recipe matrix

Defaults: cube 10/20/30, sphere radius 5, cylinder diameter 10/height 20, hole diameter 4/depth 12, hardware M4,
screw length 20, threaded depth 12. Built-in lengths have exclusiveMin=0 and max=100000 mm. Library size enums are
M3/M4/M5/M6/M8. Screw lengths 10..100 mm, threaded depth 2..100 mm. Size tables do not imply every length is purchasable.

| Qualified item suffix | Geometry call | Contact origin / normal; up always +Y |
| --- | --- | --- |
| builtin:cube | cube(size=[width,depth,height],center=false) | [width/2,depth/2,0] / -Z |
| builtin:sphere | sphere(r=radius) | [0,0,-radius] / -Z (analytic surface, tessellation may lie inside) |
| builtin:cylinder | cylinder(d=diameter,h=height,center=false) | [0,0,0] / -Z |
| builtin:plain-hole | cylinder(d=diameter,h=depth,center=false), subtractive | [0,0,0] / +Z |
| bosl2:threaded-hole | screw_hole(size,head="none",thread=true,length=depth,tolerance="6H",counterbore=0,bevel=false,anchor=BOTTOM,atype="shaft",orient=UP) | [0,0,0] / +Z; subtractive |
| bolts:iso4017 | ISO4017(key=size,l=length) in scoped helper | Under-head [0,0,0] / +Z; shaft goes into surface |
| bolts:iso4032 | ISO4032(key=size) in scoped helper | [0,0,0] / -Z |
| bolts:iso7089 | ISO7089(key=size) in scoped helper | [0,0,0] / -Z |

Actual provider IDs: scadmaxx.builtin, scadmaxx.bosl2, scadmaxx.bolts. Use these rather than the table's short suffixes.
BOSL2's first positional size becomes its named spec argument. BOTTOM and UP are emitted as literal vectors [0,0,-1]
and [0,0,1], so the serializer needs no arbitrary identifier-valued expression. Fix the $slop special argument to 0
for this initial hole recipe and expose tolerance 6H in its description. Library default threaded lead-in behavior
remains as pinned; the M4 probe has an intentional mask extension to Z=12.01 for nominal depth 12.

File imports for BOSL2: std.scad then screws.scad. BOLTS import: BOLTS.scad inside each helper body; never hoist this
import during deduplication. Helpers take size/length arguments explicitly, rather than capturing ambient variables.
No vendored wrapper library is needed: emit a short ordinary module definition into the user's source, for example:

```scad
// scadmaxx.bolts:iso4017; catalog 1.0.0; BOLTS 0.4.1; profile boltsos-0.4.1
module smx_insert_screw(size,length) {
    include <BOLTS/BOLTS.scad>
    ISO4017(key=size,l=length);
}
smx_insert_screw(size="M4",length=20);
```

12 chooses the actual helper name and attaches the returned fingerprint prefix to the comment. Only ASCII hex is
used in identity comments; arbitrary display names are not copied into source comments. 12 owns target wrappers and
imports at file scope. It must preserve local imports in helper definitions. BOLTS hardware is explicitly described
as simplified-thread reference geometry; BOSL2 hole masks contain the modeled thread.

## Matching libraries to adapters

Library requirement: libraryId, label, defaultImportPrefix, profiles. Each profile has profileId, releaseLabel,
revisionEvidence, fileHashes, importEdges and digest. Shipped profiles are exactly BOSL2 2.0.766/e173fa0 and BOLTS OpenSCAD 0.4.1
from [library-fingerprints.json](library-fingerprints.json). No implicit ranges or greater-than match.
Provider release 1.0.0 and schema 1 do not imply library version 1.0.0.

The configured library binding supplies libraryId, root and importPrefix. Defaults are BOSL2 and BOLTS in the normal
OpenSCAD search path. A user may explicitly map a different layout, including an empty prefix for a flat library;
there is no silent search through alternate spellings. Validate actual native resolution for every import.

For each required root import, resolve from the real target source directory using native resolver precedence.
Require the result to lie in the selected canonical root. For each profile file, read captured bytes, validate UTF-8,
strip one leading UTF-8 BOM and normalize CRLF/CR to LF only. SHA-256 the resulting bytes. Sort relative paths by UTF-8
byte order; overall digest is SHA-256 of concatenated path + NUL + lowercase-file-hash + LF. Match all expected files.
The lists are imported dependency closures, not arbitrary sentinel files or the whole installed directory. Extra
unreferenced files are allowed. Profiles also contain the frozen import edges from
[library-import-edges.json](library-import-edges.json): from file, include/use kind, literal import spelling and expected
to file. Only after all bytes match, resolve each edge from its originating directory with native rules and require
the expected canonical file. These edges are profile-authoring data, not guessed at runtime. Their reachable set from
declared roots must equal fileHashes. No parsing or geometry evaluation is required to query a matched installation.
Catalog authors validate edge completeness against a real native dependency trace when preparing a profile; 12 also
compares the actual preview dependency trace with the bound closure. A changed import cannot retain a content match.

Report both a readable marker and verified identity. BOSL2 has BOSL_VERSION=[2,0,766]. BOLTS's released archive reports
BOLTS_version()="development" and date [2021,9,13]; only the closure fingerprint identifies the tested 0.4.1 artifact.
Read those simple markers from text for display only. Do not execute a library merely to determine its version.
Git revision is supplementary information: a modified worktree at the same HEAD is not a match.

Availability: Available, MissingLibrary, UnsupportedRevision, ModifiedLibrary, ResolutionMismatch, InvalidCatalog,
DuplicateCatalog, AmbiguousProfile, StaleBinding. Include library ID, effective path, expected profiles, detected
marker/hash and first mismatching file. Missing/unsupported entries stay enumerable with their reason.
Select exactly one matching recipe; zero disables the entry, more than one is a catalog error. Never choose a nearby
version. Updating an external library requires a tested catalog profile before its entries become available again.

User catalogs have the same explicit version/fingerprint contract. Editing their wrapper/library may require updating
their own catalog profile after validation. A diagnostic command reports current hashes but cannot silently mark a
profile compatible or change a shipped catalog. Support additions are new profiles, not parameter-renaming shims.

## Public handoff to 12

Use value types, immutable shared snapshots and Result<T,Diagnostic>; no MainWindow/Editor/Selection types in 11.

```text
ProviderRegistry::load(CatalogSources) -> RegistrySnapshot
ProviderRegistry::query(snapshot, LibraryResolutionContext) -> vector<ItemStatus>
ProviderRegistry::bind(snapshot, qualifiedItemId, context) -> ProviderBinding
ProviderRegistry::generate(binding, ParameterValues, SymbolBindings) -> GeneratedFragment
ProviderRegistry::revalidate(binding, context) -> Result<ProviderBinding, Diagnostic>
```

LibraryResolutionContext supplies sourceDirectory, ordered search paths, explicit library bindings, resolveImport
and readBytes callbacks. readBytes returns bytes plus revision token for the captured resource. 11's standalone
adapter uses native filesystem resolution; 12 supplies 03's captured inputs, including dirty library buffers.
No second disk read can replace a captured dirty source. A binding records registry generation, catalog hash, profile
IDs, resolved paths, normalized hashes and raw revision tokens for all matched files. Content changes invalidate it;
timestamp/size are hints only, not proof. Revalidate effective resolution and bytes before commit.

GeneratedFragment contains ordered fileImports, helperDefinitions with symbolic names, geometry statement tree,
operation, local contact frame, parameter values, required module/defining-file identities and provenance. Returning AST-like recipe data does not transfer
ownership of the user's source AST. generate is deterministic and side-effect free; validate before returning any
fragment. 12 serializes with supplied names, merges imports/helpers and uses one guarded 02 transaction.
12 checks that preview evaluation used the returned resolved dependency set; a mismatch aborts the draft.
