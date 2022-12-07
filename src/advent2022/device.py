from collections import namedtuple

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
