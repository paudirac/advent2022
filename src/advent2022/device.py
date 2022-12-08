from collections import namedtuple
from utils import get_logger
log = get_logger(__name__)


Command = namedtuple('Command', 'name args')
Output = namedtuple('Output', 'raw')

def read_line(line):
    match line.split():
        case ["$", name, *args]:
            return Command(name, args)
        case _:
            return Output(line)

def read_terminal(lines):
    return [read_line(line) for line in lines]

class File(namedtuple('File', 'name size')):

    @classmethod
    def from_spec(cls, spec):
        size, name = spec.split()
        return cls(name, int(size))

    @property
    def is_dir(self):
        return False


class Dir(dict):

    def __init__(self, name, *contents):
        self.name = name
        super().__init__((content.name, content) for content in contents)

    @property
    def is_dir(self):
        return True

    @property
    def size(self):
        return sum(content.size for content in self.values())

    def __repr__(self):
        return f'Dir("{self.name}", size={self.size})'

def walk(root, condition, found=None):
    if found is None:
        found = []
    if condition(root):
        found += [root]
    if root.is_dir:
        for k, v in root.items():
            walk(v, condition=condition, found=found)
    return found
