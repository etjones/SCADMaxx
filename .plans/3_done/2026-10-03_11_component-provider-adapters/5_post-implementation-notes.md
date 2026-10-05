# Component providers: local implementation handoff

Locally complete, 2026-10-04. All five phases are implemented and verified. No commits, push, promotion, stack
selection or integrated release. Source remains uncommitted in its dedicated checkout; HEAD alone is not its identity.

## Exact source and replay

- Checkout `D:/openscad/wt-openscad-component-provider-adapters`, branch `feature/component-provider-adapters`.
- Frozen upstream base `9899c745e47dbf0f48b3ca23562eea31e66f9b82`; no 03/08/12 implementation inputs.
- Run `D:/openscad/runs/20261004-component-providers` contains build commands, source inventories, repairs and fixtures.
- Feature-only `final-feature.patch`: SHA-256 `79a0cc3aad41a4d2da9884324e4b2cb0818a495c32656c709d98fd070550d0f5`.
- Complete working input `final-complete-input.patch`:
  `10dd38dd20e35412a3985f93d7f6c1df0b25aa694c3692e4e173e938ce9d030b`.
- `final-source-evidence.json` records each actual working file hash and canonical patch layers. The feature patch
  was applied independently to the repaired base and every resulting byte compared with the final canonical source.
- `inputs/manifest.json` locks eleven separate Windows repair inputs. The executable-resource repair is adapted to
  upstream #7092 while retaining its new version fields. GUI cache-test sleep repair follows an observed MSVC failure.
- Submodule revisions are unchanged: MCAD `1ea402208c3127ffb443931e9bb1681c191dacca`,
  Clipper2 `c7f820f6a03fa91f189b866d27bf40dfe47abaa6`, OpenCSG `9bf122715213dca05e70993dd8672fe3aa36c518`,
  manifold `0edd9d54876f3135e431575214dd6d8a72866fee`, mimalloc `30b2d9d89099bee08e9f67a1ffb3e12e7ba45227`,
  sanitizers `bcb1fc68616e9645ca5acea2992412606373ab04`. Generated Clipper header bytes used by the build are retained;
  its normalized blob matched HEAD before restoring only that generated working file, without staging.

## Delivered behavior and contract refinements

Owned immutable registry/bindings, strict declarative catalogs, bounded typed expressions, exact normalized dependency
fingerprints and native resolver precedence are implemented in `src/core/providers`. Diagnostics distinguish missing,
modified, unsupported, shadowed and ambiguous dependencies while independent entries remain usable. No UI/editor types
are exposed. Query/generate operations do not evaluate or mutate the target model.

Four primitives and four library families ship as metadata: BOSL2 threaded-hole masks and BOLTS ISO4017 screws,
ISO4032 nuts and ISO7089 washers, M3/M4/M5/M6/M8. Hardware is additive Component metadata; masks are subtractive geometry.
Frame direction is independent of boolean operation. BOLTS includes remain helper-local, BOSL2 includes file-local.

`doc/component-providers.md` is the public API/CLI/authoring contract. Implemented refinements:

- `revalidate(binding, context, currentSnapshot)` explicitly observes catalog-generation replacement; no two-argument alias.
- Helpers retain owned `localImports`, allowing a consumer to preserve scoped imports when composing source.
- Profile IDs allow numeric dotted version segments, as required by the accepted pinned profile names.
- Catalog validation and recipe evaluation stay within CatalogLoader/ScadFragmentWriter rather than empty wrapper classes.
- Unreadable optional discovery locations produce diagnostics without disabling valid independent catalogs.

CLI list/check/emit commands return UTF-8 JSON with strict provider-only options and exit statuses 0/1/2. Application,
user, direct project and explicit discovery paths are deterministic; duplicate provider IDs disable every contender.
The authored project-wrapper example exercises native source/import handling without executable plugins.

## Executed verification and retained artifacts

`verification-evidence.json`, SHA-256 `0d04733fa6dc06c213d9e65fb9d0341ca789472afd207704dd9ca2ae99b5a8e8`, binds
source, exact commands/logs, dependencies, executable hashes and extracted package checks.

- 21 focused tests pass: schema/defaults, strings/locale/UTF-8, hashing, library/context/capture races, resolution
  shadowing, immutable two-document drafts, effective module collision metadata, native CLI and generated geometry.
- The pinned external suite executed 31 native Manifold renders: five sizes for five geometry families, four ambient
  BOLTS mode/unit cases and two subtraction fixtures. Exact 35-file BOSL2 and 41-file BOLTS native dependency sets match.
  SCAD, dependency traces, STL, summaries and process logs remain in `build/providers-generated`.
- Full unit discovery: 77 test cases, exit 0; JUnit contains 140 parameterized rows, zero failures/errors.
  The separately executed focused external suite supplies library coverage; ordinary full-unit runs can skip absent fixtures.
- Four existing object/import/text-metrics echo regressions pass. Harmless inherited pretty-report Git warnings remain
  in CTest logs; they are not hidden or counted as test failures.
- Selected baseline `4c325716b94e444637a80df3966197ce110b2b75` source composition was rehearsed in an owned snapshot.
  All feature hunks apply except the shared CMake test-registration context; the recorded merge retains selected widget
  autogen/C++ standard setup and adds provider test settings. The selected checkout was unchanged. This composition
  was not compiled; integrated runtime acceptance remains a separate build obligation.
- Flat portable verification ZIP SHA-256 `4e6e586ae9242f0427fb7b08d3852468de3a21caac35cea69e854e97e9622079`.
  Both extracted `.exe` and `.com` with clean runtime PATH discover all eight entries: four available with no external
  libraries, eight available with the pinned external paths. Each emits and independently renders the ISO4017 source.
  Schema, catalogs, examples and documentation are installed. BOSL2/BOLTS source and dimension tables are absent.

Build and package use the existing MSVC 14.51.36231, SDK 10.0.26100.0, Qt 6.11.1/QScintilla and shared vcpkg tree.
Dependency status SHA-256 remains `2983caf4494a3428f029553e921a862000477e8e1266a8b74846acde80c7c2e1`.
No packages were installed. The initial Python image-compare configure path lacked PIL; the existing C++ diffpng
configuration was selected explicitly. Other platforms, Qt5/headless compilation and clean-machine portability are unverified.

## Obligations for feature 12

Adapt resolution/read callbacks to 03's sealed captured inputs, including dirty included buffers, with no disk fallback.
Preserve file/helper import scope and caller-supplied unique helper names. Check effective module provenance in the
native candidate result, not catalog hashes alone. Preserve the original immutable draft proof on replacement;
revalidate bytes, context and current registry immediately before the guarded source transaction. Interpret the
returned frame using 08's Mate/Flip rules independently of operation. 12 owns placement, insertion menu, source
transactions/undo, candidate preview and residual/cut verification; no alternate renderer or source editor was added here.
