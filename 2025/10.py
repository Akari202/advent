import itertools
import re
from logging import debug

import numpy as np
from aoc import puzzle

puzzle.test_answer_one = 7
puzzle.test_answer_two = 33
data = puzzle.lines()

lines = []
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


def generate_combos(buttons, max: int = 10):
    depth = 0
    while depth < max:
        depth += 1
        for i in itertools.product(range(buttons), repeat=depth):
            yield i


presses = []
for i in lines:
    buttons = len(i[1])
    for j in generate_combos(buttons):
        lights = [False] * len(i[0])
        for k in j:
            for index in i[1][k]:
                lights[index] = not lights[index]
        if i[0] == lights:
            presses.append(len(j))
            debug(f"{j = } | {i[0] = } | {lights = }")
            break

puzzle.submit_one(sum(presses))
