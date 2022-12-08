import pytest
from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

from advent2022.forest import (
    height_map,
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
