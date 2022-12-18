import pytest

from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.cathode import (
    make_cpu,
    read_program,
    Noop,
    AddX,
    parse_instruction,
    compile_instruction,
    ExecBeginNoop,
    ExecIncCycle,
    ExecEndNoop,
)

small_example = """
noop
addx 3
addx -5
"""

large_example = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

def test_small_lines():
    assert len(read_test_input(small_example)) == 3

def test_cpu_register_starts_at_1():
    cpu = make_cpu()
    assert cpu.X == 1

def test_read_program():
    lines = read_test_input(small_example)
    program = read_program(lines)
    assert len(program) == 3
    assert program == [
        Noop,
        AddX(3),
        AddX(-5),
    ]

def test_invalid_token():
    with pytest.raises(Exception):
        parse_instruction('subsx 3')

def test_cpu_run_program_noop():
    cpu = make_cpu()
    assert cpu.X == 1
    assert cpu.ticks == 0
    program = [Noop]
    cpu.run(program)
    assert cpu.X == 1
    assert cpu.ticks == 1

def test_cpu_run_addx_V():
    cpu = make_cpu()
    assert cpu.X == 1
    assert cpu.ticks == 0
    program = [AddX(41)]
    cpu.run(program)
    assert cpu.X == 42
    assert cpu.ticks == 2

def test_cpu_run_small_program():
    cpu = make_cpu()
    lines = read_test_input(small_example)
    small_program = read_program(lines)
    cpu.run(small_program)
    assert cpu.X == -1
    assert cpu.ticks == 5

    assert cpu.history[0] == (0, 1)
    assert cpu.history[1] == (1, 1)
    assert cpu.history[2] == (2, 1)
    assert cpu.history[3] == (3, 4)
    assert cpu.history[4] == (4, 4)
    assert cpu.history[5] == (5, -1)

def xtest_cpu_run_large_program():
    cpu = make_cpu()
    lines = read_test_input(large_example)
    large_program = read_program(lines)
    cpu.run(large_program)

    assert cpu.history[20] == (20, 21)
    assert cpu.history[60] == (60, 19)
    assert cpu.history[100] == (100, 18)
    assert cpu.history[140] == (140, 21)
    assert cpu.history[180] == (180, 16)
    assert cpu.history[220] == (220, 18)


def test_():
    assert compile_instruction(Noop) == [
        ExecBeginNoop,
        ExecIncCycle,
        ExecEndNoop,
    ]

# Don't like this because (a part that it fails) it does not implement
# the "At the start of the first cycle, the noop instructions begins execution.
# During the first cycle, X is 1. After the first cycle, the noop instruction
# finishes execution, doing nothing."
# Or "At the start of the second cycle, the addx 3 instruction begins execution.
# During the second cycle, X is still 1."
#
# Visitor pattern? instead of pattern matching?
#
# instruction.execute(self)
#
# Noop.execute(self, cpu):
#   cpu.start_cycle()
#   cpu.end_cycle()
#
# AddX.execute(self, cpu):
#   cpu.start_cycle()
#   cpu.end_cycle()
#   cpu.strat_cycle()
#   cpu.X = cpu.X + self.value
#   cpu.end_cycle()
#
