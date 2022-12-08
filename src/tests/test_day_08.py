import pytest
from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

from advent2022.forest import (
    height_map,
    Tree,
    count_visible_trees,
)

example = """
30373
25512
65332
33549
35390
"""

lines = read_test_input(example)

def test_lines():
    assert len(lines) == 5

def test_height_map():
    hm = height_map(lines)
    assert hm.size == (5, 5)

    assert hm[(0, 0)].height == 3

    assert hm[(1, 2)].height == 5
    assert hm[(2, 1)].height == 5

    assert hm[(3, 1)].height == 1
    assert hm[(1, 3)].height == 3

def test_visible_edges():
    hm = height_map(lines)

    # left edge
    assert hm[(0, 0)].visible(hm) == True
    assert hm[(0, 1)].visible(hm) == True
    assert hm[(0, 2)].visible(hm) == True
    assert hm[(0, 3)].visible(hm) == True
    assert hm[(0, 4)].visible(hm) == True

    # right edge
    assert hm[(4, 0)].visible(hm) == True
    assert hm[(4, 1)].visible(hm) == True
    assert hm[(4, 2)].visible(hm) == True
    assert hm[(4, 3)].visible(hm) == True
    assert hm[(4, 4)].visible(hm) == True

    # top edge
    assert hm[(0, 0)].visible(hm) == True
    assert hm[(1, 0)].visible(hm) == True
    assert hm[(2, 0)].visible(hm) == True
    assert hm[(3, 0)].visible(hm) == True
    assert hm[(4, 0)].visible(hm) == True

    # bottom edge
    assert hm[(0, 4)].visible(hm) == True
    assert hm[(1, 4)].visible(hm) == True
    assert hm[(2, 4)].visible(hm) == True
    assert hm[(3, 4)].visible(hm) == True
    assert hm[(4, 4)].visible(hm) == True

def test_left():
    hm = height_map(lines)
    # top left 5 (1, 1)
    assert hm[(1, 1)].left(hm) == [
        hm[(0, 1)],
    ]

def test_right():
    hm = height_map(lines)
    # top left 5 (1, 1)
    assert hm[(1, 1)].right(hm) == [
        hm[(2, 1)],
        hm[(3, 1)],
        hm[(4, 1)],
    ]

def test_top():
    hm = height_map(lines)
    # top left 5 (1, 1)
    assert hm[(1, 1)].top(hm) == [
        hm[(1, 0)],
    ]

def bottom():
    hm = height_map(lines)
    # top left 5 (1, 1)
    assert hm[(1, 1)].bottom(hm) == [
        hm[(1, 2)],
        hm[(1, 3)],
        hm[(1, 4)],
    ]

def test_less_than():
    t1 = Tree(object(), 5)
    t2 = Tree(object(), 4)
    assert t2 < t1

def test_visible_from_left():
    hm = height_map(lines)
    # top left 5 (1, 1)
    assert hm.visible_from_left(hm[(1, 1)])

def test_visible_from_top():
    hm = height_map(lines)
    # top left 5 (1, 1)
    assert hm.visible_from_top(hm[(1, 1)])

def test_visible_from_right():
    hm = height_map(lines)
    # left-middle 5 (1, 2)
    assert hm.visible_from_right(hm[(1, 2)])

    assert not hm.visible_from_right(hm[(1, 1)])

def test_visible_from_bottom():
    hm = height_map(lines)
    # bottom-middle 5 (2, 3)
    assert hm.visible_from_bottom(hm[(2, 3)])

    assert not hm.visible_from_bottom(hm[(1, 1)])

def test_visible():
    hm = height_map(lines)

    assert hm[(1, 1)].visible(hm)
    assert hm[(1, 2)].visible(hm)
    assert hm[(2, 3)].visible(hm)

    # top-right 1 (3, 1)
    assert not hm[(3, 1)].visible(hm)

def test_visible_trees():
    hm = height_map(lines)
    visible = hm.visible_trees
    assert len(hm.visible_trees) == 21

def test_count_visible_trees():
    assert count_visible_trees(lines) == 21
