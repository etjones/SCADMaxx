# Phase 3: build coverage and consumer handoff

Covers GS02, GS06-GS10 and integration acceptance. No UI or HTTP endpoint is added in this phase.

1. Verify the supported Windows configuration builds both the application and OpenSCADUnitTests using the existing
   shared dependencies. Record source/base HEAD, Manifold submodule SHA, configuration and actual test discovery.
2. Exercise ENABLE_MANIFOLD-disabled compile coverage in an isolated configuration where supported by the existing
   build profile. Public headers must not include Manifold; solid/section return BackendUnavailable and PolySet bounds
   still work. If that alternate build cannot run here, record it explicitly rather than claiming coverage.
3. With ENABLE_CGAL when already supported, validate an existing CGAL solid conversion against the box fixture.
   Do not install a second toolchain just to complete optional backend coverage.
4. Identify existing projection/cut regression cases through CTest discovery and run the relevant existing subset.
   Core projection/export code should have no behavior changes; investigate any changed result instead of updating
   expectations automatically. Re-run the new numerical suite only as needed after fixes.
5. Add concise API documentation under the source repository's existing developer documentation location: frames,
   units, strict topology, half-open slice boundary, quantization, cancellation limits and caller identity ownership.
   Include one section input/result example with the 20x10x6 box and one explicit invalid-mesh diagnostic.
6. Record the public header revision and numerical evidence for 09/13, plus the exact feature delta/base/head for
   replay into the selected SCADMaxx composition. Consumers must use this API; shared extensions return to this owner.

Exit: supported native build and numerical/projection checks pass; optional coverage gaps are stated accurately.
Write `5_post-implementation-notes.md` at implementation completion. No promotion, remote push or enabled-stack change.
