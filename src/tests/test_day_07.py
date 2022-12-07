import pytest
from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

from advent2022.device import (
    read_line,
    Command,
    Output,
    read_terminal,
    File,
)

example = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


lines = read_test_input(example)

def test_test_input():
    assert len(lines) == 23

def test_read_line():
    assert read_line("$ cd /") == Command('cd', ['/'])
    assert read_line("$ ls") == Command('ls', [])
    assert read_line("dir a") == Output("dir a")

def test_read_terminal():
    assert read_terminal(lines) == [
        Command("cd", ["/"]),
        Command("ls", []),
        Output("dir a"),
        Output("14848514 b.txt"),
        Output("8504156 c.dat"),
        Output("dir d"),
        Command("cd", ["a"]),
        Command("ls", []),
        Output("dir e"),
        Output("29116 f"),
        Output("2557 g"),
        Output("62596 h.lst"),
        Command("cd", ["e"]),
        Command("ls", []),
        Output("584 i"),
        Command("cd", [".."]),
        Command("cd", [".."]),
        Command("cd", ["d"]),
        Command("ls", []),
        Output("4060174 j"),
        Output("8033020 d.log"),
        Output("5626152 d.ext"),
        Output("7214296 k"),
    ]

def test_files_are_plain_data():
    assert File.from_spec(Output("14848514 b.txt").raw) == File(name="b.txt", size=14848514)
    assert File.from_spec(Output("14848514 b.txt").raw) != File.from_spec(Output("8504156 c.dat").raw)
