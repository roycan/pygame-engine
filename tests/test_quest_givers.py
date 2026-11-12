"""Gate: the QuestGiver hierarchy -- Track 3's flagship sample.

Pins the four teaching mechanics the framing doc promises: the
template-method state machine, wired-reference composition (kill and
visit quests), symbol/name narration per state, and a real-engine
engagement where the dialogue box and log carry the quest text.
"""

from engine.actions import SpeakAction
from engine.base_classes import NPC

from arenas.quest_givers.classes import (
    PilgrimageQuest,
    QuestGiver,
    Shrine,
    SlayerQuest,
)
from arenas.quest_givers.game_config import create_game


def fresh():
    game = create_game()
    slayer = next(n for n in game.npcs if isinstance(n, SlayerQuest))
    pilgrim = next(n for n in game.npcs if isinstance(n, PilgrimageQuest))
    shrines = [n for n in game.npcs if isinstance(n, Shrine)]
    return game, slayer, pilgrim, shrines


def test_hierarchy_and_wiring_are_in_place():
    _, slayer, pilgrim, shrines = fresh()
    # The hierarchy: both specializations ARE QuestGivers ARE NPCs.
    assert isinstance(slayer, QuestGiver) and isinstance(slayer, NPC)
    assert isinstance(pilgrim, QuestGiver)
    # Composition: create_game() wired the real objects post-construction.
    assert len(slayer.targets) == 2
    assert all(t.is_alive() for t in slayer.targets)  # both alive
    assert pilgrim.targets == shrines
    assert len(pilgrim.targets) == 3


def test_state_machine_offer_accept_progress_complete():
    game, slayer, _, _ = fresh()
    # offered: first bump offers the quest and accepts it
    assert slayer.state == "offered"
    assert slayer.symbol() == "📜"
    first = slayer.interact(SafeGameViewStub())
    assert isinstance(first, SpeakAction)
    assert "restless dead" in first.message.lower()
    assert slayer.state == "accepted"
    assert slayer.symbol() == "⚔️"
    # accepted, nothing dead yet: progress reports 0/2
    mid = slayer.interact(SafeGameViewStub())
    assert "0/2" in mid.message
    # kill one target: 1/2, still not done
    slayer.targets[0].take_damage(99)
    half = slayer.interact(SafeGameViewStub())
    assert "1/2" in half.message
    assert slayer.state == "accepted"
    # kill the last: completion flips state, renames, rewards
    slayer.targets[1].take_damage(99)
    done = slayer.interact(SafeGameViewStub())
    assert slayer.state == "done"
    assert slayer.symbol() == "✅"
    assert slayer.name.endswith("(quest complete!)")
    assert "graves are quiet" in done.message
    # done is idempotent: another bump repeats the reward, no re-rename
    again = slayer.interact(SafeGameViewStub())
    assert "graves are quiet" in again.message
    assert slayer.name.count("(quest complete!)") == 1


def test_pilgrimage_counts_visited_shrines():
    game, _, pilgrim, shrines = fresh()
    view = SafeGameViewStub()
    assert pilgrim.interact(view).message  # offer accepted
    assert "0/3" in pilgrim.interact(view).message
    shrines[0].interact(view)  # visit one: the shrine's OWN state flips
    assert shrines[0].visited is True
    assert shrines[0].symbol() == "✨"
    assert shrines[1].symbol() == "🗿"  # the others stay cold
    assert "1/3" in pilgrim.interact(view).message
    shrines[1].interact(view)
    shrines[2].interact(view)
    done = pilgrim.interact(view)
    assert pilgrim.state == "done"
    assert pilgrim.symbol() == "✅"
    assert pilgrim.name.endswith("(quest complete!)")
    assert "paths remember you" in done.message


def test_real_engine_dialogue_and_log_carry_the_quest():
    """Bump-to-talk through the REAL engine: dialogue box + log + payload."""
    game = create_game()
    # Reposition the hero west of Sage Elowen at (5, 8) and bump east.
    game.hero.x, game.hero.y = 4, 8
    payload = game.step("d")
    assert payload["active_dialogue"]  # the dialogue box opens...
    assert "Sage Elowen says:" in "\n".join(game.logs)  # ...and the log names her
    # The next key dismisses the dialogue for free (villains held their breath).
    turn_before = game.turn_count
    dismissed = game.step("space")
    assert dismissed["active_dialogue"] is None
    assert game.turn_count == turn_before  # the pause frame costs no turn
    # Questgivers render with their state symbol on the board payload.
    sage = next(n for n in payload["board_state"]["npcs"] if n["name"] == "Sage Elowen")
    assert sage["symbol"] == "⚔️"  # accepted after the bump


class SafeGameViewStub:
    """Minimal read-only view stand-in for direct interact() calls."""

    def get_hero_position(self):
        return (0, 0)

    def distance_to_hero(self, entity):
        return 99

    def get_direction_toward_hero(self, entity):
        return (0, 0)

    def is_tile_passable(self, x, y):
        return True