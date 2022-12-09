import tempfile
from utils import read_input, get_logger, read_test_input, Input
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

def test_input_day_2():
    lines = read_input(2)
    assert len(lines) == 2500

def test_input_day_03():
    lines = read_input(3)
    assert len(lines) == 300

def test_input_day_04():
    lines = read_input(4)
    assert len(lines) == 1000

def test_input_strip():
    with tempfile.NamedTemporaryFile(mode="w+t") as f:
        f.write(""" 1   2   3   4   5   6   7   8   9
""")
        f.flush()
        input_object = read_input(42)
        input_object.filename = f.name
        lines = list(iter(input_object))
        assert lines[0] == " 1   2   3   4   5   6   7   8   9"

def test_input_day_07():
    lines = read_input(7)
    assert len(lines) == 988

def test_input_day_08():
    lines = read_input(8)
    assert len(lines) == 99
    assert len(list(lines)[0]) == 99

def test_input_day_09():
    lines = read_input(9)
    assert len(lines) == 2000
