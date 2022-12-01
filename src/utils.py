"""Global utilities"""

from pathlib import Path
import os

import logging
logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)
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
                yield line.strip()


def read_input(day):
    """Reads input file for `day`"""
    return Input(day=day)

def get_logger(name):
    return logging.getLogger(name)
