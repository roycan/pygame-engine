"""The Inferno Drake's cast -- a two-phase boss that shows off OOP.

Grade 9 students: this arena is a BOSS FIGHT, and the boss is a master
class in four ideas working together:

1. STATE ENCAPSULATION -- ``self.phase`` is the drake's private mood.
   Nothing outside the class flips it; the class itself decides when
   the moment of rage has come.
2. METHOD OVERRIDING -- ``symbol()`` and ``calculate_attack_damage()``
   are inherited from ``Villain``/``Character`` but REWRITTEN here, so
   the same engine question gets a different answer per phase.
3. SUPER() DELEGATION -- ``calculate_attack_damage()`` asks the parent
   class for the honest base number FIRST, then doubles it when raging.
4. CONDITIONAL BEHAVIOR -- ``act()`` checks the phase BEFORE deciding
   what this turn is for.

One honest-boundary note (the same one student_starter teaches): the
engine guards the WORLD -- movement, combat math, other entities. The
drake renaming ITSELF when it enrages is legal precisely because
``self.name`` is its own ordinary attribute. The engine then does the
explicit storytelling for free: every future log line says "ENRAGED".
"""

from engine.actions import AttackAction, MoveAction, SpeakAction, WaitAction
from engine.base_classes import Hero, NPC, Villain


class Ashwarden(Hero):
    """The drake-slayer: tough (hp=60) and sharp (attack_power=8).

    A starter knight (25 hp) cannot survive an enrage; this champion
    can. Balance is part of game design -- stats ARE design decisions.
    """

    def __init__(self, x, y):
        super().__init__("Sir Ashworth", x, y, hp=60, attack_power=8)

    def symbol(self):
        return "⚔️"


class InfernoDrake(Villain):
    """A two-phase boss: 🐉 calm hunter → 🔥 enraged firestorm.

    Phase 1 (hp above half): an ordinary chase-and-bite villain (7 dmg).

    The moment its hp drops to HALF or below, ``act()`` spends ONE whole
    turn raging (a WaitAction -- the hero gets a free hit!), and three
    things change at once, all driven by ``self.phase``:

    * ``symbol()`` now returns 🔥 -- the canvas re-draws it the very
      same turn, because the engine asks ``symbol()`` EVERY turn.
    * ``self.name`` changes, so the action log says "ENRAGED" on every
      future line -- explicit narration with zero engine changes.
    * ``calculate_attack_damage()`` returns DOUBLE the base damage.
    """

    def __init__(self, x, y):
        super().__init__("Inferno Drake", x, y, hp=40, attack_power=7)
        self.phase = 1  # internal state: 1 = calm, 2 = enraged

    def symbol(self):
        """Express the internal phase as the icon drawn on the canvas."""
        return "🔥" if self.phase == 2 else "🐉"

    def calculate_attack_damage(self):
        """Double the damage output during phase 2.

        ``super()`` fetches the honest base number first. The engine
        STILL sanitizes the answer into [0, MAX_ATK] -- overrides are
        flavor, never trusted blindly. (7 * 2 = 14 fits easily.)
        """
        base_damage = super().calculate_attack_damage()
        return base_damage * 2 if self.phase == 2 else base_damage

    def act(self, view):
        """Phase check FIRST, then the classic chase-and-bite brain."""
        if self.phase == 1 and self.hp <= self.max_hp // 2:
            self.phase = 2  # flip the internal state...
            self.name = "Inferno Drake (ENRAGED! Fire doubled!)"
            return WaitAction()  # ...the roar costs this whole turn
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)
        return MoveAction(dx, dy)


class EmberScout(NPC):
    """Bump the scout for the boss briefing (villains freeze that turn)."""

    def __init__(self, x, y):
        super().__init__("Ember Scout", x, y)

    def interact(self, view):
        return SpeakAction(
            "Boss briefing! The Inferno Drake enrages at HALF health: "
            "its mark flips to 🔥 and every hit DOUBLES. The rage costs "
            "it one full turn -- spend that free hit wisely!"
        )

    def symbol(self):
        return "🧭"
