"""T3.5 gate: full turn lifecycle with early exits (scripted doubles)."""

from engine.actions import AttackAction, MoveAction, WaitAction
from tests.helpers import ScriptedVillain, assert_valid_payload, build_engine, make_npc


def test_defeat_all_victory_skips_villain_phase(contract):
    game = build_engine(hero_atk=6)
    villain = ScriptedVillain("Last", 2, 1, hp=10, attack_power=3, script=[WaitAction()])
    game.add_villain(villain)
    first = game.step("d")  # 10 -> 4 hp; villain responds
    assert first["game_over"] is False
    assert villain.acted == 1
    second = game.step("d")  # 4 -> dead -> WIN before the villain phase
    assert second["won"] is True
    assert second["game_over"] is True
    assert villain.acted == 1  # never got to respond on the winning turn
    assert_valid_payload(second, contract)


def test_reach_goal_exit_run_beats_the_villains(contract):
    game = build_engine(win_condition="reach_goal", goal_pos=(3, 1))
    villain = ScriptedVillain("Chaser", 8, 8, script=[MoveAction(-1, 0), MoveAction(-1, 0)])
    game.add_villain(villain)
    first = game.step("d")  # hero (2,1): not the goal yet
    assert first["won"] is False
    assert villain.acted == 1
    second = game.step("d")  # hero (3,1) == goal -> instant win, villain frozen
    assert second["won"] is True
    assert second["game_over"] is True
    assert villain.acted == 1  # the villains never got their turn
    assert_valid_payload(second, contract)


def test_clear_and_reach_two_stage_win_with_retained_corpses():
    game = build_engine(
        win_condition="clear_and_reach_goal", goal_pos=(2, 1), hero_atk=6
    )
    villain = ScriptedVillain("Guard", 2, 1, hp=10, attack_power=3, script=[WaitAction()] * 3)
    game.add_villain(villain)
    game.step("d")  # bump-attack: 10 -> 4 (hero stays at (1,1))
    second = game.step("d")  # lethal; hero NOT at goal -> NO win, corpse retained
    assert second["won"] is False
    assert len(game.villains) == 1 and not game.villains[0].is_alive()
    third = game.step("d")  # hero steps onto the corpse tile == goal: WIN
    assert third["won"] is True
    assert third["game_over"] is True


def test_dialogue_cadence_turn_accounting():
    game = build_engine()
    villain = ScriptedVillain("S", 6, 6, script=[MoveAction(-1, 0)])
    game.add_villain(villain)
    game.add_npc(make_npc(x=2, y=1))
    bump = game.step("d")       # turn 1: dialogue opens, villains frozen
    assert bump["turn"] == 1 and villain.acted == 0
    dismiss = game.step("a")    # turn stays 1: free pause frame
    assert dismiss["turn"] == 1 and villain.acted == 0
    move = game.step("s")       # turn 2: villain finally acts
    assert move["turn"] == 2 and villain.acted == 1


def test_step_after_game_over_returns_payload_without_change():
    game = build_engine(hero_atk=6)
    villain = ScriptedVillain("Last", 2, 1, hp=2, attack_power=1)
    game.add_villain(villain)
    game.step("d")
    frozen = game.step("d")  # game is over
    assert frozen["game_over"] is True
    assert game.turn_count == 1  # no further turn advances
