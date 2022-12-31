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
        assert STARTING_ITEMS == '  Starting items', f'Wrong monkey definition: {lines}'
        items = list(map(int, itemsdef.strip().split(',')))
        return cls(items)

@dataclass
class Operation:
    raw: str

    @classmethod
    def from_spec(cls, spec):
        return cls(spec)

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
        assert MONKEY == 'Monkey', f'Wrong monkey name: {lines[0]}'
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
