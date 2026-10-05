## Feature 10: suspended proposals

The user postponed 10 and moved to 11. These questions are retained only for a future scope review; do not ask them
or treat any recommendation below as accepted unless the user resumes this feature.

09 is postponed and is not a dependency. These are recommendations awaiting explicit user answers.
Preserve the accepted 07/08 distinction between definitions, instances and live attachment placement.

The user has challenged the premise of these six proposals: arbitrary resizing has no agreed mapping back to the
program's inputs, and literal-only parameter controls may add little beyond 07. Resolve the intended additional
workflow, or explicitly postpone 10, before requesting acceptance of the policies below. They remain unanswered;
the user has not accepted either direct resizing or the proposed reduced scope. See the exploration's scope review.

1. Which actions should ship first?

Recommended: move and rotate an existing object, edit supported numeric invocation parameters, and manipulate
existing attachments. Support source-backed ordinary module calls as well as semantic Components when the target is
unambiguous. Use drag handles and numeric entry, local/world axes and the object origin or an explicitly chosen anchor
as pivot. Defer scale gizmos, face push/pull, measured-dimension inverse editing and section-to-geometry actions.
This still allows resizing through an explicitly supported width/height/radius parameter. Broader actions are possible.

-> 

2. What should selecting one instance allow us to change?

Recommended: default to that instance and enable editing only when a source location controls it independently.
Shared definition/call edits are explicit actions showing the affected instances. A loop or repeated Assembly body
without an independent per-instance input cannot be edited as though it were a unique call; offer shared-source
navigation/editing instead of rewriting loops or duplicating definitions automatically.

-> 

3. How should expression-valued properties be edited?

Recommended: edit literal values directly; preserve expressions such as width/2. Movement/rotation may add or update
an explicit transform wrapper around the eligible call, leaving its original expressions intact. Do not infer an
inverse formula or decide which shared variable to change. For a derived parameter, offer navigation to its input or
an explicit Make independent action that replaces that call argument with a literal and states the relationship lost.

-> 

4. How should preview, commit and cancellation work?

Recommended: show a temporary preview during dragging/numeric adjustment; mouse release or Enter requests commit.
Validate the exact proposed source against the captured inputs before applying one source transaction. Esc cancels;
failed validation leaves the original buffer unchanged and shows the error. Reject stale inputs rather than applying
to a newer document. One gesture is one normal Undo step; preview state cannot become a second saved model.
The technical plan must prove the candidate-evaluation path, including changes in included live buffers.

-> 

5. How should manipulation of an attached component behave?

Recommended: keep the live attachment. Move changes its offset in the target-anchor frame; rotation changes spin
around that anchor's normal. Other rotations are unavailable while attached. Reuse 08's expression-preserving adjust
fields and explicit shared-edit policy. Defer a graphical detach/free-move action until preserving the current pose
and source ownership is specified; source editing can still change/remove an attachment explicitly.

-> 

6. Which files can a gesture edit?

Recommended: one writable source document per gesture, main file or an explicitly opened included file. Open/activate
and identify the actual target before enabling an edit. Preserve existing unsaved text and ordinary Save/conflict
handling. No automatic library-file edits or transactions spanning several documents. When a library-defined object
can be changed by its writable call-site parameters or wrapper, edit that call instead of the library definition.

-> 
