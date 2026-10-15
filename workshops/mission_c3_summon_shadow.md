# 🌀 RogueEdu — MISSION C-3: Summon a Shadow (Genin Edition · Git Bash)

**Name:** ______________ **Team:** ______ **Rank earned:** ______

**Prerequisite:** Missions D-1 → C-2 complete. The board runs, your C-2 experiment is
reverted, and the chakra check says `Summary: 3 passed, 0 warnings, 0 failures.`

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

**Today (10–12 min):** you summon a brand-new monster — a **Shadow** — by writing one
subclass of `Villain`. Then you prove the engine already knows how to move it, collide
it, and let it fight. You write the *what*; the engine does the *how*.

---

## 🥷 PHASE 1 — The Inheritance Jutsu Blueprint (3 min)

**Objective:** define `class Shadow(Villain):` with new stats — and zero movement code.

**Steps (Operator types, Navigator reads):**
1. In VS Code open `rogue_edu` → `student_starter` → **`classes.py`**.
2. Click at the very end of the file (below the `Elder` class), press Enter twice.
3. Paste exactly this jutsu, save (`Ctrl+S`):

```python
class Shadow(Villain):
    """A genin's first summon: new stats, borrowed behavior."""

    def __init__(self, x: int, y: int):
        super().__init__("Shadow", x, y, hp=15, attack_power=4)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)   # adjacent: strike from the dark!
        return MoveAction(dx, dy)         # otherwise: drift closer.

    def symbol(self) -> str:
        return "👥"
```

**PREDICT (Scout writes the team's answers BEFORE running):**
Find the movement loop in `act()` — the `while`, the `self.x = self.x + 1`. Where is it?
______ So who will actually move the Shadow one tile at a time? ______

**Read what you just cast:**
- `class Shadow(Villain):` — Shadow is *born* a Villain: it inherits a slot in the turn
  order, a body that blocks tiles, hp that can be reduced, a tile on the board.
- `act()` is not a movement loop — it is a **3-line wish**: look (the read-only `view`)
  → decide → RETURN an Action. Being a `Villain` is what gives Shadow the *right to
  take a turn at all*; skipping `act()` means no summon (a Villain without `act()`
  cannot even be built).
- `symbol` is a **method** (`def symbol(self)` returning `"👥"`). Writing
  `self.symbol = "👥"` pastes a sticker over the skill — the checker may smile, but
  Phase 3 will not survive it.

**If it differs:** red squiggles, or you re-typed instead of pasted — `Ctrl+Z` and paste
the block in ONE action. The scroll is exact.

---

## 🥷 PHASE 2 — The Chakra Check & Auto-Discovery (2 min)

**Objective:** let the code doctor discover a class it has never seen.

**Steps:** run the chakra check from the repo root (prompt ends in `pygame-engine`;
if yours ends in `rogue_edu`, type `cd ..` first):

```bash
venv/Scripts/python.exe rogue_edu/check_my_class.py
```

You never told the checker Shadow exists. It reads the whole file, finds every
Hero/Villain/NPC subclass defined in it, builds each one, and calls its methods
against a mock view.

**Expected result:**
```
Checking student_starter.classes ...

[PASS] Hero 'BraveKnight' inherits Hero -- the engine drives its turns from your keyboard.
[PASS] Villain 'Slime' inherits Villain and act() returned AttackAction(dx=1, dy=0).
[PASS] NPC 'Elder' inherits NPC and interact() returned a SpeakAction.
[PASS] Villain 'Shadow' inherits Villain and act() returned AttackAction(dx=1, dy=0).

Summary: 4 passed, 0 warnings, 0 failures.
Beautiful. Run the game: python app.py
```

**✅ Completion check (Scout):** copy the exact `[PASS] Villain 'Shadow' …` line:
_______________________________________________________________

**If it differs:**
- `[FAIL] … 'Shadow' is missing the act() method.` → your paste lost `act()`; re-paste Phase 1.
- `syntax error near line N.` → go to line N: usually a missing `:` or a bad indent.

---

## 🥷 PHASE 3 — Registration & Encapsulation in the Village (3 min)

**Objective:** place the Shadow in the world — in the *composition* file, not the class.

`classes.py` says WHAT a Shadow is. `game_config.py` says WHERE it stands. One class,
many placements — that split only works because the Shadow carries its own state and
behavior as one self-contained bundle (encapsulation, job #1).

**Steps (Operator):**
1. Open **`game_config.py`** (same `student_starter` folder).
2. Change the import line so it reads exactly:
   ```python
   from student_starter.classes import BraveKnight, Elder, Shadow, Slime
   ```
3. Directly under `game.add_villain(Slime(x=7, y=7))` add:
   ```python
   game.add_villain(Shadow(x=2, y=6))
   ```
4. Save. Wake the village again: `Ctrl+C` the old server, `cd rogue_edu` (skip if the
   prompt already ends in `rogue_edu`), then `../venv/Scripts/python.exe app.py`.
5. Browser → refresh **http://127.0.0.1:5000**.

**Expected result:** the board shows 👥 on tile (2, 6) with its own HP bar. Registration
order is turn order: Slime moves, then Shadow. Walk toward it — the log narrates the
fight in BOTH directions:
```
Sir Ada strikes Shadow for 6 damage! (Shadow: 9/15 hp left)
Shadow hits Sir Ada for 4 damage! (Sir Ada: 21/25 hp left)
```
Near the start you may also see:
```
BLOCKED: Shadow bumped into something at (2, 5) and stayed at (2, 6).
```
Nobody wrote that collision — not in your file, not today. The Pillar at (2, 5) is
*engine* knowledge. Your 3-line `act()` made a wish; the referee resolved it.
Defeat the Shadow fully and watch the log: `Shadow is defeated!` — and later, exactly
once, `Shadow is defeated and cannot act.` The body is retired, not deleted.

**✅ Completion check (Scout):** one sentence with evidence: *"The Shadow chased /
got blocked because ____________, and we never wrote ____________ code."*

**If it differs:** `NameError: name 'Shadow' is not defined` in the terminal → step 2
was skipped (rescue card #3). Board frozen / spinner forever → rescue card #2.

---

## 🥷 PHASE 4 — The Boundary Defense Experiment (3 min)

**Objective:** see the encapsulation fence from the inside.

**The question (Navigator reads, team answers before touching anything):**
*Why didn't we write a single line telling the game loop how much damage the Shadow
takes when it is hit?*

Look at evidence you already captured:
- `Shadow: 9/15 hp left` — fifteen is Shadow's own number.
- From C-1: `Slime: … /10 hp left` — ten belongs to Slime.
- The HUD: `HP 25/25` — twenty-five is Sir Ada's.

Three creatures, three private `hp` bundles, one shared rulebook. Each object
**encapsulates** its own vitals. The engine — the mediator — reads the attacker's own
`attack_power` and calls the victim's own damage handling. Entities never reach into
*each other's* guts: villains can't see the hero except through the read-only `view`,
and every wish travels as a frozen intent (`MoveAction`, `AttackAction`) that nobody
edits after it is returned. *You decide. The engine acts.*

**Evidence grab 1 — the Inspector:** strike the Shadow once, then tick the
**Developer Inspector** checkbox (bottom of the Turn Log). The JSON of that turn
repeats the sentence with the numbers — `"…strikes Shadow for 6 damage! (Shadow: 9/15
hp left)"…`. Three different hp totals, one board: three encapsulated states.

**Evidence grab 2 — the frozen contract (60 s):** open a **second terminal** (the ＋ in
the terminal panel), then:

```bash
cd rogue_edu
../venv/Scripts/python.exe -c 'from engine.actions import AttackAction; AttackAction(1, 0, damage=999)'
```

**PREDICT first:** if attacks carried their own damage number, what would this build?
______
**Expected:**
```
TypeError: AttackAction.__init__() got an unexpected keyword argument 'damage'
```
An attack is a *direction* ("strike that tile"), never an amount. Damage is a property
of the attacker, read and clamped by the engine — nobody slips 999 into the envelope
and calls it a poke.

**✅ Completion check (Scout):** write your team's one-line answer to THE question:
_______________________________________________________________

---

## 🥷 PHASE 5 — Rank Sign-Off & Verification (1 min)

**Village gate** — the whole village's tests must still pass with your Shadow alive.
In the second terminal: `cd ..` (back to the repo root), then:

```bash
venv/Scripts/python.exe -m pytest -q
```

**Expected last line:** `193 passed` (a few more is fine — `failed` is not).

## 🎖 Rank earned

| Step | Done | Evidence written |
|---|---|---|
| Phase 1 — jutsu pasted + prediction | ☐ | ☐ |
| Phase 2 — `[PASS] Villain 'Shadow'` copied | ☐ | ☐ |
| Phase 3 — Shadow fights on the board | ☐ | ☐ |
| Phase 4 — boundary answer + TypeError | ☐ | ☐ |
| Phase 5 — village gate green | ☐ | ☐ |

Summoned, registered, fought, boundary mapped. **Rank C Shinobi status: CONFIRMED —
Genin Summoner.**

> *"You decide. The engine acts."* — the village's one law.

*(Teachers: the rescue card for this mission lives in the teacher pack. Unstick teams
with the 90-second rule; the chakra check is the first responder.)*
