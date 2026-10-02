# Preferences and secondary-dialog polish — sequential plan

Status: all four phases implemented sequentially on the existing UI branch. Native tabs and full audit scope
were explicitly approved by the user. Per-phase records and `5_post-implementation-notes.md` contain the results.

## Phase 1 — inventory and native category tabs

Complete the application-owned surface inventory from the requirements and inspect current native rendering.
Implement QTabBar in the existing category location with action/page synchronization, conditional visibility,
native keyboard/overflow behavior and stable selection. Verify light/dark, long labels and live category removal.

## Phase 2 — Preferences page hierarchy and spacing

Inspect every available Preferences page, including input/optional pages. Correct demonstrated layout and
typography defects using inherited fonts, native metrics, alignment and selective native group presentation.
Retain settings semantics, order and explicit font choices. Verify font changes, scrolling, keyboard and values.

## Phase 3 — remaining dialogs and auxiliary surfaces

Work through export/print, information, Welcome, AI and auxiliary control surfaces with separate scoped changes.
Replace applicable residual presentation stylesheets with Qt APIs; preserve branding, code/content colors and
semantic status information. Use offline fixtures for optional dialogs. Record no-change and unexercised outcomes
alongside fixed surfaces so the final audit has an explicit boundary.

## Phase 4 — cumulative validation and handoff

Build with the existing shared Windows dependencies. Run focused and full regression checks, then capture light/dark
and simulated DPI/font cases for representative layouts and distinctive controls. Recheck the completed foundation,
icons and Customizer. Record screenshots, exact commits, platform/optional-feature limits and every surface's outcome.
Complete the private source handoff and assess cumulative UI readiness under the workspace build contract, including
the already-applied #6776 and baseline repair dependency boundaries. Keep documentation/artifacts outside source.

Group source changes by phase and, where useful, surface. Commit only under the user's implementation/commit request.
