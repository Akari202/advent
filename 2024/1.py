import csv
import numpy as np

first = []
second = []

with open("1 input", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        values = row[0].split()
        first.append(int(values[0]))
        second.append(int(values[1]))

first.sort()
second.sort()
difference = np.array(first) - np.array(second)

print(f"Part One: {np.sum(np.absolute(difference))}")

similarity = 0

for i in first:
    similarity += second.count(i) * i

print(f"Part Two: {similarity}")


