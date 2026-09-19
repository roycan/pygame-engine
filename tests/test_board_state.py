"""T3.2 gate: board_state builder + payload contract + retained corpses."""

from tests.helpers import ScriptedVillain, assert_valid_payload, build_engine


def test_initial_payload_matches_contract(contract):
    game = build_engine()
    game.add_villain(ScriptedVillain("S", 5, 5))
    assert_valid_payload(game.payload(), contract)


def test_dead_villains_hidden_from_board_but_retained_in_engine():
    game = build_engine(hero_atk=6)
    villain = ScriptedVillain("Squishy", 2, 1, hp=2, attack_power=1)
    game.add_villain(villain)
    payload = game.step("d")  # hero strikes: 2 hp vs 6 damage -> dead
    assert payload["board_state"]["villains"] == []
    assert len(game.villains) == 1  # RETAINED, never purged
    assert not game.villains[0].is_alive()


def test_goal_locked_only_in_clear_and_reach_with_living_villains():
    game = build_engine(
        win_condition="clear_and_reach_goal", goal_pos=(9, 9), hero_atk=6
    )
    villain = ScriptedVillain("S", 2, 1, hp=2, attack_power=1)
    game.add_villain(villain)
    assert game.payload()["goal_locked"] is True
    game.step("d")  # villain dies; hero not at goal -> no win, corpse retained
    assert game.payload()["goal_locked"] is False


def test_goal_pos_exposed_as_list():
    game = build_engine(win_condition="reach_goal", goal_pos=(9, 9))
    assert game.payload()["goal_pos"] == [9, 9]
    assert build_engine().payload()["goal_pos"] is None
