import pytest
from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.bridge import (
    Motion,
    R, U, L, D,
    read_motions,
    Point,
    unpack,
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

def test_Point():
    assert Point(0, 0) == (0, 0)
    assert Point(2, 3) == (2, 3)
    assert not Point(0, 0) == Point(2, 3)

def test_Point_touches():
    # . . . .
    # x u y .
    # l p r .
    # z d w .
    u = Point(1, 2)
    l = Point(0, 1)
    p = Point(1, 1)
    r = Point(2, 1)
    d = Point(1, 0)
    x = Point(0, 2)
    y = Point(2, 2)
    z = Point(0, 0)
    w = Point(2, 0)
    poverlap = Point(1, 1)

    assert u.touches(p)
    assert l.touches(p)
    assert r.touches(p)
    assert d.touches(p)
    assert poverlap.touches(p)
    assert x.touches(p)
    assert y.touches(p)
    assert z.touches(p)
    assert w.touches(p)

    # is symetric
    assert p.touches(u)

def test_unpack_motions():
    assert unpack([R(4)]) == [R(1), R(1), R(1), R(1)]
    assert unpack([R(2), U(2)]) == [R(1), R(1), U(1), U(1)]
    motions = read_motions(lines)
    assert len(motions) == 8
    assert len(unpack(motions)) == sum([4, 4, 3, 1, 4, 1, 5, 2])
