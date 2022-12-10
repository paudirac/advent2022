from dataclasses import dataclass
from utils import get_logger
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


class R(Motion):
    pass

class U(Motion): pass
class L(Motion): pass
class D(Motion): pass

def read_motions(lines):
    return [Motion.from_line(line) for line in lines]
