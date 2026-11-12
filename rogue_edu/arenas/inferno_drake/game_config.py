"""Inferno Drake arena -- a two-phase boss fight, composed here.

Composition only: WHERE everything starts and WHAT winning means. All
behavior lives in classes.py. TITLE is the name on the /games card.
"""

from engine.base_classes import Wall
from engine.core import GameEngine

from arenas.inferno_drake.classes import Ashwarden, EmberScout, InfernoDrake

TITLE = "Inferno Drake — Two-Phase Boss"


def create_game() -> GameEngine:
    """An 8x8 ruined shrine. Win by defeating the drake (defeat_all).

    Balance notes (tuned beatable-but-hard): Sir Ashworth trades 8
    damage per turn against the drake's 7 (phase 1) and 14 (phase 2).
    Head-on, the drake enrages on turn 3 and the hero wins on turn 5
    at 32/60 hp -- a win, but sloppy play near the pillars can lose it.
    """
    game = GameEngine(width=8, height=8, win_condition="defeat_all")

    game.add_hero(Ashwarden(x=1, y=1))

    # A ruined shrine in the middle: cover to kite the enraged drake.
    for name, x, y in [
        ("Shrine Pillar", 3, 3),
        ("Shrine Pillar", 3, 4),
        ("Shrine Pillar", 4, 4),
        ("Fallen Obelisk", 6, 1),
        ("Fallen Obelisk", 1, 4),
    ]:
        game.add_wall(Wall(name, x, y))

    # Registration order = turn order.
    game.add_villain(InfernoDrake(x=6, y=6))
    game.add_npc(EmberScout(x=1, y=6))

    return game
