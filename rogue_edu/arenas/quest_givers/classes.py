"""The Quest Givers' cast -- Track 3's flagship NPC HIERARCHY.

Grade 9 students: every sample until now subclassed an ENGINE class
(Villain, NPC). This one goes one level deeper: it authors a BASE CLASS
of its own, then specializes it. Four ideas working together:

1. INHERITANCE + POLYMORPHISM -- ``QuestGiver`` sits BETWEEN the engine's
   ``NPC`` and its two specializations. Every questgiver answers the
   engine's one question (``interact``) with the SAME method, but each
   subclass supplies different words and different counting.
2. THE TEMPLATE-METHOD PATTERN (abstraction) -- ``QuestGiver.interact()``
   is written ONCE: a quest state machine (offered -> accepted -> done)
   that calls one hook, ``self.progress()``. Subclasses inherit the whole
   machine and override ONLY the hook. Change the machine once; every
   quest type inherits the fix.
3. COMPOSITION -- ``create_game()`` wires real objects into each giver's
   ``targets`` list AFTER construction (a ``recruit()`` call). Reading
   another object's state through a reference is collaboration; mutating
   the world is still the engine's job. That is the fence, honored.
4. STATE ON ``self`` -- ``state``, ``targets``, ``visited`` are instance
   attributes, so every player session gets its own private copy (the
   class-attribute trap in arenas/README.md is the anti-example).

Quest status is told through the three channels that already render --
tile SYMBOL (📜 -> ⚔️ -> ✅), the entity NAME (renamed on completion, so
every future log line and payload entry says "quest complete!"), and the
DIALOGUE box. No engine changes anywhere: that is Tier 3a, per
TRACK3_VISUAL_SANDBOX.md.
"""

from engine.actions import AttackAction, MoveAction, SpeakAction
from engine.base_classes import Hero, NPC, Villain


class SirCadan(Hero):
    """The questing champion. Heroes need no act() -- the keyboard drives them."""

    def __init__(self, x, y):
        super().__init__("Sir Cadan", x, y, hp=50, attack_power=7)

    def symbol(self):
        return "🗡️"


class RestlessDead(Villain):
    """A grave-quest target: the classic chase-and-bite brain.

    Two of these are wired into the SlayerQuest -- they are the
    ``targets`` the giver counts via ``is_alive()``.
    """

    def __init__(self, x, y):
        super().__init__("Restless Dead", x, y, hp=15, attack_power=7)

    def act(self, view):
        dx, dy = view.get_direction_toward_hero(self)
        if view.distance_to_hero(self) == 1:
            return AttackAction(dx, dy)
        return MoveAction(dx, dy)

    def symbol(self):
        return "🧟"


class QuestGiver(NPC):
    """The student-authored BASE class -- the hierarchy's middle rung.

    It implements ``interact()`` once, as a TEMPLATE METHOD: the state
    machine lives here, and subclasses fill in exactly one hook,
    ``self.progress()``. The doctor accepts this: it checks for
    ``interact`` with ``getattr``, so inherited methods count.

    States:
        offered  -- first bump: hear the quest, accept it (reading IS
                    accepting; the dialogue box gives no yes/no keys).
        accepted -- every bump reports progress ``done/total``; when the
                    hook says the quest is complete, flip to done.
        done     -- every later bump repeats the reward (idempotent).

    On completion the giver RENAMES itself -- the narration trick from
    the Inferno Drake: names already flow into every log line and the
    board payload, so the whole UI starts saying "quest complete!"
    without a single engine change.
    """

    def __init__(self, x, y):
        super().__init__("Quest Giver", x, y)
        self.state = "offered"  # offered -> accepted -> done
        self.targets = []  # wired by create_game() via recruit()

    def recruit(self, targets):
        """Composition wiring: hand this giver the objects it counts.

        Called from game_config.py AFTER construction, because the
        doctor constructs every class as ``cls(x, y)`` -- constructors
        must keep that exact shape.
        """
        self.targets = list(targets)

    # -- the hook: subclasses override ONLY this -----------------------
    def progress(self):
        """Return (done_count, total) for THIS quest type."""
        return (0, len(self.targets))

    def quest_text(self):
        """The offer, spoken on the first bump."""
        return "A quest awaits."

    def reward_text(self):
        """The completion reward, spoken when progress() is satisfied."""
        return "Thank you, warden."

    # -- the template method: written once, inherited by every subclass
    def interact(self, view):
        if self.state == "offered":
            self.state = "accepted"  # reading the quest accepts it
            return SpeakAction(self.quest_text())
        if self.state == "accepted":
            done, total = self.progress()
            if total > 0 and done >= total:
                self.state = "done"
                self.name += " (quest complete!)"  # narration: fires once
                return SpeakAction(self.reward_text())
            return SpeakAction(f"Quest in progress: {done}/{total} done.")
        return SpeakAction(self.reward_text())  # done: repeat the reward

    def symbol(self):
        return {"offered": "📜", "accepted": "⚔️", "done": "✅"}[self.state]


class SlayerQuest(QuestGiver):
    """Specialization 1: a KILL quest -- counts dead wired villains.

    Overrides only the hook: ``progress()`` reads each wired target's
    ``is_alive()``. The engine never sees this flag -- it is plain
    collaboration between objects wired in create_game().
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "Gravekeeper Vael"

    def progress(self):
        dead = sum(1 for target in self.targets if not target.is_alive())
        return (dead, len(self.targets))

    def quest_text(self):
        return (
            "The restless dead walk my shrine. Lay ALL of them to rest -- "
            "I feel every grave you close. (Quest: defeat every Restless Dead.)"
        )

    def reward_text(self):
        return "The graves are quiet. You have my thanks, warden."


class PilgrimageQuest(QuestGiver):
    """Specialization 2: a VISIT quest -- counts visited wired shrines.

    Same machine, different hook: ``progress()`` reads each wired
    Shrine's ``visited`` flag. One base class, two entirely different
    quest types -- polymorphism in NPC clothing.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "Sage Elowen"

    def progress(self):
        visited = sum(1 for shrine in self.targets if shrine.visited)
        return (visited, len(self.targets))

    def quest_text(self):
        return (
            "Three shrines stand cold and unvisited. Greet each one -- "
            "I feel when a shrine is honored. (Quest: visit every shrine.)"
        )

    def reward_text(self):
        return "The shrines glow again. The old paths remember you, warden."


class Shrine(NPC):
    """A visit-quest marker: records that the hero greeted it.

    ``self.visited`` is OWN-OBJECT state -- the engine neither reads nor
    guards it, exactly the honest boundary the Heist Lab teaches. The
    tile flips 🗿 -> ✨ the moment it is honored.
    """

    def __init__(self, x, y):
        super().__init__("Shrine", x, y)
        self.visited = False

    def interact(self, view):
        self.visited = True  # own-object mutation: legal, private, silent
        return SpeakAction("The shrine stirs... a cold light wakes within it.")

    def symbol(self):
        return "✨" if self.visited else "🗿"