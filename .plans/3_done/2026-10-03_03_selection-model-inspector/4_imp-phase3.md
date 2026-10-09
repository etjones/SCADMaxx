# Phase 3: exclusive tools, overlays and basic Inspector

Covers SI03/SI05/SI06/SI07/SI09. Requires validated phase 2 hits.

1. Implement ViewportToolRouter's token/lifetime/cancellation state machine and input precedence. Adapt QGLView,
   existing annotation drawing and measurement modes to acquire/release tokens. Preserve navigation cube routing.
2. Add one-shot pick and consumer drag registration, overlay registration with state guards, and selectionChanged.
   No feature-specific Section, semantic tree or source-navigation action is part of this branch.
3. Add InspectorDock, menu action and read-only geometric properties. Add contribution registration and owned widget
   replacement; contribution teardown cannot leave callbacks into a destroyed document/feature controller.
4. Test SelectionRouter unit cases [selection-router]: one owner, replace/cancel exactly once, miss stays active,
   success exits, stale result exits, QObject deletion, tab/focus change, drag versus click threshold.
5. Native TestSelection: select geometry, inspect point/normal; pick/miss/Escape; orbit/pan/zoom while picking;
   activate annotations/measurement and switch back; context menu; two windows; destroy a contribution owner.
   A test-only contribution verifies the extension contract without linking future feature code.

Run unit [selection-router], native TestSelection and existing TestNavigation/TestAnnotations. Exit: the foundation
is usable by itself and every gesture has one owner; source text, model suppression and dirty state remain unchanged.
