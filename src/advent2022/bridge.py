from dataclasses import dataclass
from collections import namedtuple

from utils import get_logger, flatten
log = get_logger(__name__)


@dataclass
class Motion:
    steps: int

    @classmethod
    def from_line(cls, line):
        direction, steps = line.split()
        match direction:
            case "R": return R(int(steps))
            case "U": return U(int(steps))
            case "L": return L(int(steps))
            case "D": return D(int(steps))
            case _:
                raise TypeError(f"{line} doesn't seem a valid motion")

    def unpack(self):
        return [self.__class__(1) for _ in range(self.steps)]

class R(Motion):
    pass

class U(Motion): pass
class L(Motion): pass
class D(Motion): pass

def read_motions(lines):
    return [Motion.from_line(line) for line in lines]


class Point(namedtuple('Point', ['x', 'y'])):

    def touches(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Invalid operation for Point and {type(other)}')
        x0, y0 = self
        x1, y1 = other
        dx = abs(x0 - x1)
        dy = abs(y0 - y1)
        return max(dx, dy) <= 1

    def move(self, motion: Motion):
        if not isinstance(motion, Motion):
            raise TypeError(f'Expected Motion got {type(motion)}')
        match motion:
            case R(steps): return Point(self.x + steps, self.y)
            case U(steps): return Point(self.x, self.y + steps)
            case L(steps): return Point(self.x - steps, self.y)
            case D(steps): return Point(self.x, self.y - steps)
            case _:
                raise TypeError(f'Invalid motion: {motion}')

def unpack(motions):
    return flatten([motion.unpack() for motion in motions])
