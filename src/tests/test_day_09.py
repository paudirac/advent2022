import pytest
from utils import get_logger, read_test_input
log = get_logger(__name__)

from advent2022.bridge import (
    Motion,
    R, U, L, D, Z,
    read_motions,
    Point,
    unpack,
    Rope,
    Vector,
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

def test_Motion_add():
    p = Point(0, 0)
    assert p.move(R(1)) == Point(1, 0)
    assert p.move(R(4)) == Point(4, 0)
    assert p.move(L(2)) == Point(-2, 0)

    assert p.move(R(1)) == Point(1, 0)
    assert p.move(L(1)) == Point(-1, 0)
    assert p.move(U(1)) == Point(0, 1)
    assert p.move(D(1)) == Point(0, -1)

    assert p.move(Z) == p

def test_Rope():
    rope = Rope(Point(0, 0), Point(0, 0))
    assert rope.head == Point(0, 0)
    assert rope.tail == Point(0, 0)

def test_Rope_move_head():
    rope = Rope(Point(0, 0), Point(0, 0))
    motions = read_motions(lines)
    for motion in motions:
        rope.move_head(motion)
    assert rope.head == Point(2, 2)

    rope.move_head(Z)
    assert rope.head == Point(2, 2)

def test_Z():
    assert Z.steps == 0

def test_Point_tail_movement():
    head = Point(0, 0)
    tail = Point(0, 0)
    assert tail.close_movement_to(Point(0, 0)) == Z
    assert tail.close_movement_to(Point(0, 1)) == U(1)
    assert tail.close_movement_to(Point(0, -1)) == D(1)
    assert tail.close_movement_to(Point(1, 0)) == R(1)
    assert tail.close_movement_to(Point(-1, 0)) == L(1)
    #assert tail.close_movement_to(Point(1, 1)) == Vector(1, 1)

def test_vector():
    o = Point(0, 0)
    assert Point(0, 0) - o  == Vector(0, 0)
    assert Point(1, 0) - o  == Vector(1, 0)
    assert Point(-1, 0) - o == Vector(-1, 0)
    assert Point(0, 1) - o  == Vector(0, 1)
    assert Point(0, -1) - o == Vector(0, -1)
    assert Point(1, 1) - o == Vector(1, 1)
    assert Point(2, -3) - o == Vector(2, -3)

    assert Point(3, 2) - Point(1, 1) == Vector(2, 1)

def test_vector_to_motion():
    assert Vector(0, 0).as_motion == Z
    assert Vector(1, 0).as_motion == R(1)
    assert Vector(-1, 0).as_motion == L(1)
    assert Vector(0, 1).as_motion == U(1)
    assert Vector(0, -1).as_motion == D(1)

    assert Vector(4, 0).as_motion == R(4)
    assert Vector(0, -3).as_motion == D(3)
