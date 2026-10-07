"""Arcade gate: /games menu, /play/<slug>, and (sid, arena) sessions.

Discovery mechanics live in test_discovery.py (pure, tmp_path-based).
This file exercises the ROUTES: the fail-soft menu, arena selection,
session isolation, and one integration test over the REAL shipped
example arena (the true import path a student PR will take).
"""

import pytest

import app as app_module
from app import GAMES, app

GOOD_CONFIG = '''
from engine.base_classes import Hero
from engine.core import GameEngine


class RouteHero(Hero):
    def __init__(self, x, y):
        super().__init__("Route Hero", x, y, hp=30, attack_power=5)

    def symbol(self):
        return "🧪"


def create_game():
    game = GameEngine(width=6, height=6, win_condition="defeat_all")
    game.add_hero(RouteHero(x=1, y=1))
    return game
'''

BROKEN_CONFIG = "def create_game(:\n    pass\n"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    GAMES.clear()
    with app.test_client() as test_client:
        yield test_client
    GAMES.clear()


@pytest.fixture
def arenas_dir(tmp_path, monkeypatch):
    good = tmp_path / "good_pair"
    good.mkdir()
    (good / "game_config.py").write_text(
        'TITLE = "Good Pair Arena"\n' + GOOD_CONFIG, encoding="utf-8"
    )
    broken = tmp_path / "broken_pair"
    broken.mkdir()
    (broken / "game_config.py").write_text(BROKEN_CONFIG, encoding="utf-8")
    monkeypatch.setattr(app_module, "ARENAS_BASE", tmp_path)
    return tmp_path


def test_games_lists_the_starter_and_healthy_arenas(client, arenas_dir):
    page = client.get("/games")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    assert "Class Arcade" in html
    assert "Good Pair Arena" in html
    assert 'href="/play/good_pair"' in html
    assert 'href="/"' in html  # the starter card


def test_broken_arena_renders_a_needs_fixing_card(client, arenas_dir):
    html = client.get("/games").data.decode("utf-8")
    assert "Needs fixing" in html
    assert "SyntaxError" in html  # the teaching artifact: the error is shown
    assert 'href="/play/broken_pair"' not in html  # unplayable: no link


def test_menu_survives_even_when_every_arena_is_broken(client, arenas_dir):
    """THE fail-soft headline: one bad merge must never 500 the menu."""
    (arenas_dir / "good_pair" / "game_config.py").write_text(
        BROKEN_CONFIG, encoding="utf-8"
    )
    assert client.get("/games").status_code == 200


def test_play_serves_the_arena_game_with_first_paint_payload(client, arenas_dir):
    page = client.get("/play/good_pair")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    assert "__INITIAL_STATE__" in html
    assert "Route Hero" in html  # THIS arena's hero is embedded on load
    assert "Good Pair Arena" in html  # the card title names the page


def test_play_unknown_slug_is_404(client, arenas_dir):
    assert client.get("/play/ghost_pair").status_code == 404


def test_play_broken_slug_shows_needs_fixing_page_not_500(client, arenas_dir):
    page = client.get("/play/broken_pair")
    assert page.status_code == 200
    assert "needs fixing" in page.data.decode("utf-8").lower()
    # Crucially, the broken arena is NOT selected into the session:
    payload = client.post("/api/step", json={"key": "zzz"}).get_json()
    assert payload["board_state"]["hero"]["name"] == "Sir Ada"  # starter


def test_arena_sessions_are_isolated_per_browser(client, arenas_dir):
    """One browser's arena choice must never leak into another's game."""
    client.get("/play/good_pair")
    other = app.test_client()
    mine = client.post("/api/step", json={"key": "space"}).get_json()
    theirs = other.post("/api/step", json={"key": "space"}).get_json()
    assert mine["board_state"]["hero"]["name"] == "Route Hero"
    assert mine["turn"] == 1  # the arena game advanced...
    assert theirs["board_state"]["hero"]["name"] == "Sir Ada"
    assert theirs["turn"] == 1  # ...a separate starter game did too


def test_slash_always_returns_to_the_starter(client, arenas_dir):
    client.get("/play/good_pair")
    client.get("/")  # clears the arena choice -- / is the starter game
    payload = client.post("/api/step", json={"key": "zzz"}).get_json()
    assert payload["board_state"]["hero"]["name"] == "Sir Ada"


def test_step_and_reset_are_arena_aware_and_double_reset_is_safe(client, arenas_dir):
    client.get("/play/good_pair")
    first = client.post("/api/step", json={"key": "space"}).get_json()
    assert first["turn"] == 1  # a real (wait) turn advances the arena game
    again = client.post("/api/reset").get_json()
    once_more = client.post("/api/reset").get_json()
    assert again["turn"] == 0 and once_more["turn"] == 0  # idempotent
    assert again["board_state"]["hero"]["name"] == "Route Hero"


def test_sample_pair_example_is_discoverable_and_playable(client):
    """Integration over the REAL arenas/ folder: the shipped worked
    example must appear on the menu and actually play."""
    html = client.get("/games").data.decode("utf-8")
    assert "Sample Pair" in html
    page = client.get("/play/sample_pair")
    assert page.status_code == 200
    assert b"Sir Rosita" in page.data
