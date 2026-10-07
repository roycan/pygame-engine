"""Sample Pair's arena -- the shipped worked example.

TITLE is what the /games menu card shows. create_game() assembles the
whole 8x8 garden: hedge walls, two slime twins (one bites, one flees),
and Auntie Bev with free advice.
"""

from engine.base_classes import Wall
from engine.core import GameEngine

from arenas.sample_pair.classes import Auntie, Rosita, ShySlime, TwinSlime

TITLE = "Sample Pair — Example Arena"


def create_game() -> GameEngine:
    """Defeat both slimes in the walled garden."""
    game = GameEngine(width=8, height=8, win_condition="defeat_all")
    game.add_hero(Rosita(x=1, y=1))

    # Two hedge walls split the garden into lanes.
    for name, x, y in [
        ("Hedge", 3, 2),
        ("Hedge", 3, 3),
        ("Hedge", 3, 4),
        ("Hedge", 3, 5),
        ("Hedge", 5, 4),
        ("Hedge", 5, 5),
    ]:
        game.add_wall(Wall(name, x, y))

    # Registration order = turn order.
    game.add_villain(TwinSlime(x=6, y=2))
    game.add_villain(ShySlime(x=6, y=6))

    game.add_npc(Auntie(x=1, y=6))

    return game
