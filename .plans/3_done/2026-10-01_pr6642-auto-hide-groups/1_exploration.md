# Hide empty Customizer groups

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

User authorized implementation of their feature request in OpenSCAD PR 6642.
Source: `wt-openscad-pr-6642-dynamic-parameter-changes`, branch `codex/pr6642`, base `a8083eb97`.

Hide a group's header and contents when every parameter is explicitly hidden. Restore it when any
parameter becomes available, preserving expansion state and values. Locked controls remain visible.
Global controls count in each group where they appear. Collapsed ancestors must not count as hidden parameters.

Refresh after full parameter evaluation, dependency updates, preset/reset selection, and widget rebuilds.
Keep planning and build output outside the source patch. No automatic commit or publication.
