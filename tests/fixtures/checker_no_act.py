"""Checker fixture: a Villain MISSING the required act() method."""

from engine.base_classes import Villain


class BrokenSlime(Villain):
    def __init__(self, x, y):
        super().__init__("BrokenSlime", x, y, hp=5, attack_power=1)

    def symbol(self):
        return "🟢"

    # act() is deliberately missing.
