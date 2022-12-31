from dataclasses import dataclass, field
from collections import namedtuple
from functools import cache
import math
import enum

from utils import get_logger, flatten
log = get_logger(__name__)

def is_blank(line):
    return len(line) == 0

class RawMonkeyDef(list):
    pass

def monkeys(lines):
    mks = []
    monkey = RawMonkeyDef()
    for i, line in enumerate(lines):
        log.debug(f'{i} "{line}"')
        if is_blank(line):
            mks.append(monkey)
            monkey = RawMonkeyDef()
        else:
            monkey.append(line)
    else:
        mks.append(monkey)
    assert all(len(monkey_def) == 6 for monkey_def in mks)
    return mks
