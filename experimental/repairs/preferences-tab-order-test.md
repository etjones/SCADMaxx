# Repair: Preferences fallback test with shortcut integration

- State: reusable; applies after pr-6878 and ui-visual-polish.
- Source repository: `D:/openscad/openscad-master`.
- Commit: `61fb8357ad3101852bb2a12fc40421f047f99e68`.
- Failure: `Typography_test.cc` expects Dialogs when hiding the selected AI page.
  Shortcuts is inserted before AI; production correctly selects the preceding visible page.
- Repair: derive the preceding action from the visible tabs, verify it becomes selected and checked,
  and verify triggering it retains the fallback page. Do not change production routing or remove the check.
- Replay: inspect page ordering and the failing assertion, then cherry-pick this commit with `-x`
  if the stale assertion remains. No change is needed if the test already follows visible ordering.
- Verification: run `20261001-scadmaxx-all-features`, failed log
  `logs/20261002T084058878Z-test.log`; first repair passed Configure/Build/Test,
  `logs/20261002T084607042Z-test.json`. No production behavior changed.
