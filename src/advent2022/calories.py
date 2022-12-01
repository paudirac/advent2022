from collections import namedtuple

class Food(namedtuple('Food', 'raw')):

    @property
    def calories(self):
        return int(self.raw)

class Elf(list):

    @property
    def total_calories(self):
        return sum(map(lambda food: food.calories, self))

def most_calories_carried(lines):
    elves = []
    elf = Elf()
    elves.append(elf)
    for line in lines:
        if len(line) == 0:
            elf = Elf()
            elves.append(elf)
        else:
            elf.append(Food(line))

    return max(elf.total_calories for elf in elves)
