import pytest

from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.monkeys import (
    monkeys,
    is_blank,
)

example = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
lines = read_test_input(example)

def test_read_example():
    assert len(lines) == 27

def test_is_blank():
    assert is_blank("")

def test_monkeys():
    assert len(monkeys(lines)) == 4
