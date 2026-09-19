"""Flask web server for the RogueEdu game session.

Routes:
    GET  /           -- the main game interface (Canvas + Bulma UI).
    POST /api/step   -- {"key": "w"|"a"|"s"|"d"|"space"} -> turn JSON.
    POST /api/reset  -- re-instantiate the game via create_game().

Session handling:
    * ``app.secret_key`` MUST be set or ``flask.session`` fails loudly.
    * Each browser gets a UUID ``session_id`` cookie; live engines live
      in the module-level ``GAMES`` dict keyed by that UUID.
    * A stale/missing session lazily creates a fresh game.
    * Unbounded dict growth is acceptable at classroom scale (see note).

Run from the rogue_edu/ folder:

    python app.py                          # student starter game
    GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py
"""

from __future__ import annotations

import importlib
import os
import uuid

from flask import Flask, jsonify, render_template, request, session

from engine.core import GameEngine

app = Flask(__name__)
# flask.session silently requires a secret key -- set one, always.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# classroom-scale note: sessions are never evicted; fine for one class,
# restart the server between periods if this ever matters.
GAMES: dict[str, GameEngine] = {}


def _config_module_name() -> str:
    """Which create_game() should power this server? Defaults to the
    student starter; point GAME_CONFIG_MODULE at a demo to override."""
    return os.environ.get("GAME_CONFIG_MODULE", "student_starter.game_config")


def _create_game():
    """Import the configured module and call its create_game() factory."""
    module = importlib.import_module(_config_module_name())
    return module.create_game()


def _session_id() -> str:
    """Get-or-create this browser's UUID session id."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]


def _get_game():
    """Return this session's engine, lazily creating one if needed."""
    sid = _session_id()
    if sid not in GAMES:
        GAMES[sid] = _create_game()
    return GAMES[sid]


@app.route("/")
def index():
    """Render the main game interface with the initial game state embedded,
    so the board paints on page load -- never a blank canvas waiting for
    the first keypress."""
    game = _get_game()
    return render_template("index.html", initial_state=game.payload())


@app.route("/api/step", methods=["POST"])
def step():
    """Advance the session's game by one player input; return turn JSON."""
    data = request.get_json(silent=True) or {}
    key = data.get("key", "")
    game = _get_game()
    return jsonify(game.step(key))


@app.route("/api/reset", methods=["POST"])
def reset():
    """Re-instantiate this session's game from create_game()."""
    sid = _session_id()
    GAMES[sid] = _create_game()
    return jsonify(GAMES[sid].payload())


if __name__ == "__main__":
    # debug=False on purpose: the reloader double-imports modules, which
    # confuses students (duplicated game state) and re-runs create_game().
    app.run(debug=False, host="127.0.0.1", port=5000)
