"""D-gates: deployment artifacts exist and are correctly configured.

These lock in the three things a free host needs from us: a production
server in requirements, a start command that is SAFE for our in-memory
game state (one worker!), and documentation covering both platforms.
"""

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_requirements_include_production_server():
    requirements = (REPO / "requirements.txt").read_text(encoding="utf-8").lower()
    assert "gunicorn" in requirements
    assert "flask" in requirements


def test_gunicorn_is_importable_in_the_project_venv():
    assert importlib.util.find_spec("gunicorn") is not None, (
        "gunicorn missing -- run: venv/bin/pip install -r requirements.txt"
    )


def test_procfile_pins_the_production_command():
    procfile = (REPO / "Procfile").read_text(encoding="utf-8")
    assert procfile.lstrip().startswith("web:")
    assert "gunicorn" in procfile
    assert "--chdir rogue_edu" in procfile, "engine imports need the chdir"
    assert "--workers 1" in procfile, (
        "in-memory GAMES means exactly one worker -- more would split players "
        "across separate game worlds"
    )
    assert "$PORT" in procfile, "the platform chooses the port; we must bind to it"


def test_app_reads_secret_key_from_environment():
    source = (REPO / "rogue_edu" / "app.py").read_text(encoding="utf-8")
    assert 'os.environ.get("SECRET_KEY"' in source


def test_deploying_doc_covers_both_platforms():
    doc = (REPO / "DEPLOYING.md").read_text(encoding="utf-8").lower()
    for needle in (
        "pythonanywhere",
        "render",
        "unzip rogue_edu_workshop.zip",
        "gunicorn --chdir rogue_edu",
        "secret_key",
        "reload",
        "workers",
        "sleep",
    ):
        assert needle in doc, f"DEPLOYING.md missing: {needle!r}"
