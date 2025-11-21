from enum import Enum
import math
import re
from aoc import puzzle

# puzzle.test_answer = 8

rgb_max = (12, 13, 14)


class Color(Enum):
    red = 0
    green = 1
    blue = 2


data = puzzle.lines()
game_re = re.compile(r"^Game (\d*): (.*)")
total_sum = 0
for i in data:
    match = game_re.search(i)
    rounds = match.group(2).split(";")
    good = True
    for j in rounds:
        shown = j.split(",")
        for k in shown:
            split = k.strip().split(" ")
            # print(split)
            if rgb_max[Color[split[1]].value] < int(split[0]):
                good = False
    if good:
        game_id = int(match.group(1))
        total_sum += game_id

puzzle.submit_one(total_sum)

puzzle.test_answer = 2286

data = puzzle.lines()
game_re = re.compile(r"^Game (\d*): (.*)")
total_sum = 0
for i in data:
    rgb_max = [0, 0, 0]
    match = game_re.search(i)
    rounds = match.group(2).split(";")
    for j in rounds:
        shown = j.split(",")
        for k in shown:
            split = k.strip().split(" ")
            rgb_max[Color[split[1]].value] = max(int(split[0]), rgb_max[Color[split[1]].value])
    power = math.prod(rgb_max)
    total_sum += power

puzzle.submit_two(total_sum)


