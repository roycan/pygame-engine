"""T1.3 gate: abstract rules for Villain/NPC, concrete Hero."""

import pytest

from engine.actions import MoveAction
from engine.base_classes import Hero, NPC, Villain


def test_villain_is_abstract_without_act():
    with pytest.raises(TypeError):
        Villain("Ghost", 1, 1, 10, 5)


def test_villain_subclass_instantiates():
    class Grub(Villain):
        def act(self, view):
            return MoveAction(1, 0)

        def symbol(self):
            return "👾"

    grub = Grub("Grub", 1, 2, 10, 5)
    assert grub.position == (1, 2)
    assert grub.is_alive()


def test_npc_is_abstract_without_interact():
    with pytest.raises(TypeError):
        NPC("Elder", 0, 0)


def test_npc_has_no_hp():
    class Hermit(NPC):
        def interact(self, view):
            return None

        def symbol(self):
            return "🧙"

    assert not hasattr(Hermit("Hermit", 0, 0), "hp")


def test_hero_is_concrete_with_default_symbol():
    hero = Hero("Ada", 1, 1)
    assert hero.symbol() == "🦸"
    assert (hero.hp, hero.attack_power) == (20, 5)
