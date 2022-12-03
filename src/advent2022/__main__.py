import sys
from utils import get_logger, read_input

log = get_logger(__name__)

from advent2022 import (
    calories,
    rock,
    rucksacks,
)

SOLVERS = {
    '1_1': calories.most_calories_carried,
    '1_2': calories.top_three_total,
    '2_1': rock.total_score,
    '2_2': rock.total_score_strategy_guide,
    '3_1': rucksacks.sum_priorities_of_common_items,
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
