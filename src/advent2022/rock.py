from collections import namedtuple
from utils import get_logger

log = get_logger(__name__)

def sentinel(name):
    def __str__(self):
        return name
    sentinel_type = type(
        name,
        (object, ),
        {
            "__repr__": __str__,
        })
    return sentinel_type()

Rock = sentinel('Rock')
Paper = sentinel('Paper')
Scissors = sentinel('Scissors')

def decode(letter):
    ENCODING = {
        'A': Rock,
        'B': Paper,
        'C': Scissors,
        'X': Rock,
        'Y': Paper,
        'Z': Scissors,
    }
    return ENCODING[letter]

def shape_score(shape):
    SCORES = {
        Rock: 1,
        Paper: 2,
        Scissors: 3,
    }
    return SCORES[shape]

Lose = sentinel('Lose')
Draw = sentinel('Draw')
Win = sentinel('Win')

def outcome_score(result):
    SCORES = {
        Lose: 0,
        Draw: 3,
        Win: 6,
    }
    return SCORES[result]

def play(left, right):
    PLAYS = {
        (Rock, Scissors): (Win, Lose),
        (Scissors, Paper): (Win, Lose),
        (Paper, Rock): (Win, Lose),
        (Scissors, Rock): (Lose, Win),
        (Paper, Scissors): (Lose, Win),
        (Rock, Paper): (Lose, Win),
        (Rock, Rock): (Draw, Draw),
        (Scissors, Scissors): (Draw, Draw),
        (Paper, Paper): (Draw, Draw),
    }
    return PLAYS[(left, right)]

def play_score(left, right):
    left_result, right_result = play(left, right)
    return shape_score(right) + outcome_score(right_result)


class Round(namedtuple('Round', 'left right')):

    @classmethod
    def from_line(cls, line):
        left, right = line.split()
        return cls(decode(left), decode(right))

    @classmethod
    def from_line_right_drives_play(cls, line):
        left, right = line.split()
        left_move = decode(left)
        _, result = decode_result(right)
        right_move = choose_right(left_move, result)
        return cls(left_move, right_move)

def total_score(lines, line_round=Round.from_line):
    rounds = [line_round(line) for line in lines]
    return sum(play_score(*rund) for rund in rounds)

def decode_result(right):
    RESULTS = {
        'X': (Win, Lose),
        'Y': (Draw, Draw),
        'Z': (Lose, Win),
    }
    return RESULTS[right]

def choose_right(left, result):
    RIGHT = {
        (Rock, Win): Paper,
        (Rock, Lose): Scissors,
        (Rock, Draw): Rock,
        (Paper, Win): Scissors,
        (Paper, Lose): Rock,
        (Paper, Draw): Paper,
        (Scissors, Win): Rock,
        (Scissors, Lose): Paper,
        (Scissors, Draw): Scissors,
    }
    return RIGHT[(left, result)]

def total_score_strategy_guide(lines):
    return total_score(lines, line_round=Round.from_line_right_drives_play)
