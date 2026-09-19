# Workshop 01 — "Meet the Engine" Implementation Plan

Deliverable: `workshops/workshop_01_meet_the_engine.md` — a 90-minute Grade 9 workshop worksheet
(Gradual Release: ME → US → YOU), with Windows/ZIP setup notes, tiered individual task,
reflection pauses, a quarter-long-project tease, and a teacher answer key.

Gate discipline: everything lands inside the existing `make test` gate (our `npm test` equivalent).
The worksheet is verified three ways: structural contract tests, engine-tested answer code
(a real fixture module), and a worksheet↔fixture sync test that kills doc-vs-code drift.

## Phases and tasks

| Phase | Task | Deliverable | Gate | Feas. | Conf. |
| --- | --- | --- | --- | --- | --- |
| W0 | T0.1 | `tools/package_workshop.py` (curated selection → `dist/rogue_edu_workshop.zip`), `make zip` target, `dist/` gitignored | `tests/test_packaging.py`: includes essentials (`rogue_edu/`, `tests/`, `README.md`, `workshops/`), excludes dev dirs (`venv`, `node_modules`, `temp`, `inceptions`, `plans`, `dist`, caches); built zip nests everything under `rogue_edu_workshop/` | 96 | 97 |
| W1 | T1.1–T1.4 | The worksheet: header blanks (Name/Section/Date), setup-on-Windows first, Hook, "What is this engine" + key features + 5 analogies, ME segment (teacher script), US code-along (fill-in-the-blanks) + Reflection 1, YOU tiered task (🌱 reskin / 🌿 personality / 🌳 mini-arena) + Reflection 2, Quarter tease, Teacher Answer Key | structural gate (T2.1) | 95 | — |
| W2a | T2.2a | `tests/fixtures/worksheet_answers.py`: real answers — `ReskinnedSlime`, `CowardSlime`, `PatrolSlime`, `create_arena_game()` + `SIGNATURE_LINES` | engine tests: coward attacks when healthy / flees when hurt; patrol cycles; reskinned passes the checker; arena boots with 2 villains and plays a turn | 94 | 95 |
| W2b | T2.1 + T2.2b | `tests/test_worksheet.py`: required sections, header blanks, 3 tier emojis, reflection question counts, balanced code fences, referenced files exist, Windows steps present, sync: every `SIGNATURE_LINES` entry appears verbatim in the worksheet | runs in `make test` | 94 | 92 |
| W3 | T3.1 | README workshop pointer; whole `make test` green | full suite | 97 | 97 |

## Simplification decision (the one ≤90 risk)

Parsing Python fences out of the markdown and `exec`-ing them is brittle (~88 feasibility).
Instead: answers live in a real fixture module the engine tests exercise directly (T2.2a), and a
sync test asserts the worksheet contains those signature lines verbatim (T2.2b). Two dumb tests
beat one clever one; the fixture doubles as the answer key's single source of truth.

## Windows setup walkthrough (embedded in the worksheet)

1. Get `rogue_edu_workshop.zip` from the teacher (LMS/USB) → save to Documents.
2. Right-click → Extract All → `rogue_edu_workshop` folder.
3. Python from python.org if missing — tick **Add python.exe to PATH**.
4. VS Code → File → Open Folder.
5. Terminal: `python -m venv venv` → `venv\Scripts\pip install -r requirements.txt`.
6. `venv\Scripts\python rogue_edu\check_my_class.py`
7. `venv\Scripts\python rogue_edu\app.py` → browser `127.0.0.1:5000`; after edits: Ctrl+C, re-run, refresh.
8. Troubleshooting: PATH checkbox, `set PYTHONUTF8=1` for emoji, port-busy.

## Verification doctrine

1. Structural contract (T2.1) — the worksheet must contain the agreed sections/blanks/tiers.
2. Answers provably work (T2.2a) — the exact code students are shown passes engine behavior tests.
3. No drift (T2.2b) — worksheet and tested fixture cannot diverge silently.
4. Pedagogy (pacing/tone/analogies) is human-reviewed — that is the user's draft review.
