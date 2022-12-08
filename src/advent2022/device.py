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
        return self.name == other.name and \
            self.items() == other.items()


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
        self.building = False

    def apply(self, command):
        match command:
            case Command("cd", [dir_name, *rest]):
                self._change_dir(dir_name)
            case Command("ls", [*rest]):
                self.building = True
            case Output(raw=raw):
                self._build(raw)
            case _:
                log.warning(f'Unable to apply {command=}')

    def _build(self, raw):
        log.debug(f'building {raw=}')
        match raw.split():
            case ["dir", dir_name]:
                self._build_dir(dir_name)
            case [size, name]:
                self._build_file(name, size)
            case _:
                log.warning(f'Unable to build {raw=}')

    def _build_dir(self, dir_name):
        new_dir = Dir(dir_name)
        self.current_dir[dir_name] = new_dir

    def _build_file(self, name, size):
        self.current_dir[name] = File(name, int(size))

    def _change_dir(self, dir_name):
        if dir_name == '..':
            self._visited_dirs.pop()
        elif dir_name == '/':
            assert len(self._visited_dirs) == 0, "Unable to change to /"
            dest = Dir(dir_name)
            self._visited_dirs.append(dest)
        else:
            dest = self.current_dir.get(dir_name)
            assert dest is not None, f"Can't change to {dir_name}, not in current: {self.current_dir.name}"
            self._visited_dirs.append(dest)
        log.debug(f"cd'd to {dir_name}")

    @property
    def current_dir(self):
        return self._visited_dirs[-1] if len(self._visited_dirs) > 0 else None

    @property
    def root(self):
        return self._visited_dirs[0]

def filesystem(lines):
    commands = read_terminal(lines)
    log.debug(f'{commands=}')
    fsb = FilesystemBuilder()
    for command in commands:
        fsb.apply(command)
    return fsb.root
