"""The class arcade: one folder per pair, auto-discovered, fail-soft.

Each immediate subfolder of ``arenas/`` whose name matches ``[a-z0-9_]+``
and that contains a ``game_config.py`` is a PLAYABLE ARENA. Folders whose
names start with ``_`` (like ``_template/``) and ``__pycache__`` are
never discovered.

Discovery is FILESYSTEM DISCOVERY plus an ISOLATED VALIDATION PROBE --
deterministic at its interface (same folders in, same ArenaInfo list
out), but the probe deliberately EXECUTES untrusted arena code
(import + ``create_game()``) inside a separately terminable subprocess
(``tools/probe_arena.py``, bounded by ``_PROBE_TIMEOUT_SECONDS``).
A subprocess can be killed; a hung import inside this process cannot,
and one wedged worker thread is enough to black out a one-worker
gunicorn deployment. Discovery NEVER raises: a broken arena (syntax
error, import crash, missing ``create_game()``, a factory that explodes,
or a probe timeout -- most likely an infinite loop) comes back as
``ArenaInfo(ok=False, error=...)`` and renders as a "needs fixing" card
in ``/games`` instead of taking down the menu for everyone.

Scope of the guarantee (read this before extending): the probe proves
that a non-terminating IMPORT or ``create_game()`` cannot wedge a
discovery request. It is NOT a general sandbox, and it says nothing
about arbitrary future per-arena execution paths.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path

_SLUG_RE = re.compile(r"^[a-z0-9_]+$")
_TITLE_RE = re.compile(r"""TITLE\s*=\s*(["'])(.+?)\1""")
_ERROR_MAX = 120  # keep the menu card readable
# Parent owns ALL timing policy; the env override exists so the test
# gate can exercise the timeout path in seconds instead of waiting.
_PROBE_TIMEOUT_SECONDS = float(os.environ.get("ROGUEEDU_PROBE_TIMEOUT", "10"))

_TOOLS_DIR = Path(__file__).resolve().parents[2] / "tools"
_PROBE_SCRIPT = _TOOLS_DIR / "probe_arena.py"


@dataclass
class ArenaInfo:
    """One discovered arena folder, healthy or broken."""

    slug: str
    title: str
    ok: bool
    error: str = ""


def _error_summary(text: str) -> str:
    return text.strip().replace("\n", " | ")[:_ERROR_MAX]


def fallback_title(slug: str) -> str:
    """Menu card name when the arena declares no usable TITLE."""
    return slug.replace("_", " ").title()


def load_game_config(slug: str, config_path: Path):
    """Import one arena's ``game_config.py`` by FILE PATH, not dotted name.

    Used by the server when a session actually PLAYS an arena (discovery
    itself uses the subprocess probe and never imports in-process).
    Loading by path works no matter which directory the server was
    started from, and the unique ``sys.modules`` key (slug + a stable
    digest of the absolute path) keeps separate arenas -- and separate
    test temp dirs that happen to reuse a slug -- from colliding.
    """
    import importlib.util

    digest = zlib.crc32(str(config_path.resolve()).encode("utf-8"))
    module_key = f"rogueedu_arena_{slug}_{digest}"
    if module_key in sys.modules:
        return sys.modules[module_key]
    spec = importlib.util.spec_from_file_location(module_key, config_path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"could not create an import spec for {config_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_key] = module
    spec.loader.exec_module(module)
    return module


def _run_probe(config_path: Path) -> tuple[bool, str]:
    """Import + build one arena inside a killable child process.

    Returns (ok, error_summary). A timeout (non-terminating import or
    ``create_game()``) is recorded as ``ok=False`` -- the child process
    is killed, so the worst an arena can cost discovery is the timeout
    window, never a hung worker thread.
    """
    try:
        completed = subprocess.run(
            [sys.executable, str(_PROBE_SCRIPT), "--config", str(config_path)],
            capture_output=True,
            text=True,
            timeout=_PROBE_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, f"timed out after {_PROBE_TIMEOUT_SECONDS:g}s (possible infinite loop)"
    if completed.returncode == 0:
        return True, ""
    return False, _error_summary(completed.stderr or f"exit code {completed.returncode}")


def discover_arenas(base: Path) -> list[ArenaInfo]:
    """Scan ``base`` for playable arena folders. Never raises.

    Sorting is by title so the menu is stable regardless of folder name.
    """
    arenas: list[ArenaInfo] = []
    if not base.is_dir():
        return arenas
    for entry in sorted(base.iterdir()):
        if not entry.is_dir() or entry.name.startswith("_"):
            continue  # _template, __pycache__, anything private
        if not _SLUG_RE.match(entry.name):
            continue  # "Ada & Ivo" is a folder we cannot route safely
        config_path = entry / "game_config.py"
        if not config_path.is_file():
            continue  # a folder with no game is not an arena
        arenas.append(_inspect_arena(entry.name, config_path))
    return sorted(arenas, key=lambda info: info.title.lower())


def _inspect_arena(slug: str, config_path: Path) -> ArenaInfo:
    """Validate one arena via the isolated probe; any failure => ok=False."""
    title = fallback_title(slug)

    # Read TITLE with plain file text first: it is metadata for the card,
    # not a reason to trust or execute anything here. Only a QUOTED string
    # counts (a non-string TITLE falls back, matching the old contract).
    try:
        for line in config_path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = _TITLE_RE.match(line.strip())
            if match and match.group(2).strip():
                title = match.group(2)
                break
    except OSError:
        pass  # the probe will report the read failure far more precisely

    ok, error = _run_probe(config_path)
    return ArenaInfo(slug=slug, title=title, ok=ok, error=error)

