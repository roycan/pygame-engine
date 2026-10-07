"""Template/JS structural gate (visual checks are the documented manual
checklist in README.md -- pixels need eyes, structure needs tests)."""

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


def test_game_js_has_no_fetch_outside_the_input_seam():
    source = GAME_JS.read_text(encoding="utf-8")
    # fetch lives ONLY inside submitKey (the shared keyboard/touch input
    # seam) and boot's wiring; never in the pure helpers or renderer.
    assert "function submitKey" in source, "the submitKey input seam is missing"
    before_seam = source.split("function submitKey")[0]
    assert "fetch(" not in before_seam, "fetch leaked into the pure/renderer sections"


def test_game_js_input_seam_has_an_in_flight_guard():
    source = GAME_JS.read_text(encoding="utf-8")
    assert "_busy" in source, "the in-flight guard is missing"
    # The guard must clear even when the request FAILS (.finally), or a
    # dropped connection would permanently lock the keyboard.
    seam = source.split("function submitKey", 1)[1].split("function boot", 1)[0]
    assert ".finally(" in seam, "submitKey must release _busy in .finally()"


def test_template_embeds_initial_state_before_game_js():
    html = TEMPLATE.read_text(encoding="utf-8")
    assert "__INITIAL_STATE__" in html
    # The bootstrap data must exist BEFORE game.js loads, or boot() cannot
    # paint the board on load.
    assert html.index("__INITIAL_STATE__") < html.index("/static/game.js")
    assert "boot" in GAME_JS.read_text(encoding="utf-8")


def test_template_is_phone_first():
    """70% of the audience is on phones: the board must scale and the
    D-pad must exist for touch input (both ride existing logic)."""
    html = TEMPLATE.read_text(encoding="utf-8")
    assert "max-width: 100%" in html, "the 500px canvas must scale on small screens"
    assert "height: auto" in html, "the scaled canvas must keep its aspect ratio"
    assert "pointer: coarse" in html, "touch devices must see the D-pad"
    for pad_id in ("dpad", "pad-up", "pad-down", "pad-left", "pad-right", "pad-wait"):
        assert f'id="{pad_id}"' in html, f"missing touch-control id {pad_id!r}"
    assert 'data-key=" "' in html, "the wait button must send Space"
    assert "KeyboardEvent" in html, "taps must ride the keyboard input path"


def test_template_shows_which_arena_is_playing():
    html = TEMPLATE.read_text(encoding="utf-8")
    assert "arena_title" in html, "the page title must show the chosen arena"
