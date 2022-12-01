import sys
from utils import get_logger, read_input

log = get_logger(__name__)

from advent2022 import calories

SOLVERS = {
    '1_1': calories.most_calories_carried,
}


def solver(day, puzzle):
    try:
        return SOLVERS[f'{day}_{puzzle}']
    except KeyError as e:
        log.error('Solver for {day=} and {puzzle_} not found')
        raise e
    except Exception as e:
        raise e


_, day, puzzle = sys.argv
log.debug(f'{day=} {puzzle=}')
lines = read_input(day)
result = solver(day, puzzle)(lines)
log.info(f'{result=}')
print(f'result: {result}')
