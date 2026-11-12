"""Necromancer's Grave Squad -- a multi-wave summoner boss, composed here.

Composition only: WHERE everything starts and WHAT winning means. All
behavior lives in classes.py. TITLE is the name on the /games card.

WIRING NOTE (the composition lesson): create_game() builds the squad
FIRST, hands each minion its ``master`` back-reference, then recruits
the squad into the Necromancer. Registration order is choreography:
the Necromancer is registered FIRST, so a grave it raises acts in the
very same tick -- "rises and immediately lurches toward you".
"""

from engine.base_classes import Wall
from engine.core import GameEngine

from arenas.necromancer_squad.classes import (
    GraveKeeper,
    GraveWarden,
    Necromancer,
    SkeletonMinion,
)

TITLE = "Necromancer — Multi-Wave Grave Squad"


def create_game() -> GameEngine:
    """A 10x10 cemetery. Win by defeating the necromancer AND its squad
    (defeat_all; dead villains are retained, so late rises cannot
    unwinnable the game)."""
    game = GameEngine(width=10, height=10, win_condition="defeat_all")

    game.add_hero(GraveWarden(x=1, y=8))

    # -- The boss (built first so the squad can reference it) -------------
    necromancer = Necromancer(x=8, y=1)

    # -- The squad: four buried graves, each wired to its master ----------
    squad = [
        SkeletonMinion(5, 2, label="I", master=necromancer),
        SkeletonMinion(6, 4, label="II", master=necromancer),
        SkeletonMinion(4, 5, label="III", master=necromancer),
        SkeletonMinion(7, 6, label="IV", master=necromancer),
    ]
    necromancer.recruit(squad)

    # -- Scenery: the sanctum screen + two cemetery fences ----------------
    for name, x, y in [
        ("Sanctum Screen", 7, 1),
        ("Sanctum Screen", 7, 2),
        ("Cemetery Fence", 3, 3),
        ("Cemetery Fence", 6, 5),
    ]:
        game.add_wall(Wall(name, x, y))

    # -- Registration order = turn order. Boss FIRST: a grave it raises
    #    acts the same tick (rise-then-lurch).
    game.add_villain(necromancer)
    for minion in squad:
        game.add_villain(minion)

    game.add_npc(GraveKeeper(x=1, y=5))

    return game
