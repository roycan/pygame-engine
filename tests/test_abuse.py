"""Abuse gate: empty inputs, malformed payloads, step storms, resets.

The Flask equivalent of "forms handle empty inputs and double submits":
/api/step is the only input surface, so we attack it from every angle --
in starter AND arena contexts -- and demand a well-formed contract
payload (never a 500) every single time.
"""

import pytest

from app import GAMES, app

PROBES = [
    {},                        # empty body
    {"key": ""},               # empty key
    {"key": None},             # null key
    {"key": "🚀"},             # unicode nonsense
    {"key": "wd"},             # multi-char garbage
    {"turn": 999, "hp": -1},   # fields the API must ignore
]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    GAMES.clear()
    with app.test_client() as test_client:
        yield test_client
    GAMES.clear()


def _assert_contract(payload, contract):
    for key in contract["required_payload_keys"]:
        assert key in payload


def test_step_probes_never_crash_the_starter(client, contract):
    for probe in PROBES:
        _assert_contract(client.post("/api/step", json=probe).get_json(), contract)


def test_malformed_json_body_is_handled(client, contract):
    response = client.post("/api/step", data="{not json", content_type="application/json")
    assert response.status_code == 200
    _assert_contract(response.get_json(), contract)


def test_step_probes_never_crash_an_arena_session(client, contract):
    client.get("/play/sample_pair")
    for probe in PROBES:
        payload = client.post("/api/step", json=probe).get_json()
        _assert_contract(payload, contract)
        assert payload["board_state"]["hero"]["name"] == "Sir Rosita"


def test_step_storm_keeps_the_engine_consistent(client):
    """Ten waits in a row: every one is a real turn (waits are always
    in-bounds, so this isolates turn accounting from board edges)."""
    turns = [
        client.post("/api/step", json={"key": "space"}).get_json()["turn"]
        for _ in range(10)
    ]
    assert turns == list(range(1, 11))
    assert client.post("/api/reset").get_json()["turn"] == 0


def test_reset_between_steps_is_always_safe(client):
    client.post("/api/step", json={"key": "d"})
    fresh = client.post("/api/reset").get_json()
    assert fresh["turn"] == 0
    moved = client.post("/api/step", json={"key": "s"}).get_json()
    assert moved["turn"] == 1
    assert moved["board_state"]["hero"]["x"] == 1  # reset restored the start tile


def test_gets_never_mutate_state(client):
    client.get("/play/sample_pair")
    client.post("/api/step", json={"key": "space"})  # turn 1
    for _ in range(3):
        assert client.get("/play/sample_pair").status_code == 200
        assert client.get("/games").status_code == 200
    payload = client.post("/api/step", json={"key": "space"}).get_json()
    assert payload["turn"] == 2  # the GETs advanced nothing


def test_refresh_preserves_progress(client):
    """A page refresh re-renders the CURRENT game -- it must never restart."""
    client.get("/play/sample_pair")
    client.post("/api/step", json={"key": "space"})  # turn 1
    assert client.get("/play/sample_pair").status_code == 200  # the "refresh"
    payload = client.post("/api/step", json={"key": "space"}).get_json()
    assert payload["turn"] == 2  # the refresh did not restart the game
