from dataclasses import dataclass, field
from collections import namedtuple
import math

from utils import get_logger, flatten
log = get_logger(__name__)


@dataclass
class Motion:
    steps: int

    @classmethod
    def from_line(cls, line):
        direction, steps = line.split()
        match line.split():
            case ["R", steps]: return R(int(steps))
            case ["U", steps]: return U(int(steps))
            case ["L", steps]: return L(int(steps))
            case ["D", steps]: return D(int(steps))
            case _:
                raise TypeError(f"{line} doesn't seem a valid motion")

    def unpack(self):
        return [self.__class__(1) for _ in range(self.steps)]


class R(Motion): pass
class U(Motion): pass
class L(Motion): pass
class D(Motion): pass
Z = Motion(0)


class Vector(namedtuple('Vector', ['dx', 'dy'])):

    @property
    def length(self):
        return math.sqrt(self.dx * self.dx + self.dy * self.dy)

    @property
    def length2(self):
        return self.dx * self.dx + self.dy * self.dy


def read_motions(lines):
    return [Motion.from_line(line) for line in lines]


def vector_to_motion(vector: Vector):
    match vector:
        case Vector(0, 0): return Z
        case Vector(dx, 0) if dx >= 0: return R(dx)
        case Vector(dx, 0) if dx < 0: return L(-dx)
        case Vector(0, dy) if dy >= 0: return U(dy)
        case Vector(0, dy) if dy < 0: return D(-dy)
        case _:
            raise NotImplementedError('Cannot convert {self} to simple motion')


def motion_to_vector(motion: Motion):
    if not isinstance(motion, Motion):
        raise TypeError(f'Expected Motion, got {type(motion)}')
    match motion:
        case R(steps): return Vector(steps, 0)
        case U(steps): return Vector(0, steps)
        case L(steps): return Vector(-steps, 0)
        case D(steps): return Vector(0, -steps)
        case Motion(0): return Vector(0, 0)
        case _:
            raise TypeError(f'Invalid motion: {motion}')


class Point(namedtuple('Point', ['x', 'y'])):

    def __add__(self, displacement: Vector) -> 'Point':
        if not isinstance(displacement, Vector):
            raise TypeError(f'Expected Vector, got {type(displacement)}')

        return Point(self.x + displacement.dx, self.y + displacement.dy)

    def __sub__(self, other: 'Point') -> Vector:
        if not isinstance(other, Point):
            raise TypeError(f'Expected Point, got {type(other)}')
        x0, y0 = self
        x1, y1 = other
        dx = x0 - x1
        dy = y0 - y1
        return Vector(dx, dy)

    @property
    def neighbours(self):
        return [Point(self.x + dx, self.y + dy) for dx, dy in [
                      (0,  1),
            (-1,  0),         (1,  0),
                      (0, -1),
        ]]

    def to(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Invalid operation for Point and {type(other)}')

        return other - self


def unpack(motions):
    return flatten([motion.unpack() for motion in motions])


class Rope:

    def __init__(self, head: Point, tail: Point):
        self.tail_visits = set()
        self.head = head
        self.tail = tail

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, value):
        self._tail = value
        self.tail_visits.add(value)

    def move_head(self, motion: Motion):
        displacement = motion_to_vector(motion)
        self.head = self.head + displacement
        if self.stretched:
            self._move_tail(self.head)

    def _move_tail(self, destination):
        if self.stretched:
            def distance_to_tail(p):
                return (p - self.tail).length2
            candidates = [(distance_to_tail(n), n) for n in destination.neighbours]
            sorted_candidates = sorted(candidates, key=lambda dp: dp[0])
            _, dest = sorted_candidates[0]
            displacement = dest - self.tail
            self.tail = self.tail + displacement

    @property
    def stretched(self):
        return not self.touching

    @property
    def touching(self):
        v = self.head - self.tail
        return v.length2 <= 2

def positions_tail_visited_at_least_once(lines):
    rope = Rope(Point(0, 0), Point(0, 0))
    motions = read_motions(lines)
    for motion in unpack(motions):
        rope.move_head(motion)
    return len(rope.tail_visits)
