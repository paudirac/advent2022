from collections import namedtuple
import string

from utils import get_logger, flatten
log = get_logger(__name__)

PRIORITIES = {
    letter: i + 1 for i,letter in enumerate(string.ascii_lowercase)
}
PRIORITIES.update({
    letter: i + 27 for i, letter in enumerate(string.ascii_uppercase)
})


class Item(namedtuple('Item', 'raw')):

    @property
    def priority(self):
        return PRIORITIES[self.raw]

class Compartment(namedtuple('Compartment', 'raw')):

    @classmethod
    def from_string(cls, raw):
        return cls(raw)

    def __iter__(self):
        for item in self.raw:
            yield item

class Rucksack(namedtuple('Rucksack', 'first second')):

    @classmethod
    def from_line(cls, line):
        left, right = halves(line)
        first = Compartment.from_string(left)
        second = Compartment.from_string(right)
        return cls(first, second)

    def common_items(self):
        first_set = set(item for item in self[0])
        second_set = set(item for item in self[1])
        return [Item(i) for i in first_set.intersection(second_set)]

def halves(string):
    lenght = len(string)
    assert lenght % 2 == 0, "Can't halve an odd string"
    midpoint = int(lenght / 2)
    return string[:midpoint], string[midpoint:]


def sum_priorities_of_common_items(lines):
    rucksacks = [Rucksack.from_line(line) for line in lines]
    common_items = flatten(rucksak.common_items() for rucksak in rucksacks)
    return sum(item.priority for item in common_items)

class Badge(Item):
    pass

class Elf(namedtuple('Elf', 'raw')):

    @classmethod
    def from_line(cls, line):
        return cls(line)

    @property
    def items(self):
        return self.raw

class Group(namedtuple('Group', 'badge')):

    @classmethod
    def from_elves(cls, *elves):
        assert len(elves) == 3, f"Impossible to make a Group with {len(elves)} elves"
        elf1, elf2, elf3 = elves
        first_set = set(item for item in elf1.items)
        second_set = set(item for item in elf2.items)
        third_set = set(item for item in elf3.items)
        badges = first_set.intersection(second_set).intersection(third_set)
        assert len(badges) == 1, f"There are {len(badges)} identical items carried by the 3 elfs"
        return cls(Badge(badges.pop()))

class _ElfGrouper:

    def __init__(self, lines, n):
        self.lines = lines
        self.n = n

    def __iter__(self):
        group = []
        for line in self.lines:
            group.append(Elf.from_line(line))
            if len(group) == self.n:
                yield Group.from_elves(*group)
                group = []


def group_elves(lines, n=3):
    assert len(lines) % n == 0, f"Impossible to make groups of {n} elves each"
    return list(_ElfGrouper(lines, n=n))

def sum_badges_priorities(*badges):
    return sum(badge.priority for badge in badges)

def sum_priorities_elf_groups(lines):
    groups = group_elves(lines)
    badges = (group.badge for group in groups)
    return sum_badges_priorities(*badges)
