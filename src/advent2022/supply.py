from collections import namedtuple, deque
import string

from utils import get_logger
log = get_logger(__name__)

def _is_move(line):
    return line.startswith('move')

class Move(namedtuple('Move', 'qty from_ to_')):

    @classmethod
    def from_line(cls, line):
        MOVE, qty, FROM, from_, TO, to_ = line.split()
        assert MOVE == 'move', f"Invalid move instruction: {line}"
        assert FROM == 'from', f"Invalid move instruction: {line}"
        assert TO == 'to', f"Invalid move instruction: {line}"
        return cls(
            qty=int(qty),
            from_=int(from_),
            to_=int(to_),
        )

Load = namedtuple('Load', 'to_ crate')


def read_moves(lines):
    return [Move.from_line(line) for line in lines if _is_move(line)]

def read_initial_crane_config_section(lines):
    lns = []
    for line in lines:
        if len(line) == 0:
            break
        lns.append(line)
    return lns

class Crate(namedtuple('Crate', 'name')):

    def __str__(self):
        return self.name

    @classmethod
    def from_name(cls, name):
        trimed_name = name.strip()
        assert len(trimed_name) > 0, f"Unamed crate"
        return cls(trimed_name)

class Stack(deque):

    def __init__(self, number, *creates):
        self.number = number
        super().__init__(creates)

    @property
    def top(self):
        return self[-1] if len(self) > 0 else None

    def __repr__(self):
        return f"Stack({self.number}, [{', '.join(str(i) for i in self)}])"

class Crane:

    def __init__(self, *stacks):
        self.stacks = stacks

    def __len__(self):
        return len(self.stacks)

    @property
    def top_crates(self):
        return [stack.top for stack in self.stacks]

    def apply(self, move):
        qty, from_, to_ = move
        for _ in range(qty):
            crate = self.stacks[from_ - 1].pop()
            self.stacks[to_ - 1].append(crate)

    def load(self, n, crate):
        self.stacks[n - 1].append(crate)

    @classmethod
    def from_spec(cls, spec):
        nums = spec.split()
        return cls(*[Stack(int(n)) for n in nums])

    def __repr__(self):
        return f"Crane({self.stacks})"

def message_after_apply_steps(lines, crane: Crane):
    steps = read_moves(lines)
    for step in steps:
        crane.apply(step)
    return ''.join(map(str, crane.top_crates))

def _flatten(list_of_lists):
    return [item for inner_list in list_of_lists
                     for item in inner_list]


def read_crane(lines):
    bottom_to_top = list(reversed(lines))
    crane = Crane.from_spec(bottom_to_top[0])
    indexes = {
        i: None if n == ' ' else int(n) for i, n in enumerate(bottom_to_top[0])
    }
    indexes = { k: v for k, v in indexes.items() if v is not None }
    loads = []
    for line in bottom_to_top[1:]:
        for i, stack in indexes.items():
            try:
                crate = Crate.from_name(line[i])
                load = Load(stack, crate)
                loads.append(load)
            except Exception as e:
                pass
    for load in loads:
        crane.load(*load)
    return crane

def top_crates(lines):
    lines = list(lines)
    config = read_initial_crane_config_section(lines)
    crane = read_crane(config)
    return message_after_apply_steps(lines, crane=crane)
