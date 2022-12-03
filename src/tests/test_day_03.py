import pytest
from utils import read_test_input, get_logger

log = get_logger(__name__)

from advent2022.rucksacks import (
    Rucksack,
    Compartment,
    halves,
    Item,
    sum_priorities_of_common_items,
    group_elves,
    Elf,
    Group,
    Badge,
    sum_badges_priorities,
    sum_priorities_elf_groups,
)

example = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

lines = read_test_input(example)

def test_read_example():
    assert len(lines) == 6

def test_halve():
    assert halves('ab') == ('a', 'b')
    assert halves('vJrwpWtwJgWrhcsFMMfFFhFp') == ('vJrwpWtwJgWr', 'hcsFMMfFFhFp')
    with pytest.raises(Exception):
        halves('abc')

def test_compartment():
    assert Compartment.from_string('vJrwpWtwJgWr') == Compartment.from_string('vJrwpWtwJgWr')
    assert not Compartment.from_string('vJrwpWtwJgWr') == Compartment.from_string('hcsFMMfFFhFp')

def test_rucksack():
    rucksack = Rucksack.from_line('vJrwpWtwJgWrhcsFMMfFFhFp')
    assert rucksack[0] == Compartment.from_string('vJrwpWtwJgWr')
    assert rucksack[1] == Compartment.from_string('hcsFMMfFFhFp')

    rucksack2 = Rucksack.from_line('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
    assert rucksack2[0] == Compartment.from_string('jqHRNqRjqzjGDLGL')
    assert rucksack2[1] == Compartment.from_string('rsFMfFZSrLrFZsSL')

def test_common_items():
    rucksack1 = Rucksack.from_line('vJrwpWtwJgWrhcsFMMfFFhFp')
    assert rucksack1.common_items() == [Item('p')]

    rucksack2 = Rucksack.from_line('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
    assert rucksack2.common_items() == [Item('L')]

    rucksack3 = Rucksack.from_line('PmmdzqPrVvPwwTWBwg')
    assert rucksack3.common_items() == [Item('P')]

    rucksack4 = Rucksack.from_line('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn')
    assert rucksack4.common_items() == [Item('v')]

    rucksack5 = Rucksack.from_line('ttgJtRGJQctTZtZT')
    assert rucksack5.common_items() == [Item('t')]

    rucksack6 = Rucksack.from_line('CrZsJsPPZsGzwwsLwLmpwMDw')
    assert rucksack6.common_items() == [Item('s')]

def test_priorities():
    lowercase_priorities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    lowercase_items = [Item(c) for c in 'abcdefghijklmnopqrstuvwxyz']
    lowercase_items_priorities = [item.priority for item in lowercase_items]
    assert lowercase_priorities == lowercase_items_priorities

    uppercase_priorities = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
    uppercase_items = [Item(c) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    uppercase_items_priorities = [item.priority for item in uppercase_items]
    assert uppercase_priorities == uppercase_items_priorities

def test_common_items_priorities():
    rucksack1 = Rucksack.from_line('vJrwpWtwJgWrhcsFMMfFFhFp')
    assert rucksack1.common_items()[0].priority == 16

    rucksack2 = Rucksack.from_line('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
    assert rucksack2.common_items()[0].priority == 38

    rucksack3 = Rucksack.from_line('PmmdzqPrVvPwwTWBwg')
    assert rucksack3.common_items()[0].priority == 42

    rucksack4 = Rucksack.from_line('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn')
    assert rucksack4.common_items()[0].priority == 22

    rucksack5 = Rucksack.from_line('ttgJtRGJQctTZtZT')
    assert rucksack5.common_items()[0].priority == 20

    rucksack6 = Rucksack.from_line('CrZsJsPPZsGzwwsLwLmpwMDw')
    assert rucksack6.common_items()[0].priority == 19

def test_sum_priorities_of_common_items():
    assert sum_priorities_of_common_items(lines) == 157

def test_elf():
    elf1 = Elf.from_line('vJrwpWtwJgWrhcsFMMfFFhFp')
    elf2 = Elf.from_line('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
    elf3 = Elf.from_line('PmmdzqPrVvPwwTWBwg')
    assert elf1 != elf2
    assert elf2 != elf3
    assert elf3 != elf1

def test_elf_group():
    elf1 = Elf.from_line('vJrwpWtwJgWrhcsFMMfFFhFp')
    elf2 = Elf.from_line('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
    elf3 = Elf.from_line('PmmdzqPrVvPwwTWBwg')
    group = Group.from_elves(elf1, elf2, elf3)
    assert group.badge == Badge('r')

    elf4 = Elf.from_line('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn')
    elf5 = Elf.from_line('ttgJtRGJQctTZtZT')
    elf6 = Elf.from_line('CrZsJsPPZsGzwwsLwLmpwMDw')
    group2 = Group.from_elves(elf4, elf5, elf6)
    assert group2.badge == Badge('Z')

def test_badge_priority():
    assert Badge('r').priority == 18
    assert Badge('Z').priority == 52

def test_sum_badges_priorities():
    assert sum_badges_priorities(Badge('r'), Badge('Z')) == 70

def test_grups_of_trhee_elves():
    groups = group_elves(lines)
    assert len(groups) == 2

def test_sum_priorities_elf_groups():
    assert sum_priorities_elf_groups(lines) == 70
