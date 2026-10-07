"""The class arcade: one folder per pair, auto-discovered, fail-soft.

Each immediate subfolder of ``arenas/`` whose name matches ``[a-z0-9_]+``
and that contains a ``game_config.py`` is a PLAYABLE ARENA. Folders whose
names start with ``_`` (like ``_template/``) and ``__pycache__`` are
never discovered.

Discovery NEVER raises: a broken arena (syntax error, import crash,
missing ``create_game()``, a factory that explodes when called) comes
back as ``ArenaInfo(ok=False, error=...)`` and renders as a "needs
fixing" card in ``/games`` instead of taking down the menu for everyone.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path

_SLUG_RE = re.compile(r"^[a-z0-9_]+$")
_ERROR_MAX = 120  # keep the menu card readable


@dataclass
class ArenaInfo:
    """One discovered arena folder, healthy or broken."""

    slug: str
    title: str
    ok: bool
    error: str = ""


def _error_summary(exc: BaseException) -> str:
    text = f"{type(exc).__name__}: {exc}".strip()
    return text[:_ERROR_MAX]


def fallback_title(slug: str) -> str:
    """Menu card name when the arena declares no usable TITLE."""
    return slug.replace("_", " ").title()


def load_game_config(slug: str, config_path: Path):
    """Import one arena's ``game_config.py`` by FILE PATH, not dotted name.

    Loading by path works no matter which directory the server was
    started from, and the unique ``sys.modules`` key (slug + a stable
    digest of the absolute path) keeps separate arenas -- and separate
    test temp dirs that happen to reuse a slug -- from colliding.
    """
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
    """Import + build one arena. Any failure => ok=False with a summary."""
    title = fallback_title(slug)
    try:
        module = load_game_config(slug, config_path)
        factory = getattr(module, "create_game", None)
        if not callable(factory):
            raise AttributeError("game_config.py does not define create_game()")
        declared = getattr(module, "TITLE", None)
        if isinstance(declared, str) and declared.strip():
            title = declared
        factory()  # a config that imports but explodes at build time is broken
    except Exception as exc:  # noqa: BLE001 - fail-soft IS the contract here
        return ArenaInfo(slug=slug, title=title, ok=False, error=_error_summary(exc))
    return ArenaInfo(slug=slug, title=title, ok=True)
