from functools import cache
from logging import debug
from math import ceil, prod

import numpy as np
from aoc import puzzle
from numpy._core.multiarray import dtype
from numpy._core.numerictypes import bool_
from numpy._typing import NDArray
from utils import parse_bool, print_bool_array

puzzle.test_answer_one = 2
data = puzzle.lines()


iterator = iter(data)
types: list[NDArray[bool_]] = []
min_sizes: list[int] = []
index = 0
while index < 5:
    index = int(next(iterator).replace(":", ""))
    shape: list[list[bool]] = []
    while (row := next(iterator)) != "":
        shape.append(list(map(parse_bool, row)))
    array = np.array(shape, dtype=bool)
    types.append(array)
    min_sizes.append(np.sum(array))

for i, j in enumerate(types):
    print(f"\nPresent shape {i}:")
    print_bool_array(j)

count = 0
for i in iterator:
    first_split = i.split(": ")
    shape: list[int] = [int(j) for j in first_split[0].split("x")]
    presents: list[int] = [int(j) for j in first_split[1].split(" ")]
    min_size_required: int = sum([k * min_sizes[j] for j, k in enumerate(presents)])
    # total_presents = sum(presents)
    spaces = prod(shape)
    if spaces > min_size_required:
        full_size_min = prod([ceil(j / 3) for j in shape])
        present_count = sum(presents)
        if present_count <= full_size_min:
            count += 1
        else:
            debug(f"Number of spaces: {spaces}, number required: {min_size_required}")
            debug(f"Full size minimum: {full_size_min}, present count: {present_count}")

debug(count)
puzzle.submit_one(count)
