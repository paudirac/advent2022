import pytest
from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.bridge import (
    Motion,
    R, U, L, D,
    read_motions,
)

example = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

lines = read_test_input(example)
def test_lines():
    assert len(lines) == 8

def test_Motion():
    assert Motion(42).steps == 42

def test_R():
    assert R(42).steps == 42
    assert isinstance(R(42), Motion)

def test_Motions_eq():
    assert Motion.from_line("R 4") == Motion.from_line("R 4")
    assert not Motion.from_line("R 4") == Motion.from_line("U 4")

def test_Motion_from_line():
    assert Motion.from_line("R 4") == R(4)
    assert isinstance(Motion.from_line("R 4"), Motion)
    with pytest.raises(Exception):
        Motion.from_line("A 42")

def test_motions():
   read_motions(lines) == [
        R(4),
        U(4),
        L(3),
        D(1),
        R(4),
        D(1),
        L(5),
        R(2),
    ]
