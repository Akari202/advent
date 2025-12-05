import copy
from logging import debug
from operator import itemgetter

import numpy as np
from aoc import puzzle
from more_itertools import peekable
from utils import expand

# puzzle.test_answer_one = 3
# puzzle.test_answer_two = 14
data = puzzle.lines()
blank = False
fresh_ranges: list[list[int]] = []
available: list[int] = []
for i in data:
    if i == "":
        blank = True
        continue
    if not blank:
        fresh_ranges.append([int(j) for j in i.split("-")])
    if blank:
        available.append(int(i))

debug(len(available))
debug(len(fresh_ranges))
debug(max(available))
count = 0
for i in available:
    for j in fresh_ranges:
        if j[0] <= i and i <= j[1]:
            count += 1
            break

puzzle.submit_one(count)

# fresh_ranges_boolean: list[list[int]] = []
# for i in fresh_ranges:
#     skip = False
#     ogi = copy.deepcopy(i)
#     for j in fresh_ranges_boolean:
#         while True:
#             if j[0] <= i[0] and i[0] <= j[1] and j[0] <= i[1] and i[1] <= j[1]:
#                 skip = True
#                 break
#             elif j[0] <= i[0] and i[0] <= j[1]:
#                 i[0] = j[1] + 1
#             elif j[0] <= i[1] and i[1] <= j[1]:
#                 i[1] = j[0] - 1
#             else:
#                 break
#         if skip:
#             break
#     if not skip:
#         debug(f"{i = } | {ogi = } | {len(fresh_ranges_boolean) = } | {i[1] - i[0] + 1}")
#         fresh_ranges_boolean.append(i)
#     else:
#         debug(f"{i = } | {ogi = }")
#     assert ogi[0] <= i[0] and i[0] <= ogi[1] and ogi[0] <= i[1] and i[1] <= ogi[1]
#     assert ogi[0] <= ogi[1]
#     assert i[0] <= i[1]
#
# count = 0
# for i in fresh_ranges_boolean:
#     # debug(f"{i[1]} - {i[0]} = {i[1] - i[0] + 1}")
#     count += i[1] - i[0] + 1

fresh_ranges_boolean: list[list[int]] = []
for i in fresh_ranges:
    assert i[0] <= i[1]
    fresh_ranges_boolean.sort(key=itemgetter(0))
    iterator = peekable(fresh_ranges_boolean)
    index = -1
    while True:
        try:
            j = next(iterator)
        except StopIteration:
            fresh_ranges_boolean.append(i)
            break
        else:
            index += 1
            if j[0] <= i[0] and i[1] <= j[1]:
                break
            elif i[0] <= j[0] and j[1] <= i[1]:
                fresh_ranges_boolean[index] = i
                break
            elif i[0] > j[1] and i[1] < iterator.peek(i)[0]:
                fresh_ranges_boolean.append(i)
                break
            elif i[0] <= j[1] and i[1] < iterator.peek(i)[0]:
                fresh_ranges_boolean[index][1] = i[1]
                break
            elif (
                i[0] <= j[1]
                and iterator.peek(None) is not None
                and i[1] >= iterator.peek()[0]
            ):
                peeked = fresh_ranges_boolean.pop(index + 1)
                fresh_ranges_boolean[index][1] = peeked[1]
                break


count = 0
for i in fresh_ranges_boolean:
    # debug(f"{i[1]} - {i[0]} = {i[1] - i[0] + 1}")
    count += i[1] - i[0] + 1


puzzle.submit_two(count)
