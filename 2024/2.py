import csv
import numpy as np
import math


levels = []
with open("2 input", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        levels.append([int(i) for i in row[0].split()])

safe = 0
for i in levels:
    i = np.array(i)
    j = np.zeros_like(i)
    j[:-1] += i[1:]
    difference = (j - i)[:-1]
    if (difference == 0).sum() != 0:
        continue
    direction = (difference < 0).sum()
    if direction != difference.size and direction != 0:
        continue
    if not max(np.abs(difference)) <= 3:
        continue
    safe += 1

print(f"Part One: {safe}")


def is_safe(report):
    i = np.array(report)
    j = np.zeros_like(i)
    j[:-1] += i[1:]
    difference = (j - i)[:-1]
    if (difference == 0).sum() != 0:
        return False
    direction = (difference < 0).sum()
    if direction != difference.size and direction != 0:
        return False
    if not max(np.abs(difference)) <= 3:
        return False
    return True

safe = 0
for i in levels:
    if is_safe(i):
        safe += 1
    else:
        # print(f"{i}")
        for j in range(len(i)):
            report = i.copy()
            report.pop(j)
            # print(f"{j=} {report=}")
            if is_safe(report):
                safe += 1
                break
    # break



    # j = i[0]
    # direction = math.copysign(i[1] - j)
    # problem = 0
    # for k in i[1:]:
    #     delta = k - j
    #     if direction != math.copysign(delta):
    #         problem += 1


    # i = np.array(i)
    # j = np.zeros_like(i)
    # j[:-1] += i[1:]
    # difference = (j - i)[:-1]
    # zeros = (difference == 0).sum()
    # if zeros != 0:
    #     if zeros
    #     continue
    # direction = (difference < 0).sum()
    # if direction != difference.size and direction != 0:
    #     if direction != difference.size - 1 and direction != 1:
    #         if max(np.abs(difference)) <= 3:
    #             safe += 1
    #     continue
    # if not max(np.abs(difference)) <= 3:
    #     max_idx = np.argmax(np.abs(difference))
    #
    #     print(f"{i=} {j=} {difference=} {direction}")
    #     if not max(np.abs((j - i)[:-1])) <= 3:
    #         continue
    # safe += 1

print(f"Part Two: {safe}")

