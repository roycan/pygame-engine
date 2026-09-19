"""T3.6 gate: event schema + beginner_text quality checks."""

from engine.actions import AttackAction, MoveAction
from engine.base_classes import Wall
from tests.helpers import ScriptedVillain, build_engine


def collect_events(game, keys):
    return [event for key in keys for event in game.step(key)["events"]]


def test_every_event_matches_contract(contract):
    game = build_engine()
    game.add_wall(Wall("Rock", 2, 1))
    game.add_villain(ScriptedVillain("S", 5, 5, script=[MoveAction(-1, 0), AttackAction(-1, 0)]))
    events = collect_events(game, ["d", "a", "d"])
    assert events  # something happened
    for event in events:
        for key in ("beginner_text", "actor", "action", "result", "tile_pos"):
            assert key in event
        assert event["result"] in ("SUCCESS", "BLOCKED", "MISSED", "WARNING", "INFO")


def test_blocked_wall_event_has_both_views():
    game = build_engine()
    game.add_wall(Wall("Rock", 2, 1))
    payload = game.step("d")
    blocked = [e for e in payload["events"] if e["result"] == "BLOCKED"]
    assert blocked
    assert blocked[0]["beginner_text"]  # beginner-friendly line
    assert blocked[0]["tile_pos"] == [2, 1]  # and precise tile data


def test_diagonal_villain_move_emits_warning():
    game = build_engine()
    villain = ScriptedVillain("Wiggle", 5, 5, script=[MoveAction(1, 1)])
    game.add_villain(villain)
    payload = game.step("space")
    warnings = [e for e in payload["events"] if e["result"] == "WARNING"]
    assert warnings and warnings[0]["actor"] == "Wiggle"
    assert warnings[0]["tile_pos"] == [5, 5]


def test_events_also_appended_to_running_log():
    game = build_engine()
    before = len(game.logs)
    game.step("d")
    assert len(game.logs) == before + len(game.events)
