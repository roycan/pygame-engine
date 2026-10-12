"""Arcade gate: arena folder discovery is complete, selective, fail-soft.

Discovery is FILESYSTEM DISCOVERY plus an ISOLATED VALIDATION PROBE:
deterministic at the interface (same folders in, same ArenaInfo list
out), but the probe executes each arena's import + create_game() inside
a separately terminable subprocess. Tests build throwaway arena folders
in tmp_path instead of touching the real ``rogue_edu/arenas/`` (the
real folder is exercised end-to-end by the route tests via the shipped
``sample_pair`` example).
"""

from pathlib import Path

from arenas import ArenaInfo, discover_arenas, fallback_title

GOOD_BODY = '''
from engine.core import GameEngine


def create_game():
    return GameEngine(width=5, height=5, win_condition="defeat_all")
'''


def make_arena(base: Path, slug: str, body: str = GOOD_BODY, title: str | None = 'TITLE = "Test Arena"') -> Path:
    folder = base / slug
    folder.mkdir(parents=True)
    lines = []
    if title is not None:
        lines.append(title)
    lines.append(body)
    (folder / "game_config.py").write_text("\n".join(lines), encoding="utf-8")
    return folder


def test_finds_a_healthy_arena_with_its_title(tmp_path):
    make_arena(tmp_path, "ada_and_ivo", title='TITLE = "Ada & Ivo Gauntlet"')
    arenas = discover_arenas(tmp_path)
    assert len(arenas) == 1
    assert arenas[0] == ArenaInfo(slug="ada_and_ivo", title="Ada & Ivo Gauntlet", ok=True, error="")


def test_discovery_is_sorted_by_title(tmp_path):
    make_arena(tmp_path, "zulu", title='TITLE = "Zulu Arena"')
    make_arena(tmp_path, "alpha", title='TITLE = "Alpha Arena"')
    assert [a.slug for a in discover_arenas(tmp_path)] == ["alpha", "zulu"]


def test_underscore_and_private_folders_are_skipped(tmp_path):
    make_arena(tmp_path, "_template")  # the shipped scaffold must stay hidden
    make_arena(tmp_path, "__pycache__")  # what it contains is irrelevant
    assert discover_arenas(tmp_path) == []


def test_bad_slug_folders_are_skipped(tmp_path):
    make_arena(tmp_path, "Ada & Ivo")  # spaces/ampersand cannot be a route slug
    make_arena(tmp_path, "Big-Devil")  # hyphen is not in [a-z0-9_]
    assert discover_arenas(tmp_path) == []


def test_folder_without_game_config_is_skipped(tmp_path):
    folder = tmp_path / "empty_pair"
    folder.mkdir()
    (folder / "classes.py").write_text("# classes but no game_config\n", encoding="utf-8")
    assert discover_arenas(tmp_path) == []


def test_syntax_error_is_fail_soft(tmp_path):
    # title=None: this test exercises the FALLBACK-title path for a file
    # too broken to import (the TITLE text scan still works on readable
    # files -- see the probe tests below).
    make_arena(tmp_path, "broken_pair", body="def create_game(:\n    pass", title=None)
    arenas = discover_arenas(tmp_path)
    assert arenas[0].ok is False
    assert "SyntaxError" in arenas[0].error
    assert arenas[0].title == "Broken Pair"  # fallback title, no crash


def test_import_crash_is_fail_soft(tmp_path):
    make_arena(tmp_path, "crashy", body="import module_that_does_not_exist_xyz")
    arenas = discover_arenas(tmp_path)
    assert arenas[0].ok is False
    assert "ModuleNotFoundError" in arenas[0].error


def test_missing_create_game_is_fail_soft(tmp_path):
    make_arena(tmp_path, "no_factory", body="# a config with no create_game()\n")
    arenas = discover_arenas(tmp_path)
    assert arenas[0].ok is False
    assert "create_game" in arenas[0].error


def test_factory_that_raises_at_build_time_is_fail_soft(tmp_path):
    make_arena(
        tmp_path,
        "explodes",
        body=(
            "from engine.core import GameEngine\n\n\n"
            "def create_game():\n"
            "    raise RuntimeError('boom at build time')\n"
        ),
    )
    arenas = discover_arenas(tmp_path)
    assert arenas[0].ok is False
    assert "RuntimeError" in arenas[0].error and "boom" in arenas[0].error


def test_non_string_title_falls_back(tmp_path):
    make_arena(tmp_path, "typed_title", title="TITLE = 123")
    arenas = discover_arenas(tmp_path)
    assert arenas[0].ok is True
    assert arenas[0].title == "Typed Title"


def test_missing_title_falls_back(tmp_path):
    make_arena(tmp_path, "humble_pair", title=None)
    arenas = discover_arenas(tmp_path)
    assert arenas[0].ok is True
    assert arenas[0].title == "Humble Pair"


def test_empty_base_dir_yields_nothing(tmp_path):
    assert discover_arenas(tmp_path) == []


def test_missing_base_dir_yields_nothing(tmp_path):
    assert discover_arenas(tmp_path / "nope") == []


def test_equal_slugs_in_different_dirs_do_not_collide(tmp_path):
    """Two tmp dirs with the SAME slug must not poison each other's cache."""
    make_arena(tmp_path / "one", "twin", title='TITLE = "First Twin"')
    make_arena(tmp_path / "two", "twin", title='TITLE = "Second Twin"')
    first = discover_arenas(tmp_path / "one")[0]
    second = discover_arenas(tmp_path / "two")[0]
    assert first.title == "First Twin"
    assert second.title == "Second Twin"


def test_fallback_title_humanizes_the_slug():
    assert fallback_title("ada_and_ivo") == "Ada And Ivo"
    assert fallback_title("sample_pair") == "Sample Pair"


# ---------------------------------------------------------------------------
# The isolated validation probe (terminable subprocess, corrections #2/#3)
# ---------------------------------------------------------------------------

def _short_probe_timeout(monkeypatch, seconds: float = 2.0) -> None:
    """Parent owns ALL timing policy; tests shrink only the parent's knob."""
    import arenas as arenas_pkg

    monkeypatch.setattr(arenas_pkg, "_PROBE_TIMEOUT_SECONDS", seconds)


def test_nonterminating_import_becomes_a_yellow_card(tmp_path, monkeypatch):
    """A `while True` at import time must NOT wedge discovery: the probe
    subprocess is killed and the arena surfaces as ok=False + 'timed out'."""
    make_arena(tmp_path, "forever_loop", body="while True:\n    pass\n", title=None)
    _short_probe_timeout(monkeypatch)
    arenas = discover_arenas(tmp_path)
    assert len(arenas) == 1
    assert arenas[0].ok is False
    assert "timed out" in arenas[0].error
    assert arenas[0].title == "Forever Loop"  # the card still renders


def test_nonterminating_create_game_becomes_a_yellow_card(tmp_path, monkeypatch):
    make_arena(
        tmp_path,
        "loopy_factory",
        body=(
            "from engine.core import GameEngine\n\n\n"
            "def create_game():\n"
            "    while True:\n"
            "        pass\n"
        ),
    )
    _short_probe_timeout(monkeypatch)
    arenas = discover_arenas(tmp_path)
    assert arenas[0].ok is False
    assert "timed out" in arenas[0].error


def test_discovery_survives_a_looping_arena_and_stays_deterministic(tmp_path, monkeypatch):
    """The scoped guarantee: looping import/create_game cannot hang the
    discovery REQUEST, and repeated scans give the same answer."""
    make_arena(tmp_path, "loop_pair", body="while True:\n    pass\n")
    make_arena(tmp_path, "calm_pair")
    _short_probe_timeout(monkeypatch)
    first = discover_arenas(tmp_path)
    second = discover_arenas(tmp_path)
    assert first == second  # deterministic at the interface level
    assert [a.slug for a in first] == ["calm_pair", "loop_pair"]
    assert first[0].ok is True and first[1].ok is False


def test_probe_child_direct_invocation_contract(tmp_path):
    """Child-side contract: exit 0 + silent on healthy; nonzero + short
    summary on stderr for broken; --timeout-ready is an accepted no-op
    (the parent owns timing)."""
    import subprocess
    import sys

    from arenas import _PROBE_SCRIPT

    good = tmp_path / "game_config.py"
    good.write_text(GOOD_BODY, encoding="utf-8")
    done = subprocess.run(
        [sys.executable, str(_PROBE_SCRIPT), "--config", str(good), "--timeout-ready", "0"],
        capture_output=True, text=True, timeout=60,
    )
    assert done.returncode == 0
    assert done.stdout.strip() == ""

    bad = tmp_path / "broken.py"
    bad.write_text("def create_game(:\n    pass\n", encoding="utf-8")
    done = subprocess.run(
        [sys.executable, str(_PROBE_SCRIPT), "--config", str(bad)],
        capture_output=True, text=True, timeout=60,
    )
    assert done.returncode != 0
    assert "SyntaxError" in done.stderr


# ---------------------------------------------------------------------------
# TITLE metadata scan (reads text; never executes anything for a title)
# ---------------------------------------------------------------------------

def test_title_scan_double_quoted_single_quoted_and_fallbacks(tmp_path):
    make_arena(tmp_path, "dq_pair", title='TITLE = "Double Quoted"')
    make_arena(tmp_path, "sq_pair", title="TITLE = 'Single Quoted'")
    make_arena(tmp_path, "numeric_pair", title="TITLE = 123")  # non-string -> fallback
    make_arena(tmp_path, "prefix_pair", title='TITLEX = "Not A Title"')  # not TITLE
    arenas = {a.slug: a for a in discover_arenas(tmp_path)}
    assert arenas["dq_pair"].title == "Double Quoted"
    assert arenas["sq_pair"].title == "Single Quoted"
    assert arenas["numeric_pair"].title == "Numeric Pair"  # fallback preserved
    assert arenas["prefix_pair"].title == "Prefix Pair"  # TITLEX never matches
