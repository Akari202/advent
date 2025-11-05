import numpy as np
import itertools
from tqdm import tqdm

values = []
with open("7 input") as file:
    for line in file:
        line = line.replace("\n", "").split(":")
        values.append([int(line[0]), [int(i) for i in line[1].split()]])

def check_combo(row):
    for j in itertools.product(["+", "*"], repeat=len(row[1]) - 1):
        result = row[1][0]
        for k, operator in enumerate(j):
            if operator == "+":
                result += row[1][k + 1]
            elif operator == "*":
                result *= row[1][k + 1]
        if result == row[0]:
            # print(f"combo: {j}")
            return row[0]
    # print("no combo")
    return 0

total = 0
for i in values:
    # print(i)
    product = np.prod(i[1])
    sum = np.sum(i[1])
    if product == i[0] or sum == i[0]:
        total += i[0]
        # print("all")
        continue
    # elif product < i[0] or sum > i[0] + 1:
    #     print(f"none {i}")
    #     assert check_combo(i) == 0
    #     continue
    else:
        total += check_combo(i)


print(f"Part One: {total}")

def concat(a, b):
    return int(f"{a}{b}")

def check_combo(row):
    for j in itertools.product(["+", "*", "|"], repeat=len(row[1]) - 1):
        result = row[1][0]
        for k, operator in enumerate(j):
            if operator == "+":
                result += row[1][k + 1]
            elif operator == "*":
                result *= row[1][k + 1]
            elif operator == "|":
                result = concat(result, row[1][k + 1])
        if result == row[0]:
            # print(f"combo: {j}")
            return row[0]
    # print("no combo")
    return 0

total = 0
for i in tqdm(values):
    # print(i)
    product = np.prod(i[1])
    sum = np.sum(i[1])
    if product == i[0] or sum == i[0]:
        total += i[0]
        # print("all")
        continue
    else:
        total += check_combo(i)

print(f"Part Two: {total}")
