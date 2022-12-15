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


class Pubsub:

    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def publish(self, event):
        log.debug(f'publishing {event=}')
        for subscriber in self._subscribers:
            subscriber(event)


def pubsub():
    return Pubsub()


class Knot(Pubsub):

    def __init__(self, initial_position: Point):
        super().__init__()
        self._visits = [initial_position]

    @property
    def position(self):
        return self._visits[-1]

    @position.setter
    def position(self, value):
        self._visits.append(value)
        self.publish(value)

    def move(self, displacement):
        self.position = self.position + displacement

    def follow(self, destination):
        log.debug(f'following to {destination=}')
        displacement = destination - self.position
        if displacement.length2 > 2:
            def distance_to_tail(p):
                return (p - self.position).length2
            candidates = [(distance_to_tail(n), n) for n in destination.neighbours]
            sorted_candidates = sorted(candidates, key=lambda dp: dp[0])
            _, dest = sorted_candidates[0]
            displacement = dest - self.position
            self.position = self.position + displacement

    @property
    def visits(self):
        return set(self._visits)


class Rope:

    def __init__(self, head: Point, tail: Point):
        self._head = Knot(head)
        self._tail = Knot(tail)
        self._head.subscribe(self._tail.follow)

    @property
    def head(self):
        return self._head.position

    @head.setter
    def head(self, value):
        self._head.position = value

    @property
    def tail(self):
        return self._tail.position

    @tail.setter
    def tail(self, value):
        self._tail.position = value

    def move_head(self, motion: Motion):
        displacement = motion_to_vector(motion)
        self._head.move(displacement)

    @property
    def stretched(self):
        return not self.touching

    @property
    def touching(self):
        v = self._head.position - self._tail.position
        return v.length2 <= 2

    @property
    def tail_visits(self):
        return self._tail.visits

def positions_tail_visited_at_least_once(lines):
    rope = Rope(Point(0, 0), Point(0, 0))
    motions = read_motions(lines)
    for motion in unpack(motions):
        rope.move_head(motion)
    return len(rope.tail_visits)


class LongRope:

    def __init__(self):
        self._head = Knot(Point(0, 0))
        self._knot_1 = Knot(Point(0, 0))
        self._knot_2 = Knot(Point(0, 0))
        self._knot_3 = Knot(Point(0, 0))
        self._knot_4 = Knot(Point(0, 0))
        self._knot_5 = Knot(Point(0, 0))
        self._knot_6 = Knot(Point(0, 0))
        self._knot_7 = Knot(Point(0, 0))
        self._knot_8 = Knot(Point(0, 0))
        self._knot_9 = Knot(Point(0, 0))

        self._head.subscribe (self._knot_1.follow)
        self._knot_1.subscribe(self._knot_2.follow)
        self._knot_2.subscribe(self._knot_3.follow)
        self._knot_3.subscribe(self._knot_4.follow)
        self._knot_4.subscribe(self._knot_5.follow)
        self._knot_5.subscribe(self._knot_6.follow)
        self._knot_6.subscribe(self._knot_7.follow)
        self._knot_7.subscribe(self._knot_8.follow)
        self._knot_8.subscribe(self._knot_9.follow)

    def move_head(self, motion: Motion):
        displacement = motion_to_vector(motion)
        self._head.move(displacement)

    @property
    def tail_visits(self):
        return self._knot_9.visits


def positions_tail_visited_at_least_once_long_rope(lines):
    rope = LongRope()
    motions = read_motions(lines)
    for motion in unpack(motions):
        rope.move_head(motion)
    return len(rope.tail_visits)
