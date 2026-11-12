"""The Necromancer's cast -- a squad fight that teaches COMPOSITION.

Grade 9 students: until now, every villain fought alone. This arena is
different -- the boss BUILDS and COMMANDS a squad. Four ideas working
together:

1. CLASS COMPOSITION -- the Necromancer holds a ``self.squad`` list of
   SkeletonMinion objects, and each minion holds a ``master``
   back-reference. They are separate objects that COLLABORATE by
   calling each other's methods. (The engine stays the sole mutator of
   the world -- positions, hp, turn order; the minions only ever flip
   their OWN internal flags.)
2. TURN COUNTERS AS INTERNAL STATE -- ``self.chants`` counts the
   Necromancer's OWN turns. (Careful: the ENGINE also has a
   ``turn_count``; a villain tracking its own rhythm is a different,
   private number.)
3. EVENT-DRIVEN AWAKENING -- graves rise on the boss's schedule
   (every third chant) AND in vengeance when the master falls.
4. SPATIAL EVALUATION -- risen skeletons read the battlefield through
   the read-only view: ``distance_to_hero`` and
   ``get_direction_toward_hero`` decide every step.

One honest fence note: a TRUE mid-game spawn ("add a brand-new entity
to the running engine") is impossible arena-only -- the engine is the
sole mutator by design, and there is no SummonAction. So the graves are
pre-placed and AWAKEN instead: same squad fantasy, zero engine changes.
"""

from engine.actions import AttackAction, MoveAction, SpeakAction, WaitAction
from engine.base_classes import Hero, NPC, Villain


class GraveWarden(Hero):
    """The graveyard's guardian: tough (hp=60), measured (attack_power=7).

    Three blows smash a sleeping bone pile; three blows also fell a
    risen skeleton. The question this arena asks is not "can you win?"
    but "in what ORDER?" -- rush the master, or clear the graves first?
    """

    def __init__(self, x, y):
        super().__init__("Warden Mora", x, y, hp=60, attack_power=7)

    def symbol(self):
        return "🕯️"


class SkeletonMinion(Villain):
    """A grave that is ALSO a future soldier -- the squad's rank and file.

    Dormant (🦴 Bone Pile): sits still, never fights, but is ALIVE and
    can be smashed in three blows before it wakes.

    Risen (💀 Risen Skeleton): the classic chase-and-bite brain.

    Awakening is event-driven, two ways:
    * the master's ``rise()`` call -- plain object-to-object composition;
    * vengeance -- if the skeleton can see its master has fallen, it
      rises unbidden (and it can act the very same tick).
    """

    def __init__(self, x, y, label="I", master=None):
        super().__init__(f"Bone Pile {label}", x, y, hp=15, attack_power=4)
        self.label = label
        self.awake = False  # internal state: the grave's own private flag
        self.master = master  # composition: a reference BACK to the boss

    def rise(self):
        """Wake up: flip internal state, rename, change the glyph.

        The rename is the narration trick: the engine's log lines embed
        ``name``, so every future line reads "Risen Skeleton ...".
        """
        self.awake = True
        self.name = f"Risen Skeleton {self.label}"

    def act(self, view):
        # Vengeance clause: a fallen master wakes every grave at once.
        if not self.awake and self.master is not None:
            if not self.master.is_alive():
                self.rise()
        if not self.awake:
            return WaitAction()  # graves do not move or fight... yet
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)
        return MoveAction(dx, dy)

    def symbol(self):
        return "💀" if self.awake else "🦴"


class Necromancer(Villain):
    """The squad's commander: stationary, harmless, and NEVER alone.

    It never moves and never strikes (attack_power=0 -- its violence is
    fully DELEGATED to its children). Every third chant it raises the
    next sleeping grave via ``minion.rise()`` -- one per chant, so the
    squad fills in WAVES. The squad list itself is the cap: four graves
    were buried, so four can ever rise.

    Explicit narration, same trick as the Inferno Drake: on a wave turn
    the boss renames itself, so the log reads
    "Necromancer (chanting! Bone Pile I rises!) waits."
    """

    def __init__(self, x, y):
        super().__init__("Necromancer", x, y, hp=40, attack_power=0)
        self.chants = 0  # its OWN turn rhythm -- not the engine's turn_count
        self.squad = []  # composition: the boss holds its children

    def recruit(self, minions):
        """Hand the boss its squad (create_game wires this up)."""
        self.squad.extend(minions)

    def act(self, view):
        self.chants += 1
        self.name = "Necromancer"  # reset, then re-narrate on a wave turn
        if self.chants % 3 == 0:
            for minion in self.squad:
                if not minion.awake:
                    grave_name = minion.name
                    minion.rise()  # object-to-object call: the "summon"
                    self.name = f"Necromancer (chanting! {grave_name} rises!)"
                    break  # one resurrection per chant: staggered waves
        return WaitAction()  # it never leaves the back of the arena

    def symbol(self):
        return "🧙‍♂️"


class GraveKeeper(NPC):
    """Bump for the strategy briefing (villains freeze that turn)."""

    def __init__(self, x, y):
        super().__init__("Grave Keeper", x, y)

    def interact(self, view):
        return SpeakAction(
            "Two rules, warden. Every THIRD chant, the Necromancer raises "
            "one bone pile -- smash a sleeping pile in three blows before "
            "its turn comes. But if you strike the master down first, "
            "every grave rises AT ONCE, in vengeance. Choose your order."
        )

    def symbol(self):
        return "🪦"
