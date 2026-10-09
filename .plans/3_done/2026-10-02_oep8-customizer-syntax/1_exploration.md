# OEP8 objects and Customizer attribute syntax

Status: done. Accepted or closed as implemented and validated at the user's request on 2026-10-07.

Requested on 2026-10-02: select OEP8a PR #6081 for future SCADMaxx builds and adapt
PR #6642 annotations to fixed `identifier: expression` members separated by commas.
Support empty blocks and trailing commas; exclude computed/quoted keys, `each`, and
comprehensions in annotations. Preserve existing reactive hidden/locked expressions.
Ordinary OEP8 objects retain their full syntax. The larger #4478 prototype is excluded.

Source: `D:/openscad/wt-openscad-pr-6642-dynamic-parameter-changes`, `codex/pr6642`,
initial HEAD `a8083eb97`. Preserve the unrelated GUI group-visibility edits.
Verification: `D:/openscad/wt-openscad-oep8-customizer-check` combines #6081, this patch,
and required Windows repairs. Evidence: `D:/openscad/runs/20261002-oep8-customizer`.

Verify accepted/rejected grammar, printer round trips, widget configuration, included
ordinary/special-variable reactive behaviour, and coexistence with object literals,
comprehensions and object(). Register reviewed source boundaries for future builds.
This updates build inputs; packaging a new full distribution is a separate build run.
