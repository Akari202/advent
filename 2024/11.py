import numpy as np
import math
from math import log10, ceil
from tqdm import tqdm
from collections import deque


def load_file(filename):
    with open(filename, "r") as file:
        return [int(i) for i in file.read().replace("\n", "").split()]


def blink(stones):
    result = []
    for i in stones:
        if i == 0:
            result.append(1)
            continue

        digits = ceil(log10(i + 1))
        if digits % 2 == 0:
            place = 10 ** (digits // 2)
            left = i // place
            right = i - left * place
            result.append(left)
            result.append(right)
        else:
            result.append(i * 2024)
    return result

stones = load_file("11 input")
for _ in range(25):
    stones = blink(stones)

print(f"Part One: {len(stones)}")

# stones = load_file("11 input test")
#
# def count_stones(stones, blinks):
#     counts = [0, 0, []]
#     for i in stones:
#         if i == 0:
#             counts[0] += 1
#         elif ceil(log10(i + 1)) % 2 == 0:
#             counts[1] += 1
#         else:
#             counts[2].append(i)
#
#     for _ in range(blinks):
#         new_counts = [0, 0, []]
#         new_counts[2].extend([1 for i in range(counts[0])])
#         new_counts[1] += 2 * counts[1]
#         for i in counts[2]:
#             if ceil(log10(i * 2024 + 1)) % 2 == 0:
#                 new_counts[1] += 1
#             else:
#                 new_counts[2].append(i)
#         counts = new_counts
#
#     return counts[0] + counts[1] + len(counts[2])
#
# print(f"Part Two: {count_stones(stones, 75)}")

# all_stones = load_file("11 input")
# values = {}
# for i in tqdm(all_stones):
#     stones = [i]
#     for j in range(25):
#         stones = blink(stones)
#     values[i] = stones
#     for j in tqdm(stones, leave=False):
#         if not j in values.keys():
#             new_stones = [j]
#             for _ in range(25):
#                 new_stones = blink(new_stones)
#             values[j] = new_stones
#
# count = 0
# double_values = {}
# try:
#     for i in tqdm(all_stones):
#         results = values[i]
#         for j in tqdm(results, leave=False):
#             if not j in double_values.keys():
#                 final_results = values[i]
#                 this_count = 0
#                 for k in tqdm(final_results, leave=False):
#                     this_count += len(values[k])
#                 double_values[j] = this_count
#                 count += this_count
#             else:
#                 count += double_values[j]
# except:
#     print(count)
#
#
#
# print(f"Part Two: {count}")




# for i in tqdm(all_stones):
#     if i not in values:
#         stones = [i]
#         for _ in range(25):
#             stones = blink(stones)
#         values[i] = stones
#
#     for j in tqdm(values[i], leave=False):
#         if j not in values:
#             new_stones = [j]
#             for _ in range(25):
#                 new_stones = blink(new_stones)
#             values[j] = new_stones

all_stones = load_file("11 input elijah")
values = {}
double_values = {}
count = 0

for i in tqdm(all_stones):
    if not i in values.keys():
        stones = [i]
        for _ in range(25):
            stones = blink(stones)
        values[i] = stones
    for j in tqdm(values[i], leave=False):
        if not j in double_values.keys():
            this_count = 0
            if not j in values.keys():
                stones = [j]
                for _ in range(25):
                    stones = blink(stones)
                values[j] = stones
            for k in values[j]:
                if not k in values.keys():
                    stones = [k]
                    for _ in range(25):
                        stones = blink(stones)
                    values[k] = stones
                this_count += len(values[k])
            double_values[j] = this_count
            count += this_count
        else:
            count += double_values[j]

print(f"Part Two: {count}")
