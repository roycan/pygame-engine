"""T6.1 gate: structural checks on templates/index.html (visual checks
are the documented 8-point manual checklist in README.md)."""

from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "rogue_edu" / "templates" / "index.html"
GAME_JS = Path(__file__).resolve().parents[1] / "rogue_edu" / "static" / "game.js"


def test_template_exists_with_required_structure():
    html = TEMPLATE.read_text(encoding="utf-8")
    for required_id in (
        "board",
        "dialogue-box",
        "dialogue-speaker",
        "dialogue-text",
        "hud-turn",
        "hud-hp",
        "hud-villains",
        "log-list",
        "inspector",
        "inspector-toggle",
        "api-card",
    ):
        assert f'id="{required_id}"' in html, f"missing element id {required_id!r}"


def test_template_loads_bulma_from_cdn_and_the_game_script():
    html = TEMPLATE.read_text(encoding="utf-8")
    assert "bulma" in html.lower() and "cdn.jsdelivr.net" in html
    assert "/static/game.js" in html


def test_game_js_separates_pure_helpers_from_dom_code():
    source = GAME_JS.read_text(encoding="utf-8")
    for fn in ("keyToIntent", "handleKey", "gridToPixel", "highlightBox"):
        assert f"function {fn}" in source, f"pure helper {fn} missing"
    assert "module.exports" in source  # Node export guard for tests


def test_game_js_has_no_fetch_outside_boot_path():
    source = GAME_JS.read_text(encoding="utf-8")
    # fetch is allowed ONLY inside the DOM wiring (boot/keydown handler),
    # never inside the pure helpers or renderer functions.
    pure_section = source.split("function boot")[0]
    assert "fetch(" not in pure_section


def test_template_embeds_initial_state_before_game_js():
    html = TEMPLATE.read_text(encoding="utf-8")
    assert "__INITIAL_STATE__" in html
    # The bootstrap data must exist BEFORE game.js loads, or boot() cannot
    # paint the board on load.
    assert html.index("__INITIAL_STATE__") < html.index("/static/game.js")
    assert "boot" in GAME_JS.read_text(encoding="utf-8")
