# Capture README features from a shipped release

Use this recipe when asked for screenshots from an existing integrated executable. Read
[the presentation brief](readme-screenshots.md) first. This task does not require another build,
test run, feature integration, or port of the older capture harness.

## Find and reuse the inputs

1. Resolve the latest delivered executable from `docs/workspace.md` and its linked run report.
   Verify its path and recorded source revision; do not infer the release from a source worktree
   name or the newest directory timestamp. Record the executable hash in image provenance.
2. Read the pending image slots in `README.md`, then compare them with files and entries in
   `docs/screenshots/sources.json`. A commented slot can already have a captured asset. Report
   that distinction and do not recapture it merely because the README still says pending.
3. Reuse the models under `docs/screenshots/models/`. Keep them together: several use
   `enclosure-cutaway.scad` as an adjacent library. Do not recreate these models, copy generic
   test fixtures, or research their syntax again unless the current release rejects them.
4. Use one task-owned application instance and the current computer-use skill. Select it by
   the exact release executable and returned window identity. Leave user instances alone.
   Launch visibly through the supported native-app API; a hidden process is not useful here.
5. Open a demo file and press F5 before interacting with its model. A newly opened document
   can still show the previous document's geometry until evaluation completes.

The 2026-10-07 capture batch used shipped revision `569220a50377c705a4c3af5cc21fd106b2e91662`.
Its images are capture candidates, not evidence of user approval. See `sources.json` for hashes,
descriptions and limitations. Resolve the delivery again for a future batch; do not hard-code
that historical executable as the latest release.

## Shot recipes

All paths below are relative to `docs/screenshots/models/`. Hide unrelated docks through Window.
Use the cameras already declared in the files, then adjust zoom only to fit the chosen layout.

| Image | Model | Real interaction and visible result |
| --- | --- | --- |
| `model-inspection.png` | `enclosure-assembly.scad` | Show Inspector; select a housing surface. Show its picked point, frame and source candidates. Choose the housing invocation so source-navigation buttons become available. Hide the editor. |
| `parts-assemblies.png` | `enclosure-assembly.scad` | Show Model structure and Inspector. Select Housing in the tree and show component parameters and the corresponding geometry bounds. Hide the editor. |
| `live-sections.png` | `enclosure-cutaway.scad` | Show Cross sections. Create a session cross section, enable cross section clipping, choose Above (+Z), set Position Z to 13, and show the cutting plane. Frame the cut walls/posts and plane-origin dot. Do not save to source merely for the shot. |
| `objects.png` | `object-enclosure.scad` | Show the object literal and its property accesses in the editor, with the evaluated enclosure beside it. Hide Inspector, Console and Customizer. |
| `customizer-attributes.png` | `reactive-enclosure.scad` | Show the attribute declarations, model and Customizer. Expand Housing and Lid; collapse the camera Parameters group. Include lid=true shows thickness; false hides it. Capture the true state with both housing and lid in view. Discard temporary preset changes afterwards. |
| `vim-editor.png` | `object-enclosure.scad` | Temporarily enable Vim in Preferences. Select the object literal with real Vim visual-line commands (`V`, then line movement); retain the VISUAL LINE indicator. Capture editor plus model, then restore the previous Vim setting. |
| `anchors-attachments.png` | `anchored-enclosure.scad` | Show Inspector, choose `Anchor · rim · /case` in Select reference, and scroll to the resolved anchor/frame and editing controls. The lid is placed by a mate attachment with a 12 mm offset. Do not apply edits for the shot. |
| `contextual-insertion.png` | `anchored-enclosure.scad` | Use **Design > Add…** (Shift+A with viewport focus), then pick the housing's right outer face. Search Cylinder and select it. Confirm Sensor housing is the editable destination. Wait for “Insertion preview — not committed” and enabled Commit; show the mounting boss, parameters and placement controls. Close the automatically opened Inspector to give insertion the full dock height. Capture, then cancel without committing. |

Opening **Window > Add component or geometry** only exposes the dock; it does not start an
insertion session. Its stale/empty destination controls are not proof that insertion is broken.
Use Design > Add and a fresh surface pick before diagnosing the feature. Built-in Cylinder needs
no external library; unrelated hardware entries may say MissingLibrary. Do not install libraries
just to take this built-in demonstration.

## Layout and capture discipline

- Choose the window size before staging the interaction. The last batch used light application
  UI and a Tomorrow Night viewport at 1283x820; insertion used 1721x1393 to expose its full panel.
  Prefer enough height for readable controls over repeatedly scrolling a cramped panel.
  Old/new comparisons still require matched dimensions and themes per the presentation brief.
- Inspector's parameter area and insertion's parameter area can clip controls independently of
  the outer dock. Check the whole image before saving; a visible dock is not necessarily a usable
  feature demonstration. Do not recreate clipping just to match an earlier capture candidate.
- Scroll over the dock scrollbar or a blank margin, not numeric fields: a wheel over a spin box
  can change its value. If that happens, restore the value before capturing; do not apply it.
- Use fresh accessibility identities and screenshots after each UI action. Do not retain pixel
  coordinates across resizing or hard-code indexes from a previous session. Use the popup's own
  screenshot for menu items when necessary.
- Capture actual application pixels. Do not redraw widgets, synthesize agent conversations or
  use image generation to make a failing interaction look successful.
- If writing image bytes directly to the repository fails in the computer-use runtime, save
  unchanged bytes under its temporary directory, then copy with the normal filesystem tool.
  Do not build another screenshot utility for this permission boundary.
- Record image/model/executable hashes, source revision, actual dimensions and the interaction
  state in `sources.json`. Keep old provenance attached to old images; never imply that the
  2026-10-02 test-enabled captures came from the later shipped release.
- Restore preferences changed for capture, cancel uncommitted previews, discard only task-owned
  temporary changes, and close only task-owned instances. Record settings that could not be restored.
- Leave README prose and image-slot activation to an explicitly requested README edit.

## Known limitations to check, not reinvent

- In the recorded release, selecting `lid_mount` in Inspector says “Named reference is missing”
  even though the attachment positions the lid correctly. Selecting `rim` resolves and shows its
  frame. Keep this diagnostic separate from the successful anchor shot; do not edit application
  source as part of a screenshot request.
- The README cross-section description still mentions graphical rotation/handles removed from
  the current UI. Show current direction/position controls and report stale prose; do not fake handles.
- `openscad-skill.png` requests an agent reviewing an annotated model. It remains uncaptured.
  Follow the current computer-use restrictions on agent interfaces; do not substitute a connection
  dialog, generic model or fabricated conversation. A real, permitted agent-side demonstration
  must be supplied before marking this slot complete.

## Separate future automation work

The older [native capture harness](readme-capture-tool.md) is reusable only with its test-enabled
build contract. Porting/extending it is separate source work requiring build/test authorization.
If repeated capture batches justify it, automate these same model/interaction recipes there,
including settings isolation, deterministic window layout and a screenshot manifest. Do not
quietly rebuild a test-enabled binary when the user requested the shipped executable.
