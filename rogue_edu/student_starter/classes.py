"""STUDENT FILE #1 -- Your class blueprints.

This is where YOU write code. Each class below is a small, complete,
working example -- edit them, rename them, copy them, break them, fix
them. When you think you are done, run:

    python check_my_class.py

Two rules for this file:
1. Classes only: define subclasses and their behavior. Do NOT create
   the game here, and do NOT store starting coordinates in the class --
   coordinates are assigned in game_config.py.
2. Never mutate the world yourself: your methods RECEIVE a read-only
   ``view`` and RETURN an Action. The engine does the moving and hitting.
"""

from engine.actions import AttackAction, MoveAction, SpeakAction
from engine.base_classes import Hero, NPC, Villain


class BraveKnight(Hero):
    """Your player character.

    Heroes do not need an ``act()`` method -- the engine translates your
    WASD/space keys for you. Customize the name and stats here:

        super().__init__(NAME, x, y, hp=HEALTH, attack_power=DAMAGE)
        hp clamps to [1, 200]; attack_power clamps to [0, 40] (loudly!).
    """

    def __init__(self, x: int, y: int):
        super().__init__("Sir Ada", x, y, hp=25, attack_power=6)

    def symbol(self) -> str:
        return "🛡️"


class Slime(Villain):
    """A classic beginner villain: chase the Hero, attack when adjacent.

    The three lines of ``act()`` below are the heart of villain AI:
        1. ask the view WHERE the hero is relative to you,
        2. decide what you WANT to do,
        3. RETURN an Action -- never move yourself!
    """

    def __init__(self, x: int, y: int):
        super().__init__("Slime", x, y, hp=10, attack_power=3)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)  # adjacent: strike!
        return MoveAction(dx, dy)        # otherwise: creep closer.

    def symbol(self) -> str:
        return "🟢"


class Elder(NPC):
    """A friendly character who says something when you bump into them.

    NPCs have no hp and never take turns. Bumping an NPC opens dialogue
    and FREEZES the villains for that turn -- a safe moment to read.
    """

    def __init__(self, x: int, y: int):
        super().__init__("Elder Maple", x, y)

    def interact(self, view):
        return SpeakAction(
            "Walls never move, but slimes never sleep. Keep your back to a corner!"
        )

    def symbol(self) -> str:
        return "🧙"
