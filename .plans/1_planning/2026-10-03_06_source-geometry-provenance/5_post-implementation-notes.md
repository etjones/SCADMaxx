# Local provenance completion, 2026-10-04

All three phases and PV01–PV09 are implemented and locally verified. Worktree
`D:/openscad/wt-openscad-source-geometry-provenance`, branch `feature/source-geometry-provenance`,
base/HEAD `6a5dc9d1555cbcf9f1f8a359f37f68f5448f44a1`. Source remains uncommitted by instruction.
The run is `D:/openscad/runs/20261004-source-geometry-provenance`; later queue entries are 14, then 04.

## Inputs and implementation

The individually verified 02/03 patches and pinned OEP8 #6081 / Customizer #6642 variant are composed in
`inputs/manifest.json`. The prerequisite-only working patch is `eabea931786ddd7cff86c8787a9fd7bf31a1a6af0efb177185f28570d12ca076`.
OEP8 head is `07b22af25704af0db39959773751fb5c6e4debbe`; Customizer head is
`8ea44273775f3c7720f2ff607e6d4ea5215422a6`. Existing aggregate and dirty PR worktrees are preserved.
05/07/08/10/12/14/15 are excluded. The later selected navigation head remains a future composition obligation.

Ranges refer to exact captured UTF-8, preserving BOM, CRLF, Unicode, comments and expressions. Lexer lookahead
retains file identity, including included file EOF; the parser records separate syntax occurrences and whole/header,
argument/name/expression ranges. A call crossing an include expansion has no fabricated whole span. Native parsing
remains independent of HTTP inspection limits and does not change effective-assignment semantics.

Session-owned RAII frames distinguish definition, call and evaluated path. Node creation records explicit ownership;
immutable publication copies records without editor/AST pointers. Actual CSG leaf matrices and polarity supplement
logical node maps. Cache hits do not acquire shared owners. Direct preview primitives have a known emitting invocation;
subtraction cutters and containing booleans remain distinct contexts. Derived results can identify a producing call
without claiming inner triangle ownership. Final merged faces expose candidates, with no implied first-candidate edit.

The frozen consumer contract is `doc/source-provenance.md` and `gui/selection/ProvenanceService.h` in the worktree.
`resolve` validates 03's complete Stamp/input set and preview frame; `navigationCandidates` exposes source ancestors.
`editableSpan` prepares a captured 02 request only for a current unique producer and explicitly chosen recorded syntax.
It checks file/editor identity, revision, fingerprint, read-only state and expected bytes. Consumers validate immediately
before applying to the retained editor; they still own expression transformations. Unopened libraries require another
evaluation after opening before edits become eligible. Navigation uses ordinary tab handling and rechecks the target.
The Inspector contribution keeps 03 independently buildable and does not introduce semantic Part/Component types.

Native navigation exposed an empty module-definition header caused by using an intermediate Bison action's location.
The corrected header spans module through closing parenthesis; an exact unit fixture and actual Inspector button
verify it. Queued navigation uses QObject guards, and published syntax includes a sealed read-only line-start cache.
Failed attempts and earlier package/snapshot versions are retained as evidence.

## Verification and handoff

Windows Release: MSVC toolset 14.51.36231, SDK 10.0.26100.0, Qt 6.11.1, QScintilla 2.14.1; shared dependencies unchanged.
Native GPU: NVIDIA GeForce RTX 3070 Ti, OpenGL 4.6, driver 616.92. Verification used actual Windows focus and GL,
including clean-PATH extracted runtime checks. No clean-machine or other-platform claim is made.

- All 15 provenance unit cases and 43 discovered focused CTest cases pass. Full unit discovery has 103 cases;
  JUnit has 184 section/generator rows with zero failures/errors.
- Four object/import/text-metrics echo regressions and the OEP8/attribute coexistence fixture pass.
- Final extracted full native run `native-20261004T014623993Z`: 75 results, comprising 59 behavior and 16 setup/cleanup,
  across eight classes. Includes 02 transactions/conflicts, HTTP/annotations, navigation and selection regressions.
- DPR 1.5 `native-20261004T014657056Z` and DPR 2 `native-20261004T014701091Z` each pass seven provenance behaviors
  plus setup/cleanup. Preview matrices, both final-render backends, native Undo, dirty dependencies, tab races,
  parser failure, reused node indices and closed editors are exercised.
- Seven Unicode export cases pass through each extracted launcher. Source snapshot application is independently
  verified. Generated Clipper2 header bytes are retained, and the original header is restored after all builds.
  Whitespace check passes with CRLF recognized as a valid line ending.

Final feature patch `final-v2-feature.patch`: `dfc078d2b428df12e5225fa514bd0c6c9d09f45c458a5cbd8f7545032c90ca6c`.
Complete working input `final-v2-complete-input.patch`: `d05ceecf8601173b7536d5a325436e9b7d5a2c33706fd93c15b9c1f6813db463`.
`verification-evidence.json`: `5de3dbe33a2411d491347542fee5748336497d51727c5f2905bff84897acf09b`.
Application: `6684340aa639e28036b6c2c893621dac4c6c33600792c2178aa312a233c73e72`;
console: `4c60e27e9274d7ee259099caf2d5fdf83722d19dfc85eb749f4b050945640290`.
Verification ZIP `portable-verification-v2.zip`: `1c2ec8ffc04e83f1ce0ff0d4b614bd695d2eccd0bf105dc93508a9458a082ac1`.
The source evidence identifies 113 source files, including 23 feature files; HEAD alone is not build identity.

Invocation IDs are current-evaluation identities. There is no persistent topology naming, generic inverse-expression
editing or unique final inner-face ownership. This is a feature verification package, not an integrated release.
No staging, commits, pushes, promotion, stack edits or changes to the hand-maintained README were performed.
Future rework choices remain fix forward (bounded correction), replan (revise approach), restart (fresh implementation)
or supersede (replacement feature); none is required to continue the authorized queue.
