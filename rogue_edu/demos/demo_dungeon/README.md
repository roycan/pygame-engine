# Demo Dungeon (read-only worked example)

This is a COMPLETE example game meant for reading, not submitting.
It shows three different villain strategies built from the same toolbox:

| Villain | Strategy | Key view calls |
| --- | --- | --- |
| Grim Chaser | relentless pursuit, attacks when adjacent | `get_hero_position()`, `distance_to_hero()`, `is_tile_passable()` |
| Sir Coward | chases above half hp, flees when wounded | `distance_to_hero()`, `get_direction_toward_hero()` |
| Stone Sentinel | walks a fixed route, strikes only nearby heroes | `distance_to_hero()` |

Win condition: `clear_and_reach_goal` -- defeat all three guardians,
then step on the stairs at (9, 9) (rendered 🔒 until the room is clear).

## Run it

```bash
GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py
```

Then open http://127.0.0.1:5000
