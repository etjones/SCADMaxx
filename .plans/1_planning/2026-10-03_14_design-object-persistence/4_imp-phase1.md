# Phase 1: annotated declarations and evaluated Section/View records

Covers DO-01 through DO-08, DO-11, DO-19 and DO-20. Requires implemented 02/03 and selected OEP8/Customizer inputs.

1. Add DesignKinds/Objects/Collector and registration of Section/View. Recognize the type Lookup in NativeAttributes
   before Customizer parsing; retain ordinary annotation handling. Detect invalid scope and design reassignment.
   Include DeclarationHost/hostName and per-handler host validation from the refined overall plan. Test synthetic
   module/call host contexts with a test kind, without adding 07 grammar or importing semantic headers. Section/View
   and assignment edit/create/promote APIs must reject these hosts before any object-field edit.
   Implement Consumer destination dispatch from the
   [scoped extension contract](../2026-10-03_00_source-first-cad-overview/semantic-extension-contract.md). Fake-kind
   tests must prove once-only values, local invocation context, use-top-level exclusion, callback lifetime and no
   accidental insertion of local IDs into the document registry. No semantic/anchor headers are needed.
2. Collect after effective file-scope assignment evaluation through EvaluationSession; use the same RHS values and
   immutable 03 inputs. Publish alongside the matching result, with per-record diagnostics and stale-state handling.
3. Implement the exact schemas, normalization/frame/quaternion order and Camera fit/fixed modes in the design.
   Add core tests tagged [design-objects] and fixtures under tests/data/scad/design-objects/.
4. Execute the example: height 40/60 gives Section z=20/30; geometry with/without the declarations is identical.
   Add direct objects, helper-returned objects, include parameter scope, use-only nonexport, duplicate ID/name,
   unknown type/member, type variable shadowing, module-local declaration, zero normal/parallel up/nonfinite fields.
5. Test GUI and headless compilation enumerate equivalent definitions; existing ordinary object/comprehension and
   Customizer fixtures still pass. Source-only editing eligibility does not prevent evaluating a valid helper object.

Exit: registered kinds evaluate without GUI consumers or CSG changes. Build the actual parser (including Bison conflict
checks) and run [design-objects]. A metadata conflict/incorrect parameter context stops this phase for correction.
