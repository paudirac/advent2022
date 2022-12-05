from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

from advent2022.supply import (
    read_moves,
    Move,
    Crate,
    Stack,
    Crane,
    message_after_apply_steps,
    read_initial_crane_config_section,
)

example = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

lines = read_test_input(example)
N = Crate('N')
Z = Crate('Z')
D = Crate('D')
C = Crate('C')
M = Crate('M')
P = Crate('P')

def test_read_moves():
    assert len(lines) == 9
    moves = read_moves(lines)
    assert len(moves) == 4
    assert moves == [
        Move(qty=1, from_=2, to_=1),
        Move(qty=3, from_=1, to_=3),
        Move(qty=2, from_=2, to_=1),
        Move(qty=1, from_=1, to_=2),
    ]

def test_crates():
    assert ''.join(map(str, [C, M, Z])) == 'CMZ'


def test_stack():
    stack_1 = Stack(1, Z, N)
    stack_2 = Stack(2, M, C, D)
    stack_3 = Stack(3, P)

    assert len(stack_1) == 2
    assert len(stack_2) == 3
    assert len(stack_3) == 1

def test_stack_top():
    stack_1 = Stack(1, Z, N)
    stack_2 = Stack(2, M, C, D)
    stack_3 = Stack(3, P)

    assert len(stack_1) == 2
    assert stack_1.top == N
    assert len(stack_1) == 2

    assert len(stack_2) == 3
    assert stack_2.top == D
    assert len(stack_2) == 3

    assert len(stack_3) == 1
    assert stack_3.top == P
    assert len(stack_3) == 1


def test_crane():
    stack_1 = Stack(1, Z, N)
    stack_2 = Stack(2, M, C, D)
    stack_3 = Stack(3, P)

    crane = Crane(stack_1, stack_2, stack_3)
    assert len(crane) == 3
    assert crane.top_crates == [N, D, P]

def test_crane_move():
    stack_1 = Stack(1, Z, N)
    stack_2 = Stack(2, M, C, D)
    stack_3 = Stack(3, P)

    crane = Crane(stack_1, stack_2, stack_3)
    assert crane.top_crates == [N, D, P]

    step_1 = Move(qty=1, from_=2, to_=1)
    crane.apply(step_1)
    assert crane.top_crates == [D, C, P]

    step_2 = Move(qty=3, from_=1, to_=3)
    crane.apply(step_2)
    assert crane.top_crates == [None, C, Z]

    step_3 = Move(qty=2, from_=2, to_=1)
    crane.apply(step_3)
    assert crane.top_crates == [M, None, Z]

    step_4 = Move(qty=1, from_=1, to_=2)
    crane.apply(step_4)
    assert crane.top_crates == [C, M, Z]

def test_message_after_apply_steps():
    stack_1 = Stack(1, Z, N)
    stack_2 = Stack(2, M, C, D)
    stack_3 = Stack(3, P)
    crane = Crane(stack_1, stack_2, stack_3)
    assert message_after_apply_steps(lines, crane=crane) == 'CMZ'

def test_initial_crane_config_section():
    config_lines = read_initial_crane_config_section(lines)
    assert len(config_lines) == 4
