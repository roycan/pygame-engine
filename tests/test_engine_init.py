"""T3.1 gate: loud config validation, registration, warning draining."""

import pytest

from engine.base_classes import Hero, Wall
from engine.core import GameEngine
from tests.helpers import ScriptedVillain, build_engine, make_test_hero


def test_unknown_win_condition_raises_with_suggestion():
    with pytest.raises(ValueError, match="defeat_all"):
        GameEngine(win_condition="defeat_al")


def test_goal_mode_requires_goal_pos():
    with pytest.raises(ValueError, match="goal_pos"):
        GameEngine(win_condition="reach_goal")


def test_goal_pos_out_of_bounds_raises():
    with pytest.raises(ValueError, match="outside"):
        GameEngine(win_condition="reach_goal", goal_pos=(15, 2))


def test_wall_on_goal_tile_raises():
    game = GameEngine(win_condition="reach_goal", goal_pos=(9, 9))
    with pytest.raises(ValueError, match="goal"):
        game.add_wall(Wall("Blocker", 9, 9))


def test_clamp_warnings_drained_into_setup_log():
    class Hercules(Hero):
        def __init__(self, x, y):
            super().__init__("Hercules", x, y, hp=9999, attack_power=999)

        def symbol(self):
            return "🦸"

    game = GameEngine()
    game.add_hero(Hercules(1, 1))
    assert any("SETUP WARNING" in line and "max_hp" in line for line in game.logs)
    assert game.hero.warnings == []  # drained, not duplicated


def test_registration_order_defines_turn_order():
    game = build_engine()
    game.add_villain(ScriptedVillain("A", 5, 1))
    game.add_villain(ScriptedVillain("B", 6, 1))
    assert [v.name for v in game.villains] == ["A", "B"]


def test_duplicate_hero_rejected_loudly():
    game = build_engine()
    with pytest.raises(ValueError, match="already has a hero"):
        game.add_hero(make_test_hero(name="SecondHero"))


def test_occupied_tile_rejected_loudly():
    game = build_engine()  # hero at (1,1)
    with pytest.raises(ValueError, match="occupied"):
        game.add_villain(ScriptedVillain("S", 1, 1))


def test_entity_out_of_bounds_rejected_loudly():
    game = build_engine()
    with pytest.raises(ValueError, match="outside"):
        game.add_villain(ScriptedVillain("S", 12, 1))


def test_step_without_hero_is_loud():
    game = GameEngine()
    with pytest.raises(RuntimeError, match="add_hero"):
        game.step("d")
