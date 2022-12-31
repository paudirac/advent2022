from dataclasses import dataclass, field
from collections import namedtuple
from functools import cache
import math
import enum
import typing

from utils import get_logger, flatten
log = get_logger(__name__)

def is_blank(line):
    return len(line) == 0


class Items(list):

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

    def __str__(self):
        return f'Operation({self.operand1} {self.operation_name} {self.operand2})'

@dataclass
class Test:
    raw_test: str
    raw_iftrue: str
    raw_iffalse: str

    @classmethod
    def from_spec(cls, test, iftrue, iffalse):
        return cls(test, iftrue, iffalse)


@dataclass
class Monkey:
    name: int
    items: Items
    operation: Operation
    test: Test

    @classmethod
    def from_lines(cls, lines):
        assert len(lines) == 6, f'Wrong monkey definition {lines}'
        MONKEY, name = lines[0].split(':')[0].split()
        assert MONKEY == 'Monkey', f'Wrong monkey name spec: "{lines[0]}"'
        items = Items.from_spec(lines[1])
        operation = Operation.from_spec(lines[2])
        test = Test(lines[3], lines[4], lines[5])
        return cls(int(name), items, operation, test)


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
    log.debug(f'{mks=}')
    return mks
