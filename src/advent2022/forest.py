from utils import get_logger
log = get_logger(__name__)

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
                index_and_height.append(((i, j), int(h)))

        return cls((I, J), index_and_height)


def height_map(lines):
    return HeightMap.from_lines(lines)
