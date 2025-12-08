from logging import debug
from math import prod
from typing import Union

import numpy as np
from aoc import puzzle

# puzzle.test_answer_one = 4277556
# puzzle.test_answer_two = 3263827
data = puzzle.lines()

values: list[list[Union[int, str]]] = []
for i in data:
    current = 0
    white = False
    values.append([])
    for j in i.strip():
        if white and j.isdigit():
            values[-1].append(current)
            current = int(j)
            white = False
        elif j.isdigit():
            current *= 10
            current += int(j)
        elif j == " ":
            white = True
        elif j == "*" or j == "+":
            values[-1].append(j)

    if isinstance(values[-1][-1], int):
        values[-1].append(current)

debug(values)
grand_total = 0
for i in range(len(values[0])):
    numbers = []
    for j in range(len(values) - 1):
        numbers.append(values[j][i])
    op = values[-1][i]
    match op:
        case "+":
            total = sum(numbers)
        case "*":
            total = prod(numbers)
    debug(f"{numbers} | {op} | {total}")
    grand_total += total

puzzle.submit_one(grand_total)

data = np.array([list(i) for i in puzzle.input.split("\n")[:-1]]).transpose()

debug(data)


def first_number(data: list[str]) -> int:
    current = 0
    for i in data:
        if i.isdigit():
            current *= 10
            current += int(i)
    return current


numbers = []
op = ""
grand_total = 0
for i in data:
    if len(numbers) == 0:
        op = i[-1]
    if (i == " ").all():
        match op:
            case "+":
                total = sum(numbers)
            case "*":
                total = prod(numbers)
        debug(f"{numbers} | {op} | {total}")
        grand_total += total
        numbers = []
    else:
        numbers.append(first_number(i))

match op:
    case "+":
        total = sum(numbers)
    case "*":
        total = prod(numbers)
debug(f"{numbers} | {op} | {total}")
grand_total += total

puzzle.submit_two(grand_total)
