from dataclasses import dataclass
from utils import get_logger
log = get_logger(__name__)


@dataclass
class Motion:
    steps: int

    @classmethod
    def from_line(cls, line):
        _, steps = line.split()
        return R(int(steps))


class R(Motion):
    pass
