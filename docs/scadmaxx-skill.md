# SCADMaxx companion skill

The product skill is [skills/scadmaxx/SKILL.md](../skills/scadmaxx/SKILL.md). It covers modeling, BOSL2
installation and edge treatments, Customizer, capability detection, live HTTP targeting and validation.
Its references and examples travel with it; agents do not need this development workspace.
Installation guidance is inside the bundle's capability reference. No user configuration is changed by packaging.

The native Customizer specification is maintained in `doc/customizer-attributes.md` in the selected #6642
source checkout. Do not edit the skill's generated copy independently. Generate a companion ZIP with:

```powershell
./experimental/scripts/Build-ScadmaxxSkill.ps1 `
  -CustomizerSourceRoot D:/openscad/wt-openscad-pr-6642-dynamic-parameter-changes `
  -OutputZip D:/openscad/artifacts/<run-id>/scadmaxx-skill.zip
```

The script refreshes the reference and records the source HEAD, whether the canonical doc is modified,
and its SHA-256. It refuses to overwrite an existing artifact. Review the capability matrix against the
intended executable; generating a skill ZIP does not establish that a binary includes every documented feature.
The companion ZIP is separate from the Windows application ZIP; existing release/build packaging is unchanged.

For verification, extract the ZIP into a fresh directory outside the control/source checkouts. Run the
skill-creator `quick_validate.py` and [Test-ScadmaxxSkill.py](../experimental/scripts/Test-ScadmaxxSkill.py)
using `uv run`. The latter takes `--skill`, `--openscad` (upstream), `--extended` (OEP8/Customizer build),
`--bosl-parent` and a new `--output` directory. Its inline dependencies are isolated Python test dependencies,
not product requirements. Configure the selected executables' Qt/runtime paths where needed.
Inspect generated base/finished PNGs as well as the mesh report. Use the feature-native suites separately
for reactive Customizer and multi-document HTTP behavior; CLI examples do not validate GUI interactions.

Evidence and remaining limits are recorded in the skill feature's post-implementation notes.
