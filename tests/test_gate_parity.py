"""Gate: `npm test` and `make test` run the SAME suite (pytest + node --test).

Two entry points, one gate: if either halves drift apart, an agent or a
teacher could believe a green `npm test` while `make test` is red (or
vice versa). This file pins the scripts so they cannot drift silently.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_package_json_scripts_cover_both_halves():
    scripts = json.loads((REPO / "package.json").read_text(encoding="utf-8"))["scripts"]
    assert "venv/bin/pytest" in scripts["test:py"], "the Python half must use the project venv"
    assert "node --test tests/js/" in scripts["test:js"], "the JS half must run the jsdom suite"
    # The glob form is deliberate: `node --test <dir>` misbehaves on some
    # Node builds; tests/js/*.test.js is the form the Makefile proves.
    assert "*.test.js" in scripts["test:js"], "the JS half must use the proven glob form"
    combined = scripts["test"]
    assert "test:py" in combined and "test:js" in combined, (
        "npm test must run BOTH halves -- parity with make test"
    )


def test_js_test_directory_is_nonempty():
    js_tests = sorted((REPO / "tests" / "js").glob("*.test.js"))
    assert js_tests, "the node half of the gate must have tests to run"
