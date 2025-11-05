import re
import numpy as np

with open("4 input", "r") as file:
    data = [[j for j in line.replace("\n", "")] for line in file]

data = np.array(data)

count = 0

word = np.array(["X", "M", "A", "S"])
wordrev = np.flip(word)

for i in range(data.shape[0]):
    for j in range(data.shape[1] - 3):
        if (word == data[i, j:j + 4]).all():
            count += 1
        elif (wordrev == data[i, j:j + 4]).all():
            count += 1

for i in range(data.shape[0] - 3):
    for j in range(data.shape[1]):
        if (word == data[i:i + 4, j]).all():
            count += 1
        elif (wordrev == data[i:i + 4, j]).all():
            count += 1

for i in range(data.shape[0] - 3):
    for j in range(data.shape[1] - 3):
        section = data[i:i + 4, j:j + 4]
        if (word == np.diag(section)).all():
            count += 1
        if (wordrev == np.diag(section)).all():
            count += 1
        if (word == np.diag(np.fliplr(section))).all():
            count += 1
        if (wordrev == np.diag(np.fliplr(section))).all():
            count += 1

print(f"Part One: {count}")

word = ["M", "A", "S"]
wordrev = np.flip(word)
count = 0

for i in range(data.shape[0] - 2):
    for j in range(data.shape[1] - 2):
        section = data[i:i + 3, j:j + 3]
        if ((word == np.diag(section)).all() or (wordrev == np.diag(section)).all()) and ((word == np.diag(np.fliplr(section))).all() or (wordrev == np.diag(np.fliplr(section))).all()):
            # print(f"{(word == np.diag(section)).all()} {(wordrev == np.diag(section)).all()} {np.diag(section)} {np.diag(np.fliplr(section))}")
            count += 1

print(f"Part Two: {count}")





