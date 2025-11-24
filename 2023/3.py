from enum import Enum
import math
import re
from typing import Optional
from numpy._typing import NDArray
from utils import expand
from numpy._core.numeric import dtype
from numpy.matlib import char
from numpy.strings import isdigit
from aoc import puzzle
import numpy as np

# puzzle.test_answer = 4361

data = np.array(puzzle.char_grid())
# print(data)


def check(index: tuple[int, int]) -> tuple[bool, int]:
    good = False
    value = int(data[index])
    coords = expand(index, shape=data.shape)
    for i in coords:
        if data[i] != "." and not isdigit(data[i]):
            good = True
    # print(f"{index=} | {value=} | {good=}")
    if index[1] != 0 and isdigit(data[index[0], index[1] - 1]):
        recurse_check = check((index[0], index[1] - 1))
        # print(recurse_check)
        return (recurse_check[0] or good, value + recurse_check[1] * 10)
    else:
        return (good, value)


total = 0
for i, j in np.ndenumerate(data):
    if isdigit(j) and not (i[1] < data.shape[1] - 1 and isdigit(data[i[0], i[1] + 1])):
        checked = check(i)
        # print(checked)
        if checked[0]:
            total += checked[1]

puzzle.submit_one(total)

# puzzle.test_answer = 467835
# data = np.array(puzzle.char_grid())
# print(data)


def expand_number_right(index: tuple[int, int], data: NDArray[Any]) -> list[int]:
    value = data[index]
    # print(f"{index=} | {value=}")
    if not isdigit(value):
        return []
    values = [int(value)]
    if index[1] < data.shape[1] - 1:
        values += expand_number_right((index[0], index[1] + 1), data)
    return values


def expand_number_left(index: tuple[int, int], data: NDArray[Any]) -> list[int]:
    value = data[index]
    # print(f"{index=} | {value=}")
    if not isdigit(value):
        return []
    values = [int(value)]
    if index[1] > 0:
        values = expand_number_left((index[0], index[1] - 1), data) + values
    return values


def expand_number(index: tuple[int, int], data: NDArray[Any]) -> Optional[int]:
    value = data[index]
    # print(f"{index=} | {value=}")
    if not isdigit(value):
        return None
    values = [int(value)]
    if index[1] < data.shape[1] - 1:
        values += expand_number_right((index[0], index[1] + 1), data)
    if index[1] > 0:
        values = expand_number_left((index[0], index[1] - 1), data) + values
    value = 0
    for i in values:
        value *= 10
        value += i
    return value


total = 0
for i, j in np.ndenumerate(data):
    if j == "*":
        coords = expand(i, shape=data.shape)
        numbers: set[int] = set()
        for k in coords:
            num = expand_number(k, data)
            # print(f"{num=} | {numbers=}")
            if num is not None:
                numbers.add(num)
        if len(numbers) == 2:
            # print(numbers)
            total += math.prod(list(numbers))

puzzle.submit_two(total)
