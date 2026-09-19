"""T2.2 gate: __getattr__ typo catcher with the dunder recursion guard."""

import copy

import pytest

from tests.helpers import build_engine


def make_view():
    game = build_engine()
    return game._build_view()


def test_typo_suggests_correct_method():
    view = make_view()
    with pytest.raises(AttributeError) as excinfo:
        view.hero_pos()
    assert "get_hero_position" in str(excinfo.value)


def test_unknown_name_lists_valid_methods():
    view = make_view()
    with pytest.raises(AttributeError) as excinfo:
        view.zzzqqq()
    assert "is_tile_passable" in str(excinfo.value)


def test_dunder_lookup_raises_immediately():
    view = make_view()
    with pytest.raises(AttributeError):
        view.__deepcopy__


def test_deepcopy_survives_no_recursion():
    view = make_view()
    cloned = copy.deepcopy(view)  # must not recurse infinitely
    assert cloned.get_hero_position() == view.get_hero_position()
    assert cloned is not view


def test_private_engine_reference_is_not_leaked():
    view = make_view()
    assert not hasattr(view, "_engine")
    with pytest.raises(AttributeError):
        view._engine
