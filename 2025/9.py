from logging import debug

import numpy as np
from aoc import puzzle

# puzzle.test_answer_one = 50
# puzzle.test_answer_two = 24
data = puzzle.csv_values()
debug(f"{len(data) = }")

sizes: list[int] = []
for i, j in enumerate(data):
    others = data[:i] + data[i + 1 :]
    sizes += [
        (abs(j[0] - k[0]) + 1) * (abs(j[1] - k[1]) + 1)
        for k in others
        if (abs(j[0] - k[0]) * abs(j[1] - k[1]) > 0)
    ]

puzzle.submit_one(max(sizes))

data = np.array(data)
x = np.unique(data[:, 0])
x.sort()
y = np.unique(data[:, 1])
y.sort()

compressed = [[np.searchsorted(x, i[0]), np.searchsorted(y, i[1])] for i in data]
debug(f"{len(y) = } | {len(x) = } | {len(compressed) = }")

grid_size = max(len(x), len(y))
grid = np.full((grid_size, grid_size), False, dtype=bool)
iterator = iter(compressed)
first = next(iterator)
prev = first
grid[*first] = True
for i in iterator:
    for j in range(min(prev[0], i[0]), max(prev[0], i[0]) + 1):
        for k in range(min(prev[1], i[1]), max(prev[1], i[1]) + 1):
            grid[j, k] = True
    prev = i
for j in range(min(prev[0], first[0]), max(prev[0], first[0]) + 1):
    for k in range(min(prev[1], first[1]), max(prev[1], first[1]) + 1):
        grid[j, k] = True

for i in range(grid_size):
    prev = False
    for j in range(grid_size):
        next = grid[i, j]
        if next:
            prev = True
        elif not prev:
            continue
        else:
            if (
                np.any(grid[i:, j])
                and np.any(grid[:i, j])
                and np.any(grid[i, j:])
                and np.any(grid[i, :j])
            ):
                grid[i, j] = True


# Make font small
# for i in range(grid_size):
#     for j in range(grid_size):
#         if grid[j, i]:
#             print("#", end="")
#         else:
#             print(".", end="")
#     print("")


def check_rect(one: list[int], two: list[int]) -> bool:
    lower = [min(one[0], two[0]), min(one[1], two[1])]
    upper = [max(one[0], two[0]), max(one[1], two[1])]
    if (
        not grid[*lower]
        or not grid[*upper]
        or not grid[lower[0], upper[1]]
        or not grid[upper[0], lower[1]]
    ):
        return False
    for i in range(lower[0], upper[0] + 1):
        for j in range(lower[1], upper[1] + 1):
            if not grid[i, j]:
                return False
    return True


biggest = 0
for i in zip(data, compressed):
    for j in zip(data, compressed):
        size = int((abs(i[0][0] - j[0][0]) + 1) * (abs(i[0][1] - j[0][1]) + 1))
        if size > biggest and check_rect(i[1], j[1]):
            biggest = size

debug(f"{biggest = }")
puzzle.submit_two(biggest)


# grid = lil_array((grid_size, grid_size), dtype=bool)
# iterator = iter(data)
# first = next(iterator)
# prev = first
# grid[*first] = True
# for i in iterator:
#     for j in range(min(prev[0], i[0]), max(prev[0], i[0]) + 1):
#         for k in range(min(prev[1], i[1]), max(prev[1], i[1]) + 1):
#             grid[j, k] = True
#     prev = i
# for j in range(min(prev[0], first[0]), max(prev[0], first[0]) + 1):
#     for k in range(min(prev[1], first[1]), max(prev[1], first[1]) + 1):
#         grid[j, k] = True
#
#
# def check(point: list[int]) -> bool:
#     row = grid[:, point[1]].nonzero()[0]
#     col = grid[point[0], :].nonzero()[0]
#     if row.size == 0 or col.size == 0:
#         return False
#     return bool(
#         row[0] <= point[0]
#         and point[0] <= row[-1]
#         and col[0] <= point[1]
#         and point[1] <= col[-1]
#     )
#
#
# def check_rect(one: list[int], two: list[int]) -> bool:
#     debug("checking")
#     lower = [min(one[0], two[0]), min(one[1], two[1])]
#     upper = [max(one[0], two[0]), max(one[1], two[1])]
#     urow = grid[: upper[1]].nonzero()[0]
#     lrow = grid[:, lower[1]].nonzero()[0]
#     ucol = grid[upper[0], :].nonzero()[0]
#     lcol = grid[lower[0], :].nonzero()[0]
#     if urow.size == 0 or ucol.size == 0 or lrow.size == 0 or lcol.size == 0:
#         return False
#     if bool(
#         lcol[0] <= lower[1]
#         and upper[1] <= lcol[-1]
#         and ucol[0] <= lower[1]
#         and upper[1] <= ucol[-1]
#         and lrow[0] <= lower[0]
#         and upper[0] <= lrow[-1]
#         and urow[0] <= lower[0]
#         and upper[0] <= urow[-1]
#     ):
#         # urow = grid[lower[0] : upper[0], upper[1]].nonzero()[0]
#         # lrow = grid[lower[0] : upper[0], lower[1]].nonzero()[0]
#         # ucol = grid[upper[0], lower[1] : upper[1]].nonzero()[0]
#         # lcol = grid[lower[0], lower[1] : upper[1]].nonzero()[0]
#         slices = [
#             grid[lower[0] : upper[0], upper[1]].nonzero()[0],
#             grid[lower[0] : upper[0], lower[1]].nonzero()[0],
#             grid[upper[0], lower[1] : upper[1]].nonzero()[0],
#             grid[lower[0], lower[1] : upper[1]].nonzero()[0],
#         ]
#         print(lower)
#         print(upper)
#         for i in slices:
#             if i.size == 0 or ((diff := np.diff(i)).size > 0 and not np.any(diff > 1)):
#                 continue
#             print(i)
#             print(diff)
#         return False
#     return False
#
#
# if puzzle.is_test():
#     for i in range(grid_size):
#         for j in range(grid_size):
#             if grid[j, i]:
#                 print("#", end="")
#             else:
#                 if check([j, i]):
#                     print("o", end="")
#                 else:
#                     print(".", end="")
#         print("")
#
#
# sizes: list[list[int]] = []
# for i, j in enumerate(data):
#     others = data[:i] + data[i + 1 :]
#     sizes += [
#         [(abs(j[0] - k[0]) + 1) * (abs(j[1] - k[1]) + 1), j, k]
#         for k in others
#         if (abs(j[0] - k[0]) * abs(j[1] - k[1]) > 0)
#     ]
# debug("Calculated sizes")
# sizes.sort(key=itemgetter(0), reverse=True)
# debug("Sorted sizes")
# for i in sizes:
#     if not puzzle.is_test():
#         assert i[0] > 291791910
#         if i[0] > 4587371068:
#             continue
#     if check_rect(i[1], i[2]):
#         biggest = i[0]
#         break
#
# debug(biggest)
# puzzle.submit_two(biggest)
