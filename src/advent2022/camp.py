from utils import get_logger

from collections import namedtuple

log = get_logger(__name__)

def count_pairs_with_overlapping_ranges(lines):
    raise NotImplementedError()

class Range(namedtuple('Range', 'spec lower upper')):

    @classmethod
    def from_spec(cls, spec):
        lower, upper = spec.split('-')
        return cls(spec, int(lower), int(upper))

    @property
    def sections(self):
        return [Section(i) for i in range(self.lower, self.upper + 1)]

    def display(self, bounds):
        return ''.join(
            'X' if self.lower <= i <= self.upper else '.'
            for i in range(bounds.lower, bounds.upper + 1)
        )

    def __contains__(self, item: 'Range'):
        return self.lower <= item.lower and item.upper <= self.upper

Section = namedtuple('Section', 'id')

class Pair(namedtuple('Pair', 'left right')):

    @classmethod
    def from_line(cls, line):
        left, right = line.split(',')
        return cls(left, right)

    @property
    def fully_contained(self):
        raise NotImplementedError()

def pair_elves(lines):
    return [Pair.from_line(line) for line in lines]
