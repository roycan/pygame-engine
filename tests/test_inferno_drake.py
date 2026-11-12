"""Gate: the InfernoDrake two-phase boss mechanics + arena winnability.

The route-level integration (menu card + playable page) lives in
test_arcade_routes.py beside its sample_pair sibling. This file pins
the BOSS CLASS contract: phase trigger at exactly half hp, the one-turn
rage cost, the symbol flip, doubled-but-sanitized damage, ENRAGED log
naming, and a deterministic head-on duel won through the REAL engine.
"""

from engine.actions import AttackAction, MoveAction, WaitAction
from engine.base_classes import MAX_ATK
from engine.view import SafeGameView

from arenas.inferno_drake.game_config import create_game


def test_phase_one_drake_is_a_normal_chaser():
    game = create_game()
    drake = game.villains[0]
    assert drake.phase == 1
    assert drake.name == "Inferno Drake"
    assert drake.symbol() == "🐉"
    assert drake.calculate_attack_damage() == 7


def test_enrage_triggers_at_half_hp_and_costs_one_full_turn():
    game = create_game()
    drake = game.villains[0]
    drake.take_damage(20)  # 40 -> 20 hp: exactly half (max_hp // 2)
    action = drake.act(SafeGameView(game))
    assert isinstance(action, WaitAction)  # the roar: no attack this turn
    assert drake.phase == 2
    assert drake.symbol() == "🔥"
    assert "ENRAGED" in drake.name  # every future log line will say it


def test_no_premature_enrage_above_half_hp():
    game = create_game()
    drake = game.villains[0]
    drake.take_damage(19)  # 40 -> 21 hp: still above half
    action = drake.act(SafeGameView(game))
    assert drake.phase == 1
    assert isinstance(action, MoveAction)  # hero far away: it closes in


def test_phase_two_damage_is_doubled_but_within_engine_bounds():
    game = create_game()
    drake = game.villains[0]
    drake.take_damage(20)
    drake.act(SafeGameView(game))  # spend the rage turn
    assert drake.calculate_attack_damage() == 14  # exactly 2x phase 1
    assert drake.calculate_attack_damage() <= MAX_ATK  # engine still sanitizes


def test_enraged_drake_still_hunts_when_adjacent():
    game = create_game()
    drake = game.villains[0]
    drake.take_damage(20)
    drake.act(SafeGameView(game))  # rage turn spent
    game.hero.x, game.hero.y = 5, 6  # adjacent, west of the drake
    action = drake.act(SafeGameView(game))
    assert isinstance(action, AttackAction)
    assert (action.dx, action.dy) == (-1, 0)  # striking toward the hero


def test_head_on_duel_is_winnable_and_loudly_narrated():
    """Deterministic duel: hero parked beside the drake, trading blows.

    Trace: 3 hero hits (32->24->16) trigger the enrage; the roar turn is
    a free hero hit (16->8); the enraged drake lands ONE 14-dmg hit;
    the 5th hero hit ends it. Explicit-text contract: the log names the
    ENRAGED drake on the roar line AND on the doubled-damage hit line.
    """
    game = create_game()
    game.hero.x, game.hero.y = 5, 6  # west of the drake at (6, 6)

    payload = None
    while not game.game_over:
        payload = game.step("d")  # bump-to-attack eastward every turn
        assert payload["turn"] < 50  # safety: the duel must end

    assert game.won is True
    assert game.hero.is_alive()
    assert game.hero.hp == 32  # 60 - 7 - 7 - 14: phase 2 hurts but is fair
    log_text = "\n".join(game.logs)
    assert "Inferno Drake (ENRAGED! Fire doubled!) waits." in log_text
    assert "hits Sir Ashworth for 14 damage!" in log_text
    assert "🏆 VICTORY!" in log_text
