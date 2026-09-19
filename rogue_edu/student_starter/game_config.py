"""STUDENT FILE #2 -- Assemble your game here.

This file is COMPOSITION ONLY: it instantiates your classes from
classes.py, assigns starting coordinates, and registers everything with
the engine in a deliberate order. No game logic lives here.

Remember the rule: subclasses define STATS and BEHAVIOR (classes.py);
this file decides WHERE everything starts and WHAT the win condition is.
"""

from engine.base_classes import Wall
from engine.core import GameEngine

from student_starter.classes import BraveKnight, Elder, Slime


def create_game() -> GameEngine:
    """Build and return the ready-to-play 10x10 starter game.

    Want a different objective? Swap the GameEngine(...) line for one of:

        # A) Arena / dungeon crawl: defeat every villain. (current)
        game = GameEngine(width=10, height=10, win_condition="defeat_all")

        # B) Escape room: ignore the monsters, reach the trophy tile.
        game = GameEngine(width=10, height=10,
                          win_condition="reach_goal", goal_pos=(9, 9))

        # C) Classic RPG: clear the room, THEN take the stairs.
        game = GameEngine(width=10, height=10,
                          win_condition="clear_and_reach_goal", goal_pos=(9, 9))
    """
    game = GameEngine(width=10, height=10, win_condition="defeat_all")

    # -- Your hero -------------------------------------------------------
    game.add_hero(BraveKnight(x=1, y=1))

    # -- Scenery: (name, x, y); walls block movement and attacks ---------
    for name, x, y in [
        ("Rock", 4, 4),
        ("Rock", 4, 5),
        ("Rock", 5, 4),
        ("Pillar", 6, 2),
        ("Pillar", 2, 5),
    ]:
        game.add_wall(Wall(name, x, y))

    # -- Enemies (registration order = the order they take turns) --------
    game.add_villain(Slime(x=7, y=7))

    # -- Friendlies -------------------------------------------------------
    game.add_npc(Elder(x=2, y=8))

    return game
