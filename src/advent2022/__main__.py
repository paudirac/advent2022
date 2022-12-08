import sys
from utils import get_logger, read_input

log = get_logger(__name__)

from advent2022 import (
    calories,
    rock,
    rucksacks,
    camp,
    supply,
    tuning,
    device,
)

SOLVERS = {
    '1_1': calories.most_calories_carried,
    '1_2': calories.top_three_total,
    '2_1': rock.total_score,
    '2_2': rock.total_score_strategy_guide,
    '3_1': rucksacks.sum_priorities_of_common_items,
    '3_2': rucksacks.sum_priorities_elf_groups,
    '4_1': camp.count_pairs_with_overlapping_ranges,
    '4_2': camp.count_pairs_with_some_overlapping_ranges,
    '5_1': supply.top_crates_9000,
    '5_2': supply.top_crates_9001,
    '6_1': tuning.start_of_packet,
    '6_2': tuning.start_of_message,
    '7_1': device.sum_dirs_with_at_most_100000,
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
