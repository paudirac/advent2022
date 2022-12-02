from collections import namedtuple

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

def total_score(lines):
    rounds = [Round.from_line(line) for line in lines]
    return sum(play_score(*rund) for rund in rounds)
