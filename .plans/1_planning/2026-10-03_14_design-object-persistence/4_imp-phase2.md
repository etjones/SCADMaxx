# Phase 2: references, identity and persistence closure

Covers DO-06, DO-09, DO-10, DO-11, DO-15, DO-16 and DO-19.

1. Implement registry/resolver contracts and built-in world/document/design/geometric domains, immutable result
   association and visited-ID cycle protection. IDs are case-sensitive and unique across kinds per evaluated root.
2. Implement dependency preflight/topological serialization planning. Keep existing source ownership; select an
   explicit destination editor only for unsourced records. Reject missing includes instead of silently editing them.
3. Add [design-references] cases: rename label/assignment, move declaration between included files, duplicate IDs,
   delete/restore, stale input/configuration fingerprint, unsupported semantic token, self/cross-object cycle.
4. Use a test-only registered consumer with required Section/View references to verify closure without 09 linked.
   Two consumers sharing one transient Section produce one declaration and retain the same ID. Unknown/cyclic
   dependencies fail before any source mutation. Two model roots with the same ID remain isolated.

Exit: reference outcomes and closure plans are deterministic and contain no invented semantic/geometric fallback.
Run [design-objects] and [design-references]; no source transaction or GUI gesture is needed to prove this core.
