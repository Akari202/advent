from logging import debug, error
from math import prod
from operator import itemgetter
from typing import Iterable

import numpy as np
from aoc import puzzle
from numba import jit
from numpy._typing import NDArray
from scipy.sparse import lil_array
from tqdm import tqdm
from utils import get_polygon_centroid_area

# puzzle.test_answer_one = 50
# puzzle.test_answer_two = 24
# data = [[i[1], i[0]] for i in puzzle.csv_values()]
data = puzzle.csv_values()
if puzzle.is_test():
    grid_size = 15
else:
    grid_size = 100000

sizes: list[int] = []
for i, j in enumerate(data):
    others = data[:i] + data[i + 1 :]
    sizes += [(abs(j[0] - k[0]) + 1) * (abs(j[1] - k[1]) + 1) for k in others]

# debug(sizes)
puzzle.submit_one(max(sizes))


# _, area = get_polygon_centroid_area(data)
# debug(f"{area = }")


# grid = np.full((grid_size, grid_size), False, dtype=bool)
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
# # grid[*first] = True
# # for i in iterator:
# #     for j in range(min(prev[0], i[0]), max(prev[0], i[0]) + 1):
# #         grid[j, i[1]] = True
# #     prev = i
# # for j in range(min(prev[0], first[0]), max(prev[0], first[0]) + 1):
# #     grid[j, i[1]] = True
#
#
# @jit(nopython=True, parallel=True, cache=True)
# def fill_grid(grid: NDArray[np.bool], grid_size: int) -> NDArray[np.bool]:
#     for i in range(grid_size):
#         prev = False
#         fill = False
#         for j in range(grid_size):
#             next = grid[i, j]
#             if not next and prev:
#                 fill = grid[i, j:].sum() % 2 != 0
#             if not next and fill:
#                 grid[i, j] = True
#             prev = next
#
#     return grid
#
#
# grid = fill_grid(grid, grid_size)
# debug("Finished filling")
#
#
# def check_rect(one: list[int], two: list[int]) -> bool:
#     lower = [min(one[0], two[0]), min(one[1], two[1])]
#     upper = [max(one[0], two[0]), max(one[1], two[1])]
#     rect = grid[lower[0] : upper[0], lower[1] : upper[1]]
#     return bool(np.all(rect))
#     return grid[*one] and grid[*two] and grid[one[0], two[1]] and grid[two[0], one[1]]

# h_grid = lil_array((grid_size, grid_size), dtype=bool)
# iterator = iter(data)
# first = next(iterator)
# prev = first
# h_grid[*first] = True
# for i in iterator:
#     for j in range(min(prev[0], i[0]), max(prev[0], i[0]) + 1):
#         h_grid[j, i[1]] = True
#     prev = i
# for j in range(min(prev[0], first[0]), max(prev[0], first[0]) + 1):
#     h_grid[j, first[1]] = True
# v_grid = lil_array((grid_size, grid_size), dtype=bool)
# iterator = iter(data)
# first = next(iterator)
# prev = first
# v_grid[*first] = True
# for i in iterator:
#     for j in range(min(prev[1], i[1]), max(prev[1], i[1]) + 1):
#         v_grid[i[0], j] = True
#     prev = i
# for j in range(min(prev[1], first[1]), max(prev[1], first[1]) + 1):
#     v_grid[first[0], j] = True

grid = lil_array((grid_size, grid_size), dtype=bool)
iterator = iter(data)
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


# def changes(slice) -> int:
#     indexes = slice.nonzero()
#     if len(indexes) == 0:
#         return 0
#     if len(indexes) == 1:
#         return 1
#     count = 0
#     iterator = iter(indexes)
#     prev = next(iterator)
#     for i in iterator:
#         if i != prev + 1:
#             count += 1
#             prev = i
#     return count


def check_points(points: list[list[int]]) -> bool:
    for i in points:
        if not (
            grid[*i]
            or (
                grid[i[0] :, i[1]].size
                and grid[i[0], i[1] :].size
                and grid[: i[0], i[1]].size
                and grid[i[0], : i[1]].size
            )
        ):
            return False
    return True


def check_rect(one: list[int], two: list[int]) -> bool:
    points = [[one[0], two[1]], [two[0], one[1]]]
    if not check_points(points):
        return False
    lower = [min(one[0], two[0]), min(one[1], two[1])]
    upper = [max(one[0], two[0]), max(one[1], two[1])]
    points = (
        [[i, lower[1]] for i in range(lower[0], upper[0])]
        + [[i, upper[1]] for i in range(lower[0], upper[0])]
        + [[lower[0], i] for i in range(lower[1], upper[1])]
        + [[upper[0], i] for i in range(lower[1], upper[1])]
    )
    if not check_points(points):
        return False
    return True


def check(i: list[int]) -> bool:
    return grid[*i] or (
        grid[i[0] :, i[1]].size
        and grid[i[0], i[1] :].size
        and grid[: i[0], i[1]].size
        and grid[i[0], : i[1]].size
    )


if puzzle.is_test():
    for i in range(grid_size):
        # for j in range(grid_size):
        #     if h_grid[j, i]:
        #         print("#", end="")
        #     else:
        #         if check_rect([j, i], [j, i]):
        #             print("o", end="")
        #         else:
        #             print(".", end="")
        # print("        ", end="")
        for j in range(grid_size):
            if grid[j, i]:
                print("#", end="")
            else:
                if check([j, i]):
                    print("o", end="")
                else:
                    print(".", end="")
        print("")


sizes: list[list[int]] = []
for i, j in enumerate(data):
    others = data[:i] + data[i + 1 :]
    sizes += [[(abs(j[0] - k[0]) + 1) * (abs(j[1] - k[1]) + 1), j, k] for k in others]
debug("Calculated sizes")
sizes.sort(key=itemgetter(0), reverse=True)
debug("Sorted sizes")
for i in sizes:
    if not puzzle.is_test():
        assert i[0] > 291791910
        if i[0] > 4587371068:
            continue
    if check_rect(i[1], i[2]):
        biggest = i[0]
        break

debug(biggest)
# # biggest = 0
# # for i, j in enumerate(data):
# #     others = data[:i] + data[i + 1 :]
# #     for k in others:
# #         size = (abs(j[0] - k[0]) + 1) * (abs(j[1] - k[1]) + 1)
# #         if size > biggest and check_rect(grid, j, k):
# #             biggest = size

puzzle.submit_two(biggest)
