# Phase 1: vendor boundary and native Scintilla bridge

Covers the foundation of VM01/VM06/VM11/VM15. No user-visible enable switch is exposed until conformance is usable.

1. Record the implemented 02/selected-source base and pin the exact vendor commit. Copy only the families in the overall
   plan into adapted C++ files, keeping notices/license/origin mapping. Use explicit CMake source registration.
2. Remove excluded command tables/helpers and GTK prompt/backend code. Replace GSList/allocation/strings/GDK keys
   with the specified C++/Qt types; remove globals. Convert every position field/message boundary to pointer-sized
   Scintilla types. Do not link unchanged C vendor files beside the adapted copies.
3. Implement Engine/Context, QtKey, ScintillaAccess and per-editor lifecycle with a real QsciScintilla widget fixture.
   Add `src/gui/vim/VimEngine_test.cc` tagged [vim-engine], using an isolated QApplication/settings fixture.
4. Compile the actual selected files with MSVC/Qt/QScintilla, then exercise h/l, i/Escape, x, 2d3w, undo and two
   independent engine contexts. Verify revision notifications and no source replacement/history clearing.
5. Inspect includes/link inputs of the Vim target; literal scan for gtk/gdk/glib headers/symbols must find none in
   executable code. Record any remaining toolkit call as a failed phase, not an invitation to install a dependency.

Exit: all selected adapted sources compile with no toolkit shim or new runtime; minimal real-widget cases pass.
This is the first runtime proof, not work claimed completed during planning. If the specified patch boundary is
insufficient, retain exact failure evidence before changing architecture or engine.
