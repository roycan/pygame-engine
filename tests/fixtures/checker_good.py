"""Checker fixture: a HEALTHY student file (all three bases, correct returns)."""

from engine.actions import AttackAction, MoveAction, SpeakAction
from engine.base_classes import Hero, NPC, Villain


class SampleHero(Hero):
    def __init__(self, x, y):
        super().__init__("Sample", x, y, hp=10, attack_power=2)

    def symbol(self):
        return "🦸"


class SampleSlime(Villain):
    def __init__(self, x, y):
        super().__init__("SampleSlime", x, y, hp=5, attack_power=1)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)
        return MoveAction(dx, dy)

    def symbol(self):
        return "🟢"


class SampleElder(NPC):
    def __init__(self, x, y):
        super().__init__("SampleElder", x, y)

    def interact(self, view):
        return SpeakAction("Hello")

    def symbol(self):
        return "🧙"
