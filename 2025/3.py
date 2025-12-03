import numpy as np
from aoc import puzzle

# puzzle.test_answer_one = 357
# puzzle.test_answer_two = 3121910778619
data = puzzle.char_grid()

count = 0
for i in data:
    one_idx = np.argmax(i[:-1])
    two_idx = np.argmax(i[one_idx + 1 :])
    joltage = int(f"{i[one_idx]}{i[two_idx + one_idx + 1]}")
    count += joltage

puzzle.submit_one(count)

count = 0
for i in data:
    joltage = ""
    start = 0
    for j in range(-11, 1):
        if j == 0:
            index = np.argmax(i[start:])
        else:
            index = np.argmax(i[start:j])
        start += index + 1
        joltage += i[start - 1]
    count += int(joltage)

puzzle.submit_two(count)
