from collections import namedtuple
from utils import get_logger
log = get_logger(__name__)

Index = namedtuple('Index', 'i j')

class Tree(namedtuple('Tree', 'index height')):

    def visible(self, hm: 'HeigtMap'):
        return hm.edge(self)

    def right_of(self, tree):
        index, _ = tree
        return index.i < self.index.i

    def left(self, hm: 'HeigtMap'):
        return [hm[(i, self.index.j)] for i in range(0, self.index.i)]

    def right(self, hm: 'HeigtMap'):
        return [hm[(i, self.index.j)] for i in range(self.index.i + 1, hm.size[0])]

    def top(self, hm: 'HeigtMap'):
        return [hm[(self.index.i, j)] for j in range(0, self.index.j)]

    def bottom(self, hm: 'HeigtMap'):
        return [hm[(self.index.i, j)] for j in range(self.index.j + 1, hm.size[1])]

    def __repr__(self):
        return f'Tree([{self.index.i}, {self.index.j}], {self.height})'


class HeightMap(dict):

    def __init__(self, size, items):
        self.size = size
        super().__init__(items)

    @classmethod
    def from_lines(cls, lines):
        index_and_height = []
        I, J = 0, 0
        for j, line in enumerate(lines):
            J += 1
            for i,h in enumerate(line):
                I += 0 if i < I else 1
                index = Index(i, j)
                tree = Tree(index, int(h))
                index_and_height.append((index, tree))

        return cls((I, J), index_and_height)

    def edge(self, tree: Tree):
        I, J = self.size
        i, j = tree.index
        return i in [0, I - 1] or j in [0, J - 1]

    def visible_from_left(self, tree: Tree):
        return all(tree.right_of(t) and tree > t for t in self.items())


def height_map(lines):
    return HeightMap.from_lines(lines)
