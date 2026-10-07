"""Flask web server for the RogueEdu class arcade.

Routes:
    GET  /              -- the starter game interface (Canvas + Bulma UI).
    GET  /games         -- the class arcade menu: one card per merged arena.
    GET  /play/<slug>   -- play one student pair's arena.
    POST /api/step      -- {"key": "w"|"a"|"s"|"d"|"space"} -> turn JSON.
    POST /api/reset     -- re-instantiate the session's game.

Session handling:
    * ``app.secret_key`` MUST be set or ``flask.session`` fails loudly.
    * Each browser gets a UUID ``session_id`` cookie; live engines live
      in the module-level ``GAMES`` dict keyed by ``(session_id, arena)``
      so one browser can hold several games without leaking state.
    * The chosen arena rides the session cookie: ``/play/<slug>`` sets
      ``session["arena"]``; visiting ``/`` clears it -- ``/`` is ALWAYS
      the starter game. A stale/missing session lazily creates a game.
    * Unbounded dict growth is acceptable at classroom scale (see note).

Run from the rogue_edu/ folder:

    python app.py                          # starter game at /
    GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py

Deployment (Render) runs gunicorn --chdir rogue_edu app:app --workers 1
(ONE worker is mandatory: the in-memory GAMES dict IS the world).
"""

from __future__ import annotations

import importlib
import os
import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, session

from arenas import discover_arenas, load_game_config
from engine.core import GameEngine

app = Flask(__name__)
# flask.session silently requires a secret key -- set one, always.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# classroom-scale note: sessions are never evicted; fine for one class,
# restart the server between periods if this ever matters.
# Keys are (session_id, arena_slug); arena_slug == "" means the starter.
GAMES: dict[tuple[str, str], GameEngine] = {}

#: The ONE seam tests monkeypatch: where to scan for arena folders.
ARENAS_BASE = Path(__file__).resolve().parent / "arenas"


def _config_module_name() -> str:
    """Which create_game() should power the starter? Defaults to the
    student starter; point GAME_CONFIG_MODULE at a demo to override."""
    return os.environ.get("GAME_CONFIG_MODULE", "student_starter.game_config")


def _starter_game() -> GameEngine:
    """Import the configured module and call its create_game() factory."""
    module = importlib.import_module(_config_module_name())
    return module.create_game()


def _arena_game(slug: str) -> GameEngine | None:
    """Build one arena's game; None when unknown or broken (fail-soft)."""
    config_path = ARENAS_BASE / slug / "game_config.py"
    if not config_path.is_file():
        return None
    try:
        module = load_game_config(slug, config_path)
        factory = getattr(module, "create_game")
        return factory()
    except Exception:  # noqa: BLE001 - a broken arena must never 500 the API
        return None


def _create_game(arena: str = "") -> GameEngine:
    """Factory for the session's current arena ("" = the starter)."""
    if arena:
        game = _arena_game(arena)
        if game is not None:
            return game
        # Belt and braces: /play only selects healthy arenas, but the
        # API routes must never 500 no matter what.
    return _starter_game()


def _session_id() -> str:
    """Get-or-create this browser's UUID session id."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]


def _current_game() -> GameEngine:
    """Return this session's engine, lazily creating one if needed."""
    sid = _session_id()
    arena = session.get("arena", "")
    key = (sid, arena)
    if key not in GAMES:
        GAMES[key] = _create_game(arena)
    return GAMES[key]


@app.route("/")
def index():
    """Render the starter game with its initial state embedded, so the
    board paints on page load -- never a blank canvas waiting for the
    first keypress. Visiting / ALWAYS plays the starter: any previously
    chosen arena is cleared."""
    session.pop("arena", None)
    game = _current_game()
    return render_template(
        "index.html", initial_state=game.payload(), arena_title="RogueEdu Starter"
    )


@app.route("/games")
def games():
    """The class arcade: one card per merged pair folder, plus the
    starter. Broken arenas render as yellow "needs fixing" cards -- the
    menu itself must never break (fail-soft discovery)."""
    return render_template("games.html", arenas=discover_arenas(ARENAS_BASE))


@app.route("/play/<slug>")
def play(slug: str):
    """Choose an arena for this browser session and render its game."""
    found = [a for a in discover_arenas(ARENAS_BASE) if a.slug == slug]
    if not found:
        abort(404)
    info = found[0]
    if not info.ok:
        return render_template("arena_broken.html", arena=info)
    session["arena"] = slug
    sid = _session_id()
    key = (sid, slug)
    if key not in GAMES:
        GAMES[key] = _create_game(slug)
    game = GAMES[key]
    return render_template(
        "index.html", initial_state=game.payload(), arena_title=info.title
    )


@app.route("/api/step", methods=["POST"])
def step():
    """Advance the session's game by one player input; return turn JSON."""
    data = request.get_json(silent=True) or {}
    key = data.get("key", "")
    game = _current_game()
    return jsonify(game.step(key))


@app.route("/api/reset", methods=["POST"])
def reset():
    """Re-instantiate this session's game from its factory."""
    sid = _session_id()
    arena = session.get("arena", "")
    GAMES[(sid, arena)] = _create_game(arena)
    return jsonify(GAMES[(sid, arena)].payload())


if __name__ == "__main__":
    # debug=False on purpose: the reloader double-imports modules, which
    # confuses students (duplicated game state) and re-runs create_game().
    app.run(debug=False, host="127.0.0.1", port=5000)
