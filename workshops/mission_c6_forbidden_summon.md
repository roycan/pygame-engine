# 🌀 RogueEdu — MISSION C-6: The Forbidden Summon (Genin Edition · Git Bash)

**Name:** ______________ **Team:** ______ **Rank earned:** ______

**Prerequisite:** Missions D-1 → C-5 complete. Four monsters hunt your board (Slime 🟢,
Shadow 👥, Coward Goblin 👺, Suspicious Box 📦) and the chakra check says
`Summary: 6 passed, 0 warnings, 0 failures.`

**Roles (rotate now):**
**Operator** — the only hands on the keyboard ·
**Navigator** — reads the scroll aloud, keeps the steps ·
**Scout** — predicts, watches the result, records the evidence ✍️

**Village laws:**
1. **Predict before you run.** A wrong prediction is information, not failure.
2. **One change at a time.** Then run and observe.
3. After **90 seconds** of being stuck → raise your hand. That's the rule, not defeat.
4. Write your evidence in the scroll. Evidence is your rank.
5. **"You decide. The engine acts."**

**Shell law:** every command is **Git Bash** — your prompt must show `MINGW64 … $`.

**⚠️ Today is different:** this mission **crashes the game on purpose — twice.** The
crashes are the lesson. You will read real tracebacks, learn their anatomy (the **last
line** is the crime; the **line above it** is the scene), and fix what they name. The
chakra check would catch these mistakes too — today we let the village burn so you can
read the smoke.

---

## 🥷 PHASE 1 — The Forbidden Base (4 mins)

**Objective:** summon the blueprint itself — and read Python's refusal.

**PREDICT (Scout writes the team's answer BEFORE running):**
`Villain` is the abstract blueprint every monster inherits from. You summon it directly.
What does the village do? ______

**Steps (Operator types, Navigator reads):**
1. Open **`game_config.py`** (same `student_starter` folder).
2. Change the engine import so it reads exactly:
   ```python
   from engine.base_classes import Villain, Wall
   ```
3. Directly above `game.add_villain(Slime(x=7, y=7))` add the forbidden line:
   ```python
   game.add_villain(Villain(2, 2))
   ```
4. Save. Wake the village: `Ctrl+C` the old server, `cd rogue_edu` (skip if the prompt
   already ends in `rogue_edu`), then `../venv/Scripts/python.exe app.py`.
5. Browser → refresh **http://127.0.0.1:5000**.

**Expected result — three facts, in order:**
1. The terminal **still shows the banner** — the server booted fine.
2. The browser shows **Internal Server Error**. The page is dead.
3. The terminal has a long traceback. **Read it backwards:**
   - **Last line** — the crime:
     ```
     TypeError: Can't instantiate abstract class Villain without an implementation for abstract method 'act'
     ```
   - **Line above it** — the scene, naming your file and line:
     ```
     File ".../student_starter/game_config.py", line 49, in create_game
         game.add_villain(Villain(2, 2))
     ```

**The banner lies. The browser screams. The terminal confesses.** Always read the
terminal.

**✅ Completion check (Scout):** copy the last line of the traceback verbatim:
_______________________________________________________________

**If it differs:** the page loads normally → the forbidden line didn't save (`Ctrl+S`,
refresh again). Server won't boot at all → the import line is broken (rescue card #3).

---

## 🥷 PHASE 2 — The Incomplete Golem (4 mins)

**Objective:** summon a monster that forgets the contract — same crash, new name.

**Steps (Operator):**
1. **Remove the forbidden line** (`game.add_villain(Villain(2, 2))`) and restore the
   engine import so it reads exactly:
   ```python
   from engine.base_classes import Wall
   ```
2. Open **`classes.py`**. At the very end of the file, press Enter twice and paste:
   ```python
   class Golem(Villain):
       def __init__(self, x: int, y: int):
           super().__init__(x, y)
           self.name = "Stone Golem"
           self.hp = 50

       def symbol(self):
           return "🪨"
       # INTENTIONALLY MISSING def act(self, view):
   ```
3. Open **`game_config.py`**. Change the student import so it reads exactly:
   ```python
   from student_starter.classes import BraveKnight, Golem, Elder, Slime
   ```
   and directly above `game.add_villain(Slime(x=7, y=7))` add:
   ```python
   game.add_villain(Golem(2, 2))
   ```
4. Save both. `Ctrl+C`, relaunch, refresh the browser.

**Expected result:** the SAME anatomy, a NEW criminal. Internal Server Error again; the
traceback's last line now names your golem:
```
TypeError: Can't instantiate abstract class Golem without an implementation for abstract method 'act'
```
**One honest footnote:** the chakra check would have caught this before the game —
`[FAIL] Villain 'Golem' is missing the act() method.` Today you read the raw crash
anyway, so the traceback stops being scary.

**✅ Completion check (Scout):** the last traceback line names ______ instead of
`Villain`. Same crime, different criminal.

**If it differs:** `NameError: name 'Golem' is not defined` → step 3's import was
skipped (rescue card #3). Anything else → rescue card #2.

---

## 🥷 PHASE 3 — Fulfilling the Vow (4 mins)

**Objective:** sign the contract — in two moves, because the first move alone springs a
hidden trap.

**Steps (Operator):**
1. In `classes.py`, add the missing method to the Golem (right after `symbol`):
   ```python
       def act(self, view):
           return WaitAction()
   ```
2. Save. `Ctrl+C`, relaunch, refresh — **STILL 500.** Read the new last line:
   ```
   TypeError: Character.__init__() missing 3 required positional arguments: 'y', 'hp', and 'attack_power'
   ```
   **A different crime.** The contract is signed — but the Golem's `__init__` calls
   `super().__init__(x, y)`, and `Character` wants five things: a `name`, `x`, `y`,
   `hp`, `attack_power`. Your `x` was silently eaten as the *name* (that is why `'x'`
   is missing from the list of the lost!), and the rest never arrived.
3. Fix the vow properly — make the Golem's `__init__` read exactly:
   ```python
       def __init__(self, x: int, y: int):
           super().__init__("Stone Golem", x, y, hp=50, attack_power=4)
   ```
   (the `self.name = "Stone Golem"` and `self.hp = 50` lines are no longer needed —
   delete them).
4. Save. `Ctrl+C`, relaunch, refresh.

**Expected result:** the village finally boots. The board shows the golem 🪨 on tile
(2, 2) with a full HP bar, waiting like a statue. The chakra check — run it, from the
repo root — now says:
```
[PASS] Villain 'Golem' inherits Villain and act() returned WaitAction().

Summary: 7 passed, 0 warnings, 0 failures.
```
The contract is fulfilled, and the village gate is still green
(`venv/Scripts/python.exe -m pytest -q` → `193 passed`).

**✅ Completion check (Scout):** two lines of evidence: the hidden second crash, and
the `[PASS] Villain 'Golem'` line. Both verbatim, both in the scroll.

**If it differs:** `NameError: name 'WaitAction' is not defined` → the C-5 import edit
was reverted (rescue card #4). Still the abstract TypeError → the method name isn't
exactly `act` (rescue card #2).

---

## 🥷 PHASE 4 — The Abstraction Interrogation (3 mins)

**Objective:** say why the village refused to play — and what disaster it prevented.

**The question (Navigator reads, team answers before writing):**
Why did the engine refuse to let us play until we added `act(view)`? What disaster
would happen in `core.py` if it allowed the incomplete Golem onto the board?

_______________________________________________________________

**Answer check:** the game loop's move-request is
`action = villain.act(view)` — every turn, for every villain, no questions asked. An
incomplete Golem on the board would crash the game **mid-fight** with an
`AttributeError` the first time the loop called `act()` on it — with players holding
the controller. The abstract contract moves that failure to **boot time**: one clean
`TypeError`, one named class, one named method, before anyone plays.
**The crash is a kindness.**

**Push one question further (Scout challenge):** which crash taught you MORE today —
the polite boot-time `TypeError` or the mid-fight `AttributeError`? Defend your answer
using the traceback anatomy from Phase 1.

**✅ Completion check (Scout):** your team's one-line answer to THE question:
_______________________________________________________________

---

## 🎖 Rank earned

| Step | Done | Evidence written |
|---|---|---|
| Phase 1 — forbidden summon + traceback read | ☐ | ☐ |
| Phase 2 — incomplete Golem, same anatomy | ☐ | ☐ |
| Phase 3 — the vow fulfilled, both moves | ☐ | ☐ |
| Phase 4 — interrogation answered | ☐ | ☐ |
| Village gate — 7 PASS + `193 passed` | ☐ | ☐ |

You crashed the village twice, read the smoke both times, and rebuilt it stronger.
**Rank C Shinobi status: CONFIRMED — Genin Contract-Keeper.**

> *"You decide. The engine acts."* — the village's one law.

*(Teachers: the rescue card for this mission lives in the teacher pack. Unstick teams
with the 90-second rule; the traceback is the first responder.)*

*Scroll forged in 2026 by Sir Roy from the PSHS curriculum. Village infrastructure and jutsus engineered alongside Hermes, Gemini, and ChatGPT.*
