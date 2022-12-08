from collections import namedtuple, deque
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

    def __eq__(self, other):
        if not isinstance(other, Dir):
            return False
        return self.name == other.name


def walk(root, condition, found=None):
    if found is None:
        found = []
    if condition(root):
        found += [root]
    if root.is_dir:
        for k, v in root.items():
            walk(v, condition=condition, found=found)
    return found

class FilesystemBuilder:

    def __init__(self):
        self._visited_dirs = deque()

    def apply(self, command):
        match command:
            case Command("cd", [dir_name, *rest]):
                self._change_dir(dir_name)
            case _:
                log.debug(f'Unable to apply {command=}')

    def _change_dir(self, dir_name):
        log.debug(f'cd to {dir_name}')
        if dir_name == '..':
            self._visited_dirs.pop()
        else:
            dest = Dir(dir_name)
            self._visited_dirs.append(dest)
        log.debug(f'{self.current_dir=}')

    @property
    def current_dir(self):
        return self._visited_dirs[-1] if len(self._visited_dirs) > 0 else None

def filesystem(lines):
    commands = read_terminal(lines)
    for command in commands:
        pass

    return None
