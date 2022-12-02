import pytest
from utils import read_test_input, get_logger

log = get_logger(__name__)

from advent2022.rock import (
    decode,
    Rock,
    Paper,
    Scissors,
    shape_score,
    outcome_score,
    Lose,
    Draw,
    Win,
    play,
    play_score,
    total_score,
    Round,
    decode_result,
    choose_right,
    total_score_strategy_guide,
)


example = """
A Y
B X
C Z
"""

lines = read_test_input(example)

def test_read_example():
    assert len(lines) == 3

def test_total_score_is_15():
    assert total_score(lines) == 15

def test_decode_strategy():
    assert decode('A') == Rock
    assert decode('B') == Paper
    assert decode('C') == Scissors

    assert decode('X') == Rock
    assert decode('Y') == Paper
    assert decode('Z') == Scissors

    with pytest.raises(Exception):
        decode('F')

def test_shape_score():
    assert shape_score(Rock) == 1
    assert shape_score(Paper) == 2
    assert shape_score(Scissors) == 3

def test_outcome_score():
    assert outcome_score(Lose) == 0
    assert outcome_score(Draw) == 3
    assert outcome_score(Win) == 6

def test_play():
    assert play(Rock, Paper) == (Lose, Win)
    assert play(Paper, Rock) == (Win, Lose)
    assert play(Scissors, Scissors) == (Draw, Draw)

def test_play_score():
    assert play_score(Rock, Paper) == 8
    assert play_score(Paper, Rock) == 1
    assert play_score(Scissors, Scissors) == 6

def test_round():
    assert Round.from_line('A Y') == Round(Rock, Paper)
    assert Round.from_line('B X') == Round(Paper, Rock)
    assert Round.from_line('C Z') == Round(Scissors, Scissors)

def test_decode_result():
    assert decode_result('X') == (Win, Lose)
    assert decode_result('Y') == (Draw, Draw)
    assert decode_result('Z') == (Lose, Win)

def test_round_driven_by_second_column():
    assert Round.from_line_right_drives_play('A Y') == Round(Rock, Rock)
    assert Round.from_line_right_drives_play('B X') == Round(Paper, Rock)
    assert Round.from_line_right_drives_play('C Z') == Round(Scissors, Rock)

def test_choose_right():
    assert choose_right(Rock, Draw) == Rock
    assert choose_right(Paper, Lose) == Rock
    assert choose_right(Scissors, Win) == Rock

def test_total_score_is_12():
    assert total_score(lines, line_round=Round.from_line_right_drives_play) == 12

def test_total_score_strategy_guide_is_12():
    assert total_score_strategy_guide(lines) == 12
