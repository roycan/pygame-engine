"""T1.1 gate: Action dataclasses (frozen, intent-based, no damage field)."""

import dataclasses

import pytest

from engine.actions import (
    Action,
    AttackAction,
    MoveAction,
    SpeakAction,
    WaitAction,
)


def test_actions_are_frozen():
    action = MoveAction(1, 0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        action.dx = 2


def test_attack_action_has_no_damage_field():
    """The cheat vector must be structurally impossible."""
    with pytest.raises(TypeError):
        AttackAction(damage=999)


def test_attack_action_is_directional():
    attack = AttackAction(-1, 0)
    assert (attack.dx, attack.dy) == (-1, 0)


def test_move_action_fields():
    move = MoveAction(0, -1)
    assert (move.dx, move.dy) == (0, -1)


def test_wait_action_takes_no_arguments():
    assert isinstance(WaitAction(), Action)


def test_speak_action_carries_message():
    assert SpeakAction("hello").message == "hello"
