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
    monkey_business,
    monkey_business_no_relieve,
    divisible_by_17,
    divisible_by_3,
    divisible_by_19,
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
    mks = monkeys(lines)

    mk0 = mks[0]
    assert mk0.items == deque([79, 98])

    mk3 = mks[3]
    assert mk3.items == deque([74])

    assert mk0.current_item == None
    mk0._inspect()
    assert mk0.current_item == 79
    mk0._operate()
    assert mk0.current_item == 1501
    mk0._relieve()
    assert mk0.current_item == 500
    assert mk0._destination() == 3

    mks._throw(mk0.current_item, 3)
    assert mk0.items == deque([98])
    assert mk3.items == deque([74, 500])

def test_monkey_turn():
    mks = monkeys(lines)

    mk0 = mks[0]
    assert mk0.items == deque([79, 98])

    mk3 = mks[3]
    assert mk3.items == deque([74])

    mk0.turn(mks)
    assert mk0.items == deque([])
    assert mk3.items == deque([74, 500, 620])


@dataclass
class MonkeyStub:
    called: bool = False

    def turn(self, troop, relieve=True):
        self.called = True

def test_troop_round():
    mk0 = MonkeyStub()
    mk1 = MonkeyStub()
    assert not mk0.called
    assert not mk1.called

    troop = Troop([(0, mk0), (1, mk1)])
    troop.round()

    assert mk0.called
    assert mk1.called

def test_round():
    mks = monkeys(lines)
    mks.round()
    assert mks[0].items == deque([20, 23, 27, 26])
    assert mks[1].items == deque([2080, 25, 167, 207, 401, 1046])
    assert mks[2].items == deque([])
    assert mks[3].items == deque([])

    mks.rounds(19)

    assert mks[0].items == deque([10, 12, 14, 26, 34])
    assert mks[1].items == deque([245, 93, 53, 199, 115])
    assert mks[2].items == deque([])
    assert mks[3].items == deque([])

    assert mks[0].inspected_count == 101
    assert mks[1].inspected_count == 95
    assert mks[2].inspected_count == 7
    assert mks[3].inspected_count == 105

def test_monkey_business():
    assert monkey_business(lines) == 10605

def xtest_monkey_business_no_relieve():
    assert monkey_business_no_relieve(lines) == 2713310158

def test_divisible_by_17():
    assert divisible_by_17(17)
    assert divisible_by_17(289)
    assert not divisible_by_17(18)
    assert not divisible_by_17(290)

def test_divisible_by_3():
    assert not divisible_by_3(17)
    assert divisible_by_3(3)
    assert divisible_by_3(21)
    assert divisible_by_3(1121031)
    assert not divisible_by_3(3456194)

def test_divisible_by_19():
    assert not divisible_by_19(18)
    assert divisible_by_19(19)
    assert not divisible_by_19(20)
    assert divisible_by_19(2337)
    assert not divisible_by_19(2338)
