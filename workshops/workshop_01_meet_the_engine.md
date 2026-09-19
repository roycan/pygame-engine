# RogueEdu Workshop 1 — Meet the Engine

> **Name:** ______________________    **Section:** ____________    **Date:** ____________

**You will need:** the `rogue_edu_workshop` folder, VS Code, and 90 curious minutes.
**You will build:** your own video-game villain — with a personality *you* designed.

---

## 0) Setup on Windows (15 min)

Do these once, in order. Check each box as you go.

- [ ] 1. Get `rogue_edu_workshop.zip` from your teacher (Google Classroom or USB). Save it in **Documents**.
- [ ] 2. Right-click the ZIP → **Extract All** → **Extract**. You now have a `rogue_edu_workshop` folder.
- [ ] 3. If Python is not installed yet: go to **python.org/downloads**, run the installer, and — this is the step everyone misses — **tick the box that says "Add python.exe to PATH"** before clicking Install.
- [ ] 4. Open **VS Code** → **File → Open Folder…** → choose the `rogue_edu_workshop` folder. (Optional but nice: install the *Python* extension when VS Code offers it.)
- [ ] 5. Open a terminal in VS Code (**Ctrl+`**) and run these two commands, one at a time:

       python -m venv venv
       venv\Scripts\pip install -r requirements.txt

- [ ] 6. Check that your code is healthy:

       venv\Scripts\python rogue_edu\check_my_class.py

  You should see three `[PASS]` lines. If you see `[FAIL]`, raise your hand — do not fix it yet.
- [ ] 7. Start the game:

       venv\Scripts\python rogue_edu\app.py

  Then open a browser to **http://127.0.0.1:5000**. You should see a 10x10 board with a hero, walls, an NPC, and a slime.
- [ ] 8. Remember this loop — you will repeat it all workshop: **edit code → `Ctrl+C` the server → re-run step 7 → refresh the browser.**

**Troubleshooting**

| Problem | Fix |
| --- | --- |
| `'python' is not recognized…` | Python was installed without the PATH box. Reinstall (step 3) and tick it. |
| Emoji prints as garbage or crashes | Run `set PYTHONUTF8=1` in the same terminal, then try again. |
| Port already in use | Another `app.py` is still running — find it and `Ctrl+C` it. |

> 🎬 **While everyone finishes setup:** your teacher will play the *Demo Dungeon* on the projector. Watch how the three monsters behave differently. One of them is doing something sneaky — see if you can spot it.

---

## 1) The Hook — Play First (5 min)

Play the starter game for three minutes. Move with **W A S D**, wait with **Space**, bump into the Elder to hear them out, and try to defeat the Slime.

While you play, jot down:

1. One thing the game **stopped you** from doing: ______________________________
2. One thing a monster did that seemed **smart**: ______________________________
3. One thing you wish the game **had**: ______________________________

---

## 2) What Is This Engine? (5 min)

RogueEdu is a tiny video-game engine built for one purpose: **teaching you Object-Oriented Programming by letting you write the monsters.**

Here is the deal it offers you:

- **You write** the characters — their names, stats, looks, and *behavior* — in plain Python classes.
- **The engine does** everything else: the grid, the turns, the collisions, the combat math, the browser graphics, the rules.

Think of the engine as the **referee of a board game**. You never move your own piece — you *say* what you want to do, the referee checks the rules, and moves it for you. You cannot cheat, and neither can anyone else.

### Key features

1. **Intent-based actions** — your code never moves anything; it *returns a request*.
2. **A read-only world (`SafeGameView`)** — your monsters can *look* at the board, but never *touch* it.
3. **Loud guardrails** — impossible stats don't crash the game; they get clamped and **announced** in a log.
4. **A code doctor (`check_my_class.py`)** — instant, friendly feedback with zero scary tracebacks.
5. **Instant playability** — save your code, restart the server, refresh the browser. Your monster is alive.

### Five analogies you'll actually remember

| Concept | Analogy |
| --- | --- |
| Returning an `Action` | An **order slip at a restaurant**: you don't barge into the kitchen and cook — you hand over a slip that says `MoveAction(1, 0)` and the kitchen (engine) decides what actually happens. |
| `SafeGameView` | A **window with a view**: your character can look out at the whole board, but the glass doesn't open. Looking is free; touching is impossible. |
| `class Slime(Villain)` | A **family recipe**: your Slime starts with everything every Villain can do, inherited from the cookbook. `act()` is the family twist you add. |
| Stat clamping | The **amusement-park height stick**: you cannot ride at 250 hp. And the operator *announces it loudly* — no quietly shrinking anyone. |
| The turn loop | **Chess, not tag**: everyone wants to move at once; the referee resolves wishes one at a time, in a fixed order. |

---

## 3) Part 1: ME — Watch Me Reskin a Villain (10 min)

Your teacher will now, live and unscripted:

1. Open `rogue_edu/student_starter/classes.py`.
2. Rename the `Slime`, change its emoji, and push its stats around (watch what happens when a stat goes too far!).
3. Run the code doctor: `venv\Scripts\python rogue_edu\check_my_class.py`.
4. Restart the server and refresh the browser to meet the new monster.

**Your job while watching** — write two things you noticed:

- I noticed: ______________________________
- I noticed: ______________________________

---

## 4) Part 2: US — Code Along (20 min)

Everyone edits `rogue_edu/student_starter/classes.py` together. Fill in the blanks with **your** villain's identity:

```python
class Slime(Villain):
    def __init__(self, x: int, y: int):
        super().__init__("____________", x, y, hp=____, attack_power=____)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)   # adjacent: bite!
        return MoveAction(dx, dy)         # otherwise: creep closer.

    def symbol(self):
        return "______"
```

Bounds: `hp` lives in **1–200**, `attack_power` in **0–40**. Try `hp=999` once — read the warning — then put it back.

Now run the loop: **doctor → restart → refresh.**

### 🌱 Reflect (3 min)

1. What did the checker say about your stats? ______________________________
2. What did **you** change, and what did the **engine** do? ______________________________
3. Why do you think your code *returns* `MoveAction` instead of moving the slime itself? ______________________________

---

## 5) Part 3: YOU — Your Villain, Your Rules (20 min)

Work **solo**. Rules of the road: the doctor must pass with zero `[FAIL]`, and you must playtest against your own creation. Climb as high as you can.

### 🌱 Tier 1 — Make it yours (everybody finishes this)

Rename your Slime, give it new stats and a new emoji. **Done when:** the doctor says three `[PASS]`, your monster appears in the browser with your emoji, and it still chases you.

### 🌿 Tier 2 — Give it a personality (the fun part)

Pick ONE: a **coward** that turns tail below half health, or a **patrol** guard that walks a route and only bites up close. The mood branch looks like this (mind the comparison!):

```python
if self.hp * 2 >= self.max_hp:
    # brave: chase / bite, like before
    ...
# wounded: flee!
return MoveAction(-dx, -dy)
```

**Done when:** you can *demonstrate both moods* — hurt your monster once (let it bite you at full HP, then fight back) and watch it change behavior.

### 🌳 Tier 3 — Compose a mini arena (for the fast ones)

Open `rogue_edu/student_starter/game_config.py` and build a scene around your creations: a hero, **two** of your villains, a couple of walls. That file is *composition only* — placement happens there, never inside your classes.

### 🌿 Reflect again (3 min)

1. What was harder than you expected, and what does that tell you about the difference between *reading* code and *writing* it? ______________________________
2. What did the doctor (or the engine's warnings) catch for you today? ______________________________
3. If you had one more hour tonight, what would your villain do next? ______________________________

---

## 6) The Quarter — What Your Pair Could Build (5 min)

Everything you did today — one class, one behavior — is the atom your quarter project is made of. With your project pair over the coming weeks:

- **Weeks 1–3:** a **cast** of villains with real personalities (brave, sneaky, territorial, greedy…) — and an NPC or two worth talking to.
- **Weeks 4–6:** a **place** — walls, mazes, rooms, a goal to reach… or a lock that only opens when the room is clear.
- **Weeks 7–8:** **rules of winning** — total conquest, escape runs, or clear-the-room-then-take-the-stairs. You choose; the engine already supports it.
- **Showcase night:** pairs demo their dungeons. Players die. Legends are made.

The engine you met today is the same engine the demo dungeon runs on — and that was built from exactly the pieces you now know how to use.

---

## 7) Teacher Answer Key

*(Students: the fun is in the struggle. Peek only to unstick yourself, then close it.)*

**Tier 🌱 — the reskinned chase:**

```python
class ReskinnedSlime(Villain):
    def __init__(self, x, y):
        super().__init__("Magma Blob", x, y, hp=14, attack_power=4)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)
        return MoveAction(dx, dy)

    def symbol(self):
        return "🔥"
```

**Tier 🌿 — the coward:**

```python
class CowardSlime(Villain):
    def __init__(self, x, y):
        super().__init__("Sir Wobbles", x, y, hp=12, attack_power=5)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if self.hp * 2 >= self.max_hp:
            if view.distance_to_hero(self) == 1:
                return AttackAction(dx, dy)
            return MoveAction(dx, dy)
        if (dx or dy) and view.is_tile_passable(self.x - dx, self.y - dy):
            return MoveAction(-dx, -dy)
        return WaitAction()

    def symbol(self):
        return "🐭"
```

**Tier 🌿 alternate — the patroller:**

```python
class PatrolSlime(Villain):
    def __init__(self, x, y):
        super().__init__("Roundabout", x, y, hp=14, attack_power=4)
        self._route = [(1, 0), (0, 1), (-1, 0), (0, -1)] * 2
        self._step = 0

    def act(self, view):
        if view.distance_to_hero(self) == 1:
            dx, dy = view.get_direction_toward_hero(self)
            return AttackAction(dx, dy)
        dx, dy = self._route[self._step % len(self._route)]
        self._step += 1
        if view.is_tile_passable(self.x + dx, self.y + dy):
            return MoveAction(dx, dy)
        return WaitAction()

    def symbol(self):
        return "🌀"
```

**Tier 🌳 — the mini arena (in `game_config.py`):**

```python
def create_arena_game() -> GameEngine:
    game = GameEngine(width=10, height=10, win_condition="defeat_all")
    game.add_hero(ArenaChamp(x=1, y=1))
    game.add_villain(ReskinnedSlime(x=8, y=1))
    game.add_villain(CowardSlime(x=8, y=8))
    game.add_wall(Wall("Rock", 4, 4))
    game.add_wall(Wall("Rock", 5, 4))
    return game
```

*(The full tested versions of every answer live in `tests/fixtures/worksheet_answers.py` — the automated test suite plays against them.)*

---

## Appendix — facilitator timings (for the teacher)

| Segment | Minutes | Watch for |
| --- | --- | --- |
| 0) Setup | 15 | The PATH checkbox; Extract All creating a nested folder; venv typos. |
| 1) Hook | 5 | Seat struggling installers next to finished ones. |
| 2) What/Analogies | 5 | Keep it brisk — the code will teach the rest. |
| 3) ME | 10 | Deliberately set `hp=999` and read the clamp warning aloud. |
| 4) US | 20 | The doctor's `[PASS]` is the checkpoint before anyone restarts the server. |
| 🌱 Reflect | 3 | Collect one insight aloud. |
| 5) YOU | 20 | Announce tier expectations: 🌱 is a complete success. |
| 🌿 Reflect 2 | 3 | Harvest struggles — they are next lesson's opening. |
| 6) Quarter tease | 5 | End on the showcase. |
