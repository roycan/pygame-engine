"""Quest Givers arena -- composition only: place everyone, wire the quests.

TITLE is the name on the /games card. The wiring below is the lesson:
build every object FIRST, then hand each questgiver its targets through
``recruit()``. Constructors stay ``(x, y)``-shaped because the doctor
constructs every class as ``cls(3, 3)``.

Win condition: defeat_all -- lay both Restless Dead to rest (which also
completes Gravekeeper Vael's quest). Sage Elowen's pilgrimage is a side
quest: pure composition, told through symbol and dialogue.
"""

from engine.base_classes import Wall
from engine.core import GameEngine

from arenas.quest_givers.classes import (
    PilgrimageQuest,
    RestlessDead,
    Shrine,
    SirCadan,
    SlayerQuest,
)

TITLE = "Quest Givers — NPC Hierarchy"


def create_game() -> GameEngine:
    """A 10x10 shrineyard. Win by defeating the Restless Dead."""
    game = GameEngine(width=10, height=10, win_condition="defeat_all")

    game.add_hero(SirCadan(x=1, y=8))

    # -- Scenery: ruined shrine pieces ---------------------------------
    for name, x, y in [
        ("Fallen Column", 3, 4),
        ("Fallen Column", 4, 4),
        ("Crumbling Wall", 7, 7),
    ]:
        game.add_wall(Wall(name, x, y))

    # -- Build EVERYTHING first (objects need references to exist) ------
    dead_a = RestlessDead(x=6, y=3)
    dead_b = RestlessDead(x=8, y=5)

    shrine_a = Shrine(x=2, y=2)
    shrine_a.name = "Shrine of Dawn"
    shrine_b = Shrine(x=5, y=5)
    shrine_b.name = "Shrine of Dusk"
    shrine_c = Shrine(x=8, y=8)
    shrine_c.name = "Shrine of Ash"

    slayer = SlayerQuest(x=1, y=1)  # "Gravekeeper Vael"
    pilgrim = PilgrimageQuest(x=5, y=8)  # "Sage Elowen"

    # -- THEN wire the quests (composition, post-construction) ----------
    slayer.recruit([dead_a, dead_b])  # kill quest: counts is_alive()
    pilgrim.recruit([shrine_a, shrine_b, shrine_c])  # visit quest: counts visited

    # -- Registration order = turn order --------------------------------
    game.add_villain(dead_a)
    game.add_villain(dead_b)

    game.add_npc(shrine_a)
    game.add_npc(shrine_b)
    game.add_npc(shrine_c)
    game.add_npc(slayer)
    game.add_npc(pilgrim)

    return game