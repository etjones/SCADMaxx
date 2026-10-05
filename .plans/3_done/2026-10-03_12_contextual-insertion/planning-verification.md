# Planning verification, 2026-10-04

Executed source examples only; no insertion feature build or UI/worker runtime verification.
Artifacts: D:/openscad/runs/20261004-contextual-insertion-planning/.
Existing console executable: D:/openscad/artifacts/20261003-scadmaxx-executable-name/attempt-2/extracted-check/scadmaxx.com.
Launcher SHA-256: 29dbf910f840c565686eed856a1a0cbb6d20181fea1630878ba9da2505b8f5e2.
Application scadmaxx.exe SHA-256: 8b7834a99c7bb74a48ab93780293aa1e79ccabb7b6bd579c9ae04ae522230f05.
The application comes from retained source audit 4c325716b94e444637a80df3966197ce110b2b75.

Invocations used --hardwarnings --summary all --summary-file <case>-summary.json -o <case>.stl <fixture>.
Both returned exit 0 and produced the expected nonempty geometry outputs. No new compiler/build was run.

| Case | Source SHA-256 | Bounds | Mesh volume / expected |
| --- | --- | --- | --- |
| fixtures/ordinary-cut.after.scad | 3023118a4904a482109a0794dbee2399269c8aee4d68c1e2d5b2d5b0c3e199ad | [0,0,0]..[20,20,10] | 3875.142193909678 / 3875.142193909678 |
| fixtures/ordinary-add.after.scad | 88d9cb9864561846f2ad8e865233d61f3f1e4c39b0fc305ecddd114d4862c972 | [0,0,0]..[20,20,40] | 10000 / 10000 |

Both native summaries report simple 3D geometry; cut has 144 triangles/72 vertices, add has 28 triangles/16 vertices.
Volume checked from STL oriented triangle tetrahedra: sum dot(a,cross(b,c))/6. The cut uses a 32-sided cylinder of
radius 2 through the 10 mm block, so expected removed volume is (32/2)*4*sin(2*pi/32)*10. Absolute tolerance 0.01 mm^3.
Add expected volume is 20*20*10 + 10*20*30; the solids meet at one face without overlapping volume.

STL SHA-256:
- cut.stl: 8839e90e3a04c4599e85eeecd66f8fa7b4dc3f8a502c962aef9b3c1277f146cf
- add.stl: 6b6094c7b9e3e00544355be3687bbabea6d02ba70441662acb75941bb840de8d

The semantic shared-Part and named-Component examples require future 07/08 syntax and were not run on the old binary.
They have explicit expected results in phase 3. Two source probes do not validate source-range selection, candidate
isolation, asynchronous cancellation, guarded Commit, single Undo, library matching or native UI behavior.
Those remain required implementation-phase checks. 11's previously executed library probes are separate evidence.

Plan review checked local Markdown links, six phase files, all eighteen requirements, accepted decision propagation,
and removal of the resolved conversation file. The 03 follow-up and 11 role additions are specifications, not source
changes. No chats were started/messaged, no plans moved lanes and no commit/push/promotion/build-stack change occurred.
