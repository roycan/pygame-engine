"""Shared test helpers: engine builders + deterministic villain doubles.

ScriptedVillain pops pre-decided Actions from a list, so scenario tests
are 100% deterministic no matter what the real AI would do.
"""

from engine.actions import SpeakAction, WaitAction
from engine.base_classes import Hero, NPC, Villain
from engine.core import GameEngine


class ScriptedVillain(Villain):
    """A villain that plays from a script and counts its turns."""

    def __init__(self, name, x, y, hp=10, attack_power=3, script=None):
        super().__init__(name, x, y, hp, attack_power)
        self.script = list(script or [])
        self.acted = 0

    def act(self, view):
        self.acted += 1
        if self.script:
            return self.script.pop(0)
        return WaitAction()

    def symbol(self):
        return "👾"


def make_test_hero(x=1, y=1, hp=25, attack_power=6, name="TestHero"):
    """A concrete Hero with tunable stats."""

    class _TestHero(Hero):
        def __init__(self, px, py):
            super().__init__(name, px, py, hp=hp, attack_power=attack_power)

        def symbol(self):
            return "🦸"

    return _TestHero(x, y)


def make_npc(name="Elder", x=2, y=1, message="Hello, traveler!"):
    """A concrete NPC with a fixed line of dialogue."""

    class _TestNPC(NPC):
        def __init__(self, px, py):
            super().__init__(name, px, py)

        def interact(self, view):
            return SpeakAction(message)

        def symbol(self):
            return "🧙"

    return _TestNPC(x, y)


def build_engine(
    win_condition="defeat_all",
    goal_pos=None,
    hero_pos=(1, 1),
    hero_hp=25,
    hero_atk=6,
) -> GameEngine:
    """A minimal valid game: hero at hero_pos, no walls/npcs/villains."""
    game = GameEngine(win_condition=win_condition, goal_pos=goal_pos)
    game.add_hero(make_test_hero(x=hero_pos[0], y=hero_pos[1], hp=hero_hp, attack_power=hero_atk))
    return game


def assert_valid_payload(payload, contract):
    """Validate a turn payload against the frozen contract fixture."""
    for key in contract["required_payload_keys"]:
        assert key in payload, f"payload missing required key {key!r}"
    bs = payload["board_state"]
    for key in contract["required_board_state_keys"]:
        assert key in bs, f"board_state missing required key {key!r}"
    for key in contract["required_hero_keys"]:
        assert key in bs["hero"], f"hero missing required key {key!r}"
    for villain in bs["villains"]:
        for key in contract["required_villain_keys"]:
            assert key in villain, f"villain missing required key {key!r}"
    for npc in bs["npcs"]:
        for key in contract["required_npc_keys"]:
            assert key in npc, f"npc missing required key {key!r}"
    for wall in bs["walls"]:
        for key in contract["required_wall_keys"]:
            assert key in wall, f"wall missing required key {key!r}"
    for event in payload["events"]:
        for key in contract["required_event_keys"]:
            assert key in event, f"event missing required key {key!r}"
        assert (
            event["result"] in contract["allowed_event_results"]
        ), f"event result {event['result']!r} not allowed"
