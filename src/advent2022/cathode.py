from dataclasses import dataclass, field
from collections import namedtuple
import math

from utils import get_logger, flatten
log = get_logger(__name__)


class CPU:

    def __init__(self, x):
        self.history = []
        self.X = x
        self.ticks = 0

    @property
    def ticks(self):
        return self._ticks

    @ticks.setter
    def ticks(self, value):
        self._ticks = value
        self.history.append((value, self.X))

    def run(self, program):
        for instruction in program:
            self._run_instruction(instruction)

    def _run_instruction(self, instruction):
        match instruction:
            case AddX(value):
                self._addx(value)
            case Noop:
                self._run_noop()

    def _run_noop(self):
        self.ticks += 1

    def _addx(self, value):
        self.ticks += 1
        self.X += value
        self.ticks += 1


def make_cpu():
    return CPU(x=1)


Noop = object()
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


ExecBeginNoop = object()
ExecIncCycle = object()
ExecEndNoop = object()

def compile_instruction(instruction):
    match instruction:
        case Noop:
            return [ExecBeginNoop, ExecIncCycle, ExecEndNoop]
