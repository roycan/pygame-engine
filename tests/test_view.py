"""T2.1 gate: SafeGameView snapshot semantics + the four helper methods."""

from engine.base_classes import Wall
from tests.helpers import ScriptedVillain, build_engine, make_npc


def make_world():
    """hero (1,1); wall (2,2); npc (1,3); villains at (4,1) and (3,3)."""
    game = build_engine()
    game.add_wall(Wall("Rock", 2, 2))
    game.add_npc(make_npc(x=1, y=3))
    game.add_villain(ScriptedVillain("East", 4, 1))
    game.add_villain(ScriptedVillain("Diag", 3, 3))
    return game, game._build_view()


def test_snapshot_is_isolated_from_later_mutations():
    game = build_engine()
    game.add_villain(ScriptedVillain("S", 6, 6))
    view = game._build_view()
    villain = game.villains[0]
    villain.x, villain.y = 2, 2  # world moves AFTER the snapshot...
    assert view.is_tile_passable(2, 2) is True  # ...but the snapshot is frozen
    assert view.is_tile_passable(6, 6) is False


def test_distance_to_hero_is_manhattan():
    world, view = make_world()
    game = build_engine()  # hero at (1,1)
    v = ScriptedVillain("V", 4, 3)
    game.add_villain(v)
    assert game._build_view().distance_to_hero(v) == 5  # |4-1| + |3-1|
    assert view.distance_to_hero(world.villains[0]) == 3  # "East" (4,1) vs (1,1)


def test_direction_larger_axis_wins():
    game = build_engine()
    v = ScriptedVillain("V", 1, 4)  # hero (1,1) is due NORTH of (1,4)
    game.add_villain(v)
    assert game._build_view().get_direction_toward_hero(v) == (0, -1)


def test_direction_tie_breaks_toward_x_axis():
    game = build_engine()
    v = ScriptedVillain("V", 3, 3)  # hero (1,1) lies NW: dx=-2, dy=-2 -> x tie
    game.add_villain(v)
    assert game._build_view().get_direction_toward_hero(v) == (-1, 0)


def test_direction_is_normalized():
    world, view = make_world()
    game = build_engine()
    v = ScriptedVillain("V", 8, 1)  # hero (1,1) is far WEST of (8,1)
    game.add_villain(v)
    step = game._build_view().get_direction_toward_hero(v)
    assert step == (-1, 0)
    assert view.get_direction_toward_hero(world.villains[1]) == (-1, 0)  # "Diag" (3,3): dx=-2, dy=-2 tie -> x


def test_passability_rules():
    _, view = make_world()
    assert view.is_tile_passable(5, 5) is True   # empty
    assert view.is_tile_passable(2, 2) is False  # wall
    assert view.is_tile_passable(1, 3) is False  # npc
    assert view.is_tile_passable(4, 1) is False  # living villain
    assert view.is_tile_passable(1, 1) is False  # the hero blocks too
    assert view.is_tile_passable(-1, 1) is False  # out of bounds
    assert view.is_tile_passable(10, 10) is False  # out of bounds


def test_get_hero_position():
    _, view = make_world()
    assert view.get_hero_position() == (1, 1)
