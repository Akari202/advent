from logging import debug
from typing import Union

import numpy as np
from aoc import puzzle
from numpy.matlib import uint32
from scipy.optimize import LinearConstraint, linprog, milp
from scipy.sparse import lil_array
from utils import generate_combos

# puzzle.test_answer_one = 7
# puzzle.test_answer_two = 33
data = puzzle.lines()

lines: list[list[Union[list[bool], list[tuple[int]], list[int]]]] = []
for i in data:
    entry = [[], [], []]
    iterator = iter(i)
    while (value := next(iterator)) != "]":
        match value:
            case "#":
                entry[0].append(True)
            case ".":
                entry[0].append(False)

    button = ""
    while (value := next(iterator)) != "{":
        if value == ")":
            entry[1].append([int(j) for j in button.split(",")])
            button = ""
        elif value == "(":
            pass
        else:
            button += value

    joltages = ""
    while (value := next(iterator)) != "}":
        button += value
    entry[2] = [int(j) for j in button.split(",")]
    lines.append(entry)


presses = []
for i in lines:
    buttons = len(i[1])
    for j in generate_combos(range(buttons)):
        lights = [False] * len(i[0])
        for k in j:
            for index in i[1][k]:
                lights[index] = not lights[index]
        if i[0] == lights:
            presses.append(len(j))
            debug(f"{j = } | {i[0] = } | {lights = }")
            break

puzzle.submit_one(sum(presses))

coeff_count = 0
rhs_eq = []
for i in lines:
    coeff_count += len(i[1])
    rhs_eq.extend(i[2])
row_count = len(rhs_eq)
rhs_eq = np.array(rhs_eq, dtype=uint32)
lhs_eq = lil_array((row_count, coeff_count), dtype=uint32)
obj = np.ones(coeff_count, dtype=uint32)
offset = (0, 0)
for row in lines:
    for i, j in enumerate(row[1]):
        for k in j:
            debug(f"{k = } {j = } {i = } {row = } {offset = } {lhs_eq.shape = }")
            lhs_eq[k + offset[0], i + offset[1]] = 1
    offset = (len(row[2]) + offset[0], len(row[1]) + offset[1])
debug(f"{obj = }\n{lhs_eq.toarray() = }\n{rhs_eq = }")
opt = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq, integrality=obj)
debug(f"{opt = }")
if opt.success:
    puzzle.submit_two(int(opt.fun))
