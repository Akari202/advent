import csv
import numpy as np
import random
from tqdm import tqdm

rules = []
updates = []
with open("5 input", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 1:
            rules.append([int(i) for i in row[0].split("|")])
        elif len(row) == 0:
            continue
        else:
            updates.append([int(i) for i in row])

rules_dict = {}
for i in rules:
    if i[0] in rules_dict:
        rules_dict[i[0]].append(i[1])
    else:
        rules_dict[i[0]] = [i[1]]

def is_safe(update):
    for i in range(len(update)):
        if update[i] in rules_dict:
            rules = rules_dict[update[i]]
            for j in rules:
                if j in update[:i]:
                    return False
    return True

sum = 0
for i in updates:
    if is_safe(i):
        sum += i[int(len(i) / 2)]

print(f"Part One: {sum}")

def fix(update):
    count = 0
    while not is_safe(update):
        for i in range(len(update)):
            if update[i] in rules_dict:
                rules = rules_dict[update[i]]
                first = len(update)
                for j in rules:
                    if j in update:
                        first = min(first, update.index(j))
                update.insert(first - 1, update.pop(i))
        count += 1


sum = 0
for i in updates:
    if not is_safe(i):
        fix(i)
        assert is_safe(i)
        sum += i[int(len(i) / 2)]

print(f"Part Two: {sum}")
