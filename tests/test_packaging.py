"""W0 gate: the workshop ZIP's file selection is exactly right."""

import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))

import package_workshop as pw  # noqa: E402


def relative_selection():
    return {
        str(p.relative_to(pw.REPO_ROOT)).replace("\\", "/")
        for p in pw.select_files()
    }


def test_selection_includes_essentials():
    rel = relative_selection()
    for needed in (
        "README.md",
        "DEPLOYING.md",
        "Procfile",
        "requirements.txt",
        "pytest.ini",
        "Makefile",
        "rogue_edu/app.py",
        "rogue_edu/engine/core.py",
        "rogue_edu/student_starter/classes.py",
        "rogue_edu/student_starter/game_config.py",
        "rogue_edu/check_my_class.py",
        "rogue_edu/demos/demo_dungeon/game_config.py",
        "rogue_edu/static/game.js",
        "workshops/workshop_01_meet_the_engine.md",
    ):
        assert needed in rel, f"workshop ZIP must include {needed!r}"


def test_selection_excludes_dev_and_cache_dirs():
    rel = relative_selection()
    banned_prefixes = (
        "venv/",
        "node_modules/",
        "temp/",
        "inceptions/",
        "plans/",
        "dist/",
        "tools/__pycache__/",
    )
    for path in rel:
        for banned in banned_prefixes:
            assert not path.startswith(banned), f"{path} must not ship to students"
        assert "__pycache__" not in path, f"{path} must not ship to students"


def test_built_zip_nests_everything_under_one_folder(tmp_path):
    dest = tmp_path / "rogue_edu_workshop.zip"
    built = pw.build_zip(dest)
    assert built == dest and dest.exists()
    with zipfile.ZipFile(dest) as archive:
        names = archive.namelist()
    assert names, "the ZIP must not be empty"
    assert all(name.startswith("rogue_edu_workshop/") for name in names)
    assert "rogue_edu_workshop/rogue_edu/app.py" in names
    assert "rogue_edu_workshop/rogue_edu/student_starter/classes.py" in names
