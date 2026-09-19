"""T4.1/T4.2 gate: the student starter files must be healthy out of the box."""

from engine.core import GameEngine
from student_starter.game_config import create_game

from check_my_class import inspect_classes


def test_checker_reports_zero_failures_for_starter():
    findings = inspect_classes("student_starter.classes")
    failures = [f for f in findings if f.level == "FAIL"]
    assert failures == [], f"starter classes failed the checker: {failures}"


def test_create_game_returns_ready_engine():
    game = create_game()
    assert isinstance(game, GameEngine)
    assert game.hero is not None
    assert game.win_condition == "defeat_all"
    assert game.width == 10 and game.height == 10
    assert len(game.villains) >= 1
    assert len(game.npcs) >= 1
    assert len(game.walls) >= 1


def test_starter_placements_are_inside_board():
    game = create_game()
    for entity in [game.hero, *game.villains, *game.npcs, *game.walls]:
        assert 0 <= entity.x < 10
        assert 0 <= entity.y < 10


def test_starter_smoke_play():
    game = create_game()
    payload = game.step("d")  # one real turn against the real Slime AI
    assert payload["turn"] == 1
    assert payload["board_state"]["hero"]["x"] == 2
