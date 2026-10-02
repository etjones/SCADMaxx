# README screenshot brief

User direction recorded on 2026-10-02. Replacement captures were made from integrated source `bcf48145d`
using the [native capture harness](readme-capture-tool.md). The README now links those captures and a matched
regular OpenSCAD baseline. See `docs/screenshots/sources.json` for provenance. Earlier screenshots were rejected;
unreferenced old images are not presentation references. Future replacements must continue to follow this brief.

## Shared presentation requirements

- Capture the SCADMaxx examples from the same working integrated build so the UI looks uniform.
- Use deliberate, feature-focused window and panel layouts. Hide the editor when it does not help demonstrate
  the feature; remove unrelated panels and other distractions.
- Show meaningful models and real interactions that explain what users can do. Do not substitute generic test
  fixtures, empty controls, incidental verification captures or design mockups for feature demonstrations.
- Keep the agreed README structure: new features first, then included PRs, with the UI changes grouped into
  one **UI improvements** section.
- Keep linked thumbnails opening full-size screenshots, with left/right placement alternating between sections.
- The README remains hand-maintained. This brief records future work; it does not start a build, schedule a task,
  or call for screenshot replacement before the integrated build works.

## Annotations

- Choose an object with a visible defect or a concrete need for improvement.
- Make an actual **red** annotation identifying that problem on the object.
- Capture the annotation/comment dialog open, with text describing the defect and the desired improvement.
- Keep the annotation tool visible in the frame, so the screenshot clearly communicates how the user makes marks.
- Compose the image around the object, red mark, annotation tool and explanatory dialog; hide the editor unless
  it is necessary. A plain model or a saved annotation list alone does not satisfy this shot.

## Navigation cube

Capture two complementary screenshots:

1. A focused view of the navigation cube itself, large enough to understand its controls.
2. The full application UI with the navigation cube's menu/popup expanded, showing its controls in context.

For the contextual shot, use a feature-focused application layout; full UI does not mean every dock must be open.
Hide the editor when it adds no value, and keep the model and expanded menu readable.

## UI improvements

- Show **old versus new**, demonstrating what changed rather than merely showing the new interface.
- Use matching models, panel layouts, themes, window sizes and display scales wherever possible so differences
  in typography, spacing, icons, Customizer and dialogs are easy to compare.
- Capture the new side from the integrated SCADMaxx build. Use the appropriate regular OpenSCAD baseline for
  the old side, and identify both versions in the screenshot provenance.
- Select comparisons that make the changes visible at thumbnail size; supplementary detail views can support them.

## Agent access

- Show only the connection dialog. The API workflow is difficult to convey visually; do not add terminal output,
  syntax-tree data or a generic viewport capture as a substitute.
- Frame the actual dialog clearly, with unrelated application panels out of the way.

## Customizable keyboard shortcuts — PR #6878

- Show the new keyboard-shortcut dialog with real application actions, not test-fixture action names.
- Frame the dialog so its action list and shortcut controls are readable.

## Dynamic dark-mode switching — PR #6776

- Show light-mode and dark-mode renders of the application.
- Use the same model, camera, panel layout, window size and display scale for both, so the theme difference
  is clear and the two images form a direct comparison.

## Windows fixes

Omit Windows fixes entirely from the README feature overview. They are build/compatibility maintenance,
not a product feature. Keep their details in the technical build and repair documentation; do not add screenshots
or restore a text-only feature section for them.

## Resume point

Once the integrated build works and screenshot work resumes, read this brief first. Record the build revision
used for captures and replace the rejected placeholders with deliberate demonstrations meeting the requirements
above. Do not silently relax a shot requirement if the UI cannot show the requested state; report that limitation.
