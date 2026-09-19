"""T3.4a gate: villain movement + reserved_tiles contention + blocks."""

from engine.actions import MoveAction
from engine.base_classes import Wall
from tests.helpers import ScriptedVillain, build_engine


def test_villain_move_success():
    game = build_engine()
    villain = ScriptedVillain("Wanderer", 5, 5, script=[MoveAction(0, -1)])
    game.add_villain(villain)
    payload = game.step("space")
    assert villain.position == (5, 4)
    assert any(
        e["actor"] == "Wanderer" and e["result"] == "SUCCESS"
        for e in payload["events"]
    )


def test_tile_contention_first_registration_wins():
    game = build_engine()
    first = ScriptedVillain("First", 3, 1, script=[MoveAction(1, 0)])   # -> (4,1)
    second = ScriptedVillain("Second", 4, 2, script=[MoveAction(0, -1)])  # wants (4,1)
    game.add_villain(first)
    game.add_villain(second)
    payload = game.step("space")
    assert first.position == (4, 1)  # claimed the tile
    assert second.position == (4, 2)  # blocked at origin
    blocked_events = [
        e
        for e in payload["events"]
        if e["actor"] == "Second" and e["result"] == "BLOCKED"
    ]
    assert blocked_events and "claimed" in blocked_events[0]["beginner_text"]


def test_villain_blocked_by_wall():
    game = build_engine()
    game.add_wall(Wall("Rock", 5, 4))
    villain = ScriptedVillain("Wanderer", 5, 5, script=[MoveAction(0, -1)])
    game.add_villain(villain)
    payload = game.step("space")
    assert villain.position == (5, 5)
    assert any(e["actor"] == "Wanderer" and e["result"] == "BLOCKED" for e in payload["events"])


def test_villain_cannot_walk_onto_hero():
    game = build_engine()
    villain = ScriptedVillain("Pushy", 2, 1, script=[MoveAction(-1, 0)])
    game.add_villain(villain)
    payload = game.step("space")
    assert villain.position == (2, 1)  # hero at (1,1) blocks; must AttackAction
    assert any(
        e["actor"] == "Pushy" and e["result"] == "BLOCKED"
        for e in payload["events"]
    )


def test_diagonal_move_rejected_as_warning_wait():
    game = build_engine()
    villain = ScriptedVillain("Wiggle", 5, 5, script=[MoveAction(1, 1)])
    game.add_villain(villain)
    payload = game.step("space")
    assert villain.position == (5, 5)
    warnings = [e for e in payload["events"] if e["result"] == "WARNING"]
    assert warnings and warnings[0]["actor"] == "Wiggle"


def test_non_action_return_treated_as_wait_with_warning():
    game = build_engine()
    villain = ScriptedVillain("Confused", 5, 5)
    villain.act = lambda view: "attack!"  # not an Action at all
    game.add_villain(villain)
    payload = game.step("space")
    assert villain.position == (5, 5)
    assert any(e["result"] == "WARNING" for e in payload["events"])
