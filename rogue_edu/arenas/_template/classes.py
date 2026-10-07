"""YOUR MONSTERS LIVE HERE.

Classes only: subclasses and their behavior. Do NOT build the game in
this file, and do NOT store starting coordinates here -- coordinates
belong in game_config.py. Rename these classes (and update the import
in game_config.py), keep the (x, y) constructor shape.
"""

from engine.actions import AttackAction, MoveAction, SpeakAction
from engine.base_classes import Hero, NPC, Villain


class MyHero(Hero):
    """Heroes need no act(): the engine translates your WASD/space keys."""

    def __init__(self, x, y):
        super().__init__("My Hero", x, y, hp=25, attack_power=6)

    def symbol(self):
        return "🧑‍🚀"


class MyVillain(Villain):
    """The classic beginner brain: chase, and bite when adjacent."""

    def __init__(self, x, y):
        super().__init__("My Villain", x, y, hp=10, attack_power=3)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)  # adjacent: strike!
        return MoveAction(dx, dy)  # otherwise: creep closer.

    def symbol(self):
        return "🦠"


class MyNPC(NPC):
    """Bump me for a free dialogue (villains freeze that turn)."""

    def __init__(self, x, y):
        super().__init__("My Elder", x, y)

    def interact(self, view):
        return SpeakAction("Welcome to our arena! Mind the villager.")

    def symbol(self):
        return "🧝"
