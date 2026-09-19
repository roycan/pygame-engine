# RogueEdu

An educational 2D turn-based grid game engine that teaches **Object-Oriented Programming** to Grade 9 students. Students write `Hero`, `Villain` and `NPC` subclasses, assemble a game in a config file, and play it in the browser (Flask + HTML5 Canvas + Bulma).

Full specification: [`plans/prompt_v2.md`](plans/prompt_v2.md) · Execution plan: [`plans/implementation_plan.md`](plans/implementation_plan.md)

**Teaching with it?** The Grade 9 workshop worksheet lives at [`workshops/workshop_01_meet_the_engine.md`](workshops/workshop_01_meet_the_engine.md), and `make zip` builds the student distribution (`dist/rogue_edu_workshop.zip`).

## Quick start

```bash
# 1) one-time setup
python3 -m venv venv
venv/bin/pip install -r requirements.txt
npm install --save-dev jsdom        # dev-only, used by the canvas tests

# 2) run the automated gate (114 pytest + 11 node tests)
make test

# 3) check your student classes, then play
cd rogue_edu
../venv/bin/python check_my_class.py     # or: python check_my_class.py
python app.py                            # open http://127.0.0.1:5000
```

Play the finished worked-example dungeon instead:

```bash
GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py
```

## How students use it

1. **Read** `rogue_edu/demos/demo_dungeon/` — a complete worked example (three different villain AIs).
2. **Edit** `rogue_edu/student_starter/classes.py` — your `Hero`/`Villain`/`NPC` subclasses. Rules: accept `(x, y)` in `__init__`, return `Action` objects from `act()`/`interact()`, never mutate the world yourself.
3. **Check** `python check_my_class.py` — friendly `[PASS]/[WARN]/[FAIL]` diagnostics, no tracebacks.
4. **Assemble** `rogue_edu/student_starter/game_config.py` — place everything, choose a win condition (`defeat_all`, `reach_goal`, `clear_and_reach_goal`).
5. **Play** `python app.py` — WASD moves / bump-attacks / bump-talks, Space waits.

## Controls

| Key | Effect |
| --- | --- |
| `W A S D` | move; into a villain = attack; into an NPC = dialogue (villains freeze that turn) |
| `Space` | wait (pass the turn) |
| any key | dismisses open dialogue for free (no turn passes) |

## Manual visual checklist (formal Phase 6 exit gate)

Automated tests cover renderer *logic* via a stub canvas; pixels need eyes. Open the game and verify:

1. [ ] The 10x10 grid draws with visible cell lines and no console errors.
2. [ ] The hero renders on a blue-bordered tile at the configured start tile, with a green hp bar.
3. [ ] Every wall renders as 🧱 on a grey tile; NPCs and villains show colored borders matching their type.
4. [ ] Moving with each of W/A/S/D moves the hero exactly one tile in the right direction.
5. [ ] Walking into a wall shows the BLOCKED entry in the log and the hero stays put.
6. [ ] Bumping the NPC opens the yellow dialogue box over the board (speaker name + "press any key to close"), villains visibly freeze, and any key dismisses it without the turn counter advancing.
7. [ ] Clicking a clickable log row draws a dashed red outline around the referenced tile and highlights the row.
8. [ ] Toggling **Developer Inspector** shows raw event JSON; the goal tile shows 🏆 (or 🔒 in `clear_and_reach_goal` while villains live); victory/defeat locks the keyboard.

## Project layout

```text
rogue_edu/
├── engine/            # the simulation core (students never edit)
│   ├── actions.py     #   frozen intent dataclasses (no damage field on attacks!)
│   ├── base_classes.py#   GameObject / Character / Hero / Villain / NPC / Wall
│   ├── view.py        #   SafeGameView: read-only snapshot + difflib typo catcher
│   └── core.py        #   GameEngine: turn loop, loud validation, turn JSON
├── student_starter/   # classes.py (edit me) + game_config.py (compose me)
├── demos/demo_dungeon/# read-only worked example
├── check_my_class.py  # student diagnostic
├── app.py             # Flask server (sessions, /api/step, /api/reset)
├── templates/         # Bulma UI: canvas, API reference card, dual-view log
└── static/game.js     # renderer + input + log-to-tile highlighting
tests/                 # 114 pytest tests + 11 node tests = the make test gate
```

## Engine invariants worth knowing

- Stats clamp **loudly**: out-of-range `hp`/`attack_power` is clamped AND logged as a warning event.
- `AttackAction(dx, dy)` carries a direction, never damage; the engine sanitizes damage (negative → 0, > 40 → 40) so overrides can't cheat.
- Dead villains are retained forever (`is_alive() == False`), hidden from the board — this keeps `clear_and_reach_goal` winnable.
- Win checks run immediately after every hero action; the hero's death aborts the remaining villain turns.
