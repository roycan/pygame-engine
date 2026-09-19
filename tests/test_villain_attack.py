"""T3.4b gate: villain directional attacks + damage sanitization."""

from engine.actions import AttackAction
from engine.base_classes import Wall
from tests.helpers import ScriptedVillain, build_engine


def test_villain_hits_adjacent_hero():
    game = build_engine(hero_hp=25)
    brute = ScriptedVillain("Brute", 2, 1, hp=30, attack_power=4, script=[AttackAction(-1, 0)])
    game.add_villain(brute)
    payload = game.step("space")
    assert game.hero.hp == 21
    assert any(
        e["actor"] == "Brute" and e["action"] == "AttackAction" and e["result"] == "SUCCESS"
        for e in payload["events"]
    )


def test_villain_swinging_at_wall_is_blocked():
    game = build_engine(hero_hp=25)
    game.add_wall(Wall("Rock", 2, 1))  # hero at (1,1); villain at (3,1)
    brute = ScriptedVillain("Brute", 3, 1, hp=30, attack_power=4, script=[AttackAction(-1, 0)])
    game.add_villain(brute)
    payload = game.step("space")
    assert game.hero.hp == 25
    assert any(
        e["actor"] == "Brute" and e["result"] == "BLOCKED" for e in payload["events"]
    )


def test_villain_swinging_at_empty_tile_misses():
    game = build_engine(hero_hp=25)
    brute = ScriptedVillain("Brute", 5, 5, hp=30, attack_power=4, script=[AttackAction(0, -1)])
    game.add_villain(brute)
    payload = game.step("space")
    assert game.hero.hp == 25
    assert any(e["actor"] == "Brute" and e["result"] == "MISSED" for e in payload["events"])


def test_no_friendly_fire_between_villains():
    game = build_engine(hero_hp=25)
    target = ScriptedVillain("Target", 5, 4, hp=10, attack_power=1)
    attacker = ScriptedVillain("Attacker", 5, 5, hp=10, attack_power=4, script=[AttackAction(0, -1)])
    game.add_villain(target)
    game.add_villain(attacker)
    payload = game.step("space")
    assert target.hp == 10  # zero damage: villains never harm each other
    assert any(e["actor"] == "Attacker" and e["result"] == "MISSED" for e in payload["events"])


def test_cheat_guard_caps_overpowered_damage_loudly():
    game = build_engine(hero_hp=25)
    cheater = ScriptedVillain("Cheater", 2, 1, hp=30, attack_power=4, script=[AttackAction(-1, 0)])
    cheater.calculate_attack_damage = lambda: 999  # override: never trusted
    game.add_villain(cheater)
    payload = game.step("space")
    assert game.hero.hp == 0  # 999 sanitized to 40; applied capped at remaining 25
    warnings = [e for e in payload["events"] if e["action"] == "DamageSanitize"]
    assert warnings and "999" in warnings[0]["beginner_text"]


def test_cheat_guard_blocks_negative_damage_heal_exploit():
    game = build_engine(hero_hp=25)
    villain = ScriptedVillain("Healer", 2, 1, hp=30, attack_power=4, script=[AttackAction(-1, 0)])
    villain.calculate_attack_damage = lambda: -50  # attempted heal-by-attack
    game.add_villain(villain)
    payload = game.step("space")
    assert game.hero.hp == 25  # zero applied
    assert any(
        e["action"] == "DamageSanitize" and e["result"] == "WARNING"
        for e in payload["events"]
    )
