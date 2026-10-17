# 🌀 RogueEdu — MISSION C-5: The Mimic's Trap (Genin Edition · Git Bash)

**Name:** ______________ **Team:** ______ **Rank earned:** ______

**Prerequisite:** Missions D-1 → C-4 complete. Your board hunts with the Slime 🟢, your
Shadow 👥 and the Coward Goblin 👺, and the chakra check says
`Summary: 5 passed, 0 warnings, 0 failures.`

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

**Today (15 min):** you summon a **Mimic** — a monster that pretends to be a harmless
treasure box until you touch it. Its `symbol()` and its `act()` both read its own `hp`
and change behavior on the spot. Same engine loop, same one-line call — a completely
different personality.

---

## 🥷 PHASE 1 — The Blueprint (5 mins)

**Objective:** subclass `Slime` and let its **own state** (`self.hp`) decide both its
disguise and its behavior.

**Steps (Operator types, Navigator reads):**
1. In VS Code open `rogue_edu` → `student_starter` → **`classes.py`**.
2. **First** — line 3 of the file. It currently reads:
   ```python
   from engine.actions import AttackAction, MoveAction, SpeakAction
   ```
   Add `WaitAction` so it reads exactly:
   ```python
   from engine.actions import AttackAction, MoveAction, SpeakAction, WaitAction
   ```
   *(The mimic waits while it is pristine — and `WaitAction` must be imported to be
   returned. Forgetting this import is rescue card #1.)*
3. Click at the very end of the file (below the Coward Goblin), press Enter twice.
4. Paste exactly this jutsu, save (`Ctrl+S`):

```python
class Mimic(Slime):
    """A box that is more than it appears."""

    def __init__(self, x, y):
        super().__init__(x, y)          # Slime's chase, inherited
        self.name = "Suspicious Box"
        self.max_hp = 30                # the box is tougher than a slime
        self.hp = 30

    def symbol(self):
        if self.hp == self.max_hp:      # pristine: still just a box
            return "📦"
        return "👹"                      # disturbed: the truth comes out

    def act(self, view):
        if self.hp == self.max_hp:      # pristine: wait, innocently
            return WaitAction()
        return super().act(view)        # disturbed: Slime's chase & bite
```

**PREDICT (Scout writes the team's answers BEFORE running):**
The player strikes the box. On the **exact turn of that strike**, what happens?
______
*(Think: whose turn comes first — and what does `symbol()` return the moment
`hp` stops being 30?)*

**Read what you just cast:**
- The mimic overrides **two** methods, and both read the **same state**: pristine
  (`hp == max_hp`) means 📦 + `WaitAction()`; disturbed means 👹 + Slime's chase via
  `super().act(view)`.
- `self.max_hp = 30` matters: it makes the board's HP bar honest (24/30 after the first
  hit) — and it gives the check a *relative* anchor instead of a magic number.
- Nothing here tricks the engine: it still just calls `villain.act(view)` and reads
  `villain.symbol()`. **The objects decide.**

**If it differs:** red squiggles, or you re-typed instead of pasted — `Ctrl+Z` and paste
the block in ONE action. The scroll is exact.

---

## 🥷 PHASE 2 — The Chakra Check (2 mins)

**Objective:** let the code doctor discover the mimic.

**Steps:** run the chakra check from the repo root (prompt ends in `pygame-engine`;
if yours ends in `rogue_edu`, type `cd ..` first):

```bash
venv/Scripts/python.exe rogue_edu/check_my_class.py
```

**Expected result:**
```
Checking student_starter.classes ...

[PASS] Hero 'BraveKnight' inherits Hero -- the engine drives its turns from your keyboard.
[PASS] Villain 'Slime' inherits Villain and act() returned AttackAction(dx=1, dy=0).
[PASS] NPC 'Elder' inherits NPC and interact() returned a SpeakAction.
[PASS] Villain 'Shadow' inherits Villain and act() returned AttackAction(dx=1, dy=0).
[PASS] Villain 'CowardGoblin' inherits Villain and act() returned AttackAction(dx=1, dy=0).
[PASS] Villain 'Mimic' inherits Villain and act() returned WaitAction().

Summary: 6 passed, 0 warnings, 0 failures.
Beautiful. Run the game: python app.py
```

The mimic's own line is the fingerprint of its disguise: at full hp its `act()` answers
`WaitAction()` — the doctor interviewed the box and it played innocent.

**✅ Completion check (Scout):** copy the exact `[PASS] Villain 'Mimic' …` line:
_______________________________________________________________

**If it differs:**
- `[FAIL] Calling Mimic.act() crashed: NameError: name 'WaitAction' is not defined` →
  step 2 was skipped (rescue card #1).
- `[WARN] … returned None instead of an Action.` → a branch lost its `return`
  (rescue card #2).

---

## 🥷 PHASE 3 — Registration & Live Combat (5 mins)

**Objective:** place the box in the open and spring the trap.

**Steps (Operator):**
1. Open **`game_config.py`** (same `student_starter` folder).
2. Change the import line so it reads exactly:
   ```python
   from student_starter.classes import BraveKnight, CowardGoblin, Elder, Mimic, Shadow, Slime
   ```
3. Directly under `game.add_villain(CowardGoblin(x=8, y=4))` add:
   ```python
   game.add_villain(Mimic(x=8, y=6))
   ```
   *(Open ground, like the goblin's spot — a mimic in the rocks would log `BLOCKED`
   instead of stalking you.)*
4. Save. Wake the village again: `Ctrl+C` the old server, `cd rogue_edu` (skip if the
   prompt already ends in `rogue_edu`), then `../venv/Scripts/python.exe app.py`.
5. Browser → refresh **http://127.0.0.1:5000**.

**Expected result:** a 📦 sits on tile (8, 6), HP bar full. Walk east — the box
**does nothing**: `Suspicious Box waits.` in the log, over and over. The other three
monsters still hunt you (Slime, Shadow, Coward Goblin — unchanged). Bump into the box:

```
Sir Ada strikes Suspicious Box for 6 damage! (Suspicious Box: 24/30 hp left)
```
and on the **same turn** — the villain phase follows your strike — the trap springs.
The sprite flips 👺-style from 📦 to 👹, the board's HP bar suddenly reads honestly
(24/30), and the box starts moving and biting:
```
Suspicious Box hits Sir Ada for 3 damage! (Sir Ada: 22/25 hp left)
```
The verified arc to the kill: strikes of 6 walk it 24 → 18 → 12 → 6 → 0, it bites for 3
each time it is adjacent, and at 0: `Suspicious Box is defeated!` — later exactly once,
`Suspicious Box is defeated and cannot act.`

**✅ Completion check (Scout):** one sentence with evidence: *"The box ______ while
pristine, and the moment `hp` dropped below `max_hp` it ______ — the engine never
learned its name."*

**If it differs:** box never transforms even when struck → you wrote `self.hp = 30` but
compared against a hardcoded number, or set the spawn to something else (rescue card
#1). `NameError: name 'CowardGoblin'` or `'Mimic'` at boot → step 2 skipped (rescue
card #3). Board frozen → rescue card #1's cousin: a crashed turn.

---

## 🥷 PHASE 4 — The Polymorphism Interrogation (3 mins)

**Objective:** say precisely why the engine never needed to know.

**The question (Navigator reads, team answers before writing):**
Look at the game loop in `engine/core.py`. Does the engine use an `if/else` to check
whether a villain is a Slime, a Mimic, or a Coward Goblin before asking for its move?

_______________________________________________________________

**Answer check:** **No.** The loop's one move-request is
`action = villain.act(view)` — the same call on every entry of the mixed `villains`
list. The engine doesn't know or care that entry 4 is a Mimic; the **object** looked at
its own `hp` and answered. That is Polymorphism — treating different objects through the
same interface and letting them handle the specifics.
**"You decide. The engine acts."**

**Push one question further (Scout challenge):** the mimic's `symbol()` and `act()` both
read `self.hp`. If the engine can't see that variable changing, how does the sprite flip
on your screen? ______ *(Every render asks every villain for its CURRENT `symbol()` —
the answer changed because the state changed.)*

**✅ Completion check (Scout):** write your team's one-line answer to THE question:
_______________________________________________________________

---

## 🥷 PHASE 5 — Rank Sign-Off & Verification (1 min)

**Village gate** — the whole village's tests must still pass with your mimic alive.
In a terminal at the repo root:

```bash
venv/Scripts/python.exe -m pytest -q
```

**Expected last line:** `193 passed` (a few more is fine — `failed` is not).

## 🎖 Rank earned

| Step | Done | Evidence written |
|---|---|---|
| Phase 1 — import fixed + jutsu pasted + prediction | ☐ | ☐ |
| Phase 2 — `[PASS] Villain 'Mimic'` copied | ☐ | ☐ |
| Phase 3 — the trap sprung on screen | ☐ | ☐ |
| Phase 4 — interrogation answered | ☐ | ☐ |
| Phase 5 — village gate green | ☐ | ☐ |

Disguised, disturbed, defeated — and the loop never learned your name. **Rank C Shinobi
status: CONFIRMED — Genin Trapmaker.**

> *"You decide. The engine acts."* — the village's one law.

*(Teachers: the rescue card for this mission lives in the teacher pack. Unstick teams
with the 90-second rule; the chakra check is the first responder.)*

*Scroll forged in 2026 by Sir Roy from the PSHS curriculum. Village infrastructure and jutsus engineered alongside Hermes, Gemini, and ChatGPT.*
