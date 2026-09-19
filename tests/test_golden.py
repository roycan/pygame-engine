"""T7.1 gate: five golden end-to-end scenarios. The FINAL arbiter.

Each scenario plays a complete scripted game through the public
``step()`` API and asserts the full turn-JSON behavior.
"""

from engine.actions import AttackAction, MoveAction, WaitAction
from tests.helpers import (
    ScriptedVillain,
    assert_valid_payload,
    build_engine,
    make_npc,
)


def test_golden_1_arena_defeat_all(contract):
    game = build_engine(hero_atk=6)
    villain = ScriptedVillain(
        "Slime", 2, 1, hp=10, attack_power=3, script=[WaitAction(), WaitAction()]
    )
    game.add_villain(villain)

    first = game.step("d")  # strike: 10 -> 4 hp
    assert_valid_payload(first, contract)
    assert first["game_over"] is False
    assert villain.acted == 1  # villains respond to non-winning turns

    second = game.step("d")  # lethal: win fires BEFORE the villain phase
    assert second["won"] is True
    assert second["game_over"] is True
    assert villain.acted == 1
    assert any(e["action"] == "WinCheck" for e in second["events"])


def test_golden_2_maze_reach_goal(contract):
    game = build_engine(win_condition="reach_goal", goal_pos=(3, 1))
    villain = ScriptedVillain(
        "Chaser", 8, 8, script=[MoveAction(-1, 0), MoveAction(-1, 0)]
    )
    game.add_villain(villain)

    first = game.step("d")  # (2,1): not the goal yet
    assert first["won"] is False

    second = game.step("d")  # (3,1) == goal: exit-run win, villain frozen
    assert second["won"] is True
    assert second["board_state"]["hero"]["position" if False else "x"] == 3
    assert villain.acted == 1
    assert_valid_payload(second, contract)


def test_golden_3_clear_and_reach_two_stage_win():
    game = build_engine(
        win_condition="clear_and_reach_goal", goal_pos=(2, 1), hero_atk=6
    )
    villain = ScriptedVillain(
        "Guard", 2, 1, hp=10, attack_power=3, script=[WaitAction()] * 3
    )
    game.add_villain(villain)

    game.step("d")  # bump-attack: 10 -> 4 (hero stays at (1,1))
    second = game.step("d")  # dead, but hero is not at the goal: NO win
    assert second["won"] is False
    assert len(game.villains) == 1 and not game.villains[0].is_alive()
    skip_events = [e for e in second["events"] if e["action"] == "SkipTurn"]
    assert len(skip_events) == 1  # corpse logged exactly once

    third = game.step("d")  # goal reached; retained corpses count as cleared
    assert third["won"] is True
    assert third["game_over"] is True
    assert all(e["action"] != "SkipTurn" for e in third["events"])  # logged once ever


def test_golden_4_hero_death_aborts_villain_phase():
    game = build_engine(hero_hp=5)
    brute = ScriptedVillain(
        "Brute", 2, 1, hp=30, attack_power=40, script=[AttackAction(-1, 0)]
    )
    crawler = ScriptedVillain(
        "Crawler", 5, 5, hp=30, attack_power=1, script=[MoveAction(-1, 0)]
    )
    game.add_villain(brute)
    game.add_villain(crawler)

    payload = game.step("space")  # hero waits; Brute lands a lethal 40
    assert payload["game_over"] is True
    assert payload["won"] is False
    assert crawler.acted == 0  # registered after Brute: aborted mid-phase
    assert any(e["action"] == "HeroDefeated" for e in payload["events"])

    frozen = game.step("d")  # input after death changes nothing
    assert frozen["game_over"] is True
    assert game.turn_count == 1


def test_golden_5_dialogue_freeze_and_cadence():
    game = build_engine()
    villain = ScriptedVillain(
        "Slime", 6, 6, hp=10, attack_power=3, script=[MoveAction(-1, 0)]
    )
    game.add_villain(villain)
    game.add_npc(make_npc(x=2, y=1, message="Beware the walls."))

    bump = game.step("d")  # turn 1: dialogue opens, villains frozen
    assert bump["active_dialogue"] == "Beware the walls."
    assert bump["turn"] == 1
    assert villain.acted == 0 and villain.position == (6, 6)

    dismiss = game.step("a")  # any key: free pause, no turn, no villains
    assert dismiss["active_dialogue"] is None
    assert dismiss["turn"] == 1
    assert villain.acted == 0

    move = game.step("s")  # turn 2: the world resumes
    assert move["turn"] == 2
    assert villain.acted == 1 and villain.position == (5, 6)
