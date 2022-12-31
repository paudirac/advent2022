import pytest

from dataclasses import dataclass
from collections import deque

from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.monkeys import (
    monkeys,
    is_blank,
    Operation,
    Test,
    Troop,
    Monkey,
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

    assert mks[0].items == deque([79, 98])
    assert mks[1].items == deque([54, 65, 75, 74])
    assert mks[2].items == deque([79, 60, 97])
    assert mks[3].items == deque([74])

    assert mks[0].operation(2) == 38
    assert mks[0].test(23)
    assert mks[0].test(46)
    assert not mks[0].test(24)

def test_operation():
    with pytest.raises(Exception):
        Operation.from_spec("  Tperation: new = old * 19")
    assert Operation.from_spec("  Operation: new = old * 19")(1) == 19
    assert Operation.from_spec("  Operation: new = old * 19")(2) == 38
    assert Operation.from_spec("  Operation: new = old + 6")(0) == 6
    assert Operation.from_spec("  Operation: new = old + 6")(6) == 12

def test_test():
    with pytest.raises(Exception):
        Test.from_spec(
            "  Protest: divisible by 17",
            "    If true: throw to monkey 0",
            "    If false: throw to monkey 1",
        )
    test = Test.from_spec(
        "  Test: divisible by 17",
        "    If true: throw to monkey 0",
        "    If false: throw to monkey 1",
    )
    assert not test(1)
    assert test(17)
    assert not test(18)
    assert test(2 * 17)

    assert test.monkey_iftrue == 0
    assert test.monkey_iffalse == 1

@dataclass
class TroopStub:
    mk: Monkey


def test_monkey_turn_algorithm():
    mk = Monkey.from_lines(
"""Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3""".split('\n'))

    assert mk.current_item == None
    mk._inspect()
    assert mk.current_item == 79
    mk._operate()
    assert mk.current_item == 1501
    mk._relieve()
    assert mk.current_item == 500
    assert mk._destination() == 3



@dataclass
class MonkeyStub:
    called: bool = False

    def turn(self, troop):
        self.called = True

def test_toop_round():
    mk0 = MonkeyStub()
    mk1 = MonkeyStub()
    assert not mk0.called
    assert not mk1.called

    troop = Troop([(0, mk0), (1, mk1)])
    troop.round()

    assert mk0.called
    assert mk1.called
