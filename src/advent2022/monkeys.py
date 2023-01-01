from dataclasses import dataclass, field
from collections import namedtuple, deque
from functools import cache
import math
import enum
import typing
import re

from utils import get_logger, flatten
log = get_logger(__name__)

def is_blank(line):
    return len(line) == 0


class Items(deque):

    @classmethod
    def from_spec(cls, spec):
        STARTING_ITEMS, itemsdef = spec.split(':')
        assert STARTING_ITEMS == '  Starting items', f'Wrong Items spec: "{spec}"'
        items = list(map(int, itemsdef.strip().split(',')))
        return cls(items)

def add(a, b): return a + b
def prod(a, b): return a * b

@dataclass
class Operation:
    operand1: str
    operand2: str
    operation: typing.Callable[int, int]
    operation_name: str

    @classmethod
    def from_spec(cls, spec):
        OPERATION, expression = spec.split(':')
        assert OPERATION == '  Operation', f'Wrong Operation spec: "{spec}"'
        left, right = expression.split('=')
        assert left == ' new ', f'Wrong expression on Operation spec: "{expression}"'
        operand1, operation_name, operand2 = right.strip().split()
        assert operation_name in ['+', '*'], f'Unknown operation: "{operation_name}" in expression "{expression}"'
        operation = add if operation_name == '+' else prod
        return cls(operand1, operand2, operation, operation_name)

    def __call__(self, old):
        op1 = locals().get(self.operand1, None)
        op2 = locals().get(self.operand2, None)
        if op1 is None:
            op1 = int(self.operand1)
        if op2 is None:
            op2 = int(self.operand2)
        return self.operation(op1, op2)

    def __repr__(self):
        return f'Operation({self.operand1} {self.operation_name} {self.operand2})'


RE_DIVISIBLE_BY = re.compile(r'\s*Test: divisible by (\d+)')
RE_IF_TRUE = re.compile(r'\s*If true: throw to monkey (\d+)')
RE_IF_FALSE = re.compile(r'\s*If false: throw to monkey (\d+)')

@dataclass
class Test:
    __test__ = False # prevent pytest to collect this class
    divisible_by: int
    monkey_iftrue: int
    monkey_iffalse: int

    @classmethod
    def from_spec(cls, test, iftrue, iffalse):
        m = RE_DIVISIBLE_BY.match(test)
        assert m is not None, f'Invalid Test spec: "{test}"'
        divisible_by = int(m[1])

        mtrue = RE_IF_TRUE.match(iftrue)
        assert mtrue is not None, f'Invalid If true spec: "{iftrue}"'
        monkey_if_true = int(mtrue[1])

        mfalse = RE_IF_FALSE.match(iffalse)
        assert mfalse is not None, f'Invalid If false spec: "{iffalse}"'
        monkey_if_false = int(mfalse[1])

        return cls(divisible_by, monkey_if_true, monkey_if_false)

    def __call__(self, worry_level):
        return worry_level % self.divisible_by == 0

    def __repr__(self):
        return f'Test(divisible by {self.divisible_by}, {self.monkey_iftrue}, {self.monkey_iffalse})'



@dataclass
class Monkey:
    name: int
    items: Items
    operation: Operation
    test: Test
    current_item: int = None
    inspected_count = 0

    @classmethod
    def from_lines(cls, lines):
        assert len(lines) == 6, f'Wrong monkey definition {lines}'
        MONKEY, name = lines[0].split(':')[0].split()
        assert MONKEY == 'Monkey', f'Wrong monkey name spec: "{lines[0]}"'
        items = Items.from_spec(lines[1])
        operation = Operation.from_spec(lines[2])
        test = Test.from_spec(lines[3], lines[4], lines[5])
        return cls(int(name), items, operation, test)

    def __repr__(self):
        return f'Monkey({self.name}, {self.items!r}, {self.operation!r}, {self.test!r})'

    def _inspect(self):
        self.current_item = self.items.popleft()
        self.inspected_count += 1

    def _operate(self):
        self.current_item = self.operation(self.current_item)

    def _relieve(self):
        self.current_item = math.floor(self.current_item / 3)

    def _destination(self):
        return self.test.monkey_iftrue if self.test(self.current_item) else self.test.monkey_iffalse


    def turn(self, monkeys):
        for item in self.items.copy():
            self._inspect()
            self._operate()
            self._relieve()
            dest = self._destination()
            monkeys._throw(self.current_item, dest)

class Troop(dict):

    def round(self):
        for mk in self.values():
            mk.turn(self)

    def _throw(self, item, dest):
        self[dest].items.append(item)

    def __iter__(self):
        return iter(self.values())


def monkeys(lines):
    mks = []
    monkey_lines = []
    for i, line in enumerate(lines):
        if is_blank(line):
            mks.append(Monkey.from_lines(monkey_lines))
            monkey_lines = []
        else:
            monkey_lines.append(line)
    else:
        mks.append(Monkey.from_lines(monkey_lines))
    return Troop([(m.name, m) for m in mks])


def monkey_business(lines):
    mks = monkeys(lines)
    for _ in range(20):
        mks.round()
    activity = sorted([mk.inspected_count for mk in mks], reverse=True)
    first, second = activity[:2]
    return first * second
