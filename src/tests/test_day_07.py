import pytest
from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

from advent2022.device import (
    read_line,
    Command,
    Output,
    read_terminal,
    File,
    Dir,
    walk,
    filesystem,
    FilesystemBuilder,
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

def test_dir_is_equal_by_name_and_contents():
    assert Dir('a') == Dir('a')
    assert not Dir('a') == Dir('b')

    dir_a1 = Dir(
        "a",
        File.from_spec("129116 f"),
    )
    dir_a2 = Dir(
        "a",
        File.from_spec("129116 f"),
        File.from_spec("2557 g"),
    )
    assert not dir_a1 == dir_a2


def test_dir_is_a_tree_of_files():
    dir_a = Dir(
        "a",
        File.from_spec("129116 f"),
        File.from_spec("2557 g"),
        File.from_spec("62596 h.lst"),
    )
    assert len(dir_a) == 3
    assert dir_a.size == 129116 + 2557 + 62596

def test_dir_is_a_tree_of_files_or_dirs():
    dir_e = Dir(
        "e",
        File.from_spec("584 i")
    )
    dir_a = Dir(
        "a",
        File.from_spec("129116 f"),
        File.from_spec("2557 g"),
        File.from_spec("62596 h.lst"),
        dir_e,
    )
    assert len(dir_a) == 4
    assert dir_a.size == 129116 + 2557 + 62596 + dir_e.size

def test_find_dir():
    dir_e = Dir(
        "e",
        File.from_spec("584 i")
    )
    dir_a = Dir(
        "a",
        File.from_spec("129116 f"),
        File.from_spec("2557 g"),
        File.from_spec("62596 h.lst"),
        dir_e,
    )
    dirs = walk(dir_a, condition=lambda c: c.is_dir)
    assert dirs == [dir_a, dir_e]

    files = walk(dir_a, condition=lambda c: not c.is_dir)
    assert files == [
        File.from_spec("129116 f"),
        File.from_spec("2557 g"),
        File.from_spec("62596 h.lst"),
        File.from_spec("584 i"),
    ]

    def file_gt_3000(f):
        return not f.is_dir and f.size > 3000
    files_gt_3000 = walk(dir_a, condition=file_gt_3000)
    assert files_gt_3000 == [
        File.from_spec("129116 f"),
        File.from_spec("62596 h.lst"),
    ]


def test_filesystem_build_directories():
    fsb = FilesystemBuilder()
    assert not fsb.building
    fsb.apply(read_line("$ cd /"))
    assert fsb.current_dir == Dir('/')
    with pytest.raises(Exception):
        fsb.apply(read_line("$ cd a"))
    fsb.apply(read_line("$ ls"))
    assert fsb.building
    fsb.apply(read_line("dir a"))
    fsb.apply(read_line("$ cd a"))
    assert fsb.current_dir == Dir('a')
    with pytest.raises(Exception):
        fsb.apply(read_line("$ cd b"))
    fsb.apply(read_line("$ ls"))
    fsb.apply(read_line("dir b"))
    fsb.apply(read_line("$ cd b"))
    fsb.apply(read_line("$ cd .."))
    assert fsb.current_dir.name == Dir('a').name

def test_filesystem_build_files():
    fs = FilesystemBuilder()
    fs.apply(read_line("$ cd /"))
    assert fs.current_dir == Dir('/')
    with pytest.raises(Exception):
        fs.current_dir['b.txt']
    fs.apply(read_line("$ ls"))
    fs.apply(read_line("14848514 b.txt"))
    assert fs.current_dir['b.txt'] == File.from_spec("14848514 b.txt")

def test_make_filesystem():
    dir_e = Dir(
        "e",
        File.from_spec("584 i")
    )
    dir_a = Dir(
        "/",
        File.from_spec("129116 f"),
        File.from_spec("2557 g"),
        File.from_spec("62596 h.lst"),
        dir_e,
    )

    lns = read_test_input("""
$ cd /
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
""")
    assert filesystem(lns).name == dir_a.name
