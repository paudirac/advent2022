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
