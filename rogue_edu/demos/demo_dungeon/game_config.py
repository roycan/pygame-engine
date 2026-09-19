"""Demo Dungeon composition -- a complete worked example.

READ THIS to see how a full game is assembled: one hero, three villains
with different strategies, maze walls, an NPC advisor, and the
``clear_and_reach_goal`` win condition (defeat everyone, THEN reach the
stairs at (9, 9)).

Run it in the browser:

    GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py
"""

from engine.base_classes import Wall
from engine.core import GameEngine

from demos.demo_dungeon.entities import (
    AncientOne,
    Chaser,
    Coward,
    DemoChampion,
    Patroller,
)


def create_game() -> GameEngine:
    """Assemble the demo dungeon: clear all three guardians, then reach
    the stairs at (9, 9)."""
    game = GameEngine(
        width=10,
        height=10,
        win_condition="clear_and_reach_goal",
        goal_pos=(9, 9),
    )

    game.add_hero(DemoChampion(x=0, y=0))

    # Two interior walls split the room into corridors.
    for x, y in [
        (3, 1), (3, 2), (3, 3), (3, 4), (3, 6), (3, 7), (3, 8),
        (6, 1), (6, 2), (6, 3), (6, 5), (6, 6), (6, 7), (6, 8),
    ]:
        game.add_wall(Wall("Crate", x, y))

    # Registration order = turn order: Chaser, then Coward, then Sentinel.
    game.add_villain(Chaser(x=5, y=5))
    game.add_villain(Coward(x=8, y=1))
    game.add_villain(Patroller(x=8, y=6))

    game.add_npc(AncientOne(x=1, y=8))

    return game
