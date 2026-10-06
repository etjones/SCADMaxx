# Inspector parser capability declaration

Discovered in `runs/20261006-scadmaxx-all-features` after merging Inspector
`6440acdfd1c21f979d3074b2cdd60478d0aa8977` onto the selected source-editing/Customizer stack.

`SourceFile::registerUse` checks `nativeParserCapabilityGuard` before registering a
font. Its declaration belongs to `core/EvaluationInputs.h`, but SourceFile.cc did
not include that header directly. MSVC reports C2065/C3861 at SourceFile.cc:77.
Failure: `logs/20261006T210730978Z-build.log` in that run.

Repair `106388a03` adds the owning header directly. No behavior change or dependency
package change is needed. Do not remove the capability check or import a downstream
feature merely to supply a transitive declaration. Earlier owner/consumer checks did
not establish that this intermediate composition compiled independently.

Before another run, check whether SourceFile.cc already includes EvaluationInputs.h.
If absent and the guard is used, apply the one-line include as a separate repair.
The current frozen feature inputs remain unchanged. Verification is recorded in the
run's Inspector repair checkpoint; final combined release checks remain separate.
