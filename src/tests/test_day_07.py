import pytest
from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)


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
