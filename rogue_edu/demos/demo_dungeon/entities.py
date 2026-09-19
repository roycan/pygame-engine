"""Demo Dungeon entities -- a READ-ONLY worked example.

Three villains, three different AI strategies, all built from the same
tiny toolbox (``view.get_direction_toward_hero`` +
``view.is_tile_passable`` + returning Actions). Study the differences:

* Chaser    -- relentless: cardinal pursuit with a blocked-axis fallback.
* Coward    -- brave above half hp, flees below it.
* Patroller -- walks a fixed route, attacks only when you get close.

Run this demo in the browser with:

    GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py
"""

from engine.actions import AttackAction, MoveAction, SpeakAction, WaitAction
from engine.base_classes import Hero, NPC, Villain


class DemoChampion(Hero):
    """The demo's hero -- slightly tougher than the starter knight."""

    def __init__(self, x: int, y: int):
        super().__init__("Rin the Champion", x, y, hp=30, attack_power=8)

    def symbol(self) -> str:
        return "⚔️"


class Chaser(Villain):
    """Relentless pursuit: preferred axis first, fallback to the other
    axis when the way is blocked, attack when orthogonally adjacent."""

    def __init__(self, x: int, y: int):
        super().__init__("Grim Chaser", x, y, hp=8, attack_power=4)

    def act(self, view):
        hx, hy = view.get_hero_position()
        dx, dy = hx - self.x, hy - self.y
        choices = []
        if dx != 0:
            choices.append((1 if dx > 0 else -1, 0))
        if dy != 0:
            choices.append((0, 1 if dy > 0 else -1))
        if view.distance_to_hero(self) == 1:
            return AttackAction(*choices[0])
        for step_x, step_y in choices:
            if view.is_tile_passable(self.x + step_x, self.y + step_y):
                return MoveAction(step_x, step_y)
        return WaitAction()

    def symbol(self) -> str:
        return "👹"


class Coward(Villain):
    """Brave above half hp (chase + strike); below half hp it flees."""

    def __init__(self, x: int, y: int):
        super().__init__("Sir Coward", x, y, hp=12, attack_power=5)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        brave = self.hp * 2 >= self.max_hp
        if brave:
            if view.distance_to_hero(self) == 1:
                return AttackAction(dx, dy)
            if (dx or dy) and view.is_tile_passable(self.x + dx, self.y + dy):
                return MoveAction(dx, dy)
            return WaitAction()
        # Wounded: run the OTHER way if that tile is open.
        if (dx or dy) and view.is_tile_passable(self.x - dx, self.y - dy):
            return MoveAction(-dx, -dy)
        return WaitAction()

    def symbol(self) -> str:
        return "🐔"


class Patroller(Villain):
    """Walks a fixed out-and-back route; attacks only if you come close."""

    def __init__(self, x: int, y: int):
        super().__init__("Stone Sentinel", x, y, hp=14, attack_power=6)
        self._route = [
            (1, 0), (1, 0), (0, 1), (0, 1),
            (-1, 0), (-1, 0), (0, -1), (0, -1),
        ]
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

    def symbol(self) -> str:
        return "🗿"


class AncientOne(NPC):
    """Dungeon lore dispenser."""

    def __init__(self, x: int, y: int):
        super().__init__("The Ancient One", x, y)

    def interact(self, view):
        return SpeakAction(
            "Three guardians pace these halls. Fell them all, then take "
            "the stairs in the far corner. The wounded one runs -- corner it!"
        )

    def symbol(self) -> str:
        return "🔮"
