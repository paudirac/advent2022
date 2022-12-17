import pytest

from utils import get_logger, read_test_input
log = get_logger(__name__)

small_example = """
noop
addx 3
addx -5
"""

def test_small_lines():
    assert len(read_test_input(small_example)) == 3
