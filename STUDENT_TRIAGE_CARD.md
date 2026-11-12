# STUDENT TRIAGE CARD — Visual Arena (Track 3)

Keep this open while you build. **90 seconds stuck → raise your hand.** That's the
rule, not defeat. Predict before you run; one change at a time; evidence is your rank.

The track's rules — what you may touch, the two tiers, the honest limits — live in
[`TRACK3_VISUAL_SANDBOX.md`](TRACK3_VISUAL_SANDBOX.md:1).

---

## The recipe (once per pair)

1. **Copy the template** and name it after your pair — lowercase letters, digits and
   underscores only, because the folder name becomes your URL:

       cp -r rogue_edu/arenas/_template rogue_edu/arenas/team_<name>

2. **Edit ONLY your two files:**
   - `arenas/team_<name>/classes.py` — your Hero / Villain / NPC
   - `arenas/team_<name>/game_config.py` — `TITLE`, placement, win condition

   Everything else is off-limits: the engine, `app.py`, and other teams' folders.

3. **Point the import at YOUR folder** (this is Trap 1 — do it before anything else).

4. **Check yourself** before you ask anyone:

       cd rogue_edu
       python check_my_class.py arenas/team_<name>/game_config

   (Windows venv: `venv\Scripts\python check_my_class.py arenas/team_<name>/game_config`)

5. **Play it:** `python app.py` → open `/games` → click your card.

---

## The 4 traps

### Trap 1 — "My symbol / class didn't change!"
**Cause:** `game_config.py` still imports from `arenas._template.classes`. Your arena
runs the *template's* code while your own edits sit ignored — and everything looks
healthy.
**Fix:** change the import line to your folder:

    from arenas.team_<name>.classes import MyHero, MyNPC, MyVillain

The checker now prints a `[WARN]` when it sees this. Re-run step 4.

### Trap 2 — The browser shows "500 Internal Server Error" when I press a key
**Cause:** your `act()` (or `interact()`) raised a Python exception at runtime.
**Fix:** the browser will never explain it — your terminal will. Look at the terminal
running `python app.py` and read the traceback: **the last line is the crime, the
line above it is the scene (file + line number).** Fix what it names, restart, refresh.

### Trap 3 — The game freezes / the browser stops responding
**Cause:** a loop that never ends (a `while True:`) inside `act()`. Every turn, your
`act()` must finish and return an Action.
**Fix:** `Ctrl+C` in the terminal, fix the loop condition, restart `python app.py`.
(A loop in `create_game()` instead shows a yellow **"timed out"** card on `/games` —
that's the menu catching it for you.)

### Trap 4 — `AttributeError: 'MyThing' object has no attribute 'x'` when the game starts
**Cause:** your `__init__` never called `super().__init__(...)`, so the engine state
(name, x, y, hp) was never set up.
**Fix:** first line inside your constructor:

    def __init__(self, x, y):
        super().__init__("My Thing", x, y, hp=10, attack_power=3)   # Hero / Villain
        # NPC instead:  super().__init__("My Thing", x, y)

The checker now prints a `[FAIL]` for this **before** the game ever runs.

---

## What the canvas can and cannot show

The browser draws exactly these six fields per character: **`name`, `x`, `y`, `hp`,
`max_hp`, `symbol`** (your emoji comes from `symbol()`). Nothing else crosses to the
canvas — that key set is frozen, on purpose.

- **Change what players see:** `symbol()` (any emoji), `hp` / `attack_power` (within
  `hp` 1–200, `attack_power` 0–40), walls and placement, and your `TITLE`.
- **Custom state works, but stays invisible:** rage meters, cooldowns, spell slots
  and turn counters run perfectly in Python and drive your behavior — they just never
  reach the screen. Show them **in-world** instead: return a different `symbol()` at a
  threshold (`"😤"` once enraged), say it through an NPC's dialogue, or write it to
  the turn log.

**Remember the deal:** you sense → you decide → you *return* an intent. The engine
validates and acts. You decide; the engine acts.