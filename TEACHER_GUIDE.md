# RogueEdu — Teacher's Guide

*How your Grade 9 students build a real, visual, turn-based RPG in Python — and put it on the internet for free.*

This guide is for **teachers**. If you want the student-facing lesson, go straight to
[`workshops/workshop_01_meet_the_engine.md`](workshops/workshop_01_meet_the_engine.md).
If you want the deploy details, go to [`DEPLOYING.md`](DEPLOYING.md).
This document explains the **why** and the **classroom path** so you can teach with confidence.

---

## 1. The 30-second pitch

Students edit **two Python files**:

1. [`rogue_edu/student_starter/classes.py`](rogue_edu/student_starter/classes.py:1) — they write *classes* (a Hero, some Villains, an NPC),
2. [`rogue_edu/student_starter/game_config.py`](rogue_edu/student_starter/game_config.py:1) — they *assemble* those classes into a 10×10 board with a win condition.

Everything else — grid rendering, keyboard input, turn order, combat math, win detection, the web page — is handled by the engine. When they run `python app.py`, their game opens in a browser. When they push to GitHub and connect Render, the same game lives at a real `https://…onrender.com` URL that friends and family can play.

**You do not need to know Flask, JavaScript, HTML, or CSS to teach this.** The two student files are pure, ordinary Python: classes, methods, `super()`, `return`, one `if`, one `for` loop.

---

## 2. Why this engine exists (the teaching problem it solves)

Object-oriented programming is the hardest abstraction Grade 9 meets: "a class is a blueprint," "a method belongs to an object" — none of it *visibly means anything* for weeks. RogueEdu closes that gap by making every OOP idea produce an **immediate consequence on a grid they can see**:

| OOP concept | Where students touch it | What they *see* happen |
| --- | --- | --- |
| Inheritance | `class Slime(Villain):` | Their creature appears on the board |
| Method overriding | `def act(self, view):`, `def symbol(self):` | New behavior, new emoji sprite |
| Calling the parent with `super()` | `super().__init__("Slime", x, y, hp=10, ...)` | Stats show up in the UI |
| Return values | `return MoveAction(dx, dy)` | The creature actually moves |
| Conditionals | "attack if adjacent, else chase" | Visible AI personality |
| Composition | placing instances in `game_config.py` | The level itself changes |
| Read-only data / encapsulation | the `view` object handed to `act()` | Students *sense* the world, never mutate it |

And the deployment step turns the project into a **real-world software story**: code → GitHub → live URL. That is the same loop professional developers use, minus the parts that need money or Linux administration.

---

## 3. The one idea that makes it all work: *"You decide, the engine acts"*

This is the single most important thing to internalize as a teacher, because it answers almost every "what if a student…" question.

**Students never move anything.** Their methods are asked for an *intent*, and they *return* it:

```python
def act(self, view):
    dx, dy = view.get_direction_toward_hero(self)   # 1. SENSE (read-only)
    if view.distance_to_hero(self) == 1:            # 2. DECIDE
        return AttackAction(dx, dy)                 # 3. RETURN an intent
    return MoveAction(dx, dy)
```

The engine then validates that intent and performs the actual move/hit. Consequences:

- A student cannot corrupt the game state, teleport, or write an infinite game-breaking loop — the engine is the **sole mutator** of the board.
- `AttackAction(dx, dy)` carries a *direction*, never a damage number. Damage comes from `attack_power` and is sanitized engine-side (negative → 0, above 40 → 40), so an "overpowered" override quietly gets clamped instead of breaking the class.
- Out-of-range stats are **clamped loudly**: the game runs, and a human-readable warning appears in the log. A typo never nukes the lesson.

Read the starter [`rogue_edu/student_starter/classes.py`](rogue_edu/student_starter/classes.py:1) once end-to-end — it is 77 lines including comments, and every class in it is a complete, working example students are meant to rename, reskin, and extend.

---

## 4. The student workflow (five steps, one loop)

Students spend the whole unit inside this loop. Each step has a built-in safety net.

### Step 1 — READ the worked example

[`rogue_edu/demos/demo_dungeon/`](rogue_edu/demos/demo_dungeon/README.md:1) is a finished game with three *different* villain AIs. Students run it first:

```bash
GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py
```

Seeing a "done" game before writing code is deliberate: it sets the target and proves the engine works.

### Step 2 — EDIT their classes

[`rogue_edu/student_starter/classes.py`](rogue_edu/student_starter/classes.py:1). The contract is tiny and stated in the file header:

- `Hero` subclasses: no `act()` needed — the keyboard drives them. Customize name, stats, emoji.
- `Villain` subclasses: **must** implement `act(view)` returning a `MoveAction` / `AttackAction` / `WaitAction`.
- `NPC` subclasses: **must** implement `interact(view)` returning a `SpeakAction` (shown as a dialogue box; villains freeze while it is open).
- Every entity overrides `symbol()` to choose its emoji.
- Coordinates are **not** stored in classes — they belong to the config file (see Step 4).

### Step 3 — CHECK with the code doctor

```bash
cd rogue_edu
python check_my_class.py
```

[`rogue_edu/check_my_class.py`](rogue_edu/check_my_class.py:1) reads their file and prints `[PASS] / [WARN] / [FAIL]` lines **with friendly fix suggestions — never a raw traceback**. It verifies inheritance, required methods, that construction with `(x, y)` works, and that `act()`/`interact()` actually *return* valid actions when called against a mock view. Exit code 1 on any `[FAIL]` means you can even use it in grading scripts.

This is your classroom management tool: "the doctor says PASS" is an objective, checkable milestone students can reach *themselves*, without queueing for you.

### Step 4 — ASSEMBLE the game

[`rogue_edu/student_starter/game_config.py`](rogue_edu/student_starter/game_config.py:1) is **composition only**: instantiate, place, register. Students pick one of three win modes by changing one line:

```python
# A) Arena:      defeat every villain            win_condition="defeat_all"
# B) Escape:     reach the trophy tile           win_condition="reach_goal", goal_pos=(9, 9)
# C) Classic:    clear the room, then exit       win_condition="clear_and_reach_goal", goal_pos=(9, 9)
```

Registration order matters and is teachable: villains take their turns **in the order you add them**, and walls are placed with a plain `for` loop over `(name, x, y)` tuples — a natural place to introduce loops to the class.

### Step 5 — PLAY

```bash
python app.py        # open http://127.0.0.1:5000
```

Controls are one line to teach: **WASD** moves (bumping a villain attacks it; bumping an NPC talks to it), **Space** waits, **any key** closes dialogue for free.

Then the loop repeats: *edit → check → play*. Instant feedback, low floor, no ceiling — a student can go from "recolor my slime" to "write a cowardly archer that flees when the hero gets close" in the same codebase.

---

## 5. What one turn actually does (so you can answer "how does it work?")

You will be asked this. The honest, complete answer in five sentences:

1. The browser sends the keypress to the Flask server ([`rogue_edu/app.py`](rogue_edu/app.py:1)) at `POST /api/step`.
2. The engine ([`rogue_edu/engine/core.py`](rogue_edu/engine/core.py:1)) translates the key into the Hero's intent and resolves it (move / bump-attack / bump-talk / wait).
3. It checks for a win, then gives every living villain its turn — each villain's `act(view)` is called, its returned intent validated and applied.
4. The engine packages the new board state as **JSON** (positions, hp bars, log lines).
5. The browser's small vanilla-JS renderer ([`rogue_edu/static/game.js`](rogue_edu/static/game.js:1)) draws that JSON on an HTML5 canvas.

Students who ask can be told: *"your Python decides, the engine referees, the browser draws."* Curious students can read `game.js` — but nothing in the curriculum requires it.

---

## 6. Differentiation ladder (already built into the workshop)

The 90-minute workshop worksheet ([`workshops/workshop_01_meet_the_engine.md`](workshops/workshop_01_meet_the_engine.md:1)) uses Gradual Release — **ME** (teacher demos) → **US** (guided trace) → **YOU** (independent build) — with a three-tier YOU task:

- 🌱 **Reskin** — change names, stats, emojis. Achievable by every student in minutes.
- 🌿 **Personality** — write a new villain AI (a "coward" that moves *away* from the hero; a "berserker" that always charges). Requires a real `if` and real reasoning about `view`.
- 🌳 **Mini-arena** — compose a new level in `game_config.py`: walls, multiple villains, a chosen win condition.

Assessment is built in: the checker's output, the working game itself, and two reflection pauses (3 questions each) already written into the worksheet. An answer key for teachers is at the bottom of the worksheet, with a single source of truth in [`tests/fixtures/worksheet_answers.py`](tests/fixtures/worksheet_answers.py:1).

---

## 7. Deployment — Render + GitHub, because it IS the lesson

One path, documented step-by-step in [`DEPLOYING.md`](DEPLOYING.md:1): push the class repo to GitHub, create a Web Service on render.com, set the start command (a [`Procfile`](Procfile:1) with the exact command already lives in the repo), add one environment variable (`SECRET_KEY` = any long random string). From then on, *every* merge of a student pull request auto-redeploys — fork → PR → merge → the class arcade at `/games` updates. That loop is the real-world skill, and students can genuinely own it. (The old ZIP-upload path was retired on purpose: teaching one real workflow beats teaching two.)

**Two honest limitations to state up front** (they are features of free hosting, not bugs, and both are already handled):

1. *Games live in memory.* If the server sleeps or restarts, the next visitor gets a fresh board. There is a Reset button in the UI anyway, so nothing is lost.
2. *One worker, always.* The start command pins `--workers 1` because two workers would keep two separate game worlds and split players mid-game. Do not "fix" slowness by raising it.

Windows note for your lab: students run `venv\Scripts\python rogue_edu\app.py` locally; `gunicorn` (in [`requirements.txt`](requirements.txt:1)) is Linux-only and only ever runs on the hosting platform — installing it on student laptops is harmless.

---

## 8. Common teacher worries, answered

**"What if a student's code crashes the game?"**
The engine validates every returned action; bad stats are clamped *with a warning*, never with a crash. And [`rogue_edu/check_my_class.py`](rogue_edu/check_my_class.py:1) catches syntax errors, missing methods, and broken `__init__` signatures *before* the game ever runs — with friendly fixes instead of tracebacks.

**"Can students cheat — giant damage, teleporting?"**
No. Attack damage is computed from sanitized `attack_power` (0–40) engine-side; movement happens only through validated intents; the `view` given to `act()` is read-only. Overrides of the damage method exist for flavor (critical hits) but are never trusted.

**"How much do I need to understand before teaching it?"**
Read [`rogue_edu/student_starter/classes.py`](rogue_edu/student_starter/classes.py:1) (77 lines) and [`rogue_edu/student_starter/game_config.py`](rogue_edu/student_starter/game_config.py:1) (54 lines) and play the demo dungeon. That is the entire student-facing surface. The engine internals ([`rogue_edu/engine/`](rogue_edu/engine/core.py:1)) you can treat as a black box — it is protected by the full automated gate (`make test` — 185 pytest + 21 node tests at last count), including end-to-end golden scenarios, so its behavior is pinned.

**"What does a multi-week unit look like?"**
Week 1: workshop (`make zip` builds the ready-to-distribute [`dist/rogue_edu_workshop.zip`](tools/package_workshop.py:1); Windows setup walkthrough included). Weeks 2–3: the edit→check→play loop toward a tiered goal. Week 4: deploy to Render, then a play-day where students try each other's games and explain each other's villain AI — explaining the AI *is* the code review.

**"How do I prove it works before standing up in front of a class?"**
Clone it, run `make test` (the whole gate green), run the checker, run `python app.py`, open `/games`, play. Ten minutes, and you have personally verified every claim in this guide.

---

## 9. Where everything lives

```text
TEACHER_GUIDE.md            ← you are here
README.md                   ← quick start + manual visual checklist (incl. mobile points)
DEPLOYING.md                ← Render + GitHub, step by step
workshops/                  ← the 90-minute student worksheet + answer key
rogue_edu/student_starter/  ← THE two files students edit (Weeks 1–4)
rogue_edu/arenas/           ← the class arcade: _template + sample_pair + one folder per pair
rogue_edu/demos/            ← read-only worked example (three villain AIs)
rogue_edu/engine/           ← the black box students never edit (the test gate guards it)
rogue_edu/check_my_class.py ← the code doctor (also checks pair arenas + TITLE)
Makefile                    ← make test (the gate) · make zip (Workshop 01) · make smoke (live check)
```

The pitch to your students writes itself: *"You write two Python files. You get an RPG game on the internet — with a menu card next to all your classmates' games."*

---

## 10. The class arcade (`/games`)

Every merged folder under [`rogue_edu/arenas/`](rogue_edu/arenas/README.md:1) becomes a playable card on the deployed site's `/games` page — auto-discovered, no registration, no shared file to edit, so pull requests never conflict on anyone else's code. What you should know as the teacher:

- **The recipe lives in [`rogue_edu/arenas/README.md`](rogue_edu/arenas/README.md:1)**: copy `_template/`, rename the folder (lowercase/underscores — it becomes the URL), set `TITLE`, compose the game, pass the doctor, PR.
- **The gate is the doctor**: `python check_my_class.py arenas/<pair>/game_config` checks the pair's classes AND that `TITLE` is set (it names their menu card).
- **Broken arenas cannot break the site.** Discovery is fail-soft: a folder that cannot build its game shows a yellow "needs fixing" card *with the error printed on it* — send the pair to read their own production error; that is real debugging, in public, with training wheels.
- **One URL serves the whole class**: sessions are per-browser-cookie and the deployment pins `--workers 1`, so every visitor gets a private game while sharing the arcade.
- **CI guards the merges**: [`.github/workflows/tests.yml`](.github/workflows/tests.yml:1) runs the full gate on every PR — merge green PRs only, and the arcade stays healthy.
- **Local live check**: `make smoke` boots the real server and probes every page. It is deliberately outside `make test` so it can never flake the gate.
