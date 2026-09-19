"""Base class blueprints for the RogueEdu engine.

Grade 9 students: THESE are the classes you subclass in
``student_starter/classes.py``. You should never need to edit this file.

Loud-invariant doctrine:
    Stats are clamped LOUDLY, never silently. Whenever ``hp``, ``max_hp``
    or ``attack_power`` arrives out of range, the value is clamped AND a
    human-readable warning is appended to ``self.warnings``. The engine
    drains those warnings into its setup log when the character is
    registered (``add_hero`` / ``add_villain``), so nothing is ever lost.
"""

from abc import ABC, abstractmethod

from .actions import Action, SpeakAction

#: Absolute ceilings for every character in the game.
MAX_HP = 200
MAX_ATK = 40


class GameObject(ABC):
    """Anything that occupies one tile on the 10x10 board.

    Stores identity (``name``) and placement (``x``, ``y``). Subclasses
    must implement ``symbol()`` so the canvas renderer knows what to draw.
    """

    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y

    @property
    def position(self) -> tuple[int, int]:
        """Read-only convenience: this object's (x, y) as a tuple."""
        return (self.x, self.y)

    @abstractmethod
    def symbol(self) -> str:
        """Return the emoji or sprite identifier drawn on this tile."""
        raise NotImplementedError


class Character(GameObject):
    """A living creature with clamped ``hp`` and ``attack_power`` stats.

    Bounds are enforced at construction time. Out-of-range values are
    clamped to ``[1, MAX_HP]`` / ``[0, MAX_ATK]`` and a warning string is
    recorded in ``self.warnings`` (the engine reads it at registration).
    """

    MAX_HP = MAX_HP
    MAX_ATK = MAX_ATK

    def __init__(self, name: str, x: int, y: int, hp: int, attack_power: int):
        super().__init__(name, x, y)
        self.warnings: list[str] = []
        self.max_hp = self._clamp_stat(hp, 1, self.MAX_HP, "max_hp")
        self.hp = self._clamp_stat(hp, 1, self.max_hp, "hp")
        self.attack_power = self._clamp_stat(attack_power, 0, self.MAX_ATK, "attack_power")

    def _clamp_stat(self, value: int, low: int, high: int, stat_name: str) -> int:
        """Clamp ``value`` into [low, high], recording a warning if clamped."""
        if low <= value <= high:
            return value
        clamped = max(low, min(high, value))
        self.warnings.append(
            f"{stat_name}={value} is out of range [{low}, {high}]; clamped to {clamped}."
        )
        return clamped

    def symbol(self) -> str:
        """Generic glyph for unnamed characters; subclasses usually
        override this (Hero -> 🦸, your Slime -> 🟢, ...). Implementing
        it here makes Character concrete, so test doubles and simple
        creatures need no symbol boilerplate. Villain/NPC stay abstract
        through ``act`` / ``interact``."""
        return "🧍"

    def calculate_attack_damage(self) -> int:
        """Damage this character deals.

        Defaults to ``attack_power``. Students MAY override this for
        flavor (critical hits, etc.) -- but the engine NEVER trusts the
        result: it sanitizes the return value (negative -> 0, above
        MAX_ATK -> MAX_ATK) before applying damage, so overrides cannot
        be abused to cheat or to heal.
        """
        return self.attack_power

    def take_damage(self, amount: int) -> int:
        """Apply damage and return how much was ACTUALLY applied.

        Defensive sanitization happens here too: negative amounts apply
        0 damage (no healing-through-damage exploits), and a killing
        blow applies at most the remaining hp.
        """
        applied = max(0, min(amount, self.hp))
        self.hp -= applied
        return applied

    def is_alive(self) -> bool:
        """True while hp is above zero. Dead villains are never purged
        from the engine's lists; they are simply skipped and hidden."""
        return self.hp > 0


class Hero(Character):
    """The player-controlled character. There is exactly one per game.

    The Hero never returns Actions itself -- the engine translates the
    player's WASD/space keys into movement, bump-to-attacks, dialogue
    bumps, or waits. Students subclass Hero to customize name, stats
    and (optionally) the symbol.
    """

    def __init__(self, name: str, x: int, y: int, hp: int = 20, attack_power: int = 5):
        super().__init__(name, x, y, hp, attack_power)

    def symbol(self) -> str:
        return "🦸"


class Villain(Character):
    """An enemy creature controlled by student code.

    Subclasses MUST implement ``act(view)`` returning an Action. Use the
    ``view`` (a read-only SafeGameView) to sense the world -- for example
    ``view.distance_to_hero(self)`` or ``view.get_direction_toward_hero(self)``.
    """

    #: Bookkeeping flag used by GameEngine: a defeated villain's
    #: "cannot act" log line fires exactly once, on its first skip.
    _death_logged: bool = False

    @abstractmethod
    def act(self, view) -> Action:
        """Decide this villain's intent for the current turn.

        Return one of: MoveAction, AttackAction, WaitAction.
        The engine validates and applies it -- you never move yourself.
        """
        raise NotImplementedError


class NPC(GameObject):
    """A friendly, indestructible tile-dweller.

    NPCs have no hp and never take turns. Subclasses MUST implement
    ``interact(view)`` returning a SpeakAction; the engine shows that
    message as dialogue and freezes the villains for that turn.
    """

    @abstractmethod
    def interact(self, view) -> SpeakAction:
        """Produce this NPC's dialogue when the Hero bumps into it."""
        raise NotImplementedError


class Wall(GameObject):
    """A solid obstacle. Blocks movement and attacks; never fights back."""

    def __init__(self, name: str = "Wall", x: int = 0, y: int = 0):
        super().__init__(name, x, y)

    def symbol(self) -> str:
        return "🧱"
