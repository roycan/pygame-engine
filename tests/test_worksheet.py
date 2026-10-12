"""W2 gates: the workshop worksheet's structural contract, its answer
code (exercised against the real engine), and key<->answer sync.

The student handout must NOT contain the answer key: the key lives in
``plans/workshop_01_teacher_answer_key.md`` (teacher-only, excluded from
the student ZIP along with this file and the answer fixture)."""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tests" / "fixtures"))

import worksheet_answers as answers  # noqa: E402

from check_my_class import inspect_classes  # noqa: E402
from engine.actions import AttackAction, MoveAction  # noqa: E402
from engine.core import GameEngine  # noqa: E402

WORKSHEET = REPO / "workshops" / "workshop_01_meet_the_engine.md"
WORKSHEET_TEXT = WORKSHEET.read_text(encoding="utf-8")
TEACHER_KEY = REPO / "plans" / "workshop_01_teacher_answer_key.md"
TEACHER_KEY_TEXT = TEACHER_KEY.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Answer code -- the exact classes the worksheet teaches, played for real.
# ---------------------------------------------------------------------------

class AdjacentHeroView:
    """Mock view: the hero stands one tile to the EAST."""

    def get_hero_position(self):
        return (5, 5)

    def distance_to_hero(self, entity):
        return 1

    def get_direction_toward_hero(self, entity):
        return (1, 0)

    def is_tile_passable(self, x, y):
        return True


class FarHeroView:
    """Mock view: the hero is three tiles to the EAST."""

    def get_hero_position(self):
        return (5, 5)

    def distance_to_hero(self, entity):
        return 3

    def get_direction_toward_hero(self, entity):
        return (1, 0)

    def is_tile_passable(self, x, y):
        return True


def test_worksheet_answers_pass_the_checker():
    findings = inspect_classes("worksheet_answers")
    failures = [f for f in findings if f.level == "FAIL"]
    assert failures == [], f"worksheet answer code failed the checker: {failures}"
    assert any(f.level == "PASS" for f in findings)


def test_reskinned_slime_bites_when_adjacent_and_chases_when_far():
    blob = answers.ReskinnedSlime(4, 5)
    bite = blob.act(AdjacentHeroView())
    assert isinstance(bite, AttackAction) and (bite.dx, bite.dy) == (1, 0)
    approach = blob.act(FarHeroView())
    assert isinstance(approach, MoveAction) and (approach.dx, approach.dy) == (1, 0)


def test_coward_attacks_while_healthy():
    coward = answers.CowardSlime(4, 5)  # full hp: brave
    action = coward.act(AdjacentHeroView())
    assert isinstance(action, AttackAction)


def test_coward_flees_when_hurt():
    coward = answers.CowardSlime(4, 5)
    coward.take_damage(10)  # 12 -> 2 hp: well below half
    action = coward.act(AdjacentHeroView())
    assert isinstance(action, MoveAction)
    assert (action.dx, action.dy) == (-1, 0), "the coward must move AWAY from the hero"


def test_patrol_slime_cycles_its_route():
    patrol = answers.PatrolSlime(5, 5)
    steps = [patrol.act(FarHeroView()) for _ in range(3)]
    assert [(s.dx, s.dy) for s in steps] == [(1, 0), (0, 1), (-1, 0)]


def test_arena_boots_and_plays_a_turn():
    game = answers.create_arena_game()
    assert isinstance(game, GameEngine)
    assert game.win_condition == "defeat_all"
    assert len(game.villains) == 2
    payload = game.step("space")
    assert payload["turn"] == 1
    assert payload["game_over"] is False


# ---------------------------------------------------------------------------
# Worksheet structural contract
# ---------------------------------------------------------------------------

def test_required_sections_present():
    lowered = WORKSHEET_TEXT.lower()
    for needle in (
        "meet the engine",
        "setup on windows",
        "the hook",
        "what is this engine",
        "key features",
        "analogies",
        "part 1: me",
        "part 2: us",
        "part 3: you",
        "reflect",
        "the quarter",
    ):
        assert needle in lowered, f"worksheet missing section: {needle!r}"
    # The key itself moved to the teacher pack...
    assert "answer key" in TEACHER_KEY_TEXT.lower(), "teacher key file lost its heading"
    # ...and the student handout must NOT contain any answer content.
    assert "Magma Blob" not in WORKSHEET_TEXT, "answers leaked into the student worksheet"
    assert "worksheet_answers" not in WORKSHEET_TEXT, "fixture reference leaked into the student worksheet"


def test_header_blanks_present():
    for label in ("**Name:**", "**Section:**", "**Date:**"):
        position = WORKSHEET_TEXT.find(label)
        assert position != -1, f"worksheet header missing {label}"
        tail = WORKSHEET_TEXT[position : position + 120]
        assert "____" in tail, f"{label} needs a fill-in blank after it"


def test_three_tiers_present():
    for emoji in ("🌱", "🌿", "🌳"):
        assert emoji in WORKSHEET_TEXT, f"missing tier emoji {emoji}"


def test_two_reflection_pauses_with_three_questions_each():
    blocks = re.findall(
        r"Reflect[^\n]*\n(.*?)(?=\n## |\Z)", WORKSHEET_TEXT, flags=re.S
    )
    strong_blocks = 0
    for block in blocks:
        numbered = re.findall(r"^\s*\d+\.\s+\S", block, flags=re.M)
        if len(numbered) >= 3:
            strong_blocks += 1
    assert strong_blocks >= 2, "expected two reflection pauses with >=3 questions each"


def test_code_fences_balanced():
    assert WORKSHEET_TEXT.count("```") % 2 == 0, "unclosed code fence"


def test_every_referenced_file_exists():
    for relative in (
        "rogue_edu/student_starter/classes.py",
        "rogue_edu/student_starter/game_config.py",
        "rogue_edu/check_my_class.py",
        "rogue_edu/app.py",
        "rogue_edu/demos/demo_dungeon/entities.py",
        "tests/fixtures/worksheet_answers.py",
        "plans/workshop_01_teacher_answer_key.md",
    ):
        assert (REPO / relative).exists(), f"worksheet references missing file {relative}"


def test_windows_setup_steps_present():
    for needle in (
        "Extract All",
        "Add python.exe to PATH",
        "python -m venv venv",
        "venv\\Scripts\\pip install -r requirements.txt",
        "check_my_class",
        "127.0.0.1:5000",
        "VS Code",
    ):
        assert needle in WORKSHEET_TEXT, f"windows setup missing: {needle!r}"


def test_worksheet_matches_tested_answers():
    """The anti-drift gate, two-sided:
    (1) the TEACHER KEY must contain the signature lines of the
        engine-tested answer fixture, verbatim;
    (2) the student handout must contain none of the ANSWER-IDENTIFYING
        content (class/identity names). Generic code lines that appear
        in the fill-in-the-blank scaffold (e.g. ``if self.hp * 2 >=
        self.max_hp:``) are deliberately allowed there -- students
        complete them; they are not answers."""
    for line in answers.SIGNATURE_LINES:
        assert line in TEACHER_KEY_TEXT, f"teacher key drifted from tested answer: {line!r}"

    answer_markers = (
        "Magma Blob",      # Tier 1 answer identity
        "Sir Wobbles",     # Tier 2 answer identity
        "Roundabout",      # Tier 2 alternate answer identity
        "ReskinnedSlime",
        "CowardSlime",
        "PatrolSlime",
        "ArenaChamp",      # Tier 3 answer identity
        "create_arena_game",
    )
    for marker in answer_markers:
        assert marker not in WORKSHEET_TEXT, f"answer content leaked into student handout: {marker!r}"
        assert marker in TEACHER_KEY_TEXT, f"teacher key lost answer content: {marker!r}"
