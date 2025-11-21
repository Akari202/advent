import csv
import re
from aoc import puzzle

total_sum = 0
data = puzzle.char_grid()
for line in data:
    values = []
    for i in line:
        if i.isdigit():
            values.append(int(i))
    total_sum += 10 * values[0] + values[-1]

puzzle.submit_one(total_sum)

def num2num(num):
    word_to_num = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9
            }
    if num.isdigit():
        return int(num)
    else:
        return word_to_num[num]
pattern = re.compile(r"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))", re.IGNORECASE)
total_sum = 0
data = puzzle.lines()
for line in data:
    values = [num2num(i) for i in pattern.findall(line)]
    total_sum += 10 * values[0] + values[-1]

puzzle.submit_two(total_sum)
