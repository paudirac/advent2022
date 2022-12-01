from utils import read_input, get_logger
log = get_logger(__name__)

def test_can_read_input():
    lines = read_input(1)
    assert len(lines) == 2255

def test_can_read_all_lines():
    lines = read_input(1)
    for line in lines:
        assert not line.endswith('\n')
