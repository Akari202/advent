import csv
import re

sum = 0
with open("1 input", "r") as file:
    for line in file:
        values = []
        for i in line:
            if i.isdigit():
                values.append(int(i))
        sum += 10 * values[0] + values[-1]

print(f"Part One: {sum}")

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
sum = 0
with open("1 input", "r") as file:
    for line in file:
        values = [num2num(i) for i in pattern.findall(line)]
        sum += 10 * values[0] + values[-1]

print(f"Part Two: {sum}")
