from collections import namedtuple


class File(namedtuple('File', 'name size')):

    @classmethod
    def from_line(cls, line):
        size, name = line.split()
        return cls(name, int(size))

class Dir(namedtuple('Dir', 'name')):

    @classmethod
    def from_line(cls, line):
        DIR, name = line.split()
        assert DIR == 'dir', f"Can't contruct an object {DIR}"
        return cls(name)

RootDir = Dir('/')

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
