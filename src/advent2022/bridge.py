from dataclasses import dataclass
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
    def as_motion(self):
        match self:
            case Vector(0, 0): return Z
            case Vector(dx, 0) if dx >= 0: return R(dx)
            case Vector(dx, 0) if dx < 0: return L(-dx)
            case Vector(0, dy) if dy >= 0: return U(dy)
            case Vector(0, dy) if dy < 0: return D(-dy)
            case _:
                raise NotImplementedError('Cannot convert {self} to simple motion')

    @property
    def length(self):
        return math.sqrt(self.dx * self.dx + self.dy * self.dy)

    @property
    def length2(self):
        return self.dx * self.dx + self.dy * self.dy


def read_motions(lines):
    return [Motion.from_line(line) for line in lines]


class Point(namedtuple('Point', ['x', 'y'])):

    def touches(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Invalid operation for Point and {type(other)}')

        motion_to_other = other - self
        return motion_to_other.length2 <= 2

    def move(self, motion: Motion):
        if not isinstance(motion, Motion):
            raise TypeError(f'Expected Motion, got {type(motion)}')
        match motion:
            case R(steps): return Point(self.x + steps, self.y)
            case U(steps): return Point(self.x, self.y + steps)
            case L(steps): return Point(self.x - steps, self.y)
            case D(steps): return Point(self.x, self.y - steps)
            case Motion(0): return Point(self.x, self.y)
            case _:
                raise TypeError(f'Invalid motion: {motion}')

    def close_movement_to(self, dest: 'Point') -> Motion:
        return (dest - self).as_motion

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Expected Point, got {type(other)}')
        x0, y0 = self
        x1, y1 = other
        dx = x0 - x1
        dy = y0 - y1
        return Vector(dx, dy)


def unpack(motions):
    return flatten([motion.unpack() for motion in motions])


@dataclass
class Rope:
    head: Point
    tail: Point

    def move_head(self, motion: Motion):
        self.head = self.head.move(motion)
        self._move_tail(motion)

    def _move_tail(self, motion):
        pass
