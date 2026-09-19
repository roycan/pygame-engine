"""T1.2 gate: Character stat clamping (loud), take_damage, is_alive, Wall."""

from engine.base_classes import MAX_ATK, MAX_HP, Character, Wall


def test_hp_clamped_loudly():
    c = Character("Titan", 0, 0, hp=500, attack_power=5)
    assert c.max_hp == MAX_HP == 200
    assert c.hp == 200
    assert c.warnings, "clamping must record a warning"
    assert "max_hp" in c.warnings[0] and "500" in c.warnings[0]


def test_negative_attack_power_clamped_loudly():
    c = Character("Weakling", 0, 0, hp=10, attack_power=-5)
    assert c.attack_power == 0
    assert any("attack_power" in w for w in c.warnings)


def test_in_range_stats_produce_no_warnings():
    c = Character("Balanced", 0, 0, hp=10, attack_power=5)
    assert c.warnings == []


def test_take_damage_returns_actually_applied():
    c = Character("Target", 0, 0, hp=10, attack_power=1)
    assert c.take_damage(4) == 4
    assert c.hp == 6
    assert c.take_damage(-3) == 0  # no healing-through-damage exploit
    assert c.take_damage(100) == 6  # capped at remaining hp
    assert c.hp == 0


def test_is_alive_lifecycle():
    c = Character("Mortal", 0, 0, hp=1, attack_power=0)
    assert c.is_alive()
    c.take_damage(1)
    assert not c.is_alive()


def test_calculate_attack_damage_defaults_to_attack_power():
    c = Character("Fighter", 0, 0, hp=5, attack_power=7)
    assert c.calculate_attack_damage() == 7


def test_position_property():
    assert Wall("W", 2, 3).position == (2, 3)


def test_wall_symbol_is_brick_emoji():
    assert Wall("W", 0, 0).symbol() == "🧱"
