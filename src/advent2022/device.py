from collections import namedtuple

class File(namedtuple('File', 'name size')):

    @classmethod
    def from_line(cls, line):
        size, name = line.split()
        return cls(name, int(size))
