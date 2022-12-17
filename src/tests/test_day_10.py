import pytest

from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.cathode import (
    make_cpu,
    read_program,
    Noop,
    AddX,
    parse_instruction,
)

small_example = """
noop
addx 3
addx -5
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
