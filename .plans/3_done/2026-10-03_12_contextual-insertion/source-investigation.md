# Source evidence and verification limits

Planning audit: 2026-10-04. No new native source was edited or built for this plan.

Read-only integrated audit checkout: D:/openscad/wt-scadmaxx-20261002,
HEAD 4c325716b94e444637a80df3966197ce110b2b75, clean before navigation.
03 implementation: D:/openscad/wt-openscad-selection-model-inspector, occupied; its completion notes identify
final-feature.patch fc9f0e8da7fa019447700bee498b09a689f00152d8ae965a106341a0569290bb.
Read the actual headers/doc from this checkout; do not treat its unchanged HEAD as its implemented source identity.
Recheck the frozen handoff and any later owner work at implementation start.

Serena pattern navigation located MainWindow functions. Symbol lookup returned no member symbols (overview only
reported an anonymous namespace); bounded direct reads of the located functions and known owner headers were used.
No source code mutation or onboarding refactor was needed. Do not claim an indexed full native call-graph audit.

## Confirmed seams

- MainWindow.cc compile(bool,bool), around audit line 766: sets global warning policy, clears live error/console state,
  calls saveBackup and parseTopLevelDocument, then updates live compilation state. Not an isolated preview API.
- MainWindow::compileCSG, around 1105: uses this->tree/rootNode, processEvents, global progress hooks, writes
  csgRoot/normalizedRoot/rootProduct/previewRenderer/thrownTogetherRenderer. Cannot borrow it by swapping editor text.
- openscad.cc do_export, around 386: establishes EvaluationSession/BuiltinContext, instantiates native root, applies
  root-tag selection and uses a local Tree/GeometryEvaluator. It also changes process CWD. Extract/reuse its native
  headless pipeline for the internal worker without invoking file export or treating worker output as a live result.
- GeometryWorker::start stores a pointer to the supplied Tree. work calls GeometryEvaluator and forces lazy Manifold
  Status. Lifetime/process-global concerns remain; do not hand it a temporary candidate Tree.
- 03 EvaluationInputs.h: exact SourceInput bytes/revisions, capturedEditors, read, consumed, freeze, NativeEvaluationScope.
  There is no seeded RejectMissing mode yet. Default read may access disk, hence the separately specified owner update.
- 03 EvaluationBinding.h: capture, inputsCurrent, install, validate, scene and replacePresentationRenderer exist.
  validateModel/draft display exclusion are proposed additions, not available APIs.
- 03 InspectionPresentationController.h: QObject-scoped provider/effect/request tokens and one central renderer
  coordinator. No draft lease exists yet. A priority-200 candidate provider under a live result would misidentify
  candidate pixels as original source, so the generic draft boundary must be implemented first.
- 03 ViewportToolRouter.h: beginPick/beginDrag, claimExternal, finish/cancel and lifetime routing exist.
  Focus-group retention is a proposed generic refinement.
- Native import_stl/import_off open independent file streams; EvaluationInputs does not capture those bytes. Other
  external-resource operations likewise need a capability guard in the first worker. Do not promise closed input
  evidence merely because all include/use source was captured.
- 06/07/08/11 plans supply source span, hierarchy, anchor and provider contracts. Their future APIs must be verified
  at branch preflight; none was assumed implemented just because its Markdown specification exists.

## Planning checks versus implementation checks

fixtures/ordinary-cut and ordinary-add before/after files provide executable source examples without new semantic
syntax. Both after examples passed geometry/bounds/volume checks; see [planning verification](planning-verification.md).
fixtures/shared-part and named-component examples require the new 07/08 implementation, so the historical
binary cannot validate them. Native preview isolation, editor undo, UI input and complete branch integration have
not been exercised by this planning work. Use the six phases' tests to establish those results.
