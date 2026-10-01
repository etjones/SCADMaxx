# Quiet Customizer — sequential implementation plan

Status: all four phases implemented and committed sequentially at the user's request on 2026-10-01.
See [results](5_post-implementation-notes.md) for source identities, validation and remaining platform limits.
Use the existing UI branch/worktree. Apply [requirements](2_requirements.md) without repeating foundation/icon work.

## Phase 1 — quiet section headers

Decouple expansion storage from QToolButton checked painting. Retain native control states and disclosure arrows,
stable original group identity, keyboard toggling and accessible expansion semantics. Verify Expand/Collapse All,
rebuild preservation and light/dark contrast before continuing.

## Phase 2 — description presentation and hover help

Rename Hide Details to Help Icons and select it initially. Add shared palette-aware help glyphs with native hover
tooltips, no focus or activation behavior. Preserve the other three modes. Test all parameter types, transitions,
absent/long/multiline descriptions and unchanged control Tab order and values.

## Phase 3 — capitalization and native metrics

Apply conservative display-only capitalization while keeping original identities separate. Preserve internal casing
and author content, following the exact first-word rule in requirements. Use translatable sentence-case strings for
application-owned Customizer captions. Remove checkbox QSS, reuse native metrics and existing spacing/font helpers, and adjust only
layout needed for labels/help. Verify collisions, wrapping, narrow panels and enlarged fonts.

## Phase 4 — native validation and handoff

Build Windows application/tests with the existing shared dependencies. Run focused regression checks and native
light/dark/scaling captures against the accepted preview. Exercise presets, reset, auto-preview, expansion and mode
switches. Record exact commits/evidence and untested limits in post-implementation notes, update downstream dialog
work and keep the cumulative UI source unready until all selected parts satisfy their handoff.

Keep source changes grouped by phase; workspace plans and artifacts stay outside upstream-facing source commits.

## Second consistency review

Confirmed the hover-only decision throughout the exploration, requirements, shared brief and plan. Removed vague
capitalization inference by specifying an exact conservative rule, restored the shared brief's application-caption
scope, and added mode-switch/value preservation and literal tooltip-text checks. No unresolved product decisions
remain. This review changes planning documents only; native rendering details will be validated during implementation.
