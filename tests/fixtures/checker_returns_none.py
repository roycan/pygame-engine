"""Checker fixture: act() returns None instead of an Action."""

from engine.base_classes import Villain


class LazySlime(Villain):
    def __init__(self, x, y):
        super().__init__("LazySlime", x, y, hp=5, attack_power=1)

    def act(self, view):
        return None  # BUG: must return an Action

    def symbol(self):
        return "🟢"
