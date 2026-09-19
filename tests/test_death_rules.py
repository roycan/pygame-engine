"""T3.4c gate: Dead-Actor skip (once) + hero death aborts remaining villains."""

from engine.actions import AttackAction, MoveAction, WaitAction
from tests.helpers import ScriptedVillain, build_engine


def make_two_villain_game():
    """Squishy dies instantly; Bystander keeps the game alive so the
    villain phase (and the corpse-skip logging) actually runs."""
    game = build_engine(hero_atk=6)
    villain = ScriptedVillain("Squishy", 2, 1, hp=2, attack_power=1, script=[WaitAction()])
    bystander = ScriptedVillain("Bystander", 8, 8, hp=10, attack_power=1, script=[WaitAction()] * 3)
    game.add_villain(villain)
    game.add_villain(bystander)
    return game, villain


def test_dead_actor_skipped_with_log_exactly_once():
    game, villain = make_two_villain_game()
    game.step("d")  # kill Squishy this turn
    second = game.step("d")  # hero walks onto the vacated tile
    assert not villain.is_alive()
    assert game.hero.position == (2, 1)
    skip_events = [e for e in second["events"] if e["action"] == "SkipTurn"]
    assert skip_events == []  # logged once on the first skip, not every turn


def test_first_skip_after_kill_is_logged():
    game, villain = make_two_villain_game()
    payload = game.step("d")
    assert not villain.is_alive()
    skip_events = [e for e in payload["events"] if e["action"] == "SkipTurn"]
    assert len(skip_events) == 1
    assert "defeated" in skip_events[0]["beginner_text"]
    assert skip_events[0]["actor"] == "Squishy"


def test_hero_death_aborts_remaining_villains():
    game = build_engine(hero_hp=5)
    brute = ScriptedVillain("Brute", 2, 1, hp=30, attack_power=40, script=[AttackAction(-1, 0)])
    crawler = ScriptedVillain("Crawler", 5, 5, hp=30, attack_power=1, script=[MoveAction(-1, 0)])
    game.add_villain(brute)
    game.add_villain(crawler)
    payload = game.step("space")  # hero waits; Brute lands a lethal 40
    assert payload["game_over"] is True
    assert payload["won"] is False
    assert not game.hero.is_alive()
    assert crawler.acted == 0  # registered after Brute: aborted
    assert crawler.position == (5, 5)
    assert any(e["action"] == "HeroDefeated" for e in payload["events"])


def test_retained_corpses_never_purged():
    game = build_engine(hero_atk=6)
    villain = ScriptedVillain("Squishy", 2, 1, hp=2, attack_power=1)
    game.add_villain(villain)
    game.step("d")
    game.step("space")  # a later turn: cleanup must NOT purge the corpse
    assert len(game.villains) == 1
    assert game.villains[0] is villain
