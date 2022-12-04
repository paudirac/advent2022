import pytest
from utils import read_test_input, get_logger

log = get_logger(__name__)

from advent2022.camp import (
    count_pairs_with_overlapping_ranges,
    Range,
    Section,
    pair_elves,
    Pair,
)

example = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

lines = read_test_input(example)

def test_lines():
    assert len(lines) == 6

def xtest_count_pairs_with_overlapping_ranges():
    assert count_pairs_with_overlapping_ranges(lines) == 2

def test_range():
    assert Range.from_spec('2-4') == Range.from_spec('2-4')
    spec1, lower1, upper1 = Range.from_spec('2-4')
    assert spec1 == '2-4'
    assert lower1 == 2
    assert upper1 == 4

    spec2, lower2, upper2 = Range.from_spec('6-8')
    assert spec2 == '6-8'
    assert lower2 == 6
    assert upper2 == 8


def test_range_display():
    bounds = Range.from_spec('1-9')
    rng = Range.from_spec('2-4')
    assert rng.display(bounds) == '.XXX.....'

def test_range_sections():
    range11 = Range.from_spec('2-4')
    assert range11.sections == [Section(2), Section(3), Section(4)]

    range12 = Range.from_spec('6-8')
    assert range12.sections == [Section(6), Section(7), Section(8)]

    range21 = Range.from_spec('2-3')
    assert len(range21.sections) == 2
    range22 = Range.from_spec('4-5')
    assert len(range22.sections) == 2

    range31 = Range.from_spec('5-7')
    assert len(range31.sections) == 3
    assert range31.sections == [Section(5), Section(6), Section(7)]
    range32 = Range.from_spec('7-9')
    assert len(range32.sections) == 3
    assert range32.sections == [Section(7), Section(8), Section(9)]

def test_pairs():
    pairs = pair_elves(lines)
    assert len(pairs) == 6

def xtest_pair_fully_contained():
    assert not Pair.from_line("2-4,6-8").fully_contained
    assert not Pair.from_line("2-3,4-5").fully_contained
    assert not Pair.from_line("5-7,7-9").fully_contained
    assert Pair.from_line("2-8,3-7").fully_contained
    assert Pair.from_line("6-6,4-6").fully_contained
    assert not Pair.from_line("2-6,4-8").fully_contained

def test_range_contains():
    range11 = Range.from_spec('2-4')
    range12 = Range.from_spec('6-8')
    assert range11 not in range12
    assert range12 not in range11

    range41 = Range.from_spec('2-8')
    range42 = Range.from_spec('3-7')
    assert range41 not in range42
    assert range42 in range41
