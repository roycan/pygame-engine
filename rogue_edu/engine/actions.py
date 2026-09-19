"""Intent-based Action types.

Grade 9 students: when the engine calls your ``act(view)`` or
``interact(view)`` method, you NEVER change the world yourself.
You return one of these small objects instead, and the engine decides
what really happens. This is called the "intent-based action pattern".

Important design rule:
    ``AttackAction`` carries a DIRECTION, never a damage number.
    Damage always comes from the attacker's own ``attack_power`` stat,
    so nobody can cheat by writing ``AttackAction(damage=999)``.
    (Try it -- Python raises a TypeError because the field does not exist.)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    """Base class for every intent an entity can return.

    Frozen (immutable) on purpose: once you announce an intent, the
    engine owns it and nobody can quietly edit it.
    """


@dataclass(frozen=True)
class MoveAction(Action):
    """Intent: "I want to step one tile in a cardinal direction."

    Valid vectors (dx, dy) are exactly one of:
        (0, -1) north, (0, 1) south, (-1, 0) west, (1, 0) east.
    Anything else (including diagonals like (1, 1)) is rejected by the
    engine, converted to a WaitAction, and a WARNING event is logged.
    """

    dx: int
    dy: int


@dataclass(frozen=True)
class AttackAction(Action):
    """Intent: "I want to strike the tile one step in this direction."

    The engine looks at the tile at (my_x + dx, my_y + dy):
        * a Villain attacking the tile where the Hero stands -> the Hero
          takes damage equal to the attacker's sanitized attack power;
        * a wall, an empty tile, or another villain -> zero damage and
          a BLOCKED or MISSED event.
    There is deliberately NO damage field here. Damage is a property of
    the attacker, decided by the engine, never by the action payload.
    """

    dx: int
    dy: int


@dataclass(frozen=True)
class WaitAction(Action):
    """Intent: "I do nothing this turn."

    Perfect for testing, thinking, or playing it safe.
    """


@dataclass(frozen=True)
class SpeakAction(Action):
    """Intent: "Here is what I want to say."

    Returned by an NPC's ``interact(view)`` method. The engine stores the
    message as the game's ``active_dialogue`` and freezes enemy turns
    until the player dismisses it with any key.
    """

    message: str
