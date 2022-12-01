from utils import read_test_input, get_logger

log = get_logger(__name__)

from advent2022.calories import (
    most_calories_carried,
    top_three_carriers
)

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

lines = read_test_input(example)

def test_the_elve_that_carries_most_calories_carries_24000():
    assert most_calories_carried(lines) == 24000

def test_top_three_carriers():
    top_carriers = top_three_carriers(lines)
    assert len(top_carriers) == 3
