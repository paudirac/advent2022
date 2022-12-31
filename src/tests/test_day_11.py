import pytest

from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.monkeys import (
    monkeys,
    is_blank,
    Operation,
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

def test_split_colon():
    assert "Monkey 0:".split(':') == ['Monkey 0', '']
    assert "Starting items: 79, 98".split(':') == ['Starting items', ' 79, 98']

def test_monkeys():
    mks = monkeys(lines)
    assert len(mks) == 4
    assert mks[0].name == 0
    assert mks[1].name == 1
    assert mks[2].name == 2
    assert mks[3].name == 3

    assert mks[0].items == [79, 98]
    assert mks[1].items == [54, 65, 75, 74]
    assert mks[2].items == [79, 60, 97]
    assert mks[3].items == [74]

def test_operation():
    with pytest.raises(Exception):
        Operation.from_spec("  Tperation: new = old * 19")
    assert Operation.from_spec("  Operation: new = old * 19")(1) == 19
    assert Operation.from_spec("  Operation: new = old * 19")(2) == 38
    assert Operation.from_spec("  Operation: new = old + 6")(0) == 6
    assert Operation.from_spec("  Operation: new = old + 6")(6) == 12
