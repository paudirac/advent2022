from utils import read_input, get_logger, read_test_input
log = get_logger(__name__)

def test_can_read_input():
    lines = read_input(1)
    assert len(lines) == 2255

def test_can_read_all_lines():
    lines = read_input(1)
    for line in lines:
        assert not line.endswith('\n')

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

def test_input_day_1():
    lines = read_test_input(example)
    for line in lines:
        assert not line.endswith('\n')
    assert len(lines) == 14
