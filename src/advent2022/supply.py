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

def read_moves(lines):
    return [Move.from_line(line) for line in lines if _is_move(line)]

class Crate(namedtuple('Crate', 'name')):

    def __str__(self):
        return self.name

class Stack(deque):

    def __init__(self, number, *creates):
        self.number = number
        super().__init__(creates)

    @property
    def top(self):
        return self[-1] if len(self) > 0 else None

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
        log.debug(f'applying {move}')
        for _ in range(qty):
            crate = self.stacks[from_ - 1].pop()
            self.stacks[to_ - 1].append(crate)

def message_after_apply_steps(lines, crane: Crane):
    steps = read_moves(lines)
    for step in steps:
        crane.apply(step)
    return ''.join(map(str, crane.top_crates))
