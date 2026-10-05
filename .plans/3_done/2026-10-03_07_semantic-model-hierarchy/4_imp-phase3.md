# Phase 3: semantic references and targeted export

Covers SH03/SH13/SH14/SH17/SH19. Depends on phase 2's owned roots, transforms and parameter snapshots.

1. Implement SemanticTargets and the registered semantic ReferenceToken decoder/resolver. Validate role and exact
   ID/path. Feed 14 same-result definition payloads and instance index, with no document-global Component ID entries.
   Use the state distinctions in the overall plan; no geometric replacement search or result-local ID persistence.
2. Implement asynchronous target-geometry preparation using retained EvaluatedScene and worker-owned Tree/cache.
   Serialize backend jobs; cache by result/target/role. Resolver requests while geometry is pending report Preparing
   target geometry and refresh later without blocking the GUI. Bounds/frame units and spaces must be explicit.
3. Implement definition default jobs by instantiating the exact retained module declaration in its native lexical
   context with empty arguments, in separate evaluation backing. Component jobs evaluate their already-instantiated
   localRoot. Neither may install a new document result or read current disk instead of captured inputs.
4. Implement SemanticExportJob and explicit target/Local/As placed options. Extract reusable existing format-options
   handling from MainWindow; never swap rootGeom or renderedEditor to reuse an action. Use existing backend validity
   checks and compatible exporters. Preserve captured $preview/global configuration and expose it in export UI.
5. Add sibling temporary output and atomic QSaveFile commit, cancellation and final stamp/input validation. Protect
   existing destinations on any failure; remove only the job's temporary file. Add [semantic-targets] and
   [semantic-export] tests, including filesystem output tests in temporary directories.

Expected outputs: /pair/right has local bounds [0,45] in X and As placed [60,105]; definition bracket uses width 30.
/pair export retains gap 60, root rack transformations are omitted only for Local, and child placements stay intact.
Exercise explicit nondefault arguments, two instances of the same definition, a used-library global default, nested
Assembly defaults, mirrors/nonuniform scaling, empty geometry and invalid/singular transformed output. Compare
geometry numerically using existing bounds/topology facilities; byte equality across exporter encodings is unnecessary.

Hide all, solo another item and enable a test inspection filter: the same target exports identical geometry. Change
source/dirty include/Customizer config or tab during preparation: no stale output published. Test cancellation,
read-only destination, existing destination content preservation and close while worker holds scene ownership.
Resolver fixtures: rename/reorder Resolved; deletion/reparent Missing; changed result Changed; malformed/colliding
target Invalid; non-rigid Section frame rejected by 14. Root Section/View behavior still passes without semantic targets.

Run [semantic-targets], [semantic-export], 14 reference tests and relevant existing STL/3MF export regressions with
the shared contract. Exit only when local/default/placed geometry and failure atomicity are verified. A successful
export of the whole document is not evidence that targeted export selected the right instance.
