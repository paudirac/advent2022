import pytest
from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

from advent2022.device import (
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


def test_test_input():
    lines = read_test_input(example)
    assert len(lines) == 23

def test_file():
    assert File.from_line("14848514 b.txt").name == 'b.txt'
    assert File.from_line("14848514 b.txt").size == 14848514
