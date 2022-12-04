from utils import get_logger

from collections import namedtuple

log = get_logger(__name__)

def count_pairs_with_overlapping_ranges(lines):
    pairs = pair_elves(lines)
    return sum(
        1 if pair.fully_contained else 0 for pair in pairs
    )

class Range(namedtuple('Range', 'spec lower upper')):

    @classmethod
    def from_spec(cls, spec):
        if len(spec) == 0:
            return Range.EMPTY
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

    def intersect(self, item: 'Range'):
        l, u = self.lower, self.upper
        L, U = item.lower, item.upper
        lower = max(l, L)
        upper = min(u, U)
        if lower > upper:
            return Range.EMPTY
        return Range(f'{lower}-{upper}', lower, upper)

class _EMPTY(Range):

    @property
    def sections(self):
        return []


Range.EMPTY = _EMPTY('', 0, 0)


Section = namedtuple('Section', 'id')

class Pair(namedtuple('Pair', 'left right')):

    @classmethod
    def from_line(cls, line):
        left_spec, right_spec = line.split(',')
        left = Range.from_spec(left_spec)
        right = Range.from_spec(right_spec)
        return cls(left, right)

    @property
    def fully_contained(self):
        left_in_right = self.left in self.right
        right_in_left = self.right in self.left
        return left_in_right or right_in_left

    @property
    def overlap(self):
        return self.left.intersect(self.right) != Range.EMPTY


def pair_elves(lines):
    return [Pair.from_line(line) for line in lines]

def count_pairs_with_some_overlapping_ranges(lines):
    pairs = pair_elves(lines)
    return sum(
        1 if pair.overlap else 0 for pair in pairs
    )
