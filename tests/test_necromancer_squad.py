"""Gate: the Necromancer squad mechanics + arena winnability.

The route-level integration (menu card + playable page) lives in
test_arcade_routes.py beside its siblings. This file pins the SQUAD
contract: dormancy, the every-third-chant wave schedule (one rise per
chant, narrated by the boss's renamed log line), structural squad cap,
vengeance rise on the master's death, risen hunting behavior, the
boss's stationary-harmless nature, and a real-engine engagement.
"""

from engine.actions import AttackAction, MoveAction, WaitAction
from engine.view import SafeGameView

from arenas.necromancer_squad.game_config import create_game


def fresh():
    game = create_game()
    necromancer = game.villains[0]
    piles = game.villains[1:]
    return game, necromancer, piles


def test_squad_is_wired_by_composition():
    _, necromancer, piles = fresh()
    assert len(necromancer.squad) == 4  # the boss HOLDS its children
    assert necromancer.squad == piles  # same objects, registered after it
    for pile in piles:
        assert pile.master is necromancer  # ...and they hold it back


def test_dormant_graves_wait_and_can_be_smashed():
    game, _, piles = fresh()
    view = SafeGameView(game)
    for pile in piles:
        assert pile.awake is False
        assert pile.symbol() == "🦴"
        assert isinstance(pile.act(view), WaitAction)  # graves hold still
    pile = piles[0]
    start = pile.position
    pile.take_damage(7)  # one blow: not enough
    assert pile.is_alive()
    pile.take_damage(7)  # second blow: 8 hp gone
    assert not pile.is_alive()  # smashed before it ever woke


def test_wave_one_fires_exactly_on_the_third_chant():
    game, necromancer, piles = fresh()
    view = SafeGameView(game)
    assert isinstance(necromancer.act(view), WaitAction)  # chant 1: nothing
    assert necromancer.name == "Necromancer"
    necromancer.act(view)  # chant 2: nothing
    assert all(not pile.awake for pile in piles)
    necromancer.act(view)  # chant 3: the first grave opens
    risen = [pile for pile in piles if pile.awake]
    assert len(risen) == 1
    assert risen[0].name == "Risen Skeleton I"
    assert risen[0].symbol() == "💀"
    # explicit narration: the boss renamed itself for this turn's log
    assert necromancer.name == "Necromancer (chanting! Bone Pile I rises!)"


def test_waves_stagger_one_rise_per_chant_until_the_cap():
    game = create_game()
    view = SafeGameView(game)
    necromancer = game.villains[0]
    piles = game.villains[1:]
    for chant in range(1, 13):
        necromancer.act(view)
        expected = min(chant // 3, 4)  # waves land ON chants 3, 6, 9, 12
        assert sum(pile.awake for pile in piles) == expected
    # chant 12 WAS a wave turn: the wave-IV narration legitimately persists
    assert necromancer.name == "Necromancer (chanting! Bone Pile IV rises!)"
    necromancer.act(view)  # chant 13: squad full, no more narrating
    assert necromancer.name == "Necromancer"


def test_master_death_triggers_the_vengeance_rise():
    game, necromancer, piles = fresh()
    view = SafeGameView(game)
    necromancer.take_damage(40)  # the warden rushes the boss down
    assert not necromancer.is_alive()
    for pile in piles:
        pile.act(view)  # each grave SEES its master has fallen
        assert pile.awake is True
        assert pile.symbol() == "💀"


def test_risen_skeletons_hunt_but_dormant_ones_do_not():
    game, _, piles = fresh()
    game.hero.x, game.hero.y = 5, 1  # adjacent (north of) pile I at (5, 2)
    view = SafeGameView(game)  # a view is a SNAPSHOT: build it AFTER moving
    assert isinstance(piles[0].act(view), WaitAction)  # still dormant
    piles[0].rise()
    action = piles[0].act(view)
    assert isinstance(action, AttackAction)
    assert (action.dx, action.dy) == (0, -1)  # striking north at the hero
    game.hero.x, game.hero.y = 1, 8  # far away again
    far_view = SafeGameView(game)  # fresh snapshot for the new position
    assert isinstance(piles[0].act(far_view), MoveAction)


def test_the_necromancer_is_stationary_and_harmless():
    game, necromancer, _ = fresh()
    view = SafeGameView(game)
    start = necromancer.position
    for _ in range(6):
        assert isinstance(necromancer.act(view), WaitAction)
        assert necromancer.position == start  # it never leaves the back
        assert necromancer.attack_power == 0  # its damage is delegated


def test_real_engine_waves_narrate_and_act_same_tick():
    game = create_game()
    p1 = game.step("space")
    p2 = game.step("space")
    p3 = game.step("space")  # chant 3: rise + same-tick lurch
    for payload, risen in ((p1, 0), (p2, 0), (p3, 1)):
        symbols = [v["symbol"] for v in payload["board_state"]["villains"]]
        assert symbols.count("💀") == risen
        assert symbols.count("🦴") == 4 - risen
    necro_entry = next(
        v for v in p3["board_state"]["villains"] if "Necromancer" in v["name"]
    )
    assert necro_entry["name"] == "Necromancer (chanting! Bone Pile I rises!)"
    risen = next(
        v for v in p3["board_state"]["villains"] if v["name"] == "Risen Skeleton I"
    )
    assert (risen["x"], risen["y"]) != (5, 2)  # it acted the tick it rose
    p4 = game.step("space")
    p5 = game.step("space")
    p6 = game.step("space")  # chant 6: wave two
    symbols = [v["symbol"] for v in p6["board_state"]["villains"]]
    assert symbols.count("💀") == 2
    assert any("Risen Skeleton II" == v["name"] for v in p6["board_state"]["villains"])


def test_vengeance_mass_rise_through_the_real_engine():
    game = create_game()
    necromancer = game.villains[0]
    necromancer.take_damage(40)  # the warden rushes the boss down
    payload = game.step("space")  # villain phase: graves SEE the fall
    symbols = [v["symbol"] for v in payload["board_state"]["villains"]]
    assert symbols.count("💀") == 4  # every grave rose at once
    assert symbols.count("🦴") == 0
