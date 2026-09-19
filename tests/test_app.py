"""T5.1 gate: Flask routes, session isolation, reset, env-based config."""

import pytest

from app import GAMES, app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    GAMES.clear()
    with app.test_client() as test_client:
        yield test_client
    GAMES.clear()


def test_index_serves_the_interface(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'id="board"' in response.data
    assert b"game.js" in response.data
    assert b"inspector-toggle" in response.data


def test_index_embeds_initial_state_for_first_paint(client):
    """Regression: the board must render on page load, before any keypress."""
    response = client.get("/")
    assert b"__INITIAL_STATE__" in response.data
    assert b"board_state" in response.data
    assert b'"Sir Ada"' in response.data  # the starter hero is embedded


def test_step_returns_full_contract_payload(client, contract):
    payload = client.post("/api/step", json={"key": "d"}).get_json()
    for key in contract["required_payload_keys"]:
        assert key in payload


def test_step_advances_and_moves(client):
    client.post("/api/step", json={"key": "d"})
    state = client.post("/api/step", json={"key": "a"}).get_json()
    assert state["board_state"]["hero"]["x"] == 1  # right, then back
    assert state["turn"] == 2


def test_reset_reinstantiates_the_game(client):
    client.post("/api/step", json={"key": "d"})
    fresh = client.post("/api/reset").get_json()
    assert fresh["turn"] == 0
    assert fresh["board_state"]["hero"]["x"] == 1


def test_browser_sessions_have_independent_games():
    GAMES.clear()
    with app.test_client() as first:
        with app.test_client() as second:
            first.post("/api/step", json={"key": "d"})
            p1 = first.post("/api/step", json={"key": "s"}).get_json()
            p2 = second.post("/api/step", json={"key": "s"}).get_json()
            assert p1["turn"] == 2
            assert p2["turn"] == 1  # second browser has its own game
    GAMES.clear()


def test_game_config_module_env_switch(monkeypatch, client):
    monkeypatch.setenv("GAME_CONFIG_MODULE", "demos.demo_dungeon.game_config")
    GAMES.clear()
    payload = client.post("/api/step", json={"key": "zzz"}).get_json()  # no-op probe
    assert payload["win_condition"] == "clear_and_reach_goal"
    assert payload["goal_pos"] == [9, 9]
    GAMES.clear()


def test_missing_key_is_handled_gracefully(client):
    payload = client.post("/api/step", json={}).get_json()
    assert "turn" in payload  # unknown key -> INFO event, no crash
