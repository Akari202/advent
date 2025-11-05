import csv
import numpy as np
import math
import re


with open("3 input", "r") as file:
    data = file.read().replace("\n", "")

total = 0
pattern = re.compile(r"mul\([0-9]+,[0-9]+\)", re.IGNORECASE)
matches = pattern.findall(data)
pattern = re.compile(r"[0-9]+", re.IGNORECASE)
split = [pattern.findall(i) for i in matches]
for i in split:
    total += int(i[0]) * int(i[1])

print(f"Part One: {total}")

pattern = re.compile(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", re.IGNORECASE)
matches = pattern.findall(data)
pattern = re.compile(r"[0-9]+", re.IGNORECASE)
total = 0
do = True
for i in matches:
    if i == "do()":
        do = True
    elif i == "don't()":
        do = False
    elif do:
        total += np.prod(np.array([int(i) for i in pattern.findall(i)]))

print(f"Part Two: {total}")


