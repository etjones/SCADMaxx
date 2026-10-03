# Build identity and portability

Comparison baseline: 2026-10-02. Stable baseline is OpenSCAD 2021.01, as listed on the
[official downloads page](https://openscad.org/downloads.html). Development snapshots and SCADMaxx are
separate comparisons. Recheck this baseline when updating the bundle; a product name is not a feature contract.

| Capability | Mainstream 2021.01 stable | Upstream development snapshots | SCADMaxx |
| --- | --- | --- | --- |
| Core parametric language, comment Customizer, CLI geometry exports | Established | Present; check changed flags/formats | Inherited |
| BOSL2 | External library; verify revision requirements | External library; verify include/render | External library, preferred by this skill |
| Manifold backend | Not the stable baseline backend | Available in relevant builds; inspect `--help` | Only when compiled/enabled in the selected composition |
| Native `@{key:expr}` Customizer metadata | Not supported | Do not assume; probe exact build | Requires the selected #6642 variant |
| OEP8 object literals and `object()` | Not supported as a complete OEP8 feature | Experimental/build dependent | Requires the OEP8 input and enabled `object-function` where applicable |
| Loopback `/v1` agent API | Not provided by stable | Do not assume an upstream API | Requires agent-server feature, enabled Agent Access |
| `/v1/help`, schema, binary image routes | Not applicable | Probe, do not infer | Direct-HTTP revision required; follow live `/v1/info` links |
| Annotations, navigation cube, UI polish | Do not assume SCADMaxx behavior | Compare exact upstream feature separately | Selected local additions; composition varies |
| Customizable shortcuts and dynamic dark-mode switching | Do not assume the selected PR behavior | Check whether #6878/#6776 landed in that snapshot | Selected upstream PRs, distinct from local additions |
| Empty Customizer group visibility | Separate UI behavior | Build dependent | Not implied by the native annotation syntax patch |

## Probe the executable

Record absolute executable path, `--version`, relevant `--help` flags and shipped build/input manifest.
Run small disposable probes for features the task actually needs. Use a new output path and inspect exit
status AND diagnostics: some unsupported modules/functions yield warnings and incomplete output.
For objects, use [objects.scad](../assets/objects.scad); for annotations use
[reactive-customizer.scad](../assets/reactive-customizer.scad). Add `--enable=object-function` only when
the build advertises/requires it. A successful annotation parse does not prove reactive GUI behavior.

Versioned evidence for this bundle's language reference: #6642 variant source
`8ea44273775f3c7720f2ff607e6d4ea5215422a6`; combined OEP8/Customizer check source
`ae5e50d7aeb13c4fcfa42ae09126434fefbd69a2`, executable `2026.10.02-oep8-check`.
That combined check is not evidence that every distributed SCADMaxx executable has both features.
The v1-only agent API source baseline is `991bb09aee1c5d3f432b4e4352ff96254821b4b5`;
direct-HTTP help/image discovery is a subsequent revision. Consult live capabilities and bundled API help.

Bundle examples were executed on upstream `2026.09.27` and `2026.10.02-oep8-check` on Windows. The former
rendered the BOSL2 plate but rejected both extension examples; the latter accepted the object and annotation
examples. BOSL2 `2.0.766`, commit `e173fa0ae45f9e2082e0d8c0382dae98621b7c20`, was freshly installed for
the plate checks. Stable 2021.01 was documented, not executed in this validation. GUI reactivity has separate
unit-test evidence; CLI success does not assert interactive acceptance of every widget.

If the selected target lacks a required feature, state that limitation. Use ordinary language/comment
Customizer for a requested mainstream-compatible model, or select an available capable executable within
the task's scope. Do not silently downgrade requested behavior or introduce compatibility aliases/shims.
Do not interpret an unsupported API operation as authorization to build a new endpoint.

## Install or carry this skill

This is a companion skill bundle, independent of an OpenSCAD binary. Keep its whole `scadmaxx` directory,
including `references` and `assets`. For Codex, a chosen installation can place that directory under
`$CODEX_HOME/skills` (default `~/.codex/skills`), so `scadmaxx/SKILL.md` is directly inside the skill root.
Refresh the agent's skill discovery/session as needed. Do not nest an extra `scadmaxx` directory.
For another agent, use its documented skill directory or point it explicitly at this `SKILL.md`.
Installing this skill does not install OpenSCAD or BOSL2. Do not write user configuration as an incidental
effect of modeling; the user chooses that installation action.
