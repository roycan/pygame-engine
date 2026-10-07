"""Checker CLI gate: `python check_my_class.py [target]` checks any pair.

The default (no argument) behavior is untouched -- student_starter.classes,
zero golden drift. New: an argument (path OR dotted module) checks that
pair's classes, and a game_config target also verifies TITLE (the /games
menu card name).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "rogue_edu"))

import check_my_class as doctor  # noqa: E402


def test_default_target_is_the_starter_file():
    assert doctor._resolve_target(None) == "student_starter.classes"
    assert doctor._resolve_target("") == "student_starter.classes"
    assert doctor._resolve_target("   ") == "student_starter.classes"


def test_paths_and_modules_normalize_to_dotted_names():
    assert doctor._resolve_target("arenas/sample_pair/game_config.py") == (
        "arenas.sample_pair.game_config"
    )
    assert doctor._resolve_target("arenas.sample_pair.classes") == (
        "arenas.sample_pair.classes"
    )
    assert doctor._resolve_target("student_starter\\classes.py") == (
        "student_starter.classes"
    )


def test_real_sample_pair_passes_the_doctor_with_a_title():
    findings = doctor.inspect_classes("arenas.sample_pair.classes")
    assert not [f for f in findings if f.level == "FAIL"], (
        "the shipped worked example must pass its own doctor"
    )
    titles = doctor._title_findings("arenas.sample_pair.game_config")
    assert titles[0].level == "PASS"
    assert "Sample Pair" in titles[0].title


def test_game_config_without_title_warns(tmp_path, monkeypatch):
    package = tmp_path / "doctor_tmp_pkg"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "game_config.py").write_text(
        "from engine.core import GameEngine\n\n\n"
        "def create_game():\n"
        "    return GameEngine(width=5, height=5, win_condition='defeat_all')\n",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    findings = doctor._title_findings("doctor_tmp_pkg.game_config")
    assert findings[0].level == "WARN"
    assert "TITLE" in findings[0].title


def test_unimportable_title_target_reports_nothing_extra():
    # inspect_classes already reported the import failure; TITLE stays quiet.
    assert doctor._title_findings("package_that_does_not_exist_xyz.game_config") == []


def test_main_returns_zero_for_the_real_sample_pair(capsys):
    assert doctor.main(["arenas/sample_pair/game_config"]) == 0
    out = capsys.readouterr().out
    assert "TITLE found" in out
    assert "arenas.sample_pair.classes" in out  # the sibling was checked
