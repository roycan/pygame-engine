"""T4.2 gate: all three win modes construct and validate loudly."""

import pytest

from engine.core import GameEngine


def test_defeat_all_needs_no_goal():
    game = GameEngine(win_condition="defeat_all")
    assert game.goal_pos is None


def test_reach_goal_mode():
    game = GameEngine(win_condition="reach_goal", goal_pos=(9, 9))
    assert game.win_condition == "reach_goal"
    assert game.goal_pos == (9, 9)


def test_clear_and_reach_mode():
    game = GameEngine(
        win_condition="clear_and_reach_goal", goal_pos=(9, 9)
    )
    assert game.win_condition == "clear_and_reach_goal"


def test_typo_in_win_condition_lists_options():
    with pytest.raises(ValueError) as excinfo:
        GameEngine(win_condition="reach_gl")
    assert "reach_goal" in str(excinfo.value)
