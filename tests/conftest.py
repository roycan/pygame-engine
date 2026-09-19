"""Shared pytest fixtures for the RogueEdu test suite."""

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def contract():
    """The frozen JSON contract shared by pytest AND the jsdom tests.

    Both sides validate against this one file, so the Python engine and
    the JavaScript renderer can never drift apart.
    """
    return json.loads((FIXTURES_DIR / "turn_payload_schema.json").read_text(encoding="utf-8"))
