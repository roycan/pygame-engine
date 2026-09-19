"""T3.3 gate: hero input resolution -- move / blocked / bump-attack /
bump-talk / space wait / unknown key / dialogue pause frame."""

from engine.actions import MoveAction, WaitAction
from tests.helpers import ScriptedVillain, build_engine, make_npc


def test_cardinal_move_success():
    game = build_engine()
    payload = game.step("d")
    assert game.hero.position == (2, 1)
    assert payload["turn"] == 1
    assert any(
        e["action"] == "MoveAction" and e["result"] == "SUCCESS"
        for e in payload["events"]
    )


def test_wall_bump_blocked_and_costs_no_turn():
    game = build_engine()
    from engine.base_classes import Wall

    game.add_wall(Wall("Rock", 2, 1))
    payload = game.step("d")
    assert game.hero.position == (1, 1)
    assert payload["turn"] == 0  # no turn spent
    assert any(e["result"] == "BLOCKED" for e in payload["events"])


def test_out_of_bounds_bump_blocked():
    game = build_engine()
    payload = game.step("a")  # hero at x=1 -> (0,1) valid; step w: (1,0) valid...
    game.step("a")  # now at (0,1)
    payload = game.step("a")  # target (-1,1): out of bounds
    assert game.hero.position == (0, 1)
    assert any(e["result"] == "BLOCKED" for e in payload["events"])


def test_bump_to_attack():
    game = build_engine(hero_atk=6)
    villain = ScriptedVillain("Slime", 2, 1, hp=10, attack_power=3, script=[WaitAction()])
    game.add_villain(villain)
    payload = game.step("d")
    assert villain.hp == 4  # 10 - 6
    assert game.hero.position == (1, 1)  # hero stays put
    assert payload["turn"] == 1
    assert villain.acted == 1  # villains still respond to an attack turn
    assert any(
        e["action"] == "AttackAction" and e["result"] == "SUCCESS"
        for e in payload["events"]
    )


def test_bump_to_talk_freezes_villains():
    game = build_engine()
    villain = ScriptedVillain("Slime", 6, 6, script=[MoveAction(-1, 0)])
    game.add_villain(villain)
    game.add_npc(make_npc(x=2, y=1, message="Beware the walls."))
    payload = game.step("d")
    assert payload["active_dialogue"] == "Beware the walls."
    assert payload["turn"] == 1  # the bump consumed the turn...
    assert villain.acted == 0  # ...but villains were frozen
    assert villain.position == (6, 6)


def test_dialogue_dismissal_is_a_free_pause():
    game = build_engine()
    villain = ScriptedVillain("Slime", 6, 6, script=[MoveAction(-1, 0)])
    game.add_villain(villain)
    game.add_npc(make_npc(x=2, y=1))
    game.step("d")  # open dialogue
    payload = game.step("a")  # any key dismisses
    assert payload["active_dialogue"] is None
    assert payload["turn"] == 1  # no turn advanced
    assert villain.acted == 0  # villains frozen during dismissal too


def test_space_waits_and_lets_villains_act():
    game = build_engine()
    villain = ScriptedVillain("Slime", 6, 6, script=[MoveAction(-1, 0)])
    game.add_villain(villain)
    payload = game.step("space")
    assert payload["turn"] == 1
    assert villain.acted == 1
    assert villain.position == (5, 6)


def test_unknown_key_is_ignored_without_turn():
    game = build_engine()
    payload = game.step("x")
    assert payload["turn"] == 0
    assert any(e["result"] == "INFO" for e in payload["events"])


def test_game_over_freezes_input():
    game = build_engine()
    game.game_over = True
    payload = game.step("d")
    assert game.hero.position == (1, 1)  # nothing moved
