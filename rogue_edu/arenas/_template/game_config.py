"""YOUR GAME'S BLUEPRINT -- compose your arena here.

Composition only: this file decides WHERE everything starts and WHAT the
win condition is. All behavior lives in classes.py.

TITLE is the name shown on your /games menu card -- make it yours.
"""

from engine.base_classes import Wall
from engine.core import GameEngine

from arenas._template.classes import MyHero, MyNPC, MyVillain

TITLE = "My Pair's Arena"


def create_game() -> GameEngine:
    """Build and return the ready-to-play game.

    Win condition options (swap one line):

        GameEngine(width=10, height=10, win_condition="defeat_all")
        GameEngine(width=10, height=10, win_condition="reach_goal", goal_pos=(9, 9))
        GameEngine(width=10, height=10, win_condition="clear_and_reach_goal", goal_pos=(9, 9))
    """
    game = GameEngine(width=10, height=10, win_condition="defeat_all")

    # -- Your hero -------------------------------------------------------
    game.add_hero(MyHero(x=1, y=1))

    # -- Scenery: walls block movement AND attacks -----------------------
    for name, x, y in [
        ("Rock", 4, 4),
        ("Rock", 4, 5),
        ("Rock", 5, 4),
    ]:
        game.add_wall(Wall(name, x, y))

    # -- Enemies (registration order = the order they take turns) --------
    game.add_villain(MyVillain(x=7, y=7))

    # -- Friendlies -------------------------------------------------------
    game.add_npc(MyNPC(x=2, y=8))

    return game
