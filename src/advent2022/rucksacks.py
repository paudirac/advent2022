from collections import namedtuple
import string

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

def _flatten(list_of_lists):
    return [item for inner_list in list_of_lists
                     for item in inner_list]

def sum_priorities_of_common_items(lines):
    rucksacks = [Rucksack.from_line(line) for line in lines]
    common_items = _flatten(rucksak.common_items() for rucksak in rucksacks)
    return sum(item.priority for item in common_items)
