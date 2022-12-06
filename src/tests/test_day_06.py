import pytest
from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

from advent2022.tuning import (
    datastream,
    all_different,
    Chunk,
    chunks,
    first_different_chunk,
    start_of_packet,
)


example_1 = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""

example_1_lines = read_test_input(example_1)

def test_read_lines():
    assert len(example_1_lines) == 1
    assert  list(example_1_lines)[0] == "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def test_datastream():
    stream = datastream(example_1_lines)
    assert len(stream) == len("mjqjpqmgbljsphdztnvjfqwrcgsmlb")


def test_all_different():
    assert all_different('a')
    assert not all_different('aa')
    assert not all_different("mjqjpqmgbljsphdztnvjfqwrcgsmlb")

def test_chunk():
    example = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    assert Chunk(example[0:4], 0).raw == 'mjqj'
    assert Chunk(example[0:4], 0).start == 0
    assert Chunk(example[0:4], 0).end == 4
    assert not Chunk(example[0:4], 0).all_different
    assert len(Chunk(example[0:4], 0)) == 4

    assert Chunk(example[0:7], 0).raw == 'mjqjpqm'
    assert Chunk(example[0:7], 0).start == 0
    assert Chunk(example[0:7], 0).end == 7
    assert len(Chunk(example[0:7], 0)) == 7
    assert not Chunk(example[0:4], 0).all_different

    assert Chunk(example[3:7], 3).raw == 'jpqm'
    assert Chunk(example[3:7], 3).start == 3
    assert Chunk(example[3:7], 3).end == 7
    assert len(Chunk(example[3:7], 0)) == 4
    assert Chunk(example[3:7], 0).all_different


def test_chunks():
    with pytest.raises(AssertionError):
        chunks('abcd', 5)

    cks1 = chunks("123456789", length=1)
    assert len(cks1) == 9
    assert all(len(ck) == 1 for ck in cks1)
    assert all(ck.all_different for ck in cks1)
    assert cks1 == [
        Chunk('1', 0),
        Chunk('2', 1),
        Chunk('3', 2),
        Chunk('4', 3),
        Chunk('5', 4),
        Chunk('6', 5),
        Chunk('7', 6),
        Chunk('8', 7),
        Chunk('9', 8),
    ]

    cks2 = chunks("123456789", length=2)
    assert len(cks2) == 8
    assert all(len(ck) == 2 for ck in cks2)
    assert all(ck.all_different for ck in cks2)
    assert cks2 == [
        Chunk('12', 0),
        Chunk('23', 1),
        Chunk('34', 2),
        Chunk('45', 3),
        Chunk('56', 4),
        Chunk('67', 5),
        Chunk('78', 6),
        Chunk('89', 7),
    ]

    cks = chunks("mjqjpqmgbljsphdztnvjfqwrcgsmlb", length=4)
    ck0 = cks[0]
    ck1 = cks[1]
    ck2 = cks[2]
    ck3 = cks[3]
    assert [ck0, ck1, ck2, ck3] == [
        Chunk('mjqj', 0),
        Chunk('jqjp', 1),
        Chunk('qjpq', 2),
        Chunk('jpqm', 3),
    ]
    assert not ck0.all_different
    assert not ck1.all_different
    assert not ck2.all_different
    assert ck3.all_different
    assert ck3.end == 7

def test_first_different_chunk():
    cks = chunks("mjqjpqmgbljsphdztnvjfqwrcgsmlb", length=4)
    assert first_different_chunk(cks) == Chunk('jpqm', 3)
    assert first_different_chunk(cks).end == 7

example_2 = """
bvwbjplbgvbhsrlpgdmjqwftvncz
"""
example_2_lines = read_test_input(example_2)

example_3 = """
nppdvjthqldpwncqszvftbrmjlhg
"""
example_3_lines = read_test_input(example_3)
example_4 = """
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
"""
example_4_lines = read_test_input(example_4)

example_5 = """
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""

example_5_lines = read_test_input(example_5)

def test_start_of_packet():
    assert start_of_packet(example_1_lines) == 7
    assert start_of_packet(example_2_lines) == 5
    assert start_of_packet(example_3_lines) == 6
    assert start_of_packet(example_4_lines) == 10
    assert start_of_packet(example_5_lines) == 11
