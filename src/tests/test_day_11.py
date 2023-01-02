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
    prime_factors,
    divisible_by,
    Int,
    Add,
    Mul,
    fold_history,
    product,
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

    assert mks[0].items == deque(map(Int.from_int, [79, 98]))
    assert mks[1].items == deque(map(Int.from_int, [54, 65, 75, 74]))
    assert mks[2].items == deque(map(Int.from_int, [79, 60, 97]))
    assert mks[3].items == deque(map(Int.from_int, [74]))

    assert mks[0].operation(Int.from_int(2)) == Int.from_int(38)
    assert mks[0].test(Int.from_int(23))
    assert mks[0].test(Int.from_int(46))
    assert not mks[0].test(Int.from_int(24))

def test_Int():
    i = Int.from_int(42)
    assert i.n == 42
    i = i + Int.from_int(3)
    assert i.n == 45
    j = Int.from_int(10)
    j = j * Int.from_int(4)
    assert j.n == 40
    j = j + Int.from_int(2)
    assert j.n == 42

def test_operation():
    with pytest.raises(Exception):
        Operation.from_spec("  Tperation: new = old * 19")
    assert Operation.from_spec("  Operation: new = old * 19")(Int.from_int(1)) == Int.from_int(19)
    assert Operation.from_spec("  Operation: new = old * 19")(Int.from_int(2)) == Int.from_int(38)
    assert Operation.from_spec("  Operation: new = old + 6")(Int.from_int(0)) == Int.from_int(6)
    assert Operation.from_spec("  Operation: new = old + 6")(Int.from_int(6)) == Int.from_int(12)

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
    assert not test(Int.from_int(1))
    assert test(Int.from_int(17))
    assert not test(Int.from_int(18))
    assert test(Int.from_int(2 * 17))

    assert test.monkey_iftrue == 0
    assert test.monkey_iffalse == 1

@dataclass
class TroopStub:
    mk: Monkey


def test_monkey_turn_algorithm():
    mks = monkeys(lines)

    mk0 = mks[0]
    assert mk0.items == deque(map(Int.from_int, [79, 98]))

    mk3 = mks[3]
    assert mk3.items == deque(map(Int.from_int, [74]))

    assert mk0.current_item == None
    mk0._inspect()
    assert mk0.current_item == Int.from_int(79)
    mk0._operate()
    assert mk0.current_item == Int.from_int(1501)
    mk0._relieve()
    assert mk0.current_item == Int.from_int(500)
    assert mk0._destination() == 3

    mks._throw(mk0.current_item, 3)
    assert mk0.items == deque(map(Int.from_int, [98]))
    assert mk3.items == deque(map(Int.from_int, [74, 500]))

def test_monkey_turn():
    mks = monkeys(lines)

    mk0 = mks[0]
    assert mk0.items == deque(map(Int.from_int, [79, 98]))

    mk3 = mks[3]
    assert mk3.items == deque(map(Int.from_int, [74]))

    mk0.turn(mks)
    assert mk0.items == deque([])
    assert mk3.items == deque(map(Int.from_int, [74, 500, 620]))


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

def lmap(constructor, iterable):
    return list(map(constructor, iterable))

def test_round():
    mks = monkeys(lines)
    mks.round()
    assert mks[0].items == deque(map(Int.from_int, [20, 23, 27, 26]))
    assert mks[1].items == deque(map(Int.from_int, [2080, 25, 167, 207, 401, 1046]))
    assert mks[2].items == deque([])
    assert mks[3].items == deque([])

    mks.rounds(19)

    assert mks[0].items == deque(map(Int.from_int, [10, 12, 14, 26, 34]))
    assert mks[1].items == deque(map(Int.from_int, [245, 93, 53, 199, 115]))
    assert mks[2].items == deque([])
    assert mks[3].items == deque([])

    assert mks[0].inspected_count == 101
    assert mks[1].inspected_count == 95
    assert mks[2].inspected_count == 7
    assert mks[3].inspected_count == 105

def xtest_monkey_business():
    assert monkey_business(lines) == 10605

def xtest_monkey_business_no_relieve():
    assert monkey_business_no_relieve(lines) == 2713310158

def test_divisible_by_17():
    assert divisible_by(17, Int.from_int(17))
    assert divisible_by(17, Int.from_int(289))
    assert not divisible_by(17, Int.from_int(18))
    assert not divisible_by(17, Int.from_int(290))

def test_divisible_by_3():
    assert not divisible_by(3, Int.from_int(17))
    assert divisible_by(3, Int.from_int(3))
    assert divisible_by(3, Int.from_int(21))
    assert divisible_by(3, Int.from_int(1121031))
    assert not divisible_by(3, Int.from_int(3456194))

def test_divisible_by_19():
    assert not divisible_by(19, Int.from_int(18))
    assert divisible_by(19, Int.from_int(19))
    assert not divisible_by(19, Int.from_int(20))
    assert divisible_by(19, Int.from_int(2337))
    assert not divisible_by(19, Int.from_int(2338))


def test_prime_factors():
    assert prime_factors(1) == [1]
    assert prime_factors(2) == [1, 2]
    assert prime_factors(3) == [1, 3]
    assert prime_factors(19) == [1, 19]
    assert prime_factors(1121031) == [1, 3, 3, 17, 17, 431]

    assert 1 == product([1])
    assert 2 == product([1, 2])
    assert 3 == product([1, 3])
    assert 19 == product([1, 19])
    assert 1121031 == product([1, 3, 3, 17, 17, 431])

def test_any_number_is_decomposable_as_a_product_of_primes():
    n = Int.from_int(42)
    assert n.n == 42

    a = Int.from_int(10)
    b = Int.from_int(4)
    c = Int.from_int(2)

    assert (a * b).n == 40
    assert (a + b).n == 14

    d = a * b + c
    assert d.n == 42
