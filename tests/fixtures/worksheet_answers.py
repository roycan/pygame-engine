"""Worksheet 01 answer key -- real, importable, engine-tested code.

This module is the SINGLE SOURCE OF TRUTH for Workshop 01's answers:
tests/test_worksheet.py exercises THESE classes against the engine, and
a sync test asserts the worksheet shows the same signature lines
verbatim. Edit here first, then update the worksheet to match.
"""

from engine.actions import AttackAction, MoveAction, WaitAction
from engine.base_classes import Hero, Villain, Wall
from engine.core import GameEngine

#: Lines that MUST appear verbatim in workshops/workshop_01_meet_the_engine.md.
SIGNATURE_LINES = (
    'super().__init__("Magma Blob", x, y, hp=14, attack_power=4)',
    "if self.hp * 2 >= self.max_hp:",
    "return MoveAction(-dx, -dy)",
    'game = GameEngine(width=10, height=10, win_condition="defeat_all")',
    "game.add_villain(ReskinnedSlime(x=8, y=1))",
)


# ---------------------------------------------------------------------------
# Tier 1 (seedling): the starter Slime's chase AI, wearing a new identity.
# ---------------------------------------------------------------------------
class ReskinnedSlime(Villain):
    """Chase-and-bite AI, new name/stats/symbol."""

    def __init__(self, x, y):
        super().__init__("Magma Blob", x, y, hp=14, attack_power=4)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)
        return MoveAction(dx, dy)

    def symbol(self):
        return "🔥"


# ---------------------------------------------------------------------------
# Tier 2 (herb): ONE personality branch -- brave above half hp, flees below.
# ---------------------------------------------------------------------------
class CowardSlime(Villain):
    """Brave above half hp; below it, runs the other way."""

    def __init__(self, x, y):
        super().__init__("Sir Wobbles", x, y, hp=12, attack_power=5)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if self.hp * 2 >= self.max_hp:
            if view.distance_to_hero(self) == 1:
                return AttackAction(dx, dy)
            return MoveAction(dx, dy)
        if (dx or dy) and view.is_tile_passable(self.x - dx, self.y - dy):
            return MoveAction(-dx, -dy)
        return WaitAction()

    def symbol(self):
        return "🐭"


# ---------------------------------------------------------------------------
# Tier 2 (herb) alternate: a patrol route instead of a mood swing.
# ---------------------------------------------------------------------------
class PatrolSlime(Villain):
    """Walks a fixed square route; bites only when you get close."""

    def __init__(self, x, y):
        super().__init__("Roundabout", x, y, hp=14, attack_power=4)
        self._route = [(1, 0), (0, 1), (-1, 0), (0, -1)] * 2
        self._step = 0

    def act(self, view):
        if view.distance_to_hero(self) == 1:
            dx, dy = view.get_direction_toward_hero(self)
            return AttackAction(dx, dy)
        dx, dy = self._route[self._step % len(self._route)]
        self._step += 1
        if view.is_tile_passable(self.x + dx, self.y + dy):
            return MoveAction(dx, dy)
        return WaitAction()

    def symbol(self):
        return "🌀"


# ---------------------------------------------------------------------------
# Tier 3 (tree): compose a mini arena around your creations.
# ---------------------------------------------------------------------------
class ArenaChamp(Hero):
    """The arena's hero."""

    def __init__(self, x, y):
        super().__init__("Arena Champ", x, y, hp=20, attack_power=7)

    def symbol(self):
        return "🦸"


def create_arena_game() -> GameEngine:
    """A tiny arena: two custom villains, two rocks, fight focus."""
    game = GameEngine(width=10, height=10, win_condition="defeat_all")
    game.add_hero(ArenaChamp(x=1, y=1))
    game.add_villain(ReskinnedSlime(x=8, y=1))
    game.add_villain(CowardSlime(x=8, y=8))
    game.add_wall(Wall("Rock", 4, 4))
    game.add_wall(Wall("Rock", 5, 4))
    return game
