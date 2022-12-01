from utils import read_test_input, get_logger

log = get_logger(__name__)

from advent2022.calories import most_calories_carried

example = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def test_the_elve_that_carries_most_calories_carries_24000():
    lines = read_test_input(example)
    assert most_calories_carried(lines) == 24000
