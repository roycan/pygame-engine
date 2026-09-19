"""T4.4 gate: the demo dungeon boots, is coherent, and its AIs behave."""

from demos.demo_dungeon.game_config import create_game
from tests.helpers import assert_valid_payload


def test_demo_boots_with_clear_and_reach_goal(contract):
    game = create_game()
    assert game.win_condition == "clear_and_reach_goal"
    assert game.goal_pos == (9, 9)
    assert len(game.villains) == 3
    assert len(game.npcs) == 1
    assert_valid_payload(game.payload(), contract)


def test_demo_entities_are_distinct_strategies():
    game = create_game()
    names = [type(v).__name__ for v in game.villains]
    assert names == ["Chaser", "Coward", "Patroller"]


def test_chaser_and_coward_close_distance_over_ten_turns():
    game = create_game()
    chaser, coward = game.villains[0], game.villains[1]
    hero = game.hero

    def manhattan(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    start_chaser, start_coward = manhattan(chaser, hero), manhattan(coward, hero)
    for _ in range(10):
        game.step("space")
    end_chaser, end_coward = manhattan(chaser, hero), manhattan(coward, hero)
    assert end_chaser < start_chaser, "the Chaser must close in"
    assert end_coward < start_coward, "the healthy Coward approaches too"


def test_demo_survives_a_full_ten_turn_scripted_run(contract):
    game = create_game()
    for _ in range(10):
        payload = game.step("space")
        assert_valid_payload(payload, contract)
    assert payload["turn"] == 10
