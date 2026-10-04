# Source-first features: local commits and build selection

Recorded 2026-10-04 after explicit authorization to commit completed features locally and select them for the build.
No push, promotion, integrated build or release was performed. This record supersedes the uncommitted-state wording
in the original feature handoffs; their tested patch identities and verification limits remain authoritative.

## Committed feature boundaries

| ID | Feature branch | Feature head | Delta base |
| --- | --- | --- | --- |
| 01 | `feature/agent-skill-workflows` | `4e5fe1b611d2ec4e6a77337511a71f1c965c3732` | `af7a0882deab83c0970360ea343e0689617eacaf` |
| 02 | `feature/source-editing-foundation` | `3131a23d6ec04f4405952d8804a41dd8296b2dc5` | `179f2d528ef32bfcdde3ad70f3094a1a2472a8c6` |
| 03 | `feature/selection-model-inspector` | `e2b3a49470b67f46b433762bdd8d49aa8be7147e` | `b611584e013b8b4dbee123d62fabe9621b4bc137` |
| 04 | `feature/live-clipping-sections` | `3e81b46a59f929870e7066e40dcf3809f4d9a2d6` | `2878c9234181f6a9cfadbd93af0e00dfc37ec42a` |
| 05 | `feature/vim-editor-mode` | `1c48233689c4582754784c66fd23ed4273d56981` | `657aeead6534583964bec8797ae99f445404714c` |
| 06 | `feature/source-geometry-provenance` | `bb68db75a8d0fb259d17f50322306007d3750ebe` | `6c8d2634c9de02265166464a1ab89fbb09eab6b8` |
| 07 | `feature/semantic-model-hierarchy` | `7e50bf157b4993ef183019e1e26e00ebd919b58f` | `e1d33c876493ed7bbe0dc61c3183280f0347e4d2` |
| 08 | `feature/anchors-attachments` | `629a6d7c809d7493583451f6a7b3ca3bb5e057b8` | `af0948f5d9711dc7f9336f6e08ffce21aba87364` |
| 11 | `feature/component-provider-adapters` | `9d0cb2097efcac6856ae5dafb31a642803ec32d7` | `35145c58c2b7c018158ce010ac18f8564a192923` |
| 12 | `feature/contextual-insertion` | `9db25842df0c3d7aad6a26bd6d96a7da86d189fe` | `2895ab7f882ca65a4b4fe35fc726ae7f74e1b43b` |
| 14 | `feature/design-object-persistence` | `015aa3172759c00979830ab178cc3515b4e7fd50` | `0b7edfd57110dead25670bfbb83b743a2abf330a` |
| 15 | `feature/geometry-services` | `4e1286c7b362f84e920a21ba65e13042178a6fea` | `e95c9bd5662f20e6df671889a3351c28a6b0f90e` |

## Separately selected foundation follow-ups

| Stack entry | Base | Head |
| --- | --- | --- |
| semantic-foundation-followups | `29c7ce594716b0fb2bb851b685113cd9248496bc` | `e1d33c876493ed7bbe0dc61c3183280f0347e4d2` |
| anchor-foundation-followups | `b223fe6702d13debc53f7c1d8ecec5ae53006131` | `af0948f5d9711dc7f9336f6e08ffce21aba87364` |
| insertion-foundation-followups | `5c5d75b133af95f90763853992bf90b62fd308dc` | `2895ab7f882ca65a4b4fe35fc726ae7f74e1b43b` |

## Preservation and verification

Each existing feature branch now retains a prerequisite/repair snapshot followed by its feature-only commit.
For 07/08/12 an intervening foundation commit retains the recorded owner follow-ups separately. The build stack
selects that intervening delta before the consumer. Never merge an entire branch as though its inherited inputs
were all new feature code. Initial snapshots are retained for reproducibility, not selected as feature deltas.

Feature 01 separately retains its recorded pre-existing control inputs, then only its fourteen owned files.
No source working files were edited. Temporary indexes assembled snapshots, checked frozen patches against current
files (allowing only end-of-line differences), and split the exact recorded deltas. Existing staged changes would
have stopped the operation. Source indexes were synchronized after the branch updates; all twelve worktrees report
clean. Excluded/ignored build outputs and generated submodule files were not swept into feature commits.

Detailed preparation, per-feature patch SHA-256 values and committed trees are retained under
`D:/openscad/runs/20261004-feature-local-commits/{prepared,commits}.json`. Original handoff reports retain native,
unit, DPI and selected composition evidence. This was a commit/selection operation: no build or behavior tests
were rerun and no new integrated binary was produced.

Registry readiness remains false until explicit promotion to its declared repository. No remote refs changed.
Unrelated dirty controls, README edits, planning work and the performance experiment were preserved.

The next integration must review newer upstream/prerequisite overlaps and apply required Windows repairs separately.
The source feature heads identify the tested code; they do not establish clean-machine or other-platform coverage.

Selection validation passed: 22 ordered native entries, including 14 newly selected entries awaiting promotion.
All twelve final Git trees match the prepared snapshots; feature diff statistics match the recorded feature patches.
