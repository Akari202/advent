from logging import debug

import numpy as np
from aoc import puzzle
from utils import expand

# puzzle.test_answer_one = 13
# puzzle.test_answer_two = 43
data = np.array(puzzle.char_grid())

count = 0
shape = data.shape
for i, j in np.ndenumerate(data):
    if j == "@":
        around = expand(i, shape)
        around_count = 0
        for j in around:
            if data[j] == "@":
                around_count += 1
        if around_count < 4:
            count += 1

puzzle.submit_one(count)

count = 0
previous = -1
shape = data.shape
while count != previous:
    previous = count
    debug(f"\n{count = }\n{data}")
    for i, j in np.ndenumerate(data):
        if j == "@":
            around = expand(i, shape)
            around_count = 0
            for j in around:
                if data[j] == "@":
                    around_count += 1
            if around_count < 4:
                count += 1
                data[i] = "x"

puzzle.submit_two(count)
