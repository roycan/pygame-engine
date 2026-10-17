# 🌀 RogueEdu — MISSION C-4: Tactical Retreat (Genin Edition · Git Bash)

**Name:** ______________ **Team:** ______ **Rank earned:** ______

**Prerequisite:** Missions D-1 → C-3 complete. Your Shadow still hunts from tile (2, 6),
and the chakra check says `Summary: 4 passed, 0 warnings, 0 failures.`

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

**Today (15 min):** you summon a **Coward Goblin** — a Slime that inherited everything and
*overrode one method* so it flees when wounded. One `if`, one `super()` — and the same
engine that chased you all quarter now runs away from you.

---

## 🥷 PHASE 1 — The Blueprint (4 mins)

**Objective:** subclass `Slime` and override `act(view)` — replace half, inherit half.

**Steps (Operator types, Navigator reads):**
1. In VS Code open `rogue_edu` → `student_starter` → **`classes.py`**.
2. Click at the very end of the file (below your `Shadow` class), press Enter twice.
3. Paste exactly this jutsu, save (`Ctrl+S`):

```python
class CowardGoblin(Slime):
    """A Slime that runs when the fight turns bad."""

    def __init__(self, x, y):
        super().__init__(x, y)          # Slime's stats, inherited
        self.name = "Coward Goblin"     # a name of its own

    def act(self, view):
        if self.hp * 2 < self.max_hp:   # wounded: flee!
            dx, dy = view.get_direction_toward_hero(self)
            return MoveAction(-dx, -dy)
        return super().act(view)        # brave: Slime's chase & bite

    def symbol(self) -> str:
        return "👺"
```

**PREDICT (Scout writes the team's answers BEFORE running):**
1. The goblin takes **15 damage** in one hit. What does it do on its next turn? ______
   *(Hint: how many hp does a Slime have to lose?)*
2. After exactly **one** strike from Sir Ada (6 damage), what will the goblin do —
   chase or flee? ______

**Read what you just cast:**
- `class CowardGoblin(Slime):` — the parent is **Slime**, not Villain: a *concrete*
  parent with a working `act()` you can delegate to.
- `act(self, view)` — the engine's turn hook. (It is **not** `get_action`: a repo-wide
  search finds no `get_action` anywhere — `base_classes.py` is the authority.)
- The `if` reads: *wounded* means `hp * 2 < max_hp` — strictly below **half**.
  Wounded → `MoveAction(-dx, -dy)`: the **opposite** of the view's chase direction.
  Healthy → `return super().act(view)`: Slime's own chase-and-bite, borrowed whole.
- `symbol` stays a **method** (`def symbol(self)` returning `"👺"`). Writing
  `self.symbol = "👺"` pastes a sticker over the skill — the checker may smile, but the
  board will not survive it.

**If it differs:** red squiggles, or you re-typed instead of pasted — `Ctrl+Z` and paste
the block in ONE action. The scroll is exact.

---

## 🥷 PHASE 2 — The Chakra Check (2 mins)

**Objective:** let the code doctor discover the override.

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

Summary: 5 passed, 0 warnings, 0 failures.
Beautiful. Run the game: python app.py
```

**Be honest about what the doctor just proved:** the goblin was built at **full hp**, so
the checker exercised the `super()` branch (it "bit" the mock hero). The *fleeing*
branch only runs when wounded — the doctor cannot see it. **The live fight is the flee
branch's proof**, next phase.

**✅ Completion check (Scout):** copy the exact `[PASS] Villain 'CowardGoblin' …` line:
_______________________________________________________________

**If it differs:**
- `[FAIL] … is missing the act() method.` → your paste lost `act()`; re-paste Phase 1.
- `[FAIL] Calling CowardGoblin.act() crashed: RecursionError…` → you wrote
  `self.act(view)` where `super().act(view)` belongs (rescue card #1).
- `[WARN] … returned None instead of an Action.` → a branch lost its `return`
  (rescue card #2).

---

## 🥷 PHASE 3 — Registration & Live Combat (5 mins)

**Objective:** register the goblin in the open field and watch the override fire.

**Steps (Operator):**
1. Open **`game_config.py`** (same `student_starter` folder).
2. Change the import line so it reads exactly:
   ```python
   from student_starter.classes import BraveKnight, CowardGoblin, Elder, Shadow, Slime
   ```
3. Directly under `game.add_villain(Shadow(x=2, y=6))` add:
   ```python
   game.add_villain(CowardGoblin(x=8, y=4))
   ```
   *(Open ground on purpose: a goblin backed into the rocks can only log `BLOCKED` —
   cornered shinobi make poor evidence.)*
4. Save. Wake the village again: `Ctrl+C` the old server, `cd rogue_edu` (skip if the
   prompt already ends in `rogue_edu`), then `../venv/Scripts/python.exe app.py`.
5. Browser → refresh **http://127.0.0.1:5000**.

**Expected result:** the 👺 stands in the open east field. Turn order: Slime, Shadow,
Coward Goblin. Walk east and fight it. The verified arc:
```
Coward Goblin hits Sir Ada for 3 damage! (Sir Ada: 22/25 hp left)
Sir Ada strikes Coward Goblin for 6 damage! (Coward Goblin: 4/10 hp left)
Coward Goblin moves to (6, 5).
Coward Goblin moves to (6, 6).
Coward Goblin moves to (6, 7).
```
**Read the flip:** before your strike it advanced (and bit). After — wounded below
half — it turned and **ran**. Those are two different `act()` outcomes from one engine
call site; only the `if` changed. Corner it against a wall or the board edge and the log
says `BLOCKED … stayed put` — the wish was still the *engine's* to refuse.
Finish it: `Coward Goblin is defeated!` — and later, exactly once,
`Coward Goblin is defeated and cannot act.` The body is retired, not deleted.

**✅ Completion check (Scout):** one sentence with evidence: *"After taking ____ damage
the goblin ____________ because ____________, and we never wrote the chase code."*

**If it differs:** `NameError: name 'CowardGoblin' is not defined` in the terminal →
step 2 was skipped (rescue card #3). Goblin fights to the death and never flees → a
branch lost its `return` (rescue card #2). Board frozen → rescue card #1.

---

## 🥷 PHASE 4 — The `super()` Interrogation (3 mins)

**Objective:** say exactly where the chase code came from.

**The question (Navigator reads, team answers before writing):**
*Why didn't we have to write the code to chase the player?*

_______________________________________________________________

**Answer check:** because when `hp` is healthy, `act()` returns
`super().act(view)` — the decision is **routed back to `Slime`**, whose three-line
chase-and-bite the goblin inherited whole. Overriding here was **extension, not
replacement**: new behavior when wounded, inherited behavior when brave — and one thing
you never wrote: the chase.

**Push one question further (Scout challenge):** what would this goblin do if you
renamed the override to `get_action(self, view)`? ______ *(Nothing — `Slime` is a
concrete parent, so a wrongly-named method just inherits silently and nothing
complains. The name is the contract.)*

**✅ Completion check (Scout):** write your team's one-line answer to THE question:
_______________________________________________________________

---

## 🥷 PHASE 5 — Rank Sign-Off & Verification (1 min)

**Village gate** — the whole village's tests must still pass with your goblin alive.
In a terminal at the repo root:

```bash
venv/Scripts/python.exe -m pytest -q
```

**Expected last line:** `193 passed` (a few more is fine — `failed` is not).

## 🎖 Rank earned

| Step | Done | Evidence written |
|---|---|---|
| Phase 1 — jutsu pasted + two predictions | ☐ | ☐ |
| Phase 2 — `[PASS] Villain 'CowardGoblin'` copied | ☐ | ☐ |
| Phase 3 — the retreat witnessed in the log | ☐ | ☐ |
| Phase 4 — `super()` interrogation answered | ☐ | ☐ |
| Phase 5 — village gate green | ☐ | ☐ |

Summoned, wounded, routed — and the chase was never yours to write. **Rank C Shinobi
status: CONFIRMED — Genin Tactician.**

> *"You decide. The engine acts."* — the village's one law.

*(Teachers: the rescue card for this mission lives in the teacher pack. Unstick teams
with the 90-second rule; the chakra check is the first responder.)*

*Scroll forged in 2026 by Sir Roy from the PSHS curriculum. Village infrastructure and jutsus engineered alongside Hermes, Gemini, and ChatGPT.*
