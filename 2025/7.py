from logging import debug
from collections import Counter

import numpy as np
from aoc import puzzle

# puzzle.test_answer_one = 21
# puzzle.test_answer_two = 40
data = np.array(puzzle.char_grid())

start = np.where(data == "S")
shape = data.shape

debug(f"{start = } | {shape = }")

beam_y = start[0][0]
beam_x = [start[1][0]]
count = 0
while beam_y < shape[0] - 1:
    debug(f"{beam_x = } | {beam_y = }")
    beam_y += 1
    next_beam_x = []
    for i in beam_x:
        if data[beam_y, i] == "^":
            count += 1
            if i - 1 >= 0:
                next_beam_x.append(i - 1)
            if i + 1 < shape[1]:
                next_beam_x.append(i + 1)
        elif data[beam_y, i] == ".":
            next_beam_x.append(i)

    beam_x = list(set(next_beam_x))

puzzle.submit_one(count)

# start = np.where(data == "S")
# beam_y = start[0][0]
# beam_x = Counter([start[1][0]])
# while beam_y < shape[0] - 1:
#     beam_y += 1
#     debug(f"{beam_y = } of {shape[0]}")
#     next_beam_x = Counter()
#     for i, j in beam_x.items():
#         if data[beam_y, i] == "^":
#             if i - 1 >= 0:
#                 more = [i - 1] * j
#                 next_beam_x.update(more)
#             if i + 1 < shape[1]:
#                 more = [i + 1] * j
#                 next_beam_x.update(more)
#         elif data[beam_y, i] == ".":
#             more = [i] * j
#             next_beam_x.update(more)
#
#     beam_x = next_beam_x

start = np.where(data == "S")
beam_y = start[0][0]
beam_x = Counter([start[1][0]])
while beam_y < shape[0] - 1:
    beam_y += 1
    debug(f"{beam_y = } of {shape[0]}")
    next_beam_x = Counter()
    for i, j in beam_x.items():
        if data[beam_y, i] == "^":
            if i - 1 >= 0:
                if i - 1 in next_beam_x.keys():
                    next_beam_x[i - 1] += j
                else:
                    next_beam_x[i - 1] = j
            if i + 1 < shape[1]:
                if i + 1 in next_beam_x.keys():
                    next_beam_x[i + 1] += j
                else:
                    next_beam_x[i + 1] = j
        elif data[beam_y, i] == ".":
            if i in next_beam_x.keys():
                next_beam_x[i] += j
            else:
                next_beam_x[i] = j

    beam_x = next_beam_x

puzzle.submit_two(beam_x.total())
