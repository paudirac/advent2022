from dataclasses import dataclass, field
from collections import namedtuple
from functools import cache
import math
import enum

from utils import get_logger, flatten
log = get_logger(__name__)


class CPU:

    def __init__(self, x):
        self.history = []
        self.X = x
        self.ticks = 0

    def run(self, program):
        for instruction in program:
            self._run_instruction(instruction)

    def _run_instruction(self, instruction):
        bytecodes = compile_instruction(instruction)
        for bytecode in bytecodes:
            match bytecode:
                case BC.Tick:
                    self._tick()
                case BC.Store:
                    self._store()
                case BC.Add1:
                    self._add1()
                case BC.Sub1:
                    self._sub1()

    def _tick(self):
        self.ticks += 1

    def _store(self):
        state = (self.ticks, self.X)
        self.history.append(state)

    def _add1(self):
        self.X += 1

    def _sub1(self):
        self.X -= 1


def make_cpu():
    return CPU(x=1)

def sentinel(name):
    def __str__(self):
        return name
    sentinel_type = type(
        name,
        (object, ),
        {
            "__repr__": __str__,
        })
    return sentinel_type()

Noop = sentinel('Noop')
AddX = namedtuple('AddX', 'value')

def parse_instruction(line):
    match line.split():
        case ['noop']:
            return Noop
        case ['addx', value]:
            return AddX(int(value))
        case _:
            raise NotImplementedError('Unknown token {line}'.format(line=line))


def read_program(lines):
    return [parse_instruction(line) for line in lines]



class BC(enum.IntEnum):
    Tick = enum.auto()
    Store = enum.auto()
    Add1 = enum.auto()
    Sub1 = enum.auto()

    def __repr__(self):
        return f'{self.name}'


def compile_instruction(instruction):
    match instruction:
        case AddX(n) if n >= 0:
            return [BC.Tick, BC.Store] + \
                [BC.Tick, BC.Store] + \
                [BC.Add1 for _ in range(n)]
        case AddX(n) if n < 0:
            return [BC.Tick, BC.Store] + \
                [BC.Tick, BC.Store] + \
                [BC.Sub1 for _ in range(abs(n))]
        case Noop:
            return [BC.Tick, BC.Store]


def strength(state):
    cycle, register = state
    return cycle * register

def sum_signal_strenths(strengths, condition):
    sum(signal_strength(c))

def sum_20_and_40s_strengths(lines):
    cpu = make_cpu()
    large_program = read_program(lines)
    cpu.run(large_program)

    MAX = cpu.history[-1][0]
    selected_cycles = list(range(20, MAX, 40))
    def condition(state):
        cycle, _ = state
        return cycle in selected_cycles
    selected = [state for state in cpu.history if condition(state)]
    return sum(map(strength, selected))

def sprite(state):
    c, pos = state
    return (c, [pos - 1, pos, pos + 1])

def sprite_history(lines):
    cpu = make_cpu()
    large_program = read_program(lines)
    cpu.run(large_program)
    history = cpu.history
    return list(map(sprite, history))

def crt(lines):
    spritehistory = sprite_history(lines)
    def pos(c):
        return (c - 1) % 40
    return ''.join(['#' if pos(c) in positions else '.' for c, positions in spritehistory])

def print_crt(lines):
    crtlines = crt(lines)
    for i in range(6):
        print(crtlines[40*i: 40*i+40])
