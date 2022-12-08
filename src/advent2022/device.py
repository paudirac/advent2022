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

    @property
    def current_dir(self):
        return self._visited_dirs[-1] if len(self._visited_dirs) > 0 else None

    @property
    def root(self):
        return self._visited_dirs[0]

def filesystem(lines):
    commands = read_terminal(lines)
    fsb = FilesystemBuilder()
    for command in commands:
        fsb.apply(command)
    return fsb.root

def sum_dirs_with_at_most_100000(lines):
    root = filesystem(lines)
    def dir_with_at_most_100000(d):
        return d.is_dir and d.size <= 100000
    dirs = walk(root, condition=dir_with_at_most_100000)
    return sum(d.size for d in dirs)


TOTAL_DISK_SPACE_AVAILABLE = 70000000
UPDATE_SPACE_NEEDED = 30000000


def used(fs):
    return fs.size

def unused(fs, total=TOTAL_DISK_SPACE_AVAILABLE):
    unused_space = total - used(fs)
    assert unused_space >= 0, f"More space used ({used(fs)})than available ({total})"
    return unused_space

def space_needed_to_be_freed(fs, required):
    unused_space = unused(fs)
    yet_to_be_freed = required - unused_space
    return yet_to_be_freed if yet_to_be_freed > 0 else 0

def smallest_dir_to_delte_size(lines):
    fs = filesystem(lines)
    least_size = space_needed_to_be_freed(fs, required=UPDATE_SPACE_NEEDED)
    def dir_with_least_size(d):
        return d.is_dir and d.size >= least_size
    candidates = walk(fs, condition=dir_with_least_size)
    sorted_candidates = sorted(candidates, key=lambda d: d.size)
    return sorted_candidates[0].size
