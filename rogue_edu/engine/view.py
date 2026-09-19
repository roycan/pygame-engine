"""SafeGameView: the read-only world snapshot handed to student code.

Grade 9 students: when the engine calls your ``act(view)`` or
``interact(view)`` method, this ``view`` object is your EYES. You can
ask it questions, but you can never change the world through it -- it
holds frozen copies of positions, not live references to the engine.

Bonus feature: if you typo a method name, the view guesses what you
meant. ``view.hero_pos()`` raises an AttributeError that says
"Did you mean 'get_hero_toward_position'?" -- wait, no:
"Did you mean 'get_hero_position'?".
"""

from __future__ import annotations

import difflib


class SafeGameView:
    """An immutable snapshot of the board, taken at the moment it is built.

    Guaranteed properties:
        * No reference to the GameEngine is stored -- the world cannot be
          mutated through the view, not even by accident.
        * All stored data is immutable (tuples and frozensets of ints).
        * ``copy.deepcopy(view)`` is safe: dunder attribute lookups fail
          fast instead of recursing forever (see ``__getattr__``).
    """

    #: The complete list of methods student code may call. Used by the
    #: typo catcher in ``__getattr__`` to suggest corrections.
    _PUBLIC_API = (
        "get_hero_position",
        "distance_to_hero",
        "get_direction_toward_hero",
        "is_tile_passable",
    )

    def __init__(self, engine):
        """Build the snapshot from the engine's CURRENT state.

        The engine passes itself in here but the view keeps only plain
        data -- never the engine itself.
        """
        hero = engine.hero
        self._width = engine.width
        self._height = engine.height
        self._hero_position = (hero.x, hero.y)
        self._wall_tiles = frozenset((w.x, w.y) for w in engine.walls)
        self._npc_tiles = frozenset((n.x, n.y) for n in engine.npcs)
        self._villain_tiles = frozenset(
            (v.x, v.y) for v in engine.villains if v.is_alive()
        )

    # ------------------------------------------------------------------
    # Public helper API (the only methods student code should call)
    # ------------------------------------------------------------------

    def get_hero_position(self) -> tuple[int, int]:
        """Return the Hero's (x, y) position as a tuple."""
        return self._hero_position

    def distance_to_hero(self, entity) -> int:
        """Manhattan distance from ``entity`` to the Hero.

        Strictly cardinal: ``abs(x1 - x2) + abs(y1 - y2)``.
        A distance of exactly 1 guarantees the entity is orthogonally
        adjacent to the Hero (diagonals read as distance 2).
        """
        hx, hy = self._hero_position
        return abs(entity.x - hx) + abs(entity.y - hy)

    def get_direction_toward_hero(self, entity) -> tuple[int, int]:
        """One cardinal step from ``entity`` toward the Hero.

        Returns a normalized (dx, dy) where each component is -1, 0 or 1
        and exactly one component is non-zero -- perfect for feeding
        straight into ``MoveAction`` or ``AttackAction``.

        Tie-breaking: the larger axis delta wins; on an exact tie the
        horizontal (x) axis wins. Standing on the Hero returns (0, 0).
        """
        hx, hy = self._hero_position
        dx, dy = hx - entity.x, hy - entity.y
        if dx == 0 and dy == 0:
            return (0, 0)
        if abs(dx) >= abs(dy):
            return (1 if dx > 0 else -1, 0)
        return (0, 1 if dy > 0 else -1)

    def is_tile_passable(self, x: int, y: int) -> bool:
        """True if a character could stand on tile (x, y).

        A tile is passable when it is inside the board and contains no
        wall, no Hero, no NPC and no living Villain.
        """
        if not (0 <= x < self._width and 0 <= y < self._height):
            return False
        if (x, y) in self._wall_tiles:
            return False
        if (x, y) == self._hero_position:
            return False
        if (x, y) in self._npc_tiles:
            return False
        if (x, y) in self._villain_tiles:
            return False
        return True

    # ------------------------------------------------------------------
    # Typo catcher (safe __getattr__)
    # ------------------------------------------------------------------

    def __getattr__(self, name: str):
        """Suggest the correct method name when students make a typo.

        GUARD ORDER MATTERS:
        1. Dunder names raise immediately -- otherwise copy/pickle/
           introspection machinery recurses into __getattr__ forever.
        2. Everything else gets a difflib "Did you mean ...?" hint built
           from _PUBLIC_API, or a list of valid methods.
        """
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(f"SafeGameView has no attribute {name!r}")
        close = difflib.get_close_matches(name, self._PUBLIC_API, n=1)
        if close:
            raise AttributeError(
                f"SafeGameView has no method {name!r}. Did you mean {close[0]!r}?"
            )
        raise AttributeError(
            f"SafeGameView has no method {name!r}. "
            f"Valid methods: {', '.join(self._PUBLIC_API)}"
        )
