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
    BC,
    strength,
    sum_20_and_40s_strengths,
    sprite,
    sprite_history,
    crt,
    print_crt,
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

def test_cpu_run_small_program():
    cpu = make_cpu()
    assert cpu.ticks == 0
    assert cpu.X == 1
    lines = read_test_input(small_example)
    small_program = read_program(lines)
    cpu.run(small_program)
    assert cpu.X == -1
    log.debug(f'{cpu.history=}')
    log.debug(f'{[compile_instruction(i) for i in small_program]=}')
    assert cpu.ticks == 1 + 2 + 2

    assert cpu.history == [
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 4),
        (5, 4),
    ]


def test_cpu_run_large_program():
    cpu = make_cpu()
    lines = read_test_input(large_example)
    large_program = read_program(lines)
    cpu.run(large_program)

    assert cpu.history[20 - 1] == (20, 21)
    assert cpu.history[60 - 1] == (60, 19)
    assert cpu.history[100 - 1] == (100, 18)
    assert cpu.history[140 - 1] == (140, 21)
    assert cpu.history[180 - 1] == (180, 16)

    assert cpu.history[220 - 1] == (220, 18)

def test_compile_noop():
    assert compile_instruction(Noop) == [
        BC.Tick,
        BC.Store,
    ]

def test_cpu_run_program_noop():
    cpu = make_cpu()
    assert cpu.X == 1
    assert cpu.ticks == 0
    program = [Noop]
    cpu.run(program)
    assert cpu.X == 1
    assert cpu.ticks == 1

def test_compile_addx_v():
    assert compile_instruction(AddX(2)) == [
        BC.Tick,
        BC.Store,
        BC.Tick,
        BC.Store,
        BC.Add1,
        BC.Add1,
    ]
    assert compile_instruction(AddX(-3)) == [
        BC.Tick,
        BC.Store,
        BC.Tick,
        BC.Store,
        BC.Sub1,
        BC.Sub1,
        BC.Sub1,
    ]

def test_cpu_run_addx_V():
    cpu = make_cpu()
    assert cpu.X == 1
    assert cpu.ticks == 0
    program = [AddX(41)]
    cpu.run(program)
    assert cpu.X == 42
    assert cpu.ticks == 2

def test_cpu_signal_strength():
    cpu = make_cpu()
    lines = read_test_input(large_example)
    large_program = read_program(lines)
    cpu.run(large_program)

    assert strength(cpu.history[20 - 1]) == 20 * 21
    assert strength(cpu.history[60 - 1]) == 60 * 19
    assert strength(cpu.history[100 - 1]) == 100 * 18
    assert strength(cpu.history[140 - 1]) == 140 * 21
    assert strength(cpu.history[180 - 1]) == 180 * 16

def test_signal_strength_20_and_every_40():
    lines = read_test_input(large_example)
    assert sum_20_and_40s_strengths(lines) == 13140

def test_sprite_position():
    cpu = make_cpu()
    lines = read_test_input(large_example)
    large_program = read_program(lines)
    cpu.run(large_program)
    history = cpu.history

    spritehistory = list(map(sprite, history))
    assert history[1 - 1] == (1, 1)
    assert spritehistory[0] == (1, [0, 1, 2])
    assert history[2 - 1] == (2, 1)
    assert spritehistory[1] == (2, [0, 1, 2])
    assert history[3 - 1] == (3, 16)
    assert spritehistory[2] == (3, [15, 16, 17])

def test_sprite_history():
    lines = read_test_input(large_example)
    spritehistory = sprite_history(lines)
    assert len(spritehistory) == 6 * 40

def test_crt():
    lines = read_test_input(large_example)
    crtlines = crt(lines)
    assert len(crtlines) == 6 * 40
    log.debug(f'{crtlines=}')
    assert crtlines[0:40] == '##..##..##..##..##..##..##..##..##..##..'
    assert crtlines[40:80] == '###...###...###...###...###...###...###.'

def xtest_print_crt():
    lines = read_test_input(large_example)
    print_crt(lines)
    assert False
