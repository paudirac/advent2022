from collections import namedtuple

class Food(namedtuple('Food', 'raw')):

    @property
    def calories(self):
        return int(self.raw)

class Elf(list):

    @property
    def total_calories(self):
        return sum(map(lambda food: food.calories, self))

def _elves(lines):
    elves = []
    elf = Elf()
    elves.append(elf)
    for line in lines:
        if len(line) == 0:
            elf = Elf()
            elves.append(elf)
        else:
            elf.append(Food(line))
    return elves

def most_calories_carried(lines):
    elves = _elves(lines)
    return max(elf.total_calories for elf in elves)

def top_three_carriers(lines):
    elves = _elves(lines)
    return sorted(elves, key=lambda e: e.total_calories, reverse=True)[:3]

def top_three_total(lines):
    top_carriers = top_three_carriers(lines)
    return sum(map(lambda elf: elf.total_calories, top_carriers))
