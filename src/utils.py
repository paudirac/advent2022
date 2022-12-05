"""Global utilities"""

from pathlib import Path
import os

import logging
logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

def get_logger(name):
    return logging.getLogger(name)

_CURRENT = os.path.dirname(os.path.abspath(__file__))

class Input:

    def __init__(self, day):
        current = Path(_CURRENT)
        self.filename = current / f'inputs/{day}/input.txt'

    def __len__(self):
        with open(self.filename, 'r') as f:
            return len(f.readlines())

    def __iter__(self):
        with open(self.filename, 'r') as f:
            for line in f:
                yield line.rstrip()


def read_input(day):
    """Reads input file for `day`"""
    return Input(day=day)

class TestInput:

    def __init__(self, example):
        self.example = example.split('\n')[1:-1]

    def __len__(self):
        return len(self.example)

    def __iter__(self):
        for line in self.example:
            yield line


def read_test_input(example):
    """Reads test input, expecting a format that starts and ends with
    an empty line, so that the triple quote syntax can be used for examples."""
    return TestInput(example)
