from dataclasses import dataclass, field
from collections import namedtuple, deque
from functools import cache, wraps, reduce
import math
import enum
import typing
import re
import time

from utils import get_logger, flatten
log = get_logger(__name__)

def is_blank(line):
    return len(line) == 0


def debug(fn):
    @wraps(fn)
    def debugee(*args, **kwargs):
        start = time.time()
        try:
            ret = fn(*args, **kwargs)
        except Exception as e:
            log.error(f"Error in {fn.__name__}({','.join(map(str,args))})")
            raise e
        end = time.time()
        ms = end - start
        log.debug(f"{fn.__name__}({','.join(map(str,args))}) -> {ret} {ms:0.3f}")
        return ret
    return debugee



@cache
def prime_factors(n):
    factors = [1]
    i = 2
    while i *  i <= n:
        if n % i == 0:
            factors.append(i)
            n = int(n / i)
        else:
            i += 1
    if n > 1:
        factors.append(n)
    return factors

@cache
def make_int(n):
    factors = prime_factors(n)
    return Int(
        factors=factors,
        divisors=set(factors),
    )

Add = namedtuple('Sum', 'n')
Mul = namedtuple('Prod', 'n')

def fold_history(init, history):
    val = init
    for op in history:
        match op:
            case Add(n):
                val += n
            case Prod(n):
                val *= n
    return val


def product(factors):
    return reduce(lambda a, b: a * b, factors, 1)


@cache
def _mul(a: 'Int', b: 'Int'):
    factors = a.factors + b.factors
    return Int(
        factors=factors,
        divisors=set(factors),
    )

@cache
def _add(a: 'Int', b: 'Int'):
    n = a.n + b.n
    return make_int(n)


@dataclass(frozen=True)
class Int:
    factors: typing.List[int]
    divisors: typing.Set[int]

    @property
    def n(self):
        return product(self.factors)

    def __add__(self, other):
        assert isinstance(other, Int), f'Expecting Int, got {type(other)}'
        return _add(self, other)

    def __mul__(self, other):
        assert isinstance(other, Int), f'Expecting Int, got {type(other)}'
        return _mul(self, other)

    def __floordiv__(self, other: int):
        new_factors = self.factors
        if other in self.factors:
            i = new_factors.index(other)
            del new_factors[i]
        return Int(
            factors=new_factors,
            divisors=set(new_factors),
        )
        # n = self.n // other.n
        # return self.from_int(n)

    @classmethod
    def from_str(cls, s):
        return cls.from_int(int(s))

    @classmethod
    def from_int(cls, n):
        return make_int(n)

    def __hash__(self):
        return hash(''.join(map(str, self.factors)))

    def divisible_by(self, n):
        return n in self.divisors

class Items(deque):

    @classmethod
    def from_spec(cls, spec):
        STARTING_ITEMS, itemsdef = spec.split(':')
        assert STARTING_ITEMS == '  Starting items', f'Wrong Items spec: "{spec}"'
        items = list(map(Int.from_str, itemsdef.strip().split(',')))
        return cls(items)

@cache
def add(a, b): return a + b

@cache
def prod(a, b): return a * b

@cache
def do_operation(operation, old, operand1, operand2):
    op1 = locals().get(operand1, None)
    op2 = locals().get(operand2, None)
    if op1 is None:
        op1 = Int.from_str(operand1)
    if op2 is None:
        op2 = Int.from_str(operand2)
    return operation(op1, op2)


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
        return do_operation(self.operation, old, self.operand1, self.operand2)
        # op1 = locals().get(self.operand1, None)
        # op2 = locals().get(self.operand2, None)
        # if op1 is None:
        #     op1 = Int.from_str(self.operand1)
        # if op2 is None:
        #     op2 = Int.from_str(self.operand2)
        # return self.operation(op1, op2)


    def __repr__(self):
        return f'Operation({self.operand1} {self.operation_name} {self.operand2})'


RE_DIVISIBLE_BY = re.compile(r'\s*Test: divisible by (\d+)')
RE_IF_TRUE = re.compile(r'\s*If true: throw to monkey (\d+)')
RE_IF_FALSE = re.compile(r'\s*If false: throw to monkey (\d+)')




@cache
def divisible_by(divisor, worry_level):
    assert isinstance(worry_level, Int), f'Expecting Int, got {worry_level} of type {type(worry_level)}'
    return worry_level.divisible_by(divisor)


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
        return divisible_by(self.divisible_by, worry_level)

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
        return f'Monkey({self.name}, {self.items!r}, {self.operation!r}, {self.test!r}, {self.current_item})'

    def _inspect(self):
        self.current_item = self.items.popleft()
        self.inspected_count += 1

    def _operate(self):
        self.current_item = self.operation(self.current_item)

    def _relieve(self):
        self.current_item = self.current_item // 3

    def _destination(self):
        return self.test.monkey_iftrue if self.test(self.current_item) else self.test.monkey_iffalse

    def turn(self, monkeys, relieve=True):
        for item in self.items.copy():
            self._inspect()
            self._operate()
            if relieve:
                self._relieve()
            dest = self._destination()
            monkeys._throw(self.current_item, dest)
        #log.debug(f'{self=}')

class Troop(dict):

    def round(self, relieve=True):
        for mk in self.values():
            mk.turn(self, relieve=relieve)

    def rounds(self, n, relieve=True):
        for i in range(n):
            self.round(relieve=relieve)
            log.debug(f'{i}: {self.monkey_business}')

    def _throw(self, item, dest):
        self[dest].items.append(item)

    def __iter__(self):
        return iter(self.values())

    @property
    def monkey_business(self):
        activity = sorted([mk.inspected_count for mk in self], reverse=True)
        first, second = activity[:2]
        return first * second

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


def monkey_business(lines, rounds=20, relieve=True):
    mks = monkeys(lines)
    mks.rounds(rounds, relieve=relieve)
    return mks.monkey_business

def monkey_business_no_relieve(lines):
    return monkey_business(lines, rounds=10000, relieve=False)
