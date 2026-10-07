"""Sample Pair -- a finished pair folder, in its final merged form.

Read this to see what "done" looks like, then copy arenas/_template/
and make it YOURS. Note the inheritance trick at the bottom: ShySlime
extends TwinSlime and overrides ONLY act() -- one line of difference.
"""

from engine.actions import AttackAction, MoveAction, SpeakAction, WaitAction
from engine.base_classes import Hero, NPC, Villain


class Rosita(Hero):
    """The sample champion: sturdier than the starter knight."""

    def __init__(self, x, y):
        super().__init__("Sir Rosita", x, y, hp=30, attack_power=5)

    def symbol(self):
        return "🌹"


class TwinSlime(Villain):
    """Chase-and-bite -- the starter Slime's brain, purple and meaner."""

    def __init__(self, x, y):
        super().__init__("Twin Slime", x, y, hp=8, attack_power=3)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)
        return MoveAction(dx, dy)

    def symbol(self):
        return "🟣"


class ShySlime(TwinSlime):
    """Inherits everything from TwinSlime; overrides ONLY act().

    Same stats, same family -- but when the hero gets close it runs.
    Polymorphism in one overridden method.
    """

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) <= 2:
            return MoveAction(-dx, -dy)  # too shy: flee!
        return WaitAction()

    def symbol(self):
        return "🔮"


class Auntie(NPC):
    """Free advice, one bump away."""

    def __init__(self, x, y):
        super().__init__("Auntie Bev", x, y)

    def interact(self, view):
        return SpeakAction(
            "The purple one bites, but the shy one just runs. Chase it into a corner!"
        )

    def symbol(self):
        return "🧓"
